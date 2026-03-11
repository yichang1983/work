import os
import re
import sys
from typing import List, Tuple, Set, Dict

# 若未安裝：pip install pandas openpyxl
try:
    import pandas as pd
except ImportError:
    print("需要 pandas 與 openpyxl，請先執行：pip install pandas openpyxl")
    sys.exit(1)

# ========= 檔案路徑（可調整）=========
source_excel_file_path = "/Topology/Device_new version.xlsx"
source_txt_file_path = "/Topology/FRA11-CFW.txt"
graphviz_file_path = "/Topology/Graphviz.txt"
output_file_path = "/Topology/FRA11-CFW.gv"


# ========= 工具函式 =========
def load_device_map(excel_path: str) -> dict:
    """讀取 Excel，建立雙鍵對照表 {NAME: (NAME, IP, SN)} 以及 {SN: (NAME, IP, SN)}"""
    xl = pd.ExcelFile(excel_path)
    sheet = next((s for s in xl.sheet_names if s.strip().lower() == "device name"), xl.sheet_names[0])
    df = xl.parse(sheet)
    df.columns = [str(c).strip().upper() for c in df.columns]

    required = {"SN", "NAME", "IP"}
    if not required.issubset(df.columns):
        raise ValueError(f"Excel 工作表缺少必要欄位，需要 {required}；目前欄位：{list(df.columns)}")

    device_map = {}
    for _, row in df.iterrows():
        name = str(row["NAME"]).strip()
        sn = str(row["SN"]).strip()
        ip = str(row["IP"]).strip()

        name_valid = name and name.lower() not in ("nan", "null", "none")
        sn_valid = sn and sn.lower() not in ("nan", "null", "none")

        final_name = name if name_valid else "null"
        final_ip = ip if (ip and ip.lower() not in ("nan", "null", "none")) else "null"
        final_sn = sn if sn_valid else "null"

        if name_valid:
            device_map[name.upper()] = (final_name, final_ip, final_sn)
        if sn_valid:
            device_map[sn.upper()] = (final_name, final_ip, final_sn)

    return device_map


def fmt_triple(name: str, ip: str, sn: str) -> str:
    """組合成 'NAME\\nIP\\nSN'"""
    return f"{name}\\n{ip}\\n{sn}"


def get_device_info(identifier: str, device_map: dict) -> str:
    """從 Hostname 或 SN 取 'NAME\\nIP\\nSN'"""
    identifier_upper = identifier.strip().upper()
    if identifier_upper in device_map:
        name, ip, sn = device_map[identifier_upper]
        return fmt_triple(name, ip, sn)
    return fmt_triple(identifier, "null", "null")


def clean_port(port_str: str) -> str:
    """過濾出純 port 號碼"""
    m = re.search(r"port\s*\d+", port_str, flags=re.IGNORECASE)
    return m.group(0).replace(" ", "") if m else port_str


def parse_pair_line(line: str) -> Tuple[str, str, str, str] | None:
    """解析連線字串"""
    pairs = re.findall(r"([A-Za-z0-9\-_\.]+)\(([^)]*)\)", line)
    if len(pairs) != 2:
        return None
    (host1, raw_port1), (host2, raw_port2) = pairs
    return host1.strip(), raw_port1.strip(), host2.strip(), raw_port2.strip()


def convert_txt_to_edges(txt_file: str, device_map: dict) -> List[Tuple[str, str, str]]:
    edges_list = []
    cfw_other_processed_keys = set()

    # --- 核心新增：FortiGate 實體還原字典 ---
    # 利用 Switch 的 Name 與 Port 反推 CFW 實體機與 Port
    HA_PHYSICAL_MAPPING = {
        ("FRA11-1.2.33-R2.1A-RU26-CDSW-01", "port47"): ("FRA11-CFW-M1", "port27"),
        ("FRA11-1.2.33-R2.1A-RU26-CDSW-01", "port48"): ("FRA11-CFW-M2", "port28"),
        ("FRA11-3.2.49-R1-RU28-CDSW-01", "port47"): ("FRA11-CFW-M2", "port27"),
        ("FRA11-3.2.49-R1-RU28-CDSW-01", "port48"): ("FRA11-CFW-M1", "port28"),
    }

    with open(txt_file, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    for line in lines:
        parsed = parse_pair_line(line)
        if not parsed:
            continue
        host1, raw_port1, host2, raw_port2 = parsed

        p1_clean = clean_port(raw_port1)
        p2_clean = clean_port(raw_port2)

        # 遇到邏輯 Fortilink 或 SN 顯示時，執行實體還原替換
        if "Fortilink" in raw_port1 or "FG" in host1.upper():
            mapping_key = (host2, p2_clean)
            if mapping_key in HA_PHYSICAL_MAPPING:
                host1, p1_clean = HA_PHYSICAL_MAPPING[mapping_key]
        elif "Fortilink" in raw_port2 or "FG" in host2.upper():
            mapping_key = (host1, p1_clean)
            if mapping_key in HA_PHYSICAL_MAPPING:
                host2, p2_clean = HA_PHYSICAL_MAPPING[mapping_key]

        # 取得 Excel 完整資訊
        left_dev = get_device_info(host1, device_map)
        right_dev = get_device_info(host2, device_map)
        label = f"{p1_clean} -> {p2_clean}"

        # 雙向去重邏輯
        is_left_switch = "SW" in left_dev.upper()
        is_right_switch = "SW" in right_dev.upper()
        is_switch_to_switch = is_left_switch and is_right_switch

        if is_switch_to_switch:
            edges_list.append((left_dev, right_dev, label))
        else:
            key = tuple(sorted([left_dev, right_dev]))
            if key not in cfw_other_processed_keys:
                cfw_other_processed_keys.add(key)
                edges_list.append((left_dev, right_dev, label))

    return edges_list


def extract_nodes_from_edges(edges_list: List[Tuple[str, str, str]]):
    """將節點抓出並分類，擴充支援 CDSW"""
    cfw_nodes = set()
    fsw_nodes = set()
    asw_nodes = set()

    for left, right, _ in edges_list:
        left_upper = left.upper()
        right_upper = right.upper()

        if "CFW" in left_upper: cfw_nodes.add(left)
        if "CFW" in right_upper: cfw_nodes.add(right)

        # 新增 CDSW 到 FSW 的分類判定中
        if "FSW" in left_upper or "CDSW" in left_upper: fsw_nodes.add(left)
        if "FSW" in right_upper or "CDSW" in right_upper: fsw_nodes.add(right)

        if "ASW" in left_upper: asw_nodes.add(left)
        if "ASW" in right_upper: asw_nodes.add(right)

    return cfw_nodes, fsw_nodes, asw_nodes


def insert_after_marker(lines: List[str], marker: str, insert_lines: List[str]):
    """在 GV 模板中插入資料"""
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line.rstrip("\n"))
        if (not inserted) and (marker in line):
            is_edge_marker = "edge" in marker.lower()

            for item in insert_lines:
                if is_edge_marker:
                    new_lines.append(item)
                else:
                    new_lines.append(f'"{item}"')
            inserted = True
    return new_lines


# ========= 主流程 =========
def main():
    for path in (source_excel_file_path, source_txt_file_path, graphviz_file_path):
        if not os.path.exists(path):
            print(f"找不到檔案：{path}")
            sys.exit(1)

    device_map = load_device_map(source_excel_file_path)
    print(f"已載入設備對照：{len(device_map)} 筆")

    edges_list = convert_txt_to_edges(source_txt_file_path, device_map)
    print(f"已處理 edges：{len(edges_list)} 條連線")

    cfw_nodes, fsw_nodes, asw_nodes = extract_nodes_from_edges(edges_list)
    print(f"CFW 節點：{len(cfw_nodes)}，FSW 節點：{len(fsw_nodes)}，ASW 節點：{len(asw_nodes)}")

    with open(graphviz_file_path, "r", encoding="utf-8") as f:
        gv_lines = f.readlines()

    cfw_insert_lines = sorted(list(cfw_nodes))
    fsw_insert_lines = sorted(list(fsw_nodes))
    asw_insert_lines = sorted(list(asw_nodes))

    all_edge_lines = []
    for left, right, label in edges_list:
        all_edge_lines.append(f'"{left}" -> {{"{right}"}} [label="{label}"]')

    gv_lines = insert_after_marker(gv_lines, "node [fillcolor = red]", cfw_insert_lines)
    gv_lines = insert_after_marker(gv_lines, "node [fillcolor = blue]", fsw_insert_lines)
    gv_lines = insert_after_marker(gv_lines, "node [fillcolor = green]", asw_insert_lines)
    gv_lines = insert_after_marker(gv_lines, "edge [color = grey, arrowhead=none]", all_edge_lines)

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(gv_lines))

    print(f"✅ 完成！輸出檔案：{output_file_path}")


if __name__ == "__main__":
    main()


#這次修改後：

#HA_PHYSICAL_MAPPING 會完美攔截 FG10E...，並用實體的 FRA11-CFW-M1/M2 及正確的 Port 進行替換，因為名字包含 CFW，紅色區塊就會成功顯示。

#因為在 extract_nodes_from_edges 中加入了 CDSW 的條件，你的 Tier 1 藍色區塊也能順利顯示了。

#未來如果有別的 Site（例如 CWL11），你只要修改 HA_PHYSICAL_MAPPING 裡的對應表就可以了！執行看看，確認結果是不是你要的樣子！
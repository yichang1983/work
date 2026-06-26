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
source_excel_file_path = "C:/Users/yi-chang.chen/PyCharmMiscProject/Python_topology/FortiSwitchManager/Device.xlsx"
source_txt_file_path = "C:/Users/yi-chang.chen/PyCharmMiscProject/Python_topology/FortiSwitchManager/CWL13-FortiSWMGMT-01.txt"
graphviz_file_path = "C:/Users/yi-chang.chen/PyCharmMiscProject/Python_topology/FortiSwitchManager/Graphviz.txt"
output_file_path = "C:/Users/yi-chang.chen/PyCharmMiscProject/Python_topology/FortiSwitchManager/CWL13-FortiSWMGMT-01.gv"


# ========= 工具函式 =========
def load_name_map(excel_path: str) -> dict:
    """讀取 Excel，改為回傳 {NAME_大寫: (原始NAME, IP, SN)} 以便用 Hostname 來反查"""
    xl = pd.ExcelFile(excel_path)

    # 找 "Device name" 工作表（忽略大小寫與空白），找不到就用第一個
    sheet = next((s for s in xl.sheet_names if s.strip().lower() == "device name"), xl.sheet_names[0])

    df = xl.parse(sheet)
    df.columns = [str(c).strip().upper() for c in df.columns]
    required = {"SN", "NAME", "IP"}
    if not required.issubset(df.columns):
        raise ValueError(f"Excel 工作表缺少必要欄位，需要 {required}；目前欄位：{list(df.columns)}")

    name_map = {}
    for _, row in df.iterrows():
        name = str(row["NAME"]).strip()
        if not name or name.lower() == 'nan':
            continue

        sn = str(row["SN"]).strip() if pd.notna(row["SN"]) else "null"
        ip = str(row["IP"]).strip() if pd.notna(row["IP"]) else "null"

        # 為了避免大小寫問題，將字典的 key 轉大寫，但保留原始名稱
        name_map[name.upper()] = (name, ip, sn)
    return name_map


def fmt_triple(name: str, ip: str, sn: str) -> str:
    """組合成 'NAME\\nIP\\nSN'（注意為反斜線 n，而非實際換行，給 Graphviz 識別用）"""
    return f"{name}\\n{ip}\\n{sn}"


def get_device_info_by_name(hostname: str, name_map: dict) -> str:
    """從 Hostname 取 'NAME\\nIP\\nSN'；若無對應，IP/SN 顯示為 null"""
    key = hostname.upper()
    if key in name_map:
        orig_name, ip, sn = name_map[key]
        # 使用 Excel 內的名稱，或者 TXT 抓出來的名稱都可以
        return fmt_triple(orig_name, ip, sn)
    # 如果 Excel 沒這台，就顯示原本抓到的名稱，配上 null
    return fmt_triple(hostname, "null", "null")


def clean_port(port_str: str) -> str:
    """從 'port48/_xxx_' 或 'port 45' 取出 'port48' / 'port45'"""
    m = re.search(r"port\s*\d+", port_str, flags=re.IGNORECASE)
    return m.group(0).replace(" ", "") if m else port_str


def parse_pair_line(line: str) -> Tuple[str, str, str, str] | None:
    """
    解析像：Hostname1(portX)  <<-->>  Hostname2(portY)
    回傳 (host1, raw_port1, host2, raw_port2)
    注意：加入了 \-_ 來允許名稱中包含減號與底線 (如 CWL13-DM110-PRB-U23)
    """
    # [A-Za-z0-9\-_]+ 可以匹配大小寫字母、數字、減號及底線
    pairs = re.findall(r"([A-Za-z0-9\-_]+)\(([^)]*)\)", line)
    if len(pairs) != 2:
        return None
    (host1, raw_port1), (host2, raw_port2) = pairs
    return host1.strip(), raw_port1.strip(), host2.strip(), raw_port2.strip()


def convert_txt_to_edges(txt_file: str, name_map: dict) -> List[Tuple[str, str, str]]:
    """
    將原始文字檔轉換為 Graphviz edge 元組列表，並依設備類型處理重複連線。
    """
    edges_list = []
    cfw_other_processed_keys = set()

    with open(txt_file, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    for line in lines:
        parsed = parse_pair_line(line)
        if not parsed:
            continue

        name1, raw_port1, name2, raw_port2 = parsed

        # 這裡改用 name 去映射 Excel 的資訊
        left_dev = get_device_info_by_name(name1, name_map)
        right_dev = get_device_info_by_name(name2, name_map)
        p1 = clean_port(raw_port1)
        p2 = clean_port(raw_port2)
        label = f"{p1} -> {p2}"

        # 檢查是否為 SWITCH 對 SWITCH 的連線
        is_left_switch = "SW" in left_dev.upper()
        is_right_switch = "SW" in right_dev.upper()
        is_switch_to_switch = is_left_switch and is_right_switch

        if is_switch_to_switch:
            edges_list.append((left_dev, right_dev, label))
        else:
            # 其他連線 (CFW-SWITCH, CFW-CFW)，進行去重
            key = tuple(sorted([left_dev, right_dev]))
            if key not in cfw_other_processed_keys:
                cfw_other_processed_keys.add(key)
                edges_list.append((left_dev, right_dev, label))

    return edges_list


def extract_nodes_from_edges(edges_list: List[Tuple[str, str, str]]):
    """
    從 edge 列表抓出所有節點，並依 CFW/FSW/ASW 分類。
    """
    cfw_nodes = set()
    fsw_nodes = set()
    asw_nodes = set()

    for left, right, _ in edges_list:
        if "CFW" in left:
            cfw_nodes.add(left)
        if "CFW" in right:
            cfw_nodes.add(right)

        if "FSW" in left:
            fsw_nodes.add(left)
        if "FSW" in right:
            fsw_nodes.add(right)

        if "ASW" in left:
            asw_nodes.add(left)
        if "ASW" in right:
            asw_nodes.add(right)

    return cfw_nodes, fsw_nodes, asw_nodes


def insert_after_marker(lines: List[str], marker: str, insert_lines: List[str]):
    """在第一個包含 marker 的行後面插入多行內容"""
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
    # 檔案存在性檢查
    for path in (source_excel_file_path, source_txt_file_path, graphviz_file_path):
        if not os.path.exists(path):
            print(f"找不到檔案：{path}")
            sys.exit(1)

    # 1) Excel → 以 NAME 當 Key 建立對照
    name_map = load_name_map(source_excel_file_path)
    print(f"已載入 Hostname 對照：{len(name_map)} 筆")

    # 2) 轉換來源 TXT → edges
    edges_list = convert_txt_to_edges(source_txt_file_path, name_map)
    print(f"已處理 edges：{len(edges_list)} 條連線")

    # 3) 從 edges 抽出節點並分類
    cfw_nodes, fsw_nodes, asw_nodes = extract_nodes_from_edges(edges_list)
    print(f"CFW 節點：{len(cfw_nodes)}，FSW 節點：{len(fsw_nodes)}，ASW 節點：{len(asw_nodes)}")

    # 4) 讀取 Graphviz 模板
    with open(graphviz_file_path, "r", encoding="utf-8") as f:
        gv_lines = f.readlines()

    # 5) 處理所有要插入的內容
    cfw_insert_lines = sorted(list(cfw_nodes))
    fsw_insert_lines = sorted(list(fsw_nodes))
    asw_insert_lines = sorted(list(asw_nodes))

    # 所有邊緣
    all_edge_lines = []
    for left, right, label in edges_list:
        all_edge_lines.append(f'"{left}" -> {{"{right}"}} [label="{label}"]')

    # 6) 插入到模板中
    gv_lines = insert_after_marker(gv_lines, "node [fillcolor = red]", cfw_insert_lines)
    gv_lines = insert_after_marker(gv_lines, "node [fillcolor = blue]", fsw_insert_lines)
    gv_lines = insert_after_marker(gv_lines, "node [fillcolor = green]", asw_insert_lines)
    gv_lines = insert_after_marker(gv_lines, "edge [color = grey, arrowhead=none]", all_edge_lines)

    # 7) 寫出 .gv
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(gv_lines))

    print(f"✅ 完成！輸出檔案：{output_file_path}")


if __name__ == "__main__":
    main()

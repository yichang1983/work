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
source_excel_file_path = "C:/Users\yi-chang.chen\PycharmProjects\PythonProject\Topology/Device.xlsx"
source_txt_file_path = "C:/Users\yi-chang.chen\PycharmProjects\PythonProject\Topology/WAW11-CFW-M2-01.txt"
graphviz_file_path = "C:/Users\yi-chang.chen\PycharmProjects\PythonProject\Topology/Graphviz.txt"
output_file_path = "C:/Users\yi-chang.chen\PycharmProjects\PythonProject\Topology/WAW11.gv"


# ========= 工具函式 =========
def load_sn_map(excel_path: str) -> dict:
    """讀取 Excel，回傳 {SN: (NAME, IP)}"""
    xl = pd.ExcelFile(excel_path)

    # 找 "Device name" 工作表（忽略大小寫與空白），找不到就用第一個
    sheet = next((s for s in xl.sheet_names if s.strip().lower() == "device name"), xl.sheet_names[0])

    df = xl.parse(sheet)
    df.columns = [str(c).strip().upper() for c in df.columns]
    required = {"SN", "NAME", "IP"}
    if not required.issubset(df.columns):
        raise ValueError(f"Excel 工作表缺少必要欄位，需要 {required}；目前欄位：{list(df.columns)}")

    sn_map = {}
    for _, row in df.iterrows():
        sn = str(row["SN"]).strip()
        if not sn:
            continue
        name = str(row["NAME"]).strip() if pd.notna(row["NAME"]) else "null"
        ip = str(row["IP"]).strip() if pd.notna(row["IP"]) else "null"
        sn_map[sn] = (name, ip)
    return sn_map


def fmt_triple(name: str, ip: str, sn: str) -> str:
    """組合成 'NAME\\nIP\\nSN'（注意為反斜線 n，而非實際換行）"""
    return f"{name}\\n{ip}\\n{sn}"


def get_device_info(sn: str, sn_map: dict) -> str:
    """從 SN 取 'NAME\\nIP\\nSN'；若無對應，NAME/IP 以 null"""
    if sn in sn_map:
        name, ip = sn_map[sn]
        return fmt_triple(name, ip, sn)
    return fmt_triple("null", "null", sn)


def clean_port(port_str: str) -> str:
    """從 'port48/_xxx_' 或 'port 45' 取出 'port48' / 'port45'"""
    m = re.search(r"port\s*\d+", port_str, flags=re.IGNORECASE)
    return m.group(0).replace(" ", "") if m else port_str


def parse_pair_line(line: str) -> Tuple[str, str, str, str] | None:
    """
    解析像：SN1(portX)  <<-->>  SN2(portY)
    回傳 (sn1, raw_port1, sn2, raw_port2)
    """
    pairs = re.findall(r"([A-Za-z0-9]+)\(([^)]*)\)", line)
    if len(pairs) != 2:
        return None
    (sn1, raw_port1), (sn2, raw_port2) = pairs
    return sn1.strip(), raw_port1.strip(), sn2.strip(), raw_port2.strip()


def convert_txt_to_edges(txt_file: str, sn_map: dict) -> List[Tuple[str, str, str]]:
    """
    將原始文字檔轉換為 Graphviz edge 元組列表，並依設備類型處理重複連線。
    - CFW/非 SWITCH 之間的連線，去重只保留第一條。
    - SWITCH/SWITCH 之間的連線，保留所有連線。
    """
    edges_list = []
    cfw_other_processed_keys = set()

    with open(txt_file, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    for line in lines:
        parsed = parse_pair_line(line)
        if not parsed:
            continue
        sn1, raw_port1, sn2, raw_port2 = parsed

        left_dev = get_device_info(sn1, sn_map)
        right_dev = get_device_info(sn2, sn_map)
        p1 = clean_port(raw_port1)
        p2 = clean_port(raw_port2)
        label = f"{p1} -> {p2}"

        # 檢查是否為 SWITCH 對 SWITCH 的連線
        is_left_switch = "SW" in left_dev.upper()
        is_right_switch = "SW" in right_dev.upper()
        is_switch_to_switch = is_left_switch and is_right_switch

        if is_switch_to_switch:
            # SWITCH-SWITCH 連線，直接加入列表，不進行去重
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

    # 1) Excel → SN 對照
    sn_map = load_sn_map(source_excel_file_path)
    print(f"已載入 SN 對照：{len(sn_map)} 筆")

    # 2) 轉換來源 TXT → edges (依設備類型處理)
    edges_list = convert_txt_to_edges(source_txt_file_path, sn_map)
    print(f"已處理 edges：{len(edges_list)} 條連線")

    # 3) 從 edges 抽出節點並分類
    cfw_nodes, fsw_nodes, asw_nodes = extract_nodes_from_edges(edges_list)
    print(f"CFW 節點：{len(cfw_nodes)}，FSW 節點：{len(fsw_nodes)}，ASW 節點：{len(asw_nodes)}")

    # 4) 讀取 Graphviz 模板
    with open(graphviz_file_path, "r", encoding="utf-8") as f:
        gv_lines = f.readlines()

    # 5) 處理所有要插入的內容
    # 這裡將所有節點和邊緣合併到同一個列表中
    all_insert_lines = []

    # CFW 節點
    cfw_insert_lines = sorted(list(cfw_nodes))
    all_insert_lines.extend(cfw_insert_lines)

    # FSW 節點
    fsw_insert_lines = sorted(list(fsw_nodes))
    all_insert_lines.extend(fsw_insert_lines)

    # ASW 節點
    asw_insert_lines = sorted(list(asw_nodes))
    all_insert_lines.extend(asw_insert_lines)

    # 所有邊緣
    all_edge_lines = []
    for left, right, label in edges_list:
        all_edge_lines.append(f'"{left}" -> {{"{right}"}} [label="{label}"]')

    # 6) 插入到模板中，節點和邊緣分開插入
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
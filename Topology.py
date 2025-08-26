import os
import re
import sys

try:
    import pandas as pd
except ImportError:
    print("需要 pandas 與 openpyxl，請先執行：pip install pandas openpyxl")
    sys.exit(1)

# ========= 檔案路徑 =========
source_excel_file_path = "C:/Users\yi-chang.chen\PycharmProjects\PythonProject\Topology/TPE.xlsx"
source_txt_file_path = "C:/Users\yi-chang.chen\PycharmProjects\PythonProject\Topology/TPE11-CFW-M1.txt"
graphviz_file_path = "C:/Users\yi-chang.chen\PycharmProjects\PythonProject\Topology/Graphviz.txt"
output_file_path = "C:/Users\yi-chang.chen\PycharmProjects\PythonProject\Topology/TPE11.gv"

# ========= 工具函式 =========
def load_sn_map(excel_path: str) -> dict:
    xl = pd.ExcelFile(excel_path)
    sheet = None
    for s in xl.sheet_names:
        if s.strip().lower() == "device name":
            sheet = s
            break
    if sheet is None:
        sheet = xl.sheet_names[0]

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
        ip   = str(row["IP"]).strip()   if pd.notna(row["IP"])   else "null"
        sn_map[sn] = (name, ip)
    return sn_map


def fmt_triple(name: str, ip: str, sn: str) -> str:
    # 這裡的字串不包含引號，以便後續可以統一添加
    return f"{name}\\n{ip}\\n{sn}"


def get_device_info(sn: str, sn_map: dict) -> str:
    if sn in sn_map:
        name, ip = sn_map[sn]
        return fmt_triple(name, ip, sn)
    return fmt_triple("null", "null", sn)


def clean_port(port_str: str) -> str:
    m = re.search(r"port\s*\d+", port_str, flags=re.IGNORECASE)
    return m.group(0).replace(" ", "") if m else port_str


def parse_pair_line(line: str):
    pairs = re.findall(r"([A-Za-z0-9]+)\(([^)]*)\)", line)
    if len(pairs) != 2:
        return None
    (sn1, raw_port1), (sn2, raw_port2) = pairs
    return sn1.strip(), raw_port1.strip(), sn2.strip(), raw_port2.strip()


def convert_txt_to_edges(txt_file: str, sn_map: dict):
    edges = []
    with open(txt_file, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    for line in lines:
        parsed = parse_pair_line(line)
        if not parsed:
            continue
        sn1, raw_port1, sn2, raw_port2 = parsed

        left_dev  = get_device_info(sn1, sn_map)
        right_dev = get_device_info(sn2, sn_map)
        p1 = clean_port(raw_port1)
        p2 = clean_port(raw_port2)

        edges.append((left_dev, right_dev, f"{p1} -> {p2}"))
    return edges


def extract_nodes_from_edges(edges):
    cfw_nodes = set()
    fsw_nodes = set()
    for left, right, _ in edges:
        if "CFW" in left:
            cfw_nodes.add(left)
        if "CFW" in right:
            cfw_nodes.add(right)
        if "FSW" in left:
            fsw_nodes.add(left)
        if "FSW" in right:
            fsw_nodes.add(right)
    return sorted(cfw_nodes), sorted(fsw_nodes)


def insert_after_marker(lines, marker: str, insert_lines):
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line.rstrip("\n"))
        if (not inserted) and (marker in line):
            # 判斷是否為邊緣的標記
            is_edge_marker = "edge" in marker.lower()

            for item in insert_lines:
                if is_edge_marker:
                    # 邊緣部分，因為我們在主程式中已經處理好格式，所以直接插入
                    new_lines.append(item)
                else:
                    # 節點部分，需要添加引號
                    new_lines.append(f'"{item}"')
            inserted = True
    return new_lines


# ========= 主程式 =========
def main():
    # 檔案存在性檢查
    for path in (source_excel_file_path, source_txt_file_path, graphviz_file_path):
        if not os.path.exists(path):
            print(f"找不到檔案：{path}")
            sys.exit(1)

    # 1) 讀 Excel
    sn_map = load_sn_map(source_excel_file_path)
    print(f"已載入 SN 對照：{len(sn_map)} 筆")

    # 2) 轉換來源 TXT -> edges
    edges_list = convert_txt_to_edges(source_txt_file_path, sn_map)
    print(f"已產生 edges：{len(edges_list)} 行")

    # 3) 抽節點分類
    cfw_nodes, fsw_nodes = extract_nodes_from_edges(edges_list)
    print(f"CFW 節點：{len(cfw_nodes)}，FSW 節點：{len(fsw_nodes)}")

    # 4) 讀 Graphviz 模板
    with open(graphviz_file_path, "r", encoding="utf-8") as f:
        gv_lines = f.readlines()

    # 5) 處理 edge，去除重複（雙向視為同一條）
    edge_set = set()
    edge_lines = []
    for left, right, label in edges_list:
        key = tuple(sorted([left, right]))
        if key not in edge_set:
            edge_set.add(key)
            # 這裡直接產生最終的完整邊緣格式字串
            edge_lines.append(f'"{left}" -> {{"{right}"}} [label="{label}"]')

    # 6) 插入節點和邊緣到模板
    gv_lines = insert_after_marker(gv_lines, "node [fillcolor = red]",  cfw_nodes)
    gv_lines = insert_after_marker(gv_lines, "node [fillcolor = blue]", fsw_nodes)
    gv_lines = insert_after_marker(gv_lines, "edge [color = grey, arrowhead=none]", edge_lines)

    # 7) 輸出
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(gv_lines))

    print(f"✅ 完成！輸出檔案：{output_file_path}")


if __name__ == "__main__":
    main()
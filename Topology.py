import os
import re
import sys

# 如果你沒裝 pandas，請先：pip install pandas openpyxl
try:
    import pandas as pd
except ImportError as e:
    print("需要 pandas 與 openpyxl：請先執行 `pip install pandas openpyxl`")
    sys.exit(1)

# =========================
# File paths (可自行修改)
# =========================
source_excel_file_path = "C:/Users\yi-chang.chen\PycharmProjects\PythonProject\Topology/TPE.xlsx"
source_txt_file_path   = "C:/Users\yi-chang.chen\PycharmProjects\PythonProject\Topology/TPE11-CFW-M1.txt"
output_file_path       = "C:/Users\yi-chang.chen\PycharmProjects\PythonProject\Topology/TPE11-raw.txt"

# =============== 工具函式 ===============

def ensure_file_exists(path: str, desc: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{desc} 不存在：{path}")

def find_device_sheet(xl: pd.ExcelFile, target_name="Device name") -> str:
    # 嘗試精確(忽略大小寫與空白)
    for s in xl.sheet_names:
        if s.strip().lower() == target_name.strip().lower():
            return s
    # 找不到就用第一個
    return xl.sheet_names[0]

def load_sn_map(excel_path: str) -> dict:
    """讀取 Excel，回傳 {SN: (NAME, IP)}"""
    xl = pd.ExcelFile(excel_path)
    sheet = find_device_sheet(xl, "Device name")
    df = xl.parse(sheet)

    # 標頭正規化
    df.columns = [str(c).strip().upper() for c in df.columns]
    required = {"SN", "NAME", "IP"}
    if not required.issubset(df.columns):
        raise ValueError(f"工作表「{sheet}」缺少必要欄位，需含 {required}，目前欄位：{list(df.columns)}")

    sn_map = {}
    for _, row in df.iterrows():
        sn = str(row["SN"]).strip()
        name = str(row["NAME"]).strip() if pd.notna(row["NAME"]) else "null"
        ip = str(row["IP"]).strip() if pd.notna(row["IP"]) else "null"
        if sn:  # 避免空 SN
            sn_map[sn] = (name, ip)
    return sn_map, sheet

def fmt_triple(name: str, ip: str, sn: str) -> str:
    """回傳 'NAME\\nIP\\nSN'（注意為反斜線 n，而非真正換行）"""
    return f"{name}\\n{ip}\\n{sn}"

def get_device_info(sn: str, sn_map: dict) -> str:
    """組成 'NAME\\nIP\\nSN'；若找不到，NAME=IP='null'"""
    if sn in sn_map:
        name, ip = sn_map[sn]
        return fmt_triple(name, ip, sn)
    return fmt_triple("null", "null", sn)

def clean_port(port_str: str) -> str:
    """
    從像 'port48/_FlInK1_ICL0_' 或 'port45' 取出 'port48' / 'port45'。
    若找不到就回傳原字串。
    """
    m = re.search(r"port\s*\d+", port_str, flags=re.IGNORECASE)
    return m.group(0).replace(" ", "") if m else port_str

def parse_line(line: str):
    """
    解析一行：
    FS1E48T422005241(port45)  <<------------------>>  94FF3C7A5BFF(port31)
    回傳 (sn1, port1, sn2, port2)；若不匹配回傳 None
    """
    # 抓出 兩組  <SN>(<內文到右括號>)
    pairs = re.findall(r"([A-Za-z0-9]+)\(([^)]*)\)", line)
    if len(pairs) != 2:
        return None
    (sn1, raw_port1), (sn2, raw_port2) = pairs
    return sn1.strip(), raw_port1.strip(), sn2.strip(), raw_port2.strip()

# =============== 主程式 ===============

def main():
    # 路徑檢查
    ensure_file_exists(source_excel_file_path, "Excel 檔")
    ensure_file_exists(source_txt_file_path, "TXT 檔")

    # 讀 Excel -> 對照表
    sn_map, used_sheet = load_sn_map(source_excel_file_path)
    print(f"已載入 SN 對照表，共 {len(sn_map)} 筆（工作表：{used_sheet}）。")

    # 讀 TXT
    with open(source_txt_file_path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    output_lines = []
    unmatched_sns = set()
    parsed_count = 0
    skipped_count = 0

    for line in lines:
        parsed = parse_line(line)
        if not parsed:
            skipped_count += 1
            continue

        parsed_count += 1
        sn1, raw_port1, sn2, raw_port2 = parsed

        # 將 SN 映射成 NAME/IP/SN 三段（用 \\n 串接）
        left_dev  = get_device_info(sn1, sn_map)
        right_dev = get_device_info(sn2, sn_map)

        # 蒐集沒對到 Excel 的 SN
        if "null\\nnull" in left_dev:
            unmatched_sns.add(sn1)
        if "null\\nnull" in right_dev:
            unmatched_sns.add(sn2)

        # 清理 port 成 'portXX'
        p1 = clean_port(raw_port1)
        p2 = clean_port(raw_port2)

        # 照「輸入的左右順序」輸出（如需特殊規則可再調整）
        output_lines.append(f"\"{left_dev}\" -> {{\"{right_dev}\"}} [label=\"{p1} -> {p2}\"]")

    # 寫檔
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"完成！解析 {parsed_count} 行，略過 {skipped_count} 行。")
    print(f"輸出：{output_file_path}")
    if unmatched_sns:
        print(f"以下 SN 在 Excel 找不到（NAME/IP 以 null 代替）：\n  " + "\n  ".join(sorted(unmatched_sns)))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("執行發生錯誤：", e)
        sys.exit(1)

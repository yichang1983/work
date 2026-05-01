import os
import shutil
import re
import pandas as pd


def _find_header_row(excel_path: str, sheet_name: str = "Sheet1", max_scan_rows: int = 300) -> int:
    """在 Sheet1 前幾列中找出真正表頭（包含 Hostname / Serial Number / Phases）。"""
    preview = pd.read_excel(excel_path, sheet_name=sheet_name, header=None, nrows=max_scan_rows, engine="openpyxl")

    target = {"hostname", "serial number", "phases"}
    for i in range(len(preview)):
        row_vals = set(
            str(x).strip().lower()
            for x in preview.iloc[i].tolist()
            if pd.notna(x)
        )
        if target.issubset(row_vals):
            return i

    raise ValueError(f"找不到表頭列（需要包含 Hostname / Serial Number / Phases）。請檢查 {sheet_name} 內容。")


def _extract_blocks_from_lldp(excel_path: str, lldp_sheet: str = "lldp_neighbor_completed") -> dict:
    """
    解析 lldp_neighbor_completed → { serial: block_df }
    block_df 會保留「Serial 行 + 欄位標題行 + 底線行 + port rows...」
    """
    raw = pd.read_excel(excel_path, sheet_name=lldp_sheet, header=None, engine="openpyxl")

    # 你的檔案這張表是 8 欄結構（Serial / Portname / Status / Device-name / VLAN / IP / MAC / Port-ID）
    if raw.shape[1] > 8:
        raw = raw.iloc[:, :8]

    # Serial 行特徵：第0欄有值、其餘欄位全空
    serial_rows = raw.index[(raw[0].notna()) & (raw.loc[:, 1:].isna().all(axis=1))].tolist()

    blocks = {}
    for idx, start in enumerate(serial_rows):
        end = serial_rows[idx + 1] if idx + 1 < len(serial_rows) else len(raw)
        block = raw.iloc[start:end].copy()
        serial = str(block.iloc[0, 0]).strip()
        blocks[serial] = block

    return blocks


def _phase_sort_key(phase: str):
    """
    讓 Phase-23-1 這種也能排序：
    Phase-1 < Phase-2 < ... < Phase-23 < Phase-23-1 < Phase-24 ...
    """
    nums = re.findall(r"\d+", phase)
    return tuple(int(n) for n in nums) if nums else (999999,)


def build_all_phase_tabs(
    input_path: str,
    output_path: str,
    sheet1_name: str = "Sheet1",
    lldp_sheet: str = "lldp_neighbor_completed",
    serial_col_name: str = "Serial Number",
    phase_col_name: str = "Phases",
):
    # 1) 確保 output 目錄存在
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # 2) 複製 input → output（避免原檔被鎖住/權限問題）
    if os.path.abspath(input_path) != os.path.abspath(output_path):
        shutil.copy2(input_path, output_path)
    else:
        print("[WARN] output_path 與 input_path 相同：若檔案被 Excel 開著，可能寫入失敗。")

    # 3) 讀 Sheet1（找出表頭列後讀成 DataFrame）
    header_row = _find_header_row(output_path, sheet_name=sheet1_name)
    devices = pd.read_excel(output_path, sheet_name=sheet1_name, header=header_row, engine="openpyxl")

    if phase_col_name not in devices.columns or serial_col_name not in devices.columns:
        raise ValueError(
            f"Sheet1 欄位不存在：需要 '{phase_col_name}' 與 '{serial_col_name}'。\n"
            f"目前欄位：{list(devices.columns)}"
        )

    # 4) 把 Sheet1 的所有 Phase-* 抓出來（你要的是 Phase-1 到最後）
    phases = (
        devices[phase_col_name]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )
    phases = [p for p in phases if p.startswith("Phase-") and p != "Phase-0"]  # 你要 Phase-1 起跳
    phases.sort(key=_phase_sort_key)

    if not phases:
        print("[WARN] Sheet1 找不到任何 Phase-*（排除 Phase-0）")
        return

    # 5) 先把 lldp_neighbor_completed 的所有 serial blocks 解析好（只做一次）
    blocks = _extract_blocks_from_lldp(output_path, lldp_sheet=lldp_sheet)

    # 6) 逐個 Phase 建立 tab
    missing_summary = {}

    for phase_name in phases:
        phase_serials = (
            devices.loc[devices[phase_col_name].astype(str).str.strip() == phase_name, serial_col_name]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

        combined = []
        missing = []
        for s in phase_serials:
            if s in blocks:
                combined.append(blocks[s])
            else:
                missing.append(s)

        if not combined:
            print(f"[SKIP] {phase_name}：在 '{lldp_sheet}' 找不到任何對應 serial block")
            if missing:
                missing_summary[phase_name] = missing
            continue

        out_df = pd.concat(combined, ignore_index=True)

        # 覆蓋寫入對應 Phase tab（格式會像你的 Phase-1：不輸出 header/index）
        with pd.ExcelWriter(output_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            out_df.to_excel(writer, sheet_name=phase_name, index=False, header=False)

        print(f"[OK] 已寫入 {phase_name}（Switch數：{len(phase_serials)}，找到 block：{len(combined)}）")

        if missing:
            missing_summary[phase_name] = missing

    # 7) 統一輸出找不到的 serial（若有）
    if missing_summary:
        print("\n[WARN] 以下 Phase 有 Serial 在 lldp_neighbor_completed 找不到對應資料：")
        for ph, miss in missing_summary.items():
            print(f"  - {ph}: {len(miss)} 台")
            for s in miss:
                print(f"      {s}")

    print(f"\n[DONE] 全部完成！輸出檔案：{output_path}")


# ===========================
# ✅ 最簡單的執行方式：只改這三行
# ===========================
if __name__ == "__main__":
    input_path = r"C:\Users\yi-chang.chen\Downloads\KUL12-Firmware-Upgrade_for myself.xlsx"
    output_path = r"C:\Users\yi-chang.chen\Downloads\KUL12-Firmware-Upgrade_for myself_ALL_PHASES.xlsx"

    build_all_phase_tabs(input_path=input_path, output_path=output_path)
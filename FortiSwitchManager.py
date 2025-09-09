import re

# 來源檔案
source_get_physical_conn_file_path = "C:/Users\yi-chang.chen\PycharmProjects\PythonProject\Topology\FortiSwitchManager/VA14-get-physical-conn.txt"
source_get_conn_status_file_path = "C:/Users\yi-chang.chen\PycharmProjects\PythonProject\Topology\FortiSwitchManager/VA14-get-conn-status.txt"
output_file_path = "C:/Users\yi-chang.chen\PycharmProjects\PythonProject\Topology\FortiSwitchManager/VA14-raw.txt"

# 讀取 get-physical-conn，提取 Serial number
serial_numbers = set()
with open(source_get_physical_conn_file_path, "r", encoding="utf-8") as f:
    for line in f:
        # 找出 "XXXXXXX(" 之前的字串
        matches = re.findall(r"(\S+?)\(", line)
        serial_numbers.update(matches)

# 讀取 get-conn-status，過濾掉 serial_numbers 中的行
filtered_lines = []
with open(source_get_conn_status_file_path, "r", encoding="utf-8") as f:
    for line in f:
        serial = line.split()[0] if line.strip() else ""
        if serial not in serial_numbers:
            filtered_lines.append(line)

# 輸出結果
with open(output_file_path, "w", encoding="utf-8") as f:
    f.writelines(filtered_lines)

print(f"✅ 已完成比對，輸出檔案：{output_file_path}")

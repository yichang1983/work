# num = input('Mode 2 (static) or Mode 4 (lacp):')
#
# if num == '2':
#         var1 = input('port that you want to add in a LAG, ie 21&22 or 5&6&7&8...etc')
#         var2 = input('server ip address')
#         print(
# f'''
# interface Eth-Trunk {var1}
#  description {var2}/21&22
#  port default vlan102
#  stp edged-port enable
#  trust dscp
# ''')


num = input('Mode 2 (static) or Mode 4 (lacp):')

if num == '2':
    var1 = input('port that you want to add in a LAG, ie 21&22 or 5&6&7&8...etc: ')
    var2 = input('server ip address: ')

    # 將 var1 拆分為數字列表
    # var1.split('&'): 這一部分使用字符串的split方法，將 var1 字符串根據 & 符號分割成多個子字符串。返回的結果是一個包含這些子字符串的列表。
    # [int(port.strip()) for port in ...]: 這是一個列表推導式。它遍歷 var1.split('&')中的每個子字符串，對每個子字符串執行操作，然後將結果收集成一個新的列表。
    # port.strip(): 對每個子字符串（port）使用strip方法，去除頭尾的空格（或換行符等）。
    # int(port.strip()): 將去除空格後的字符串轉換為整數。
    # 總之，這一行代碼的目的是將var1中以 & 符號分隔的數字部分提取出來，去除空格，並以整數形式存儲在ports列表中。例如，如果var1是字符串'21& 22 & 5 & 6'，則ports將成為整數列表[21, 22, 5, 6]。
    ports = [int(port.strip()) for port in var1.split('&')]

    # 找到最大的數字
    max_port = max(ports)

    print(f'''
interface Eth-Trunk{max_port}
 description {var2}/{var1}
 port default vlan102
 stp edged-port enable
 trust dscp
''', end=' ') # 將 end 設置為空字符串，以縮小 interface 10GE1/0/ 和下一個 interface 之間的距離

    # 為每個 port 生成一個獨立的 interface
    for port in ports:
        print(f'''
interface 10GE1/0/{port}
 description {var2}
 eth-trunk {max_port}
''', end=' ') # 將 end 設置為空字符串，以縮小 interface 10GE1/0/ 和下一個 interface 之間的距離

elif num == '4':
    var1 = input('port that you want to add in a LAG, ie 21&22 or 5&6&7&8...etc: ')
    var2 = input('server ip address: ')
    ports = [int(port.strip()) for port in var1.split('&')]
    max_port = max(ports)
    print(f'''
interface Eth-Trunk{max_port} 
description {var2}/{var1} 
port default vlan102 
stp edged-port enable
mode lacp-static
trust dscp
''', end=' ') # 將 end 設置為空字符串，以縮小 interface 10GE1/0/ 和下一個 interface 之間的距離
    for port in ports:
        print(f'''
interface 10GE1/0/{port}
 description {var2}
 eth-trunk{max_port}
''', end=' ') # 將 end 設置為空字符串，以縮小 interface 10GE1/0/ 和下一個 interface 之間的距離

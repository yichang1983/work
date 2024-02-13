"""
Mode 4 is mode active, Mode 2 is mode on:
***********************************
Huawei mode 4 example:
interface Eth-Trunk32
description xxx.xxx.xxx.xxx/21&22
port default vlan 102
stp edged-port enable
mode lacp-static
trust dscp

interface 10GE1/0/21
description xxx.xxx.xxx.xxx
eth-trunk 32

Huawei mode 2 example:
interface Eth-Trunk18

description xxx.xxx.xxx.xxx/18&18

port default vlan 102

stp edged-port enable

trust dscp


interface 10GE1/0/18

description xxx.xxx.xxx.xxx

eth-trunk 18

***********************************
***********************************
H3C mode 4 example:
interface Bridge-Aggregation28
description xxx.xxx.xxx.xxx/25&26&27&28
port access vlan 102
link-aggregation mode dynamic
stp edged-port

interface Ten-GigabitEthernet1/0/28
port link-mode bridge
description xxx.xxx.xxx.xxx
port access vlan 102
stp edged-port
stp tc-restriction
qos trust dscp
port link-aggregation group 28


H3C mode 2 example:
interface Bridge-Aggregation56
description xxx.xxx.xxx.xxx/15&16
port access vlan 102
stp edged-port

interface Ten-GigabitEthernet1/0/15
port link-mode bridge
description xxx.xxx.xxx.xxx
port access vlan 102
stp edged-port
stp tc-restriction
qos trust dscp
port link-aggregation group 56
***********************************
#
***********************************
Arista mode 4 example:
interface Port-Channel32
description xxx.xxx.xxx.xxx/19&20&21&22
switchport access vlan 102
spanning-tree portfast
spanning-tree bpduguard enable

interface Ethernet19
description xxx.xxx.xxx.xxx
switchport access vlan 102
channel-group 32 mode active
#
Arista mode 2 example:
interface Port-Channel24
description xxx.xxx.xxx.xxx/23&24
switchport access vlan 102
spanning-tree portfast
spanning-tree bpduguard enable

interface Ethernet24
description xxx.xxx.xxx.xxx
switchport access vlan 102
channel-group 24 mode on
spanning-tree portfast
spanning-tree bpduguard enable
***********************************
#
***********************************
Cisco mode 4 example:
interface port-channel44
description xxx.xxx.xxx.xxx
switchport access vlan 102
spanning-tree port type edge
spanning-tree bpduguard enable

interface Ethernet1/41
description xxx.xxx.xxx.xxx
switchport access vlan 102
spanning-tree port type edge
spanning-tree bpduguard enable
channel-group 44 mode active
#
Cisco mode 2 example:
interface Port-Channel24
description 157.185.174.53/23&24
switchport access vlan 102
spanning-tree portfast
spanning-tree bpduguard enable

interface Ethernet24
description 157.185.174.53
switchport access vlan 102
channel-group 24 mode on
spanning-tree portfast
spanning-tree bpduguard enable
***********************************
"""
vendor = input('Which vendor do you need, 1.Huawei, 2.H3C, 3.Arista, 4.Cisco: ')
mode = input('Mode 2 (Static/On) or Mode 4 (LACP/Active):')

if vendor == '1':
    if mode == '2':
        switch_port = input('Switch port that you want to add in a LAG, ie 21&22 or 5&6&7&8...etc: ')
        server_ip = input('server ip address: ')

        # 將 switch_port 拆分為數字列表
        # switch_port.split('&'): 這一部分使用字符串的split方法，將 switch_port 字符串根據 & 符號分割成多個子字符串。返回的結果是一個包含這些子字符串的列表。
        # [int(port.strip()) for port in ...]: 這是一個列表推導式。它遍歷 switch_port.split('&')中的每個子字符串，對每個子字符串執行操作，然後將結果收集成一個新的列表。
        # port.strip(): 對每個子字符串（port）使用strip方法，去除頭尾的空格（或換行符等）。
        # int(port.strip()): 將去除空格後的字符串轉換為整數。
        # 總之，這一行代碼的目的是將switch_port中以 & 符號分隔的數字部分提取出來，去除空格，並以整數形式存儲在ports列表中。例如，如果switch_port是字符串'21& 22 & 5 & 6'，則ports將成為整數列表[21, 22, 5, 6]。
        ports = [int(port.strip()) for port in switch_port.split('&')]

        # 找到最大的數字
        max_port = max(ports)

        print(f'''
interface Eth-Trunk{max_port}
 description {server_ip}/{switch_port}
 port default vlan102
 stp edged-port enable
 trust dscp
''', end=' ') # 將 end 設置為空字符串，以縮小 interface 10GE1/0/ 和下一個 interface 之間的距離

        # 為每個 port 生成一個獨立的 interface
        for port in ports:
            print(f'''
interface 10GE1/0/{port}
 description {server_ip}
 eth-trunk {max_port}
''', end=' ') # 將 end 設置為空字符串，以縮小 interface 10GE1/0/ 和下一個 interface 之間的距離

    elif mode == '4':
        switch_port = input('Switch port that you want to add in a LAG, ie 21&22 or 5&6&7&8...etc: ')
        server_ip = input('server ip address: ')
        ports = [int(port.strip()) for port in switch_port.split('&')]
        max_port = max(ports)
        print(f'''
interface Eth-Trunk{max_port}
 description {server_ip}/{switch_port}
 port default vlan102
 stp edged-port enable
 mode lacp-static
 trust dscp
''', end=' ') # 將 end 設置為空字符串，以縮小 interface 10GE1/0/ 和下一個 interface 之間的距離
        for port in ports:
            print(f'''
interface 10GE1/0/{port}
 description {server_ip}
 eth-trunk{max_port}
''', end=' ') # 將 end 設置為空字符串，以縮小 interface 10GE1/0/ 和下一個 interface 之間的距離

elif vendor == '2':
    if mode == '2':
        switch_port = input('Switch port that you want to add in a LAG, ie 21&22 or 5&6&7&8...etc: ')
        server_ip = input('Server IP: ')
        ports = [int(port.strip()) for port in switch_port.split('&')]
        max_port = max(ports)
        print(f'''
interface Bridge-Aggregation{max_port}
description {server_ip}/{switch_port}
port access vlan 102
stp edged-port
''', end=' ')
        for port in ports:
            print(f'''
interface Ten-GigabitEthernet1/0/{port}
port link-mode bridge
description {server_ip}
port access vlan 102
stp edged-port
stp tc-restriction
qos trust dscp
port link-aggregation group {max_port}
''', end=' ')
    elif mode == '4':
        switch_port = input('Switch port that you want to add in a LAG, ie 21&22 or 5&6&7&8...etc: ')
        server_ip = input('Server IP: ')
        ports = [int(port.strip()) for port in switch_port.split('&')]
        max_port = max(ports)
        print(f'''
interface Bridge-Aggregation{max_port}
 description {server_ip}/{switch_port}
 port access vlan 102
 link-aggregation mode dynamic
 stp edged-port
''', end=' ')
        for port in ports:
            print(f'''
interface Ten-GigabitEthernet1/0/{port}
 port link-mode bridge
 description {server_ip}
 port access vlan 102
 stp edged-port
 stp tc-restriction
 qos trust dscp
 port link-aggregation group {max_port}
''', end=' ')

elif vendor == '3':
    if mode == '2':
        switch_port = input('Switch port that you want to add in a LAG, ie 21&22 or 5&6&7&8...etc: ')
        server_ip = input('Server IP: ')
        ports = [int(port.strip()) for port in switch_port.split('&')]
        max_port = max(ports)
        print(f'''
interface Port-Channel{max_port}
description {server_ip}/{switch_port}
switchport access vlan 102
spanning-tree portfast
spanning-tree bpduguard enable        
''', end=' ')
        for port in ports:
            print(f'''
interface Ethernet{port}
description {server_ip}
switchport access vlan 102
channel-group {max_port} mode on
spanning-tree portfast
spanning-tree bpduguard enable
''', end=' ')

    elif mode == '4':
        switch_port = input('Switch port that you want to add in a LAG, ie 21&22 or 5&6&7&8...etc: ')
        server_ip = input('Server IP: ')
        ports = [int(port.strip()) for port in switch_port.split('&')]
        max_port = max(ports)
        print(f'''
interface Port-Channel{max_port}
description {server_ip}/{switch_port}
switchport access vlan 102
spanning-tree portfast
spanning-tree bpduguard enable        
''', end=' ')
        for port in ports:
            print(f'''
interface Ethernet{port}
description {server_ip}
switchport access vlan 102
channel-group {max_port} mode active
''', end=' ')

elif vendor == '4':
    if mode == '2':
        switch_port = input('Switch port that you want to add in a LAG, ie 21&22 or 5&6&7&8...etc: ')
        server_ip = input('Server IP: ')
        ports = [int(port.strip()) for port in switch_port.split('&')]
        max_port = max(ports)
        print(f'''
interface Port-Channel{max_port}
description {server_ip}/{switch_port}
switchport access vlan 102
spanning-tree portfast
spanning-tree bpduguard enable    
''', end=' ')
        for port in ports:
            print(f'''
interface Ethernet{port}
description {server_ip}
switchport access vlan 102
channel-group {max_port} mode on
spanning-tree portfast
spanning-tree bpduguard enable
''', end=' ')

    elif mode == '4':
        switch_port = input('Switch port that you want to add in a LAG, ie 21&22 or 5&6&7&8...etc: ')
        server_ip = input('Server IP: ')
        ports = [int(port.strip()) for port in switch_port.split('&')]
        max_port = max(ports)
        print(f'''
interface Port-Channel{max_port}
description {server_ip}/{switch_port}
switchport access vlan 102
spanning-tree port type edge
spanning-tree bpduguard enable    
''', end=' ')
        for port in ports:
            print(f'''
interface Ethernet{port}
description {server_ip}
switchport access vlan 102
spanning-tree port type edge
spanning-tree bpduguard enable
channel-group {max_port} mode active
''', end=' ')
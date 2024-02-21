# """
# Object:
# Mode 4 is mode active, Mode 2 is mode on:
# ***********************************
# Huawei mode 4 example:
# interface Eth-Trunk32
# description xxx.xxx.xxx.xxx/21&22
# port default vlan 102
# stp edged-port enable
# mode lacp-static
# trust dscp
#
# interface 10GE1/0/21
# description xxx.xxx.xxx.xxx
# eth-trunk 32
#
# Huawei mode 2 example:
# interface Eth-Trunk18
#
# description xxx.xxx.xxx.xxx/18&18
#
# port default vlan 102
#
# stp edged-port enable
#
# trust dscp
#
#
# interface 10GE1/0/18
#
# description xxx.xxx.xxx.xxx
#
# eth-trunk 18
#
# ***********************************
# ***********************************
# H3C mode 4 example:
# interface Bridge-Aggregation28
# description xxx.xxx.xxx.xxx/25&26&27&28
# port access vlan 102
# link-aggregation mode dynamic
# stp edged-port
#
# interface Ten-GigabitEthernet1/0/28
# port link-mode bridge
# description xxx.xxx.xxx.xxx
# port access vlan 102
# stp edged-port
# stp tc-restriction
# qos trust dscp
# port link-aggregation group 28
#
#
# H3C mode 2 example:
# interface Bridge-Aggregation56
# description xxx.xxx.xxx.xxx/15&16
# port access vlan 102
# stp edged-port
#
# interface Ten-GigabitEthernet1/0/15
# port link-mode bridge
# description xxx.xxx.xxx.xxx
# port access vlan 102
# stp edged-port
# stp tc-restriction
# qos trust dscp
# port link-aggregation group 56
# ***********************************
# #
# ***********************************
# Arista mode 4 example:
# interface Port-Channel32
# description xxx.xxx.xxx.xxx/19&20&21&22
# switchport access vlan 102
# spanning-tree portfast
# spanning-tree bpduguard enable
#
# interface Ethernet19
# description xxx.xxx.xxx.xxx
# switchport access vlan 102
# channel-group 32 mode active
# #
# Arista mode 2 example:
# interface Port-Channel24
# description xxx.xxx.xxx.xxx/23&24
# switchport access vlan 102
# spanning-tree portfast
# spanning-tree bpduguard enable
#
# interface Ethernet24
# description xxx.xxx.xxx.xxx
# switchport access vlan 102
# channel-group 24 mode on
# spanning-tree portfast
# spanning-tree bpduguard enable
# ***********************************
# #
# ***********************************
# Cisco mode 4 example:
# interface port-channel44
# description xxx.xxx.xxx.xxx
# switchport access vlan 102
# spanning-tree port type edge
# spanning-tree bpduguard enable
#
# interface Ethernet1/41
# description xxx.xxx.xxx.xxx
# switchport access vlan 102
# spanning-tree port type edge
# spanning-tree bpduguard enable
# channel-group 44 mode active
# #
# Cisco mode 2 example:
# interface Port-Channel24
# description 157.185.174.53/23&24
# switchport access vlan 102
# spanning-tree portfast
# spanning-tree bpduguard enable
#
# interface Ethernet24
# description 157.185.174.53
# switchport access vlan 102
# channel-group 24 mode on
# spanning-tree portfast
# spanning-tree bpduguard enable
# ***********************************
# """
#
# from flask import Flask, render_template, request
#
# # 创建一个 Flask 应用程序实例
# app = Flask(__name__)
#
# # 定义根路由 /，用于显示输入表单
# @app.route('/')
# def lag():
#     return render_template('lag.html')
#
# # 定义 /generate 路由，用于处理表单提交并生成配置和回滚计划
# @app.route('/generate', methods=['POST'])
# def generate_config():
#     # 从表单中获取用户输入的数据
#     vendor = request.form['vendor']     #在Flask应用程序中，使用request.form['vendor']来获取表单中名为'vendor'的字段的值。根据在網頁中（lag.html）用户选择的值（'1'代表Huawei，'2'代表Juniper），Flask应用程序将相应地生成配置和回滚计划。因此，系统知道用户选择了哪个供应商是通过在表单提交后获取名为'vendor'的字段的值来实现的。
#     hostname = request.form['hostname']
#     host_ip = request.form['host_ip']
#     next_hop_ip = request.form['next_hop_ip']
#     server_ips = request.form.getlist('server_ip')
#
#     # 根据用户选择的供应商生成配置和回滚计划
#     if vendor == '1':  # Huawei
#         var1 = []
#         for ip in server_ips:
#             if ip != '0':
#                 var1.append(f'ip route-static {ip} 255.255.255.255 {next_hop_ip}')
#
#         solution = f'''Solution:
# 1.On {hostname} ({host_ip}) router
#
# system-view
# #
# '''
#         for command in var1:
#             solution += command.strip() + '\n'
#
#         solution += '''#
# display configuration commit list
# #
# commit trial 300
# #
# commit
# return
# save
# '''
#
#         rollback_plan = f'''Rollback plan:
# 1.On {hostname}({host_ip}) router
#
# system-view
# #
# '''
#         for command in var1:
#             rollback_plan += f'undo {command}\n'
#
#         rollback_plan += '''#
# display configuration commit list
# #
# commit trial 300
# #
# commit
# return
# save
# '''
#     elif vendor == '2':  # Juniper
#         var1 = []
#         for ip in server_ips:
#             if ip != '0':
#                 var1.append(f'set routing-options static route {ip}/32 next-hop {next_hop_ip}')
#
#         solution = f'''Solution:
# 1.On {hostname} ({host_ip}) router
# configure
# #
# '''
#         for command in var1:
#             solution += command + '\n'
#
#         solution += '''#
# show | compare
# commit check
# commit confirmed 10
# #
# commit
# '''
#
#         rollback_plan = f'''Rollback plan:
# 1.On {hostname}({host_ip}) router
# configure
# #
# '''
#         for command in var1:
#             command_without_set = command.replace("set", "").strip()
#             rollback_plan += f'delete {command_without_set}\n'
#
#         rollback_plan += '''#
# show | compare
# commit check\
# commit confirmed 10
# #
# commit
# '''
#
#     # 返回生成的配置和回滚计划到结果页面
#     return render_template('lag_result.html', solution=solution, rollback_plan=rollback_plan)
#
# # 启动 Flask 应用程序
# if __name__ == '__main__':
#     app.run(debug=True)


##############################################################




"""
Object:
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

from flask import Flask, render_template, request

# 创建一个 Flask 应用程序实例
app = Flask(__name__)

# 定义根路由 /，用于显示输入表单
@app.route('/')
def lag():
    return render_template('lag.html')

# 定义 /generate 路由，用于处理表单提交并生成配置和回滚计划
@app.route('/generate', methods=['POST'])
def generate_config():
    # 从表单中获取用户输入的数据
    vendor = request.form['vendor']     #在Flask应用程序中，使用request.form['vendor']来获取表单中名为'vendor'的字段的值。根据在網頁中（lag.html）用户选择的值（'1'代表Huawei，'2'代表Juniper），Flask应用程序将相应地生成配置和回滚计划。因此，系统知道用户选择了哪个供应商是通过在表单提交后获取名为'vendor'的字段的值来实现的。
    mode = request.form['mode']
    switch_port = request.form['switch_port']
    server_ip = request.form['server_ip']
    ports = []  # 初始化 ports 變數為空列表,它給了選項vendor 1,2,3,4 的for port in ports 使用 , 將 ports 變數初始化為空列表，然後在適當的條件下再賦值.

    # 根据用户选择的供应商生成配置和回滚计划
    if vendor == '1':       # Huawei
        if mode == '2':     # Mode 2
            ports = [int(port.strip()) for port in switch_port.split('&')]
            max_port = max(ports)
            #$$$ 以下的 f'''不能用 print（f'''）把它包起來，不然 solutoin 就不被賦值
            solution = f'''                 
interface Eth-Trunk{max_port}
 description {server_ip}/{switch_port}
 port default vlan102
 stp edged-port enable
 trust dscp
'''

            for port in ports:
                solution = solution + f'''
interface 10GE1/0/{port}
description {server_ip}
eth-trunk {max_port}
'''

        if mode == '4':     # Mode 4
            ports = [int(port.strip()) for port in switch_port.split('&')]
            max_port = max(ports)
            solution = f'''
interface Eth-Trunk{max_port}
description {server_ip}/{switch_port}
port default vlan 102
stp edged-port enable
mode lacp-static
trust dscp
'''
            for port in ports:
                solution = solution + f'''
interface 10GE1/0/{port}
description {server_ip}
eth-trunk {max_port}
'''

    elif vendor == '2':     # H3C
        if mode == '2':     # Mode 2
           ports = [int(port.strip()) for port in switch_port.split('&')]
           max_port = max(ports)
           solution = f'''
interface Bridge-Aggregation{max_port}
description {server_ip}/{switch_port}
port access vlan 102
stp edged-port
'''

        for port in ports:
            solution = solution + f'''
interface Ten-GigabitEthernet1/0/{port}
port link-mode bridge
description {server_ip}
port access vlan 102
stp edged-port
stp tc-restriction
qos trust dscp
port link-aggregation group {max_port}
'''
        if mode == '4':
            ports = [int(port.strip()) for port in switch_port.split('&')]
            max_port = max(ports)
            solution = f'''
interface Bridge-Aggregation{max_port}
description {server_ip}/{switch_port}
port access vlan 102
link-aggregation mode dynamic
stp edged-port
'''
            for port in ports:
                solution = solution + f'''
interface Ten-GigabitEthernet1/0/{port}
port link-mode bridge
description {server_ip}
port access vlan 102
stp edged-port
stp tc-restriction
qos trust dscp
port link-aggregation group {max_port}
'''

    elif vendor == '3':  # Arista
        if mode == '2':  # Mode 2
            ports = [int(port.strip()) for port in switch_port.split('&')]
            max_port = max(ports)
            solution = f'''            
interface Port-Channel{max_port}
description {server_ip}/{switch_port}
switchport access vlan 102
spanning-tree portfast
spanning-tree bpduguard enable
'''

            for port in ports:
                solution = solution + f'''
interface Ethernet{port}
description {server_ip}
switchport access vlan 102
channel-group {max_port} mode on
spanning-tree portfast
spanning-tree bpduguard enable       
'''

        if mode == '4':
            ports = [int(port.strip()) for port in switch_port.split('&')]
            max_port = max(ports)
            solution = f'''
interface Port-Channel{max_port}
description {server_ip}/{switch_port}
switchport access vlan 102
spanning-tree portfast
spanning-tree bpduguard enable
'''
            for port in ports:
                solution = solution + f'''
interface Ethernet{port}
description {server_ip}
switchport access vlan 102
channel-group {max_port} mode active         
'''

    elif vendor == '4':  # Cisco
        if mode == '2':  # Mode 2
            ports = [int(port.strip()) for port in switch_port.split('&')]
            max_port = max(ports)
            solution = f'''            
interface Port-Channel{max_port}
description {server_ip}/{switch_port}
switchport access vlan 102
spanning-tree portfast
spanning-tree bpduguard enable
'''

            for port in ports:
                solution = solution + f'''
interface Ethernet{port}
description {server_ip}
switchport access vlan 102
channel-group {max_port} mode on
spanning-tree portfast
spanning-tree bpduguard enable       
'''
        if mode == '4':
            ports = [int(port.strip()) for port in switch_port.split('&')]
            max_port = max(ports)
            solution = f'''
interface Port-Channel{max_port}
description {server_ip}/{switch_port}
switchport access vlan 102
spanning-tree portfast
spanning-tree bpduguard enable
'''
            for port in ports:
                solution = solution + f'''
interface Ethernet{port}
description {server_ip}
switchport access vlan 102
channel-group {max_port} mode active         
'''

    # 返回生成的配置和回滚计划到结果页面
    return render_template('lag_result.html', solution=solution)

# 启动 Flask 应用程序
if __name__ == '__main__':
    app.run(debug=True)

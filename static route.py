#
""" Huawei Solution:
1.On Hostname (Host-IP) router
system-view
#
ip route-static xxx.xxx.xxx.xxx 255.255.255.255 xxx.xxx.xxx.xxx
ip route-static xxx.xxx.xxx.xxx 255.255.255.255 xxx.xxx.xxx.xxx
#
dis configuration commit list
#
commit trial 300
#
commit
return
save

Rollback plan:
1.On Hostname (Host-IP) router
system-view
#
undo ip route-static xxx.xxx.xxx.xxx 255.255.255.255 xxx.xxx.xxx.xxx
undo ip route-static xxx.xxx.xxx.xxx 255.255.255.255 xxx.xxx.xxx.xxx
#
dis configuration commit list
#
commit trial 300
#
commit
return
save
"""

"""
Juniper Solution:
Solution:
1. On Hostname (Host-IP) router
configure
#
set routing-options static route xxx.xxx.xxx.xxx/32 next-hop xxx.xxx.xxx.xxx
set routing-options static route xxx.xxx.xxx.xxx/32 next-hop xxx.xxx.xxx.xxx

#
show | compare
commit check
commit confirmed 10
#
commit

Rollback plan:
1. On Hostname (Host-IP) router
configure
#
delete routing-options static route xxx.xxx.xxx.xxx/32 next-hop xxx.xxx.xxx.xxx
delete routing-options static route xxx.xxx.xxx.xxx/32 next-hop xxx.xxx.xxx.xxx
#
show | compare
commit check
commit confirmed 10
#
commit
"""


#######################
vendor = input('Which vendor do you need, 1.Huawei or 2.Juniper:')
if vendor == '1':
    next_hop_ip = input('Next-hop IP:')
    server_ips = []
    var1 = []
    while True:
        server_ip = input('Please provide a Server IP, type 0 means no longer needed: ')
        if server_ip == '0':
            break
        server_ips.append(server_ip)

    for ip in server_ips:
        var1.append(f'ip route-static {ip} 255.255.255.255 {next_hop_ip}') #在形成 var1 列表時去除每個命令字符串的前導和尾隨空格,如 f' ip, IP 前不能有空隔。

    print('''Solution:

system-view
#''')
    for command in var1:
        print(command.strip())  # 去掉命令前面的空格

    print('''#
dis configuration commit list
#
commit trial 300
#
commit
return
save
''', end='')    # 使用 end='' 防止插入額外的空行
    print('''
Rollback plan:
system-view
#''')
    for command in var1:
        print(f'undo {command}')
    print('''#
dis configuration commit list
#
commit trial 300
#
commit
return
save
''')


elif vendor == '2':
    next_hop_ip = input('Next-hop IP:')
    server_ips = []
    var1 = []
    while True:
        server_ip = input('Please provide a Server IP, type 0 means no longer needed: ')
        if server_ip == '0':
            break
        server_ips.append(server_ip)
    for ip in server_ips:
        var1.append(f'set routing-options static route {ip}/32 next-hop {next_hop_ip}')
    print('''Solution:

configure
#
''', end='')
    for command in var1:
        print(command)
    print('''#
show | compare
commit check
commit confirmed 10
#
commit
''')
    print('''
Rollback plan:
configure
#
''', end='')
    for command in var1:
        command_without_set = command.replace("set","").strip()      # 去掉命令中的 "set" 并去除前后空格
        print(f'delete {command_without_set}')
    print('''#
show | compare
commit check
commit confirmed 10
#
commit
''')
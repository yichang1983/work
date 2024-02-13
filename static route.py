vendor = input('Which vendor do you need, 1.Huawei or 2.Juniper:')
if vendor == '1':
    next_hop_ip = input('Next-hop IP:')
    server_ips = []
    var1 = []
    while True:
        server_ip = input('Please provide a ServerIP, type 0 means no longer needed: ')
        if server_ip == '0':
            break
        server_ips.append(server_ip)

    for ip in server_ips:
        var1.append(f' ip route-static {ip} 255.255.255.255 {next_hop_ip} ')

    print('''
system-view
#''')
    for command in var1:
        print(command)

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
    while True:
        server_ip = input('ServerIP, if serverIP is 0 means no longer needed: ')
        if server_ip == '0':
            break
        server_ips.append(server_ip)
    for ip in server_ips:
        print(f'set routing-options static route {ip}/32 next-hop {next_hop_ip}')

#######################
# vendor = input('Which vendor do you need, 1.Huawei or 2.Juniper:')
# if vendor == '1':
#     next_hop_ip = input('Next-hop IP:')
#     server_ips = []
#     var1 = []
#     while True:
#         server_ip = input('Please provide a ServerIP, type 0 means no longer needed: ')
#         if server_ip == '0':
#             break
#         server_ips.append(server_ip)
#
#     for ip in server_ips:
#         var1.append(f'ip route-static {ip} 255.255.255.255 {next_hop_ip}')  # 將命令添加到列表中
#
#     print("""
# system-view
# #""")  # 打印開頭部分
#
#     for command in var1:
#         print(command)  # 逐行打印命令
#
#     print("""
# #
# dis configuration commit list
# #
# commit trial 300
# #
# commit
# return
# save
# """)  # 打印結尾部分
#
# elif vendor == '2':
#     next_hop_ip = input('Next-hop IP:')
#     server_ips = []
#     while True:
#         server_ip = input('ServerIP, if serverIP is 0 means no longer needed: ')
#         if server_ip == '0':
#             break
#         server_ips.append(server_ip)
#
#     for ip in server_ips:
#         print(f'set routing-options static route {ip}/32 next-hop {next_hop_ip}')

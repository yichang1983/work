# from flask import Flask, render_template, request
#
# # 创建一个 Flask 应用程序实例
# app = Flask(__name__)
#
# # 定义根路由 /，用于显示输入表单
# @app.route('/')
# def static_index():
#     return render_template('static_index.html')
#
# # 定义 /generate 路由，用于处理表单提交并生成配置和回滚计划
# @app.route('/generate', methods=['POST'])
# def generate_solution_static():
#     # 从表单中获取用户输入的数据
#     vendor = request.form['vendor']     #在Flask应用程序中，使用request.form['vendor']来获取表单中名为'vendor'的字段的值。根据在網頁中（static_index.html）用户选择的值（'1'代表Huawei，'2'代表Juniper），Flask应用程序将相应地生成配置和回滚计划。因此，系统知道用户选择了哪个供应商是通过在表单提交后获取名为'vendor'的字段的值来实现的。
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
# commit check
# commit confirmed 10
# #
# commit
# '''
#
#     # 返回生成的配置和回滚计划到结果页面
#     return solution
#








from flask import Flask, render_template, request

# 创建一个 Flask 应用程序实例
app = Flask(__name__)

# 定义根路由 /，用于显示输入表单
@app.route('/')
def static_index():
    return render_template('static_index.html')

# 定义 /generate 路由，用于处理表单提交并生成配置和回滚计划
@app.route('/generate', methods=['POST'])
def generate_solution_static():
    # 从表单中获取用户输入的数据
    vendor = request.form['vendor']     #在Flask应用程序中，使用request.form['vendor']来获取表单中名为'vendor'的字段的值。根据在網頁中（static_index.html）用户选择的值（'1'代表Huawei，'2'代表Juniper），Flask应用程序将相应地生成配置和回滚计划。因此，系统知道用户选择了哪个供应商是通过在表单提交后获取名为'vendor'的字段的值来实现的。
    hostname = request.form['hostname']
    host_ip = request.form['host_ip']
    next_hop_ip = request.form['next_hop_ip']
    server_ips = request.form.getlist('server_ip')

    # 根据用户选择的供应商生成配置和回滚计划
    if vendor == '1':  # Huawei
        var1 = []
        for ip in server_ips:
            if ip != '0':
                var1.append(f'ip route-static {ip} 255.255.255.255 {next_hop_ip}')

        solution = f'''Solution:
1.On {hostname} ({host_ip}) router

system-view
#
'''
        for command in var1:
            solution += command.strip() + '\n'

        solution += '''#
display configuration commit list
#
commit trial 300
#
commit
return
save

'''
        rollback_plan = f'''Rollback plan:
1.On {hostname}({host_ip}) router

system-view
#
'''
        for command in var1:
            rollback_plan += f'undo {command}\n'

        rollback_plan += '''#
display configuration commit list
#
commit trial 300
#
commit
return
save

'''
    elif vendor == '2':  # Juniper
        var1 = []
        for ip in server_ips:
            if ip != '0':
                var1.append(f'set routing-options static route {ip}/32 next-hop {next_hop_ip}')

        solution = f'''Solution:
1.On {hostname} ({host_ip}) router
configure
#
'''
        for command in var1:
            solution += command + '\n'

        solution += '''#
show | compare
commit check
commit confirmed 10
#
commit


'''

        rollback_plan = f'''Rollback plan:
1.On {hostname}({host_ip}) router
configure
#
'''
        for command in var1:
            command_without_set = command.replace("set", "").strip()
            rollback_plan += f'delete {command_without_set}\n'

        rollback_plan += '''#
show | compare
commit check
commit confirmed 10
#
commit

'''

    solution = solution + rollback_plan
    # 返回生成的配置和回滚计划到结果页面
    return solution




# -*- coding: utf-8 -*-
# from flask import Flask
#
# # 创建一个 Flask 应用程序实例
# app = Flask(__name__)
#
# # 定义一个简单的路由
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
#
# # 运行应用程序
# if __name__ == '__main__':
#     app.run(debug=True)


# Flask 的工作流程如下：
# 1.当你访问根路由 / 时，会显示一个表单，让你输入所需的信息。
# 2.当你在表单中输入信息并提交时，表单数据会被发送到 /generate 路由处理。
# 3.在 /generate 路由中，表单数据会被提取出来，并根据用户输入生成配置和回滚计划。
# 4.生成的配置和回滚计划会被传递到 result.html 模板文件中进行渲染。
# 5.最终，渲染后的结果会显示在浏览器中。

from flask import Flask, render_template, request

# 创建一个 Flask 应用程序实例
app = Flask(__name__)

# 定义根路由 /，用于显示输入表单：
# 这个路由函数用于处理根路由 / 的请求，它返回一个 HTML 模板文件 index.html，该模板包含用户输入所需信息的表单。
@app.route('/')
def index():
    return render_template('index.html')

# 定义 /generate 路由，用于处理表单提交并生成配置和回滚计划：
# 这个路由函数用于处理表单提交的请求，并从表单中获取用户输入的数据。然后根据用户输入生成配置和回滚计划，并将它们传递到 result.html 模板文件中进行渲染。
@app.route('/generate', methods=['POST'])
def generate_config():
    # 从表单中获取用户输入的数据
    vendor = request.form['vendor']
    hostname = request.form['hostname']
    host_ip = request.form['host_ip']
    next_hop_ip = request.form['next_hop_ip']
    server_ips = request.form.getlist('server_ip')

    # 根据用户输入生成配置和回滚计划
    var1 = []

    for ip in server_ips:
        if ip != '0':
            var1.append(f'ip route-static {ip} 255.255.255.255 {next_hop_ip}')

    solution = f'''Solution:
1.On {hostname} ({host_ip}) router

system-view
#'''
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

    rollback_plan = f'''
Rollback plan:
1.On {hostname}({host_ip}) router
system-view
#'''
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
    # 返回生成的配置和回滚计划到结果页面
    return render_template('result.html', solution=solution, rollback_plan=rollback_plan)

# 启动 Flask 应用程序：
# 这段代码确保只有在直接运行这个脚本时才启动 Flask 应用程序，而不是当它作为模块导入到其他脚本中时。debug=True 参数开启调试模式，当你对应用程序做出更改时，它会自动重启。
if __name__ == '__main__':
    app.run(debug=True)






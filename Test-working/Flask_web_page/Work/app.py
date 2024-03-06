import sys
import os
# 获取当前文件所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# programs目录的路径
programs_dir = os.path.join(current_dir, 'programs')

# 将programs目录添加到Python路径中
sys.path.append(programs_dir)

from flask import Flask, render_template, request
from static import generate_solution_static  # 导入 static.py 中的函数

app = Flask(__name__)

#### 一行一行的解釋下面它的用法
#@app.route('/'): 這是一個裝飾器(decorator)，用於將函數與指定的路徑綁定。在這個情況下，它將函數 index() 與根路徑 '/' 綁定在一起，意味著當用戶訪問根路徑時，將調用 index() 函數。
#定義了一個名為 index 的函數，這個函數將在訪問根路徑時被調用。
#該函數返回一個由 Flask 提供的 render_template 函數的呼叫，用於將模板文件 'index.html' 渲染成一個 HTML 響應。 呼叫 templates 資料夾內的index.html
@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/select', methods=['POST', 'GET']): 同樣是一個裝飾器，將函數 select() 與路徑 '/select' 綁定在一起。此外，它聲明了該路由支持 POST 和 GET 方法。
# def select():: 定義了名為 select 的函數，當訪問路徑 '/select' 時被調用。
# if request.method == 'POST' or 'choice' in request.args:: 檢查請求的方法是否為 POST，或者請求參數中是否包含名為 'choice' 的值。
# choice = request.form['choice'] if request.method == 'POST' else request.args.get('choice'): 根據請求的方法，從 POST 數據或 GET 參數中獲取名為 'choice' 的值。
# if choice == 'static':: 如果 choice 的值為 'static'，則返回靜態模板 'static_index.html'
# elif choice == 'lag':: 如果 choice 的值為 'lag'，則返回 'lag.html' 模板。
# return render_template('index.html'): 如果 choice 的值既不是 'static' 也不是 'lag'，則返回 'index.html' 模板。


@app.route('/select', methods=['POST', 'GET'])
def select():
    if request.method == 'POST' or 'choice' in request.args:
        choice = request.form['choice'] if request.method == 'POST' else request.args.get('choice')
        if choice == 'static':
            return render_template('static_index.html')
        elif choice == 'lag':
            return render_template('lag.html')
    return render_template('index.html')

# 同樣地，@app.route('/generate', methods=['POST', 'GET']) 將函數 generate_configuration() 綁定到路徑 '/generate' 上，同時聲明該路由支持 POST 和 GET 方法。
# def generate_configuration():: 定義了一個名為 generate_configuration 的函數，當訪問路徑 '/generate' 時被調用。
# if request.method == 'POST':: 檢查請求的方法是否為 POST。
# solution = generate_solution_static(): 如果是 POST 請求，調用static.py 中的函数 generate_solution_static() 函數來生成解決方案。
# return render_template('static_result.html', solution=solution): 返回 'static_result.html' 模板，並將生成的解決方案傳遞給模板
# else:: 如果請求方法不是 POST，則返回一個包含文本 "This is the generate_configuration page." 的響應。
@app.route('/generate', methods=['POST', 'GET'])
def generate_configuration():
    if request.method == 'POST':
        solution = generate_solution_static()
        return render_template('static_result.html', solution=solution)
    else:
        return "This is the generate_configuration page."

# if __name__ == '__main__':: 檢查是否正在直接運行這個腳本。
# app.run(debug=True): 如果是直接運行腳本，則啟動 Flask 應用程式，並開啟 debug 模式，這將在終端中顯示詳細的錯誤信息。
if __name__ == '__main__':
    app.run(debug=True)








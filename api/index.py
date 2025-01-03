from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# 配置静态文件目录
app.static_folder = 'app/static'
app.template_folder = 'app/templates'

# 导入路由
from app.routes import *

# 添加错误处理
@app.errorhandler(404)
def not_found_error(error):
    return {"error": "Not Found"}, 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Internal Server Error"}, 500

# 添加健康检查路由
@app.route('/health')
def health_check():
    return {"status": "healthy"}, 200

# 处理根路由
@app.route('/')
def index():
    return render_template('index.html') 
from flask import Flask, send_from_directory, render_template
import os

app = Flask(__name__, 
    static_folder='../app/static',
    template_folder='../app/templates'
)

# 配置上传文件夹路径
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
# 配置最大文件大小为16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
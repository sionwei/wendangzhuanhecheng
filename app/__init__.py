from flask import Flask
import os

app = Flask(__name__)

# 配置上传文件夹路径
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
# 配置最大文件大小为16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 导入路由
from app import routes 
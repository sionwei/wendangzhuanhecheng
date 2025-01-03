from flask import Flask, send_from_directory, render_template, request, jsonify
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

# 配置静态文件和模板目录
app.static_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app/static')
app.template_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app/templates')

# 配置
app.config.update(
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024,  # 降到5MB更安全
    UPLOAD_FOLDER = '/tmp',
    MAX_BUFFER_SIZE = 3 * 1024 * 1024  # 限制内存缓冲区
)

# 导入路由
from app import routes 
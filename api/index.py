from flask import Flask, send_from_directory, render_template, request, jsonify
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

# 配置静态文件和模板目录
app.static_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app/static')
app.template_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app/templates')

# 配置最大文件大小
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

# 导入路由
from app import routes 
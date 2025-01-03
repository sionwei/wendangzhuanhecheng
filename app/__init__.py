from flask import Flask, Blueprint

# 创建蓝图
app = Blueprint('main', __name__)

# 导入路由
from app import routes 
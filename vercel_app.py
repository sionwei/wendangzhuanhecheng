from flask import Flask
from app import app as flask_app

# 创建应用实例
app = Flask(__name__)

# 注册蓝图或路由
app.register_blueprint(flask_app)

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

if __name__ == '__main__':
    app.run() 
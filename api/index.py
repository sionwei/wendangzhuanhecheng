from flask import Flask, send_from_directory, render_template, request, jsonify
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

# 配置静态文件和模板目录
app.static_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app/static')
app.template_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app/templates')

# 配置上传文件夹路径
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
# 配置最大文件大小为16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 导入文档处理器
from app.document_processor import DocumentProcessor
processor = DocumentProcessor()

def allowed_file(filename):
    """检查文件是否允许上传"""
    ALLOWED_EXTENSIONS = {'doc', 'docx', 'pdf', 'txt', 'md'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'status': 'error', 'message': '没有上传文件'})
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({'status': 'error', 'message': '没有选择文件'})
    
    # 检查文件类型
    for file in files:
        if not allowed_file(file.filename):
            return jsonify({
                'status': 'error',
                'message': f'不支持的文件类型: {file.filename}'
            })
    
    try:
        # 保存文件并合并
        doc_id = processor.merge_documents(files)
        preview = processor.get_preview(doc_id)
        return jsonify({
            'status': 'success',
            'doc_id': doc_id,
            'preview': preview,
            'message': '文件上传并合成成功'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/preview/<doc_id>')
def get_preview(doc_id):
    try:
        preview = processor.get_preview(doc_id)
        if preview is None:
            return jsonify({'status': 'error', 'message': '文档不存在'})
        return jsonify({'status': 'success', 'preview': preview})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/export/<doc_id>')
def export_document(doc_id):
    format = request.args.get('format', 'docx')
    
    try:
        doc = processor.export_document(doc_id, format)
        
        if format == 'docx':
            # 保存为临时文件并发送
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{doc_id}.docx')
            doc.save(temp_path)
            return send_file(
                temp_path,
                as_attachment=True,
                download_name='merged_document.docx',
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
        elif format == 'pdf':
            # 直接发送PDF内容
            return send_file(
                io.BytesIO(doc),
                as_attachment=True,
                download_name='merged_document.pdf',
                mimetype='application/pdf'
            )
        elif format in ['txt', 'md']:
            # 直接发送文本内容
            mimetype = 'text/plain' if format == 'txt' else 'text/markdown'
            return send_file(
                io.BytesIO(doc),
                as_attachment=True,
                download_name=f'merged_document.{format}',
                mimetype=mimetype
            )
        else:
            return jsonify({'status': 'error', 'message': f'不支持的格式：{format}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

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
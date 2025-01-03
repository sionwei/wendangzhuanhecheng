from flask import render_template, request, jsonify, send_file, current_app
from app import app
from app.document_processor import DocumentProcessor
import os
from werkzeug.utils import secure_filename
import io
import mimetypes
import json

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
    
    layout_type = request.form.get('layout_type', 'default')
    style_config = None
    
    # 如果是自定义排版，获取样式配置
    if layout_type == 'custom':
        try:
            style_config = json.loads(request.form.get('style_config', '{}'))
        except json.JSONDecodeError:
            return jsonify({'status': 'error', 'message': '样式配置格式错误'})
    
    try:
        # 保存文件并合并
        doc_id = processor.merge_documents(files, layout_type, style_config)
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
            temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f'{doc_id}.docx')
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
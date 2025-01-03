from flask import render_template, request, jsonify, send_file, current_app
from app import app
from app.document_processor import DocumentProcessor
import os
from werkzeug.utils import secure_filename
import io
import mimetypes
import json

processor = DocumentProcessor()

# 修改配置常量
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 提高到10MB

def allowed_file(filename):
    """检查文件是否允许上传"""
    ALLOWED_EXTENSIONS = {'doc', 'docx', 'pdf', 'txt', 'md'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_files():
    try:
        if 'files' not in request.files:
            return jsonify({'status': 'error', 'message': '没有上传文件'})
        
        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return jsonify({'status': 'error', 'message': '没有选择文件'})
        
        # 检查文件大小
        for file in files:
            file.seek(0, 2)
            size = file.tell()
            file.seek(0)
            if size > MAX_CONTENT_LENGTH:
                return jsonify({
                    'status': 'error', 
                    'message': f'文件过大: {file.filename}. 最大允许10MB'
                })
        
        # 检查文件类型
        for file in files:
            if not allowed_file(file.filename):
                return jsonify({
                    'status': 'error',
                    'message': f'不支持的文件类型: {file.filename}'
                })
        
        layout_type = request.form.get('layout_type', 'default')
        style_config = None
        
        if layout_type == 'custom':
            try:
                style_config = json.loads(request.form.get('style_config', '{}'))
            except json.JSONDecodeError:
                return jsonify({'status': 'error', 'message': '样式配置格式错误'})
        
        # 使用内存中的文件对象处理
        doc_id = processor.merge_documents(files, layout_type, style_config)
        preview = processor.get_preview(doc_id)
        
        return jsonify({
            'status': 'success',
            'doc_id': doc_id,
            'preview': preview,
            'message': '文件上传并合成成功'
        })
        
    except Exception as e:
        # 详细的错误日志
        current_app.logger.error(f'Upload failed: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': '文件处理失败,请稍后重试',
            'detail': str(e)
        }), 500

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
        
        # 直接在内存中处理
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'merged_document.{format}',
            mimetype=mimetypes.guess_type(f'file.{format}')[0]
        )
    except Exception as e:
        current_app.logger.error(f'Export failed: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': '导出失败,请稍后重试'
        }), 500 
import os
from docx import Document
from docx.shared import Pt, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import markdown
import uuid
from werkzeug.utils import secure_filename
import io
import tempfile
from docx2pdf import convert

class DocumentProcessor:
    def __init__(self):
        self.documents = {}  # 使用内存字典存储文档
        self.previews = {}   # 存储预览文本
        
    def merge_documents(self, files, layout_type='default', style_config=None):
        """合并多个文档"""
        merged_doc = Document()
        doc_id = str(uuid.uuid4())
        preview_text = []
        
        try:
            for file in files:
                file_ext = file.filename.lower().split('.')[-1]
                content = file.read()
                
                if file_ext == 'docx':
                    doc = Document(io.BytesIO(content))
                    # 复制段落
                    for para in doc.paragraphs:
                        new_para = merged_doc.add_paragraph(para.text)
                        if layout_type == 'custom' and style_config:
                            self._apply_style(new_para, style_config)
                        preview_text.append(para.text)
                
                elif file_ext in ['txt', 'md']:
                    text = content.decode('utf-8')
                    if file_ext == 'md':
                        # 转换Markdown为纯文本
                        text = markdown.markdown(text)
                    paragraphs = text.split('\n')
                    for para in paragraphs:
                        if para.strip():  # 跳过空行
                            new_para = merged_doc.add_paragraph(para)
                            if layout_type == 'custom' and style_config:
                                self._apply_style(new_para, style_config)
                            preview_text.append(para)
            
            # 限制预览文本大小
            preview = '\n'.join(preview_text)
            if len(preview) > 50000:  # 限制预览长度为50KB
                preview = preview[:50000] + '...(预览已截断)'
            
            self.documents[doc_id] = merged_doc
            self.previews[doc_id] = preview
            return doc_id
            
        except Exception as e:
            raise Exception(f"文档合并失败: {str(e)}")
    
    def _apply_style(self, paragraph, style_config):
        """应用自定义样式"""
        try:
            # 字体设置
            if 'font_family_cn' in style_config:
                run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
                run.font.name = style_config['font_family_cn']
            
            # 字号设置
            if 'font_size' in style_config:
                size = float(style_config['font_size'])
                run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
                run.font.size = Pt(size)
            
            # 对齐方式
            if 'alignment' in style_config:
                align_map = {
                    'left': WD_ALIGN_PARAGRAPH.LEFT,
                    'center': WD_ALIGN_PARAGRAPH.CENTER,
                    'right': WD_ALIGN_PARAGRAPH.RIGHT,
                    'justify': WD_ALIGN_PARAGRAPH.JUSTIFY
                }
                paragraph.alignment = align_map.get(style_config['alignment'])
            
            # 行间距
            if 'line_spacing' in style_config:
                spacing = float(style_config['line_spacing'])
                paragraph.paragraph_format.line_spacing = spacing
            
            # 段落间距
            if 'space_before' in style_config:
                space = float(style_config['space_before'])
                paragraph.paragraph_format.space_before = Pt(space)
            
            if 'space_after' in style_config:
                space = float(style_config['space_after'])
                paragraph.paragraph_format.space_after = Pt(space)
            
            # 缩进
            if 'first_line_indent' in style_config:
                indent = float(style_config['first_line_indent'])
                paragraph.paragraph_format.first_line_indent = Cm(indent)
            
            if 'left_indent' in style_config:
                indent = float(style_config['left_indent'])
                paragraph.paragraph_format.left_indent = Cm(indent)
            
            if 'right_indent' in style_config:
                indent = float(style_config['right_indent'])
                paragraph.paragraph_format.right_indent = Cm(indent)
                
        except Exception as e:
            # 如果样式应用失败，记录错误但继续处理
            print(f"样式应用失败: {str(e)}")
    
    def get_preview(self, doc_id):
        """获取文档预览"""
        return self.previews.get(doc_id)
    
    def export_document(self, doc_id, format='docx'):
        """导出文档"""
        doc = self.documents.get(doc_id)
        if not doc:
            raise ValueError("文档不存在")
        
        if format == 'docx':
            return doc
        elif format in ['txt', 'md']:
            # 直接返回预览文本
            preview = self.get_preview(doc_id)
            if not preview:
                raise ValueError("预览文本不存在")
            return preview.encode('utf-8')
        else:
            raise ValueError(f"不支持的格式：{format}") 
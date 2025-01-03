# 文档合成工具

一个在线文档合成工具，支持多种格式文档的合并和转换。

## 功能特点

- 支持多文件上传和合并
- 支持Word、PDF、TXT、Markdown格式
- 自定义排版设置
  - 字体设置（中英文分别设置）
  - 段落格式（对齐方式、行间距）
  - 间距设置（段前段后间距）
  - 缩进设置（首行缩进、左右缩进）
- 实时预览
- 多格式导出
  - Word文档 (.docx)
  - PDF文档 (.pdf)
  - 文本文档 (.txt)
  - Markdown文档 (.md)
- 美观的用户界面
- 拖拽上传支持
- 进度显示和状态提示

## 技术栈

- 后端：Python + Flask
- 前端：HTML + CSS + JavaScript
- 文档处理：
  - python-docx (Word文档处理)
  - PyPDF2 (PDF文档处理)
  - markdown (Markdown处理)
  - docx2pdf (PDF转换)

## 安装说明

1. 克隆仓库：
```bash
git clone [仓库地址]
cd wendangzhuanhecheng
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 运行应用：
```bash
python run.py
```

5. 访问应用：
打开浏览器访问 http://localhost:5000

## 使用说明

1. 点击上传区域或拖拽文件到上传区域
2. 选择排版方式：
   - 保持原文档排版
   - 自定义排版（可设置字体、段落、间距等）
3. 点击"上传并合成"按钮
4. 在预览区查看效果
5. 选择所需格式导出文档

## 注意事项

- 支持的最大文件大小为16MB
- 请确保上传文件格式正确
- PDF导出功能需要安装Microsoft Word
- 建议使用现代浏览器以获得最佳体验

## 开发计划

- [ ] 添加更多文档格式支持
- [ ] 优化PDF导出功能
- [ ] 添加批量导出功能
- [ ] 添加文档模板功能
- [ ] 支持更多自定义样式选项

## 贡献指南

欢迎提交Issue和Pull Request。

## 许可证

MIT License 
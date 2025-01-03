import React, { useState } from 'react';

function FileUpload() {
  const [files, setFiles] = useState([]);
  const MAX_FILE_SIZE = 10 * 1024 * 1024;
  
  const handleUpload = (e) => {
    const uploadedFiles = Array.from(e.target.files).filter(file => {
      if (file.size > MAX_FILE_SIZE) {
        alert(`文件 ${file.name} 过大。最大允许 10MB`);
        return false;
      }
      return true;
    });
    
    setFiles(uploadedFiles);
  };

  return (
    <div className="upload-container">
      <input 
        type="file" 
        multiple
        accept=".docx,.txt,.md"
        onChange={handleUpload}
      />
      <div className="file-list">
        {files.map(file => (
          <div key={file.name}>{file.name}</div>
        ))}
      </div>
      <div className="upload-info">
        <p>支持的文件格式: DOCX, TXT, MD</p>
        <p>单个文件最大: 10MB</p>
      </div>
    </div>
  );
}

export default FileUpload; 
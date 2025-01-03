import React, { useState } from 'react';

function FileUpload() {
  const [files, setFiles] = useState([]);
  
  const handleUpload = (e) => {
    const uploadedFiles = Array.from(e.target.files);
    setFiles(uploadedFiles);
  };

  return (
    <div className="upload-container">
      <input 
        type="file" 
        multiple
        accept=".doc,.docx,.pdf"
        onChange={handleUpload}
      />
      <div className="file-list">
        {files.map(file => (
          <div key={file.name}>{file.name}</div>
        ))}
      </div>
    </div>
  );
}

export default FileUpload; 
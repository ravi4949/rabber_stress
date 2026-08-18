import React, { useState } from 'react';

interface UploadDropzoneProps {
  onFileSelect: (file: File) => void;
}

export const UploadDropzone: React.FC<UploadDropzoneProps> = ({ onFileSelect }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewRows, setPreviewRows] = useState<string[][]>([]);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const parseCsvPreview = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target?.result as string;
      if (!text) return;
      const lines = text.trim().split('\n').slice(0, 6);
      const rows = lines.map(line => line.split(',').map(cell => cell.trim()));
      setPreviewRows(rows);
    };
    reader.readAsText(file);
  };

  const handleFile = (file: File) => {
    if (!file.name.endsWith('.csv')) {
      setErrorMsg('Invalid file format. Please upload a .csv file.');
      return;
    }
    setErrorMsg(null);
    setSelectedFile(file);
    parseCsvPreview(file);
    onFileSelect(file);
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        style={{
          border: `2px dashed ${dragActive ? '#2563eb' : '#cbd5e1'}`,
          borderRadius: '8px',
          padding: '32px',
          textAlign: 'center',
          background: dragActive ? '#eff6ff' : '#f8fafc',
          cursor: 'pointer',
          transition: 'all 0.2s ease'
        }}
      >
        <input
          type="file"
          accept=".csv"
          onChange={handleChange}
          style={{ display: 'none' }}
          id="csv-file-input"
        />
        <label htmlFor="csv-file-input" style={{ cursor: 'pointer' }}>
          <p style={{ fontWeight: 600, fontSize: '1rem', color: '#1e293b', marginBottom: '4px' }}>
            {selectedFile ? `Selected: ${selectedFile.name}` : 'Click or Drag & Drop experimental test CSV'}
          </p>
          <p style={{ color: '#64748b', fontSize: '0.85rem' }}>
            Required columns: <code>stretch</code>, <code>stress</code>
          </p>
        </label>
      </div>

      {errorMsg && (
        <div style={{ padding: '10px', background: '#fef2f2', border: '1px solid #fca5a5', color: '#991b1b', borderRadius: '6px', fontSize: '0.9rem' }}>
          {errorMsg}
        </div>
      )}

      {previewRows.length > 0 && (
        <div style={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: '6px', padding: '12px' }}>
          <h4 style={{ fontSize: '0.85rem', color: '#64748b', marginBottom: '8px' }}>Client-Side CSV Sanity Preview (First 5 Rows):</h4>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
            <thead>
              <tr style={{ background: '#f1f5f9', textAlign: 'left' }}>
                {previewRows[0].map((header, idx) => (
                  <th key={idx} style={{ padding: '6px 8px', borderBottom: '1px solid #cbd5e1' }}>{header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {previewRows.slice(1).map((row, rIdx) => (
                <tr key={rIdx} style={{ borderBottom: '1px solid #f1f5f9' }}>
                  {row.map((cell, cIdx) => (
                    <td key={cIdx} style={{ padding: '6px 8px' }}>{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

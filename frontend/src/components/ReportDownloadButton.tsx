import React from 'react';
import { analysesApi } from '../api/analyses';

interface ReportDownloadButtonProps {
  runId: string;
  format?: 'pdf' | 'csv';
}

export const ReportDownloadButton: React.FC<ReportDownloadButtonProps> = ({ runId, format = 'pdf' }) => {
  const handleDownload = () => {
    const url = analysesApi.downloadReportUrl(runId, format);
    const a = document.createElement('a');
    a.href = url;
    a.download = `RubberStress_${runId}.${format}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <button
      onClick={handleDownload}
      style={{
        padding: '8px 14px',
        backgroundColor: format === 'pdf' ? '#dc2626' : '#16a34a',
        color: '#ffffff',
        border: 'none',
        borderRadius: '6px',
        fontWeight: 600,
        fontSize: '0.85rem',
        cursor: 'pointer',
        display: 'inline-flex',
        alignItems: 'center',
        gap: '6px'
      }}
    >
      Download {format.toUpperCase()} {format === 'pdf' ? 'Report' : 'Curves Export'}
    </button>
  );
};

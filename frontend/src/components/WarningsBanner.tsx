import React from 'react';

interface WarningsBannerProps {
  warnings: string[];
}

export const WarningsBanner: React.FC<WarningsBannerProps> = ({ warnings }) => {
  if (!warnings || warnings.length === 0) return null;

  return (
    <div style={{ padding: '12px 16px', background: '#fffbeb', border: '1px solid #fde68a', borderRadius: '8px', color: '#92400e' }}>
      <h4 style={{ margin: 0, fontSize: '0.9rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
        ⚠️ Model Fitting Warnings ({warnings.length}):
      </h4>
      <ul style={{ margin: '6px 0 0 18px', padding: 0, fontSize: '0.85rem' }}>
        {warnings.map((warn, idx) => (
          <li key={idx}>{warn}</li>
        ))}
      </ul>
    </div>
  );
};

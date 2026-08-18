import React from 'react';

interface MetricsSummaryProps {
  metrics: Record<string, number>;
  fittedParams?: Record<string, number | string>;
}

export const MetricsSummary: React.FC<MetricsSummaryProps> = ({ metrics, fittedParams }) => {
  const r2 = metrics.r2_score ?? metrics.r2 ?? 0;
  const rmse = metrics.rmse ?? 0;
  const mae = metrics.mae ?? 0;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px' }}>
        <div style={{ background: '#fff', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <span style={{ fontSize: '0.8rem', color: '#64748b', textTransform: 'uppercase', fontWeight: 600 }}>Goodness of Fit ($R^2$)</span>
          <div style={{ fontSize: '1.75rem', fontWeight: 700, color: r2 >= 0.95 ? '#16a34a' : '#d97706', marginTop: '4px' }}>
            {r2.toFixed(4)}
          </div>
        </div>

        <div style={{ background: '#fff', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <span style={{ fontSize: '0.8rem', color: '#64748b', textTransform: 'uppercase', fontWeight: 600 }}>Root Mean Square Error</span>
          <div style={{ fontSize: '1.75rem', fontWeight: 700, color: '#2563eb', marginTop: '4px' }}>
            {rmse.toFixed(4)} <span style={{ fontSize: '0.9rem', fontWeight: 500 }}>MPa</span>
          </div>
        </div>

        <div style={{ background: '#fff', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <span style={{ fontSize: '0.8rem', color: '#64748b', textTransform: 'uppercase', fontWeight: 600 }}>Mean Absolute Error</span>
          <div style={{ fontSize: '1.75rem', fontWeight: 700, color: '#475569', marginTop: '4px' }}>
            {mae.toFixed(4)} <span style={{ fontSize: '0.9rem', fontWeight: 500 }}>MPa</span>
          </div>
        </div>
      </div>

      {fittedParams && (
        <div style={{ background: '#fff', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <h4 style={{ fontSize: '0.9rem', color: '#1e293b', marginBottom: '12px' }}>Fitted Material Parameters</h4>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '8px' }}>
            {Object.entries(fittedParams).map(([key, val]) => (
              <div key={key} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 10px', background: '#f8fafc', borderRadius: '4px', fontSize: '0.85rem' }}>
                <span style={{ color: '#64748b', fontWeight: 500 }}>{key}</span>
                <span style={{ fontFamily: 'monospace', fontWeight: 600 }}>{val}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

import React, { useState } from 'react';
import { ManualPoint } from '../types/api';

interface ManualEntryFormProps {
  onSubmit: (points: ManualPoint[]) => void;
}

export const ManualEntryForm: React.FC<ManualEntryFormProps> = ({ onSubmit }) => {
  const [rows, setRows] = useState<ManualPoint[]>([
    { stretch: 1.0, stress: 0.0 },
    { stretch: 1.5, stress: 1.25 },
    { stretch: 2.0, stress: 2.85 },
    { stretch: 2.5, stress: 4.90 },
  ]);

  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleRowChange = (index: number, field: 'stretch' | 'stress', value: string) => {
    const num = parseFloat(value);
    const updated = [...rows];
    updated[index] = { ...updated[index], [field]: isNaN(num) ? 0 : num };
    setRows(updated);
  };

  const addRow = () => {
    const lastRow = rows[rows.length - 1];
    const newStretch = lastRow ? lastRow.stretch + 0.5 : 1.0;
    setRows([...rows, { stretch: newStretch, stress: 0.0 }]);
  };

  const removeRow = (index: number) => {
    if (rows.length <= 3) {
      setErrorMsg('At least 3 test points are required for hyperelastic model fitting.');
      return;
    }
    setErrorMsg(null);
    setRows(rows.filter((_, idx) => idx !== index));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (rows.length < 3) {
      setErrorMsg('At least 3 test points are required for hyperelastic model fitting.');
      return;
    }
    setErrorMsg(null);
    onSubmit(rows);
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <p style={{ fontSize: '0.9rem', color: '#64748b', margin: 0 }}>
        Enter test data points below (Stretch ratio $\lambda \ge 1.0$, Stress in MPa).
      </p>

      {errorMsg && (
        <div style={{ padding: '8px 12px', background: '#fef2f2', border: '1px solid #fca5a5', color: '#991b1b', borderRadius: '6px', fontSize: '0.85rem' }}>
          {errorMsg}
        </div>
      )}

      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ background: '#f8fafc', textAlign: 'left', borderBottom: '1px solid #e2e8f0' }}>
            <th style={{ padding: '8px' }}>#</th>
            <th style={{ padding: '8px' }}>Stretch ($\lambda$)</th>
            <th style={{ padding: '8px' }}>Nominal Stress (MPa)</th>
            <th style={{ padding: '8px', textAlign: 'center' }}>Action</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr key={idx} style={{ borderBottom: '1px solid #f1f5f9' }}>
              <td style={{ padding: '8px', color: '#64748b', fontWeight: 500 }}>{idx + 1}</td>
              <td style={{ padding: '8px' }}>
                <input
                  type="number"
                  step="0.01"
                  min="1.0"
                  value={row.stretch}
                  onChange={(e) => handleRowChange(idx, 'stretch', e.target.value)}
                  style={{ width: '100%', padding: '6px 8px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
                />
              </td>
              <td style={{ padding: '8px' }}>
                <input
                  type="number"
                  step="0.01"
                  value={row.stress}
                  onChange={(e) => handleRowChange(idx, 'stress', e.target.value)}
                  style={{ width: '100%', padding: '6px 8px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
                />
              </td>
              <td style={{ padding: '8px', textAlign: 'center' }}>
                <button
                  type="button"
                  onClick={() => removeRow(idx)}
                  style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', fontWeight: 600 }}
                >
                  Remove
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '8px' }}>
        <button
          type="button"
          onClick={addRow}
          style={{ padding: '6px 12px', background: '#f1f5f9', border: '1px solid #cbd5e1', borderRadius: '6px', cursor: 'pointer', fontWeight: 500 }}
        >
          + Add Point Row
        </button>
        <span style={{ fontSize: '0.85rem', color: '#64748b' }}>Total points: {rows.length}</span>
      </div>
    </form>
  );
};

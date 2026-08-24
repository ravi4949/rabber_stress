import React from 'react';
import { DeformationMode } from '../types/api';

interface DeformationModeSelectProps {
  value: DeformationMode;
  onChange: (mode: DeformationMode) => void;
}

export const DeformationModeSelect: React.FC<DeformationModeSelectProps> = ({ value, onChange }) => {
  return (
    <div>
      <label style={{ display: 'block', fontWeight: 600, marginBottom: '6px', color: '#1e293b' }}>
        Deformation State / Loading Mode
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value as DeformationMode)}
        style={{
          width: '100%',
          padding: '10px 12px',
          borderRadius: '6px',
          border: '1px solid #cbd5e1',
          fontSize: '0.95rem',
          background: '#fff'
        }}
      >
        <option value="uniaxial">Uniaxial Tension ($\lambda_1 = \lambda$)</option>
        <option value="biaxial">Equibiaxial Tension ($\lambda_1 = \lambda_2 = \lambda$)</option>
      </select>
    </div>
  );
};

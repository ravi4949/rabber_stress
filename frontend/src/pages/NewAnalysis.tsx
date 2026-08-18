import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadDropzone } from '../components/UploadDropzone';
import { ManualEntryForm } from '../components/ManualEntryForm';
import { DeformationModeSelect } from '../components/DeformationModeSelect';
import { DeformationMode, ManualPoint, MaterialSample } from '../types/api';
import { analysesApi } from '../api/analyses';

export const NewAnalysis: React.FC = () => {
  const [tab, setTab] = useState<'upload' | 'manual'>('upload');
  const [mode, setMode] = useState<DeformationMode>('uniaxial');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [materials, setMaterials] = useState<MaterialSample[]>([]);
  const [selectedSampleId, setSelectedSampleId] = useState<number | undefined>(undefined);
  const [showNewMaterialInput, setShowNewMaterialInput] = useState(false);
  const [newMaterialName, setNewMaterialName] = useState('');
  const [isCreatingMaterial, setIsCreatingMaterial] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchMaterials = async () => {
      try {
        const data = await analysesApi.listMaterials();
        setMaterials(data);
      } catch (err) {
        console.error('Failed to fetch materials list:', err);
      }
    };
    fetchMaterials();
  }, []);

  const handleCreateMaterial = async () => {
    if (!newMaterialName.trim()) return;
    setIsCreatingMaterial(true);
    try {
      const created = await analysesApi.createMaterial(newMaterialName.trim());
      setMaterials((prev) => [...prev, created]);
      setSelectedSampleId(created.id);
      setNewMaterialName('');
      setShowNewMaterialInput(false);
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Failed to create material sample.');
    } finally {
      setIsCreatingMaterial(false);
    }
  };

  const handleCsvSubmit = async () => {
    if (!selectedFile) {
      setErrorMsg('Please select a valid CSV test data file.');
      return;
    }
    setErrorMsg(null);
    setIsSubmitting(true);

    try {
      const res = await analysesApi.submitCsv(selectedFile, mode, selectedSampleId);
      navigate(`/analyses/${res.run_id}/status`);
    } catch (err: any) {
      const detail = err.response?.data?.detail || 'Analysis submission failed.';
      setErrorMsg(detail);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleManualSubmit = async (points: ManualPoint[]) => {
    setErrorMsg(null);
    setIsSubmitting(true);

    try {
      const res = await analysesApi.submitManual(points, mode, selectedSampleId);
      navigate(`/analyses/${res.run_id}/status`);
    } catch (err: any) {
      const detail = err.response?.data?.detail || 'Analysis submission failed.';
      setErrorMsg(detail);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: '650px', margin: '40px auto', padding: '32px', background: '#fff', borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }}>
      <h2 style={{ fontSize: '1.3rem', color: '#1e293b', marginBottom: '4px' }}>New Hyperelastic Material Analysis</h2>
      <p style={{ fontSize: '0.85rem', color: '#64748b', marginBottom: '24px' }}>
        Submit stress-strain test data to fit a CANN constitutive model.
      </p>

      {errorMsg && (
        <div style={{ padding: '12px', background: '#fef2f2', border: '1px solid #fca5a5', color: '#991b1b', borderRadius: '6px', fontSize: '0.85rem', marginBottom: '20px' }}>
          {errorMsg}
        </div>
      )}

      {/* Material Sample Selection */}
      <div style={{ marginBottom: '20px', background: '#f8fafc', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
        <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: '#334155', marginBottom: '8px' }}>
          Material Sample Tag (Optional):
        </label>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <select
            value={selectedSampleId || ''}
            onChange={(e) => setSelectedSampleId(e.target.value ? Number(e.target.value) : undefined)}
            style={{ flex: 1, padding: '8px 12px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.85rem' }}
          >
            <option value="">-- General Uncategorized Sample --</option>
            {materials.map((m) => (
              <option key={m.id} value={m.id}>{m.name}</option>
            ))}
          </select>
          <button
            type="button"
            onClick={() => setShowNewMaterialInput(!showNewMaterialInput)}
            style={{ padding: '8px 12px', background: '#e2e8f0', color: '#1e293b', border: 'none', borderRadius: '6px', fontWeight: 600, fontSize: '0.85rem', cursor: 'pointer' }}
          >
            {showNewMaterialInput ? 'Cancel' : '+ New Material'}
          </button>
        </div>

        {showNewMaterialInput && (
          <div style={{ display: 'flex', gap: '8px', marginTop: '10px' }}>
            <input
              type="text"
              placeholder="e.g. Carbon Black Compound B-102"
              value={newMaterialName}
              onChange={(e) => setNewMaterialName(e.target.value)}
              style={{ flex: 1, padding: '8px 12px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.85rem' }}
            />
            <button
              type="button"
              onClick={handleCreateMaterial}
              disabled={isCreatingMaterial || !newMaterialName.trim()}
              style={{ padding: '8px 14px', background: '#16a34a', color: '#fff', border: 'none', borderRadius: '6px', fontWeight: 600, fontSize: '0.85rem', cursor: 'pointer' }}
            >
              {isCreatingMaterial ? 'Saving...' : 'Save Tag'}
            </button>
          </div>
        )}
      </div>

      <div style={{ marginBottom: '20px' }}>
        <DeformationModeSelect value={mode} onChange={setMode} />
      </div>

      <div style={{ display: 'flex', borderBottom: '2px solid #e2e8f0', marginBottom: '20px' }}>
        <button
          type="button"
          onClick={() => setTab('upload')}
          style={{
            padding: '10px 16px',
            border: 'none',
            background: 'none',
            fontWeight: 600,
            fontSize: '0.9rem',
            borderBottom: tab === 'upload' ? '3px solid #2563eb' : '3px solid transparent',
            color: tab === 'upload' ? '#2563eb' : '#64748b',
            cursor: 'pointer'
          }}
        >
          Upload CSV Dataset
        </button>
        <button
          type="button"
          onClick={() => setTab('manual')}
          style={{
            padding: '10px 16px',
            border: 'none',
            background: 'none',
            fontWeight: 600,
            fontSize: '0.9rem',
            borderBottom: tab === 'manual' ? '3px solid #2563eb' : '3px solid transparent',
            color: tab === 'manual' ? '#2563eb' : '#64748b',
            cursor: 'pointer'
          }}
        >
          Manual Point Entry
        </button>
      </div>

      {tab === 'upload' ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <UploadDropzone onFileSelect={setSelectedFile} />
          <button
            onClick={handleCsvSubmit}
            disabled={!selectedFile || isSubmitting}
            style={{
              padding: '12px',
              background: '#2563eb',
              color: '#fff',
              border: 'none',
              borderRadius: '6px',
              fontWeight: 600,
              cursor: (!selectedFile || isSubmitting) ? 'not-allowed' : 'pointer',
              opacity: (!selectedFile || isSubmitting) ? 0.6 : 1
            }}
          >
            {isSubmitting ? 'Uploading & Queuing Job...' : 'Submit CSV for CANN Fitting'}
          </button>
        </div>
      ) : (
        <ManualEntryForm onSubmit={handleManualSubmit} />
      )}
    </div>
  );
};

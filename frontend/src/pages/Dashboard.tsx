import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { analysesApi } from '../api/analyses';
import { AnalysisRun, MaterialSample } from '../types/api';

export const Dashboard: React.FC = () => {
  const [runs, setRuns] = useState<AnalysisRun[]>([]);
  const [materials, setMaterials] = useState<MaterialSample[]>([]);
  const [selectedMaterialFilter, setSelectedMaterialFilter] = useState<string>('all');
  const [selectedModeFilter, setSelectedModeFilter] = useState<string>('all');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();

  const loadData = async (materialFilter = selectedMaterialFilter, modeFilter = selectedModeFilter) => {
    setIsLoading(true);
    setError(null);
    try {
      const sampleIdParam =
        materialFilter === 'uncategorized'
          ? 'uncategorized'
          : materialFilter !== 'all'
          ? Number(materialFilter)
          : undefined;

      const [runsData, materialsData] = await Promise.all([
        analysesApi.listAnalyses(0, 50, sampleIdParam, modeFilter),
        analysesApi.listMaterials(),
      ]);
      setRuns(runsData);
      setMaterials(materialsData);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load analysis history.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData(selectedMaterialFilter, selectedModeFilter);
  }, [selectedMaterialFilter, selectedModeFilter]);

  const handleUpdateRunTag = async (runId: string, newSampleIdStr: string) => {
    const newSampleId = newSampleIdStr ? Number(newSampleIdStr) : undefined;
    try {
      await analysesApi.updateRunTag(runId, newSampleId);
      // Reload history to reflect updated tag
      loadData(selectedMaterialFilter, selectedModeFilter);
    } catch (err) {
      console.error('Failed to update run material tag:', err);
    }
  };

  return (
    <div style={{ padding: '32px', maxWidth: '1150px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h2 style={{ fontSize: '1.4rem', color: '#1e293b', margin: 0 }}>Material Test Analysis History</h2>
          <p style={{ fontSize: '0.85rem', color: '#64748b', margin: '4px 0 0 0' }}>Track hyperelastic CANN model fits across test samples</p>
        </div>
        <button
          onClick={() => navigate('/analyses/new')}
          style={{
            padding: '10px 18px',
            background: '#2563eb',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            fontWeight: 600,
            cursor: 'pointer',
            fontSize: '0.9rem'
          }}
        >
          + New Material Analysis
        </button>
      </div>

      {/* History Analysis Filters */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', alignItems: 'center', marginBottom: '20px', background: '#f8fafc', padding: '14px 18px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <label style={{ fontSize: '0.85rem', fontWeight: 600, color: '#475569' }}>Filter by Material Tag:</label>
          <select
            value={selectedMaterialFilter}
            onChange={(e) => setSelectedMaterialFilter(e.target.value)}
            style={{ padding: '8px 12px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.85rem', minWidth: '200px' }}
          >
            <option value="all">All Material Samples ({runs.length})</option>
            <option value="uncategorized">Uncategorized (General)</option>
            {materials.map((m) => (
              <option key={m.id} value={m.id.toString()}>{m.name}</option>
            ))}
          </select>
        </div>

        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <label style={{ fontSize: '0.85rem', fontWeight: 600, color: '#475569' }}>Deformation Mode:</label>
          <select
            value={selectedModeFilter}
            onChange={(e) => setSelectedModeFilter(e.target.value)}
            style={{ padding: '8px 12px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.85rem', minWidth: '160px' }}
          >
            <option value="all">All Modes</option>
            <option value="uniaxial">Uniaxial</option>
            <option value="biaxial">Equibiaxial</option>
          </select>
        </div>

        {(selectedMaterialFilter !== 'all' || selectedModeFilter !== 'all') && (
          <button
            onClick={() => {
              setSelectedMaterialFilter('all');
              setSelectedModeFilter('all');
            }}
            style={{ padding: '6px 12px', background: '#e2e8f0', color: '#475569', border: 'none', borderRadius: '6px', fontSize: '0.8rem', fontWeight: 600, cursor: 'pointer', marginLeft: 'auto' }}
          >
            Clear Filters
          </button>
        )}
      </div>

      {isLoading ? (
        <div style={{ padding: '40px', textAlign: 'center', color: '#64748b' }}>Loading history...</div>
      ) : error ? (
        <div style={{ padding: '16px', background: '#fef2f2', border: '1px solid #fca5a5', color: '#991b1b', borderRadius: '6px' }}>
          {error}
        </div>
      ) : runs.length === 0 ? (
        <div style={{ padding: '40px', background: '#fff', border: '1px solid #e2e8f0', borderRadius: '8px', textAlign: 'center', color: '#64748b' }}>
          {selectedMaterialFilter !== 'all' || selectedModeFilter !== 'all'
            ? 'No history analysis runs match the selected filters.'
            : 'No past analysis runs found. Click "+ New Material Analysis" to upload test data.'}
        </div>
      ) : (
        <div style={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: '8px', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
            <thead>
              <tr style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0', textAlign: 'left' }}>
                <th style={{ padding: '12px 16px' }}>Date</th>
                <th style={{ padding: '12px 16px' }}>Run ID</th>
                <th style={{ padding: '12px 16px' }}>Material Tag</th>
                <th style={{ padding: '12px 16px' }}>Deformation Mode</th>
                <th style={{ padding: '12px 16px' }}>Status</th>
                <th style={{ padding: '12px 16px' }}>$R^2$ Score</th>
                <th style={{ padding: '12px 16px', textAlign: 'right' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {runs.map((run) => {
                const r2 = run.result?.metrics?.r2_score ?? run.result?.metrics?.r2;
                return (
                  <tr key={run.id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                    <td style={{ padding: '12px 16px', color: '#64748b' }}>
                      {new Date(run.created_at).toLocaleDateString()}
                    </td>
                    <td style={{ padding: '12px 16px', fontFamily: 'monospace', fontSize: '0.85rem' }}>
                      {run.id.slice(0, 8)}...
                    </td>
                    <td style={{ padding: '12px 16px' }}>
                      <select
                        value={run.material_sample_id || ''}
                        onChange={(e) => handleUpdateRunTag(run.id, e.target.value)}
                        style={{
                          padding: '4px 8px',
                          borderRadius: '6px',
                          border: '1px solid #cbd5e1',
                          fontSize: '0.8rem',
                          background: run.material_sample_id ? '#eff6ff' : '#f8fafc',
                          color: run.material_sample_id ? '#1d4ed8' : '#64748b',
                          fontWeight: 500
                        }}
                      >
                        <option value="">Uncategorized</option>
                        {materials.map((m) => (
                          <option key={m.id} value={m.id}>{m.name}</option>
                        ))}
                      </select>
                    </td>
                    <td style={{ padding: '12px 16px', textTransform: 'capitalize' }}>
                      {run.deformation_mode.replace('_', ' ')}
                    </td>
                    <td style={{ padding: '12px 16px' }}>
                      <span
                        style={{
                          padding: '4px 8px',
                          borderRadius: '12px',
                          fontSize: '0.75rem',
                          fontWeight: 700,
                          textTransform: 'uppercase',
                          background:
                            run.status === 'done'
                              ? '#dcfce7'
                              : run.status === 'failed'
                              ? '#fee2e2'
                              : '#fef9c3',
                          color:
                            run.status === 'done'
                              ? '#15803d'
                              : run.status === 'failed'
                              ? '#991b1b'
                              : '#a16207',
                        }}
                      >
                        {run.status}
                      </span>
                    </td>
                    <td style={{ padding: '12px 16px', fontWeight: 600 }}>
                      {r2 !== undefined ? r2.toFixed(4) : '-'}
                    </td>
                    <td style={{ padding: '12px 16px', textAlign: 'right' }}>
                      <button
                        onClick={() =>
                          navigate(run.status === 'done' ? `/analyses/${run.id}/results` : `/analyses/${run.id}/status`)
                        }
                        style={{ background: 'none', border: 'none', color: '#2563eb', cursor: 'pointer', fontWeight: 600 }}
                      >
                        View Details
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

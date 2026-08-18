import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { analysesApi } from '../api/analyses';
import { AnalysisRun } from '../types/api';

export const JobStatus: React.FC = () => {
  const { runId } = useParams<{ runId: string }>();
  const navigate = useNavigate();

  const [job, setJob] = useState<AnalysisRun | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!runId) return;

    let isMounted = true;

    const checkStatus = async () => {
      try {
        const data = await analysesApi.getJobStatus(runId);
        if (!isMounted) return;

        setJob(data);

        if (data.status === 'done') {
          navigate(`/analyses/${runId}/results`, { replace: true });
        } else if (data.status === 'failed') {
          setErrorMsg(data.error_message || 'Model optimization failed.');
        }
      } catch (err: any) {
        if (isMounted) {
          setErrorMsg(err.response?.data?.detail || 'Failed to poll job status.');
        }
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 2000);

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, [runId, navigate]);

  return (
    <div style={{ maxWidth: '550px', margin: '80px auto', padding: '36px', background: '#fff', borderRadius: '8px', border: '1px solid #e2e8f0', textAlign: 'center', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }}>
      <h3 style={{ fontSize: '1.25rem', color: '#1e293b', marginBottom: '8px' }}>CANN Model Optimization Job</h3>
      <p style={{ fontSize: '0.85rem', color: '#64748b', marginBottom: '24px' }}>
        Run ID: <code style={{ fontFamily: 'monospace' }}>{runId}</code>
      </p>

      {errorMsg ? (
        <div style={{ padding: '16px', background: '#fef2f2', border: '1px solid #fca5a5', color: '#991b1b', borderRadius: '6px', textAlign: 'left' }}>
          <h4 style={{ margin: '0 0 6px 0', fontSize: '0.95rem' }}>Analysis Failed</h4>
          <p style={{ margin: 0, fontSize: '0.85rem' }}>{errorMsg}</p>
          <div style={{ marginTop: '16px', textAlign: 'right' }}>
            <Link to="/analyses/new" style={{ color: '#2563eb', fontWeight: 600, fontSize: '0.85rem', textDecoration: 'none' }}>
              ← Try Again with New Analysis
            </Link>
          </div>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
          <div style={{ width: '48px', height: '48px', border: '4px solid #e2e8f0', borderTopColor: '#2563eb', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
          <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
          <p style={{ fontWeight: 600, color: '#1e293b', margin: 0 }}>
            {job?.status === 'queued' ? 'Job queued in background worker...' : 'Fitting neural strain energy model (CANN)...'}
          </p>
          <p style={{ fontSize: '0.8rem', color: '#64748b', margin: 0 }}>
            Evaluating invariants & autograd stress derivatives. Please wait.
          </p>
        </div>
      )}
    </div>
  );
};

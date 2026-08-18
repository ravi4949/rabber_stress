import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { analysesApi } from '../api/analyses';
import { AnalysisRun } from '../types/api';
import { WarningsBanner } from '../components/WarningsBanner';
import { StressStrainChart } from '../components/StressStrainChart';
import { MetricsSummary } from '../components/MetricsSummary';
import { ReportDownloadButton } from '../components/ReportDownloadButton';

export const Results: React.FC = () => {
  const { runId } = useParams<{ runId: string }>();
  const [run, setRun] = useState<AnalysisRun | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!runId) return;

    const fetchResults = async () => {
      setIsLoading(true);
      setErrorMsg(null);
      try {
        const data = await analysesApi.getJobStatus(runId);
        setRun(data);
      } catch (err: any) {
        setErrorMsg(err.response?.data?.detail || 'Failed to fetch analysis results.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchResults();
  }, [runId]);

  if (isLoading) {
    return <div style={{ padding: '40px', textAlign: 'center', color: '#64748b' }}>Loading results...</div>;
  }

  if (errorMsg || !run || !run.result) {
    return (
      <div style={{ maxWidth: '600px', margin: '40px auto', padding: '20px', background: '#fef2f2', border: '1px solid #fca5a5', color: '#991b1b', borderRadius: '8px' }}>
        {errorMsg || 'No results available for this run.'}
      </div>
    );
  }

  const { result } = run;
  const warnings = result.warnings || [];
  const metrics = result.metrics || {};
  const fittedParams = result.fitted_params || {};
  const predictedCurves = result.predicted_curves || {};

  return (
    <div style={{ padding: '32px', maxWidth: '1100px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '1.4rem', color: '#1e293b', margin: 0 }}>CANN Analysis Results</h2>
          <p style={{ fontSize: '0.85rem', color: '#64748b', margin: '4px 0 0 0' }}>
            Run ID: <code style={{ fontFamily: 'monospace' }}>{run.id}</code> | Mode: <strong style={{ textTransform: 'capitalize' }}>{run.deformation_mode}</strong>
          </p>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <ReportDownloadButton runId={run.id} format="pdf" />
          <ReportDownloadButton runId={run.id} format="csv" />
        </div>
      </div>

      <WarningsBanner warnings={warnings} />

      <MetricsSummary metrics={metrics} fittedParams={fittedParams} />

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(480px, 1fr))', gap: '20px' }}>
        {Object.entries(predictedCurves).map(([modeName, curveData]) => (
          <StressStrainChart
            key={modeName}
            modeName={modeName}
            predictedCurve={curveData}
          />
        ))}
      </div>
    </div>
  );
};

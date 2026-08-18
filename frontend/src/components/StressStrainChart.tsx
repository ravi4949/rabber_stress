import React from 'react';
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';

interface StressStrainChartProps {
  modeName: string;
  predictedCurve: { stretch: number[]; stress: number[] };
  inputPoints?: { stretch: number; stress: number }[];
}

export const StressStrainChart: React.FC<StressStrainChartProps> = ({
  modeName,
  predictedCurve,
  inputPoints = [],
}) => {
  // Merge curve points for continuous line plotting
  const chartData = predictedCurve.stretch.map((lmb, idx) => ({
    stretch: lmb,
    predictedStress: predictedCurve.stress[idx],
  }));

  return (
    <div style={{ background: '#fff', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
      <h3 style={{ fontSize: '1rem', color: '#1e293b', marginBottom: '16px', textTransform: 'capitalize' }}>
        Stress vs Stretch Response ({modeName})
      </h3>
      <div style={{ width: '100%', height: '320px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis
              dataKey="stretch"
              type="number"
              domain={['auto', 'auto']}
              label={{ value: 'Stretch Ratio (λ)', position: 'bottom', offset: 0 }}
            />
            <YAxis
              label={{ value: 'Nominal Stress (MPa)', angle: -90, position: 'insideLeft' }}
            />
            <Tooltip
              formatter={(val: number) => [val.toFixed(3) + ' MPa', 'Stress']}
              labelFormatter={(label: number) => `Stretch λ: ${Number(label).toFixed(2)}`}
            />
            <Legend verticalAlign="top" height={36} />
            
            {/* Predicted CANN Curve */}
            <Line
              type="monotone"
              dataKey="predictedStress"
              name="CANN Fit Curve"
              stroke="#2563eb"
              strokeWidth={2}
              dot={false}
            />

            {/* Original Input Data Points Overlay */}
            {inputPoints.length > 0 && (
              <Scatter
                data={inputPoints.map(p => ({ stretch: p.stretch, inputStress: p.stress }))}
                name="Input Experimental Data"
                fill="#ef4444"
                shape="circle"
              />
            )}
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

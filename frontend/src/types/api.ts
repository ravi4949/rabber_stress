export type DeformationMode = 'uniaxial' | 'biaxial' | 'simple_shear' | 'pure_shear' | 'volumetric';

export type JobStatus = 'queued' | 'running' | 'done' | 'failed';

export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface ManualPoint {
  stretch: number;
  stress: number;
}

export interface AnalysisResult {
  fitted_params: Record<string, number | string>;
  predicted_curves: Record<string, { stretch: number[]; stress: number[] }>;
  metrics: Record<string, number>;
  warnings: string[];
}

export interface AnalysisRun {
  id: string;
  user_id: number;
  material_sample_id?: number | null;
  status: JobStatus;
  deformation_mode: DeformationMode;
  input_file_path: string;
  config?: Record<string, any> | null;
  result?: AnalysisResult | null;
  error_message?: string | null;
  created_at: string;
  completed_at?: string | null;
}

export interface MaterialSample {
  id: number;
  user_id: number;
  name: string;
  notes?: string | null;
  created_at: string;
}

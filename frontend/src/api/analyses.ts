import { apiClient } from './client';
import { AnalysisRun, DeformationMode, ManualPoint, MaterialSample } from '../types/api';

export const analysesApi = {
  submitCsv: async (file: File, mode: DeformationMode, sampleId?: number): Promise<{ run_id: string; status: string }> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('deformation_mode', mode);
    if (sampleId) {
      formData.append('material_sample_id', sampleId.toString());
    }
    const res = await apiClient.post<{ run_id: string; status: string }>('/analyses', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  submitManual: async (points: ManualPoint[], mode: DeformationMode, sampleId?: number): Promise<{ run_id: string; status: string }> => {
    const formData = new FormData();
    formData.append('manual_data_json', JSON.stringify(points));
    formData.append('deformation_mode', mode);
    if (sampleId) {
      formData.append('material_sample_id', sampleId.toString());
    }
    const res = await apiClient.post<{ run_id: string; status: string }>('/analyses', formData);
    return res.data;
  },

  getJobStatus: async (runId: string): Promise<AnalysisRun> => {
    const res = await apiClient.get<AnalysisRun>(`/jobs/${runId}`);
    return res.data;
  },

  listAnalyses: async (
    skip = 0,
    limit = 50,
    sampleId?: number | 'uncategorized',
    deformationMode?: string
  ): Promise<AnalysisRun[]> => {
    const params: any = { skip, limit };
    if (sampleId === 'uncategorized') {
      params.uncategorized = true;
    } else if (sampleId) {
      params.material_sample_id = sampleId;
    }
    if (deformationMode && deformationMode !== 'all') {
      params.deformation_mode = deformationMode;
    }
    const res = await apiClient.get<AnalysisRun[]>('/analyses', { params });
    return res.data;
  },

  updateRunTag: async (runId: string, sampleId?: number): Promise<AnalysisRun> => {
    const res = await apiClient.patch<AnalysisRun>(`/jobs/${runId}`, {
      material_sample_id: sampleId || null,
    });
    return res.data;
  },

  downloadReportUrl: (runId: string, format: 'pdf' | 'csv' = 'pdf'): string => {
    const baseURL = apiClient.defaults.baseURL || '/api/v1';
    return `${baseURL}/analyses/${runId}/report?format=${format}`;
  },

  listMaterials: async (): Promise<MaterialSample[]> => {
    const res = await apiClient.get<MaterialSample[]>('/materials');
    return res.data;
  },

  createMaterial: async (name: string, notes?: string): Promise<MaterialSample> => {
    const res = await apiClient.post<MaterialSample>('/materials', { name, notes });
    return res.data;
  },
};

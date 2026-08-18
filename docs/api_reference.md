# API Reference

## REST API Endpoints

### Authentication
- `POST /api/v1/auth/register`: Register new user account.
- `POST /api/v1/auth/login`: Authenticate user and receive JWT access token.

### Data Uploads & Processing
- `POST /api/v1/uploads/csv`: Upload raw experimental stress-strain CSV data.
- `POST /api/v1/uploads/manual`: Submit manual experimental data points.

### Analysis Jobs
- `POST /api/v1/jobs/submit`: Queue Celery analysis task for CANN training/fitting.
- `GET /api/v1/jobs/{job_id}/status`: Poll processing job execution state.

### Results & Material Runs
- `GET /api/v1/results/{job_id}`: Retrieve fitted model parameters, stress-strain curves, and evaluation metrics.
- `GET /api/v1/materials`: List user historical material analysis runs.

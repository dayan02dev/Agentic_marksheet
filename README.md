# CBSE Marksheet Marks Fetcher (v1)

A production-ready web application for extracting and computing marks from CBSE Class 12 marksheets using AI-powered OCR.

## Features

- Batch upload of marksheets (images, PDFs, ZIP files)
- AI-powered extraction using OpenAI Vision API
- Automatic computation of Overall % and PCM %
- Review and edit extracted data before export
- Excel export with conditional formatting for special cases
- Real-time progress updates via SSE
- LangGraph-powered agentic workflow

## Project Structure

```
MUJ_Marksheet/
├── backend/          # FastAPI + LangGraph backend
├── frontend/         # Next.js + shadcn/ui frontend
├── README.md         # This file
└── .env.example      # Environment variables template
```

## Prerequisites

- **Backend**: Python 3.11+
- **Frontend**: Node.js 18+
- **OpenAI API Key** for vision extraction
- **Redis** (optional, for job state management)

## Setup Instructions

### 1. Clone and Navigate

```bash
cd /Users/apple/Desktop/work/MUJ_Marksheet
```

### 2. Backend Setup

```bash
# Create virtual environment
cd backend
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example .env

# Edit .env and add your OPENAI_API_KEY
# OPENAI_API_KEY=sk-...
# REDIS_URL=redis://localhost:6379  # Optional
```

### 3. Frontend Setup

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# No additional env setup needed (proxies to backend)
```

### 4. Start Services

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Redis (Optional):**
```bash
redis-server
```

### 5. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Usage

1. **Upload**: Drag and drop marksheets (JPG, PNG, PDF, or ZIP)
2. **Process**: Watch real-time progress as AI extracts data
3. **Review**: Edit any incorrect values in the review table
4. **Export**: Download results as Excel with highlighted issues

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/jobs` | Create new batch job |
| GET | `/api/jobs/{job_id}` | Get job status and records |
| GET | `/api/jobs/{job_id}/events` | SSE stream for progress |
| PATCH | `/api/jobs/{job_id}/records/{record_id}` | Update a record |
| POST | `/api/jobs/{job_id}/records/{record_id}/rerun` | Re-extract with fallback |
| GET | `/api/jobs/{job_id}/export` | Download Excel |

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | OpenAI API key for vision |
| `REDIS_URL` | No | In-memory | Redis connection URL |
| `MAX_UPLOAD_SIZE` | No | 100MB | Max upload size |
| `CONCURRENT_LIMIT` | No | 5 | Concurrent extractions |
| `ALLOWED_ORIGINS` | No | * | CORS allowed origins |

## Running Tests

```bash
cd backend
pytest tests/ -v
```

## Tech Stack

### Backend
- FastAPI - Async web framework
- LangGraph - Workflow orchestration
- OpenAI API - Vision extraction
- PyMuPDF - PDF processing
- Pillow/OpenCV - Image preprocessing
- openpyxl - Excel generation

### Frontend
- Next.js App Router - React framework
- shadcn/ui - UI components
- Tailwind CSS - Styling
- react-dropzone - File uploads
- TypeScript - Type safety

## License

MIT

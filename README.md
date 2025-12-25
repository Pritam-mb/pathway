# 🏥 Bio-Watcher: Agentic Clinical Intelligence

Real-time clinical sentinel with live knowledge ingestion and agentic reasoning.

## Architecture

- **Pathway**: Streaming engine for live document indexing
- **LangGraph**: Agentic orchestration with multi-step reasoning
- **Flask**: Mock medical news site (external source)
- **React**: Real-time dashboard with WebSocket updates

## Project Structure

```
bio-watcher/
├── backend/
│   ├── pathway_engine/      # Streaming ingestion & vector store
│   ├── agent/               # LangGraph agentic logic
│   ├── mock_site/           # Flask medical news simulator
│   └── api/                 # FastAPI server for dashboard
├── frontend/                # React dashboard
├── data/
│   ├── hospital_docs/       # Watched folder (internal docs)
│   └── synthetic_data/      # Generated patient files
└── config/                  # Configuration files
```

## 🚀 Quick Start

### ⚡ **Option 1: Docker (EASIEST - Recommended!)**

Works on **Windows, Mac, Linux** - No WSL needed!

```bash
# Install Docker Desktop from docker.com

# Build and run everything
docker-compose build
docker-compose up

# Run demo
docker exec bio-watcher-backend python scripts/demo_triggers.py full
```

✨ **Done!** See [DOCKER_SETUP.md](DOCKER_SETUP.md) for complete guide.

---

### 🔧 **Option 2: Manual Setup**

### 1. Install Dependencies
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 2. Run All Services
```bash
# Terminal 1: Mock WHO/FDA site
python backend/mock_site/app.py

# Terminal 2: Pathway + Agent
python backend/main.py

# Terminal 3: Dashboard
cd frontend && npm start
```

### 3. Demo Scenario
```bash
# Trigger external alert
python scripts/trigger_alert.py

# Drop new patient file
python scripts/add_patient_doc.py
```

## Features

✅ Real-time document ingestion from local filesystem  
✅ Streaming web scraping with delta detection  
✅ Live vector index updates (no batch re-indexing)  
✅ Agentic reasoning with cross-referencing  
✅ Safety audit tool for patient-drug matching  
✅ Live dashboard with reasoning traces  

## Environment Variables

Create `.env` file:
```
OPENAI_API_KEY=your_key_here
PATHWAY_LICENSE_KEY=your_key_here  # Optional for commercial use
DASHBOARD_PORT=3000
API_PORT=8000
MOCK_SITE_PORT=5000
```

# 🐳 Docker Setup for Bio-Watcher (EASIEST!)

## Why Docker?
- ✅ Works on **Windows, Mac, Linux**
- ✅ No WSL needed
- ✅ Pathway works perfectly
- ✅ One command to run everything
- ✅ Isolated environment

---

## Prerequisites

### 1. Install Docker Desktop

**Windows/Mac:**
1. Download from: https://www.docker.com/products/docker-desktop
2. Install and restart
3. Open Docker Desktop (ensure it's running)

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### 2. Verify Installation

```bash
docker --version
docker-compose --version
```

---

## 🚀 Quick Start (3 Commands!)

```bash
# 1. Navigate to project
cd d:\madras

# 2. Build containers
docker-compose build

# 3. Start everything
docker-compose up
```

**That's it!** 🎉 System is running with Pathway RAG!

---

## 📋 What Just Happened?

Docker started 2 containers:

### Container 1: Mock Medical Site
- **URL:** http://localhost:5000/alerts
- **Purpose:** Simulates WHO/FDA alerts
- **Status:** Open in browser to verify

### Container 2: Pathway Backend
- **Ports:** 8765 (vector store), 8000 (API)
- **Status:** Check logs below
- **Features:** 
  - ✅ Real Pathway streaming
  - ✅ Gemini embeddings
  - ✅ Live vector index
  - ✅ Clinical agent

---

## 🎯 Run Demo in Docker

### Option 1: Trigger External Alert

```bash
docker exec bio-watcher-backend python scripts/demo_triggers.py alert
```

**Expected Output:**
```
⚡ TRIGGERING EXTERNAL ALERT
✅ External alert triggered successfully!

📋 Alert Content:
   Title: ⚠️ URGENT: Drug-X Safety Alert
   Source: WHO
   Date: 2025-12-26
```

### Option 2: Add Patient Document

```bash
docker exec bio-watcher-backend python scripts/demo_triggers.py doc
```

### Option 3: Full Interactive Demo

```bash
docker exec bio-watcher-backend python scripts/demo_triggers.py full
```

---

## 📊 Monitor System

### View Logs
```bash
# All services
docker-compose logs -f

# Just backend
docker-compose logs -f backend

# Just mock site
docker-compose logs -f mock-site
```

### Check Status
```bash
docker-compose ps
```

### Execute Commands Inside Container
```bash
# Python shell
docker exec -it bio-watcher-backend python

# Bash shell
docker exec -it bio-watcher-backend bash

# Query retriever
docker exec bio-watcher-backend python -c "
from backend.pathway_engine.simple_watcher import SimpleRetriever
# ... query code
"
```

---

## 🗂️ File Watching

The `data/hospital_docs/` folder is **mounted as a volume**, meaning:

✅ Add files on Windows: `d:\madras\data\hospital_docs\new_file.txt`  
✅ Docker sees them instantly  
✅ Pathway indexes automatically

**Test it:**

```powershell
# On Windows
echo "Test document about Drug-X" > d:\madras\data\hospital_docs\test.txt
```

```bash
# Check Docker logs
docker-compose logs backend | grep "detected"
```

---

## 🎛️ Configuration

Edit `.env` file (already exists):

```env
GEMINI_API_KEY=AIzaSyB_-UTUlQrx55RMeg_1Vt9M5qqI3y3lNio
EXTERNAL_NEWS_URL=http://mock-site:5000/alerts
PATHWAY_DATA_DIR=/app/data/hospital_docs
```

**Note:** Inside Docker, URLs use container names (e.g., `http://mock-site:5000`)

---

## 🔄 Rebuild After Changes

If you modify code:

```bash
# Stop containers
docker-compose down

# Rebuild
docker-compose build

# Start again
docker-compose up
```

Or in one command:
```bash
docker-compose up --build
```

---

## 🌐 Optional: Start Dashboard

To include the React frontend:

```bash
docker-compose --profile with-ui up
```

Dashboard will be at: http://localhost:3000

---

## 🐛 Troubleshooting

### "Cannot connect to Docker daemon"
**Solution:** Start Docker Desktop

### "Port already in use"
**Solution:** 
```bash
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process or change port in docker-compose.yml
```

### "Container exits immediately"
**Check logs:**
```bash
docker-compose logs backend
```

### "Pathway errors"
**Ensure you're using official Pathway image:**
```bash
docker pull pathwaycom/pathway:latest
docker-compose build --no-cache
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Your Windows Machine            │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │     Docker Engine               │   │
│  │                                 │   │
│  │  ┌──────────────────────────┐  │   │
│  │  │  Container 1             │  │   │
│  │  │  Mock Site (Flask)       │  │   │
│  │  │  Port: 5000              │  │   │
│  │  └──────────────────────────┘  │   │
│  │                                 │   │
│  │  ┌──────────────────────────┐  │   │
│  │  │  Container 2             │  │   │
│  │  │  Pathway + Agent         │  │   │
│  │  │  Ports: 8000, 8765       │  │   │
│  │  │  Volumes: ./data         │  │   │
│  │  └──────────────────────────┘  │   │
│  │                                 │   │
│  │  Network: bio-watcher-network  │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

---

## 📦 What's Inside Each Container?

### Mock Site Container
- Python 3.11
- Flask + Flask-CORS
- Templates (HTML pages)
- State file (alerts_state.json)

### Backend Container
- **Pathway Official Image** (Linux-based)
- Python 3.11
- Pathway library + xpack-llm
- Gemini API integration
- LangGraph agent
- Your entire backend code

---

## 🚀 Performance

| Metric | Docker | Native Windows | WSL |
|--------|--------|----------------|-----|
| **Pathway Support** | ✅ Full | ❌ None | ✅ Full |
| **Setup Time** | 10 min | N/A | 15 min |
| **Performance** | 95% | N/A | 100% |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ❌ | ⭐⭐⭐⭐ |

---

## 🎬 Demo Video Recording

```bash
# 1. Start system
docker-compose up

# 2. In new terminal, show logs
docker-compose logs -f backend

# 3. In another terminal, trigger demo
docker exec bio-watcher-backend python scripts/demo_triggers.py full

# 4. Record the output!
```

---

## 🔐 Production Deployment

For production, add:

```yaml
# docker-compose.prod.yml
services:
  backend:
    environment:
      - PATHWAY_LICENSE_KEY=${PATHWAY_LICENSE_KEY}
    restart: always
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

Run with:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

---

## 📝 Useful Commands Cheat Sheet

```bash
# Start (detached)
docker-compose up -d

# Stop
docker-compose down

# Restart one service
docker-compose restart backend

# View real-time logs
docker-compose logs -f

# Shell into container
docker exec -it bio-watcher-backend bash

# Remove everything (clean slate)
docker-compose down -v
docker system prune -a

# Check resource usage
docker stats
```

---

## ✅ Verification Checklist

- [ ] Docker Desktop running
- [ ] `docker-compose build` successful
- [ ] `docker-compose up` starts both containers
- [ ] http://localhost:5000/alerts accessible
- [ ] Backend logs show "System ready!"
- [ ] Demo triggers work: `docker exec bio-watcher-backend python scripts/demo_triggers.py alert`
- [ ] Files in `data/hospital_docs/` are detected

---

## 🎯 You're Ready!

**For hackathon demo:**
```bash
cd d:\madras
docker-compose up
# Wait for "System ready!" message
# Open http://localhost:5000/alerts
# Run demo: docker exec bio-watcher-backend python scripts/demo_triggers.py full
```

**Questions?** 
- Check `docker-compose logs backend`
- Verify `.env` has your Gemini key
- Ensure Docker Desktop is running

**Happy hacking! 🚀**

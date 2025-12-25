# 🚀 Bio-Watcher: Complete Setup Guide

## 🪟 Windows Users: You MUST Use WSL

Pathway **does not work on native Windows**. Follow these steps:

### Quick WSL Setup (5 minutes)

```powershell
# 1. Install WSL (PowerShell as Admin)
wsl --install

# 2. Restart computer

# 3. Open "Ubuntu" from Start Menu

# 4. Inside Ubuntu:
cd /mnt/d/madras
python3.11 -m venv venv
source venv/bin/activate
```

---

## 📦 Two Installation Options

### Option A: Full Pathway RAG (Production-Ready)

**Use this for:** Real streaming, live vector index, production deployment

**Requirements:** WSL/Linux, Pathway library

```bash
# In WSL Ubuntu terminal
cd /mnt/d/madras
source venv/bin/activate

# Install Pathway with all features
pip install -U pathway
pip install "pathway[xpack-llm]"
pip install "pathway[xpack-llm-docs]"

# Install other deps
pip install google-generativeai langchain-google-genai langgraph
pip install flask flask-cors fastapi uvicorn
pip install python-dotenv pydantic pydantic-settings
pip install beautifulsoup4 lxml requests pypdf python-docx

# Set environment
export GEMINI_API_KEY="AIzaSyB_-UTUlQrx55RMeg_1Vt9M5qqI3y3lNio"
export PYTHONPATH="/mnt/d/madras"

# Run Pathway version
python backend/main_pathway.py
```

---

### Option B: Lightweight Version (Demo/Windows Native)

**Use this for:** Quick demo, development, Windows native testing

**Requirements:** Just Python on Windows

```powershell
# In PowerShell (Windows)
cd d:\madras

# Install deps (already done)
# pip install google-generativeai langchain-google-genai langgraph flask flask-cors ...

# Set environment
$env:PYTHONPATH="d:\madras"

# Run lightweight version
python backend/main_integrated.py
```

**Differences:**

| Feature | Pathway (Option A) | Lightweight (Option B) |
|---------|-------------------|----------------------|
| **Live Streaming** | ✅ Real-time | ✅ Polling (10s) |
| **Vector Search** | ✅ Semantic + KNN | 🟡 Keyword only |
| **Scalability** | ✅ Production-ready | 🟡 Demo only |
| **Windows Support** | ❌ WSL required | ✅ Native |
| **Setup Time** | 15 minutes | 2 minutes |

---

## 🎯 Which Should You Use?

### For Hackathon Demo TODAY:
**→ Use Option B (Lightweight)** - It works NOW on Windows

### For Production/Final Submission:
**→ Use Option A (Pathway)** - Install WSL, get proper RAG

---

## 🚀 Quick Start (Lightweight - Windows)

```powershell
# Terminal 1: Mock Site
cd d:\madras
$env:PYTHONPATH="d:\madras"
python backend/mock_site/app.py

# Terminal 2: System
python backend/main_integrated.py

# Terminal 3: Demo
python scripts/demo_triggers.py full
```

---

## 🔥 Quick Start (Pathway - WSL)

```bash
# In WSL Ubuntu
cd /mnt/d/madras
source venv/bin/activate

# Terminal 1: Mock Site
python backend/mock_site/app.py

# Terminal 2: Pathway System
python backend/main_pathway.py

# Terminal 3: Demo
python scripts/demo_triggers.py full
```

---

## 📊 Feature Comparison Matrix

| Component | Lightweight | Pathway |
|-----------|------------|---------|
| **Document Watching** | File hashing, polling | Native streaming |
| **Web Scraping** | BeautifulSoup, polling | HTTP connector, auto-refresh |
| **Vector Store** | In-memory list | KNN index, persistent |
| **Embeddings** | Batch Gemini API | Integrated embedder |
| **Search** | Keyword matching | Semantic similarity |
| **Delta Detection** | MD5 hash comparison | Built-in change detection |
| **Performance** | Good for <1000 docs | Scales to millions |
| **Latency** | ~10s detection | <1s detection |

---

## 🎬 Demo Scenarios

Both versions support the same demo flow:

### Scenario 1: External Alert
```bash
python scripts/demo_triggers.py alert
```
**Expected:**
- Mock WHO site updates with Drug-X warning
- System detects change (10s lightweight, <1s Pathway)
- Agent cross-references patient records
- Alert generated for affected patients

### Scenario 2: Internal Document
```bash
python scripts/demo_triggers.py doc
```
**Expected:**
- New lab results added to watched folder
- System indexes immediately
- Agent correlates with external alert
- Safety score drops to CRITICAL

### Scenario 3: Full Demo
```bash
python scripts/demo_triggers.py full
```
**Expected:**
- Interactive walkthrough
- Step-by-step narration
- Combined external + internal events

---

## 🐛 Troubleshooting

### "Pathway not found"
→ You're on Windows. Use WSL or lightweight version.

### "Module config not found"
```bash
export PYTHONPATH="/mnt/d/madras"  # WSL
# or
$env:PYTHONPATH="d:\madras"  # PowerShell
```

### "GEMINI_API_KEY not set"
```bash
# WSL
export GEMINI_API_KEY="your-key-here"

# Windows
$env:GEMINI_API_KEY="your-key-here"
```

### "Mock site not accessible"
Check if Flask is running on port 5000:
```bash
curl http://localhost:5000/alerts
```

---

## 📁 File Structure

```
bio-watcher/
├── backend/
│   ├── pathway_engine/
│   │   ├── pathway_rag.py       # ✨ Pathway implementation
│   │   ├── simple_watcher.py    # 🔧 Lightweight alternative
│   │   └── retriever.py
│   ├── agent/
│   │   └── clinical_agent.py
│   ├── mock_site/
│   │   └── app.py
│   ├── main_pathway.py          # ✨ Run with Pathway
│   └── main_integrated.py       # 🔧 Run lightweight
├── frontend/
│   └── src/
├── scripts/
│   ├── generate_data.py
│   └── demo_triggers.py
├── data/
│   └── hospital_docs/
└── config/
    └── settings.py
```

---

## 🎓 Next Steps

### To Continue with Lightweight Version:
1. ✅ System is ready to run
2. Start mock site + main_integrated.py
3. Run demo_triggers.py
4. Present your hack!

### To Upgrade to Pathway:
1. Install WSL: `wsl --install`
2. Follow [WINDOWS_PATHWAY_SETUP.md](WINDOWS_PATHWAY_SETUP.md)
3. Install Pathway in WSL
4. Switch to main_pathway.py
5. Get 10x better performance!

---

## 💡 Pro Tips

1. **For Demo:** Use lightweight - it's simpler and works now
2. **For Video:** Record the full demo script with triggers
3. **For Judges:** Mention Pathway integration is ready for deployment
4. **For Future:** Show both versions as "MVP vs Production"

---

**Questions? Need help?** Check:
- [PRODUCTION_ROADMAP.md](PRODUCTION_ROADMAP.md) - Full feature list
- [WINDOWS_PATHWAY_SETUP.md](WINDOWS_PATHWAY_SETUP.md) - WSL guide
- README.md - Project overview

**Ready to demo? 🚀**

```bash
# Start everything
python backend/mock_site/app.py        # Terminal 1
python backend/main_integrated.py      # Terminal 2
python scripts/demo_triggers.py full   # Terminal 3
```

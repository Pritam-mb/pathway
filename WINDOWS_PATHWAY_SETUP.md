# 🪟 Setting Up Pathway on Windows via WSL

## Step 1: Install WSL

Open PowerShell as Administrator and run:

```powershell
wsl --install
```

This installs Ubuntu by default. Restart your computer when prompted.

## Step 2: Set Up Ubuntu Environment

Launch "Ubuntu" from Start Menu, then:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install system dependencies
sudo apt install build-essential libssl-dev libffi-dev python3-dev -y
```

## Step 3: Access Your Project in WSL

Your Windows drives are mounted at `/mnt/`:

```bash
# Navigate to your project
cd /mnt/d/madras

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install Pathway with LLM support
pip install -U pathway
pip install "pathway[xpack-llm]"
pip install "pathway[xpack-llm-docs]"  # For PDF parsing

# Install other dependencies
pip install google-generativeai langchain-google-genai langgraph
pip install flask flask-cors fastapi uvicorn
pip install python-dotenv pydantic pydantic-settings
pip install beautifulsoup4 lxml requests
```

## Step 4: Set Environment Variables

```bash
# In WSL Ubuntu terminal
export GEMINI_API_KEY="AIzaSyB_-UTUlQrx55RMeg_1Vt9M5qqI3y3lNio"
export PYTHONPATH="/mnt/d/madras"
```

Or create `.bashrc` entry:

```bash
echo 'export GEMINI_API_KEY="AIzaSyB_-UTUlQrx55RMeg_1Vt9M5qqI3y3lNio"' >> ~/.bashrc
echo 'export PYTHONPATH="/mnt/d/madras"' >> ~/.bashrc
source ~/.bashrc
```

## Step 5: Run Pathway System

```bash
cd /mnt/d/madras

# Terminal 1: Mock site
python backend/mock_site/app.py

# Terminal 2: Pathway + Agent
python backend/main_pathway.py

# Terminal 3: Trigger demo
python scripts/demo_triggers.py full
```

## VS Code Integration (Optional)

Install "Remote - WSL" extension in VS Code:

1. Open VS Code
2. Install "Remote - WSL" extension
3. Click green icon in bottom-left corner
4. Select "Connect to WSL"
5. Open folder: `/mnt/d/madras`

Now you can edit files in VS Code but run them in WSL!

---

## Alternative: Docker Setup

If you prefer Docker:

```bash
# In PowerShell (Windows)
docker pull pathwaycom/pathway

# Build custom image
docker build -t bio-watcher .

# Run
docker-compose up
```

---

## Which Option Should You Choose?

| Option | Pros | Cons | Recommended For |
|--------|------|------|-----------------|
| **WSL** | Native Linux, easy access to files | Requires Windows 10+ | Development |
| **Docker** | Isolated, portable | More complex setup | Production |
| **Cloud VM** | Full Linux environment | Costs money | Production deployment |

**For this hackathon: Use WSL** - It's the fastest way to get Pathway working on Windows.

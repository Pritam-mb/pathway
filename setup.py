"""
Quick Start Script - Sets up and runs Bio-Watcher
"""
import subprocess
import sys
import time
from pathlib import Path


def check_python_version():
    """Ensure Python 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")


def check_env_file():
    """Check if .env exists, copy from example if not"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("📝 Creating .env from .env.example...")
            env_file.write_text(env_example.read_text())
            print("⚠️  Please edit .env and add your OPENAI_API_KEY")
            return False
        else:
            print("❌ .env.example not found")
            return False
    
    # Check if API key is set
    env_content = env_file.read_text()
    if "your_openai_key_here" in env_content:
        print("⚠️  Please set your OPENAI_API_KEY in .env file")
        return False
    
    print("✅ Environment configured")
    return True


def install_python_deps():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Python packages installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python packages: {e}")
        return False


def install_node_deps():
    """Install Node dependencies for frontend"""
    print("\n📦 Installing Node.js dependencies...")
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("⚠️  Frontend directory not found, skipping")
        return False
    
    try:
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True, capture_output=True)
        print("✅ Node packages installed")
        return True
    except FileNotFoundError:
        print("⚠️  Node.js not found. Install from https://nodejs.org/")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Node packages: {e}")
        return False


def generate_synthetic_data():
    """Generate sample medical documents"""
    print("\n🏥 Generating synthetic medical data...")
    try:
        subprocess.run([sys.executable, "scripts/generate_data.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to generate data")
        return False


def print_instructions():
    """Print startup instructions"""
    print("\n" + "="*70)
    print("🚀 BIO-WATCHER SETUP COMPLETE")
    print("="*70)
    print("\nTo run the system, open 3 separate terminal windows:\n")
    
    print("Terminal 1 - Mock Medical News Site:")
    print("  $ python backend/mock_site/app.py")
    print("  → Runs on http://localhost:5000\n")
    
    print("Terminal 2 - Pathway Engine + Agent:")
    print("  $ python backend/main.py")
    print("  → Starts streaming ingestion and agent\n")
    
    print("Terminal 3 - Dashboard (optional):")
    print("  $ cd frontend")
    print("  $ npm run dev")
    print("  → Runs on http://localhost:3000\n")
    
    print("="*70)
    print("📚 DEMO COMMANDS")
    print("="*70)
    print("\nTrigger events to see the agent in action:\n")
    
    print("# Trigger external WHO alert")
    print("$ python scripts/demo_triggers.py alert\n")
    
    print("# Add urgent patient document")
    print("$ python scripts/demo_triggers.py doc\n")
    
    print("# Run full demo sequence")
    print("$ python scripts/demo_triggers.py full\n")
    
    print("# Reset to baseline")
    print("$ python scripts/demo_triggers.py reset\n")
    
    print("="*70)
    print("✨ Ready to demonstrate real-time clinical intelligence!")
    print("="*70)


def main():
    """Main setup flow"""
    print("\n🏥 BIO-WATCHER QUICK START\n")
    
    # Check Python version
    check_python_version()
    
    # Check environment
    env_ok = check_env_file()
    if not env_ok:
        print("\n⚠️  Setup incomplete. Please configure .env and run again.")
        return
    
    # Install dependencies
    python_ok = install_python_deps()
    if not python_ok:
        print("\n❌ Setup failed. Please fix errors and try again.")
        return
    
    node_ok = install_node_deps()
    
    # Generate data
    data_ok = generate_synthetic_data()
    
    # Print instructions
    print_instructions()
    
    if not node_ok:
        print("\n⚠️  Note: Dashboard requires Node.js. Backend will work without it.")


if __name__ == "__main__":
    main()

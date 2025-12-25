"""
Main orchestrator - Runs Pathway engine + Agent together
"""
import asyncio
import threading
import time
from pathlib import Path


def run_pathway_engine():
    """Run Pathway streaming engine in background thread"""
    print("🚀 Starting Pathway Engine...")
    from backend.pathway_engine.engine import main as pathway_main
    pathway_main()


def run_agent_monitor():
    """Monitor Pathway for changes and trigger agent"""
    print("🤖 Starting Agent Monitor...")
    from backend.agent.clinical_agent import BioWatcherAgent
    from backend.pathway_engine.retriever import PathwayRetriever
    
    agent = BioWatcherAgent()
    retriever = PathwayRetriever()
    
    print("✅ Agent ready and monitoring for events...")
    
    # In production, this would listen to Pathway's change events
    # For demo, we'll poll for recent changes
    last_check = time.time()
    
    while True:
        time.sleep(10)  # Check every 10 seconds
        
        # Check for recent changes
        # This is simplified - Pathway has better event mechanisms
        try:
            recent = retriever.get_recent_changes(minutes=1)
            
            if recent:
                print(f"\n⚡ Detected {len(recent)} new/updated documents!")
                
                # Trigger agent analysis
                event_data = {
                    "timestamp": time.time(),
                    "num_changes": len(recent),
                    "sources": [doc.get("metadata", {}).get("source_type") for doc in recent]
                }
                
                agent.process_event("data_update", event_data)
        except Exception as e:
            # Pathway might not be ready yet
            pass


def main():
    """Main entry point"""
    from config.settings import settings
    
    print("\n" + "="*70)
    print("🏥 BIO-WATCHER: AGENTIC CLINICAL INTELLIGENCE")
    print("="*70)
    print(f"\n📁 Monitoring Directory: {settings.pathway_data_dir}")
    print(f"🌐 External Source: {settings.external_news_url}")
    print(f"🤖 LLM Model: {settings.llm_model}")
    print("\n" + "="*70)
    
    # Check if Gemini key is set
    if not settings.gemini_api_key or settings.gemini_api_key == "your_gemini_key_here":
        print("\n⚠️  WARNING: Gemini API key not configured!")
        print("    Please set GEMINI_API_KEY in your .env file")
        print("    Copy .env.example to .env and add your key")
        return
    
    # Check if data directory has files
    data_files = list(Path(settings.pathway_data_dir).glob("*.txt"))
    if not data_files:
        print("\n📝 No documents found. Generating synthetic data...")
        from scripts.generate_data import main as generate_data
        generate_data()
    else:
        print(f"\n✅ Found {len(data_files)} documents to monitor")
    
    print("\n🚀 Starting services...")
    print("\nMake sure these are running in separate terminals:")
    print("  1. Mock Site: python backend/mock_site/app.py")
    print("  2. This script: python backend/main.py")
    print("\n" + "="*70)
    
    try:
        # Start Pathway in a separate thread
        pathway_thread = threading.Thread(target=run_pathway_engine, daemon=True)
        pathway_thread.start()
        
        # Wait for Pathway to initialize
        print("\n⏳ Waiting for Pathway to initialize (10 seconds)...")
        time.sleep(10)
        
        # Start agent monitor in main thread
        run_agent_monitor()
        
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down Bio-Watcher...")
        print("Goodbye!")


if __name__ == "__main__":
    main()

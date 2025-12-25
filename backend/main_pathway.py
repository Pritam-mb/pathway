"""
Main runner for Pathway-based Bio-Watcher
Requires: WSL/Linux environment
"""
import pathway as pw
from backend.pathway_engine.pathway_rag import PathwayRAGSystem
from backend.agent.clinical_agent import BioWatcherAgent
import logging
import time
from threading import Thread

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_pathway_engine(rag_system):
    """Run Pathway in background thread"""
    logger.info("🚀 Starting Pathway computation engine...")
    rag_system.run_server()


def monitor_changes(rag_system, agent):
    """Monitor for document changes and trigger agent"""
    logger.info("🤖 Agent monitoring active...")
    
    # In production, Pathway would emit events
    # We'd subscribe to them here
    while True:
        time.sleep(10)
        # Check for new documents and trigger analysis
        # This is simplified - real version uses Pathway callbacks


def main():
    from config.settings import settings
    
    logger.info("\n" + "="*70)
    logger.info("🏥 BIO-WATCHER: PATHWAY RAG EDITION")
    logger.info("="*70)
    logger.info(f"\n📁 Monitoring: {settings.pathway_data_dir}")
    logger.info(f"🌐 External: {settings.external_news_url}")
    logger.info(f"🤖 Model: {settings.llm_model}")
    logger.info("\n" + "="*70)
    
    # Check environment
    if not settings.gemini_api_key:
        logger.error("❌ GEMINI_API_KEY not set!")
        return
    
    # Create systems
    logger.info("\n🔧 Initializing systems...")
    
    rag_system = PathwayRAGSystem(
        data_dir=str(settings.pathway_data_dir),
        external_urls=[settings.external_news_url],
        gemini_api_key=settings.gemini_api_key,
    )
    
    agent = BioWatcherAgent()
    
    # Start Pathway engine in background
    pathway_thread = Thread(target=run_pathway_engine, args=(rag_system,), daemon=True)
    pathway_thread.start()
    
    # Start monitoring
    logger.info("✅ System live!")
    logger.info("\n📋 Ready for demo:")
    logger.info("  python scripts/demo_triggers.py alert")
    logger.info("  python scripts/demo_triggers.py doc")
    logger.info("\nPress Ctrl+C to stop\n")
    
    try:
        monitor_changes(rag_system, agent)
    except KeyboardInterrupt:
        logger.info("\n\n🛑 Shutting down...")
        logger.info("👋 Goodbye!")


if __name__ == "__main__":
    main()

"""
Docker-optimized main runner for Pathway
"""
import os
import sys
from pathlib import Path

# Ensure imports work in Docker
sys.path.insert(0, '/app')

from backend.pathway_engine.pathway_rag import PathwayRAGSystem
from backend.agent.clinical_agent import BioWatcherAgent
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    # Get config from environment
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    external_url = os.getenv('EXTERNAL_NEWS_URL', 'http://mock-site:5000/alerts')
    data_dir = os.getenv('PATHWAY_DATA_DIR', '/app/data/hospital_docs')
    
    logger.info("\n" + "="*70)
    logger.info("🏥 BIO-WATCHER: PATHWAY RAG (DOCKER)")
    logger.info("="*70)
    logger.info(f"\n📁 Data Directory: {data_dir}")
    logger.info(f"🌐 External Source: {external_url}")
    logger.info(f"🐳 Running in Docker container")
    logger.info("\n" + "="*70)
    
    if not gemini_api_key:
        logger.error("❌ GEMINI_API_KEY environment variable not set!")
        logger.error("   Set it in .env file or docker-compose.yml")
        sys.exit(1)
    
    # Ensure data directory exists
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    
    # Create RAG system
    logger.info("\n🔧 Initializing Pathway RAG system...")
    rag_system = PathwayRAGSystem(
        data_dir=data_dir,
        external_urls=[external_url],
        gemini_api_key=gemini_api_key,
    )
    
    # Create agent
    logger.info("🤖 Initializing Clinical Agent...")
    agent = BioWatcherAgent()
    
    logger.info("\n✅ System ready!")
    logger.info("📊 Monitoring for changes...")
    logger.info("\n🎯 To trigger demo:")
    logger.info("   docker exec bio-watcher-backend python scripts/demo_triggers.py alert")
    logger.info("\nPress Ctrl+C to stop\n")
    
    # Run Pathway
    try:
        rag_system.run_server()
    except KeyboardInterrupt:
        logger.info("\n\n🛑 Shutting down...")
        logger.info("👋 Goodbye!")


if __name__ == "__main__":
    main()

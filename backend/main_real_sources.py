"""
Demo launcher with real WHO/FDA scraping support
Choose your data sources for the demo
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import os
import time
from backend.pathway_engine.multi_source_watcher import MultiSourceWatcher
from backend.agent.clinical_agent import create_clinical_agent
from config.settings import settings
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def parse_sources_from_env():
    """Parse EXTERNAL_NEWS_SOURCES from environment"""
    sources_str = os.getenv('EXTERNAL_NEWS_SOURCES', 'MOCK:http://localhost:5000/alerts')
    
    # Split by comma and strip whitespace
    sources = [s.strip() for s in sources_str.split(',')]
    
    return sources


def main():
    """Run Bio-Watcher with multi-source support"""
    
    print("\n" + "="*70)
    print("🏥 BIO-WATCHER: Agentic Clinical Intelligence")
    print("="*70)
    
    # Parse sources
    sources = parse_sources_from_env()
    
    print(f"\n📡 Monitoring Sources:")
    for source in sources:
        if source == 'WHO':
            print("   🌍 WHO Disease Outbreak News (LIVE)")
        elif source == 'FDA':
            print("   💊 FDA Drug Safety Communications (LIVE)")
        elif source == 'CDC':
            print("   🏥 CDC Health Alert Network (LIVE)")
        elif source.startswith('MOCK:'):
            print(f"   🎭 Mock Site (Controllable Demo)")
        else:
            print(f"   📰 {source}")
    
    print(f"\n📂 Local Documents: {settings.pathway_data_dir}")
    print(f"🔄 Poll Interval: 10 seconds")
    print("="*70 + "\n")
    
    # Create watcher
    watcher = MultiSourceWatcher(
        watch_dir=str(settings.pathway_data_dir),
        sources=sources,
        poll_interval=10
    )
    
    # Create agent
    agent = create_clinical_agent(watcher.retrieve)
    
    # Set up callbacks
    def on_web_changed(alerts, content):
        logger.info(f"🌐 Web update: {len(alerts)} new alerts detected")
        
        # Show first alert
        if alerts:
            first = alerts[0]
            logger.info(f"   Source: {first.get('source')}")
            logger.info(f"   Title: {first.get('title')}")
        
        # Trigger agent analysis
        try:
            logger.info("🤖 Activating agent for analysis...")
            response = agent.invoke({
                "messages": [("user", f"Analyze these new medical alerts: {content[:500]}")]
            })
            
            # Extract safety score and alerts
            if 'safety_score' in response:
                logger.info(f"   Safety Score: {response['safety_score']}/100")
            if 'alerts' in response and response['alerts']:
                logger.info(f"   Generated {len(response['alerts'])} clinical alerts")
        except Exception as e:
            logger.error(f"Agent analysis failed: {e}")
    
    def on_file_added(path, content):
        logger.info(f"📄 New file: {Path(path).name}")
    
    watcher.on_web_changed = on_web_changed
    watcher.on_file_added = on_file_added
    
    # Start monitoring
    logger.info("✅ System ready! Monitoring sources...\n")
    
    try:
        watcher.start()
    except KeyboardInterrupt:
        logger.info("\n\n👋 Shutting down gracefully...")
        print("\n" + "="*70)
        stats = watcher.get_stats()
        print(f"📊 Final Statistics:")
        print(f"   Files tracked: {stats['files_tracked']}")
        print(f"   Documents indexed: {stats['documents_indexed']}")
        print(f"   Sources monitored: {stats['sources_monitored']}")
        print("="*70 + "\n")


if __name__ == "__main__":
    # Show configuration help
    print("\n💡 TIP: Configure data sources in .env file:")
    print("   EXTERNAL_NEWS_SOURCES=MOCK:http://localhost:5000/alerts  (demo only)")
    print("   EXTERNAL_NEWS_SOURCES=WHO,FDA,MOCK:...                   (hybrid)")
    print("   EXTERNAL_NEWS_SOURCES=WHO,FDA,CDC                        (production)")
    print("\n   Test real scrapers first: python scripts/test_real_scrapers.py\n")
    
    time.sleep(2)
    main()

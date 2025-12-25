"""
Integrated Bio-Watcher System
Combines document monitoring with agentic reasoning
"""
import asyncio
import time
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BioWatcherSystem:
    """Main system orchestrator"""
    
    def __init__(self):
        from config.settings import settings
        from backend.pathway_engine.simple_watcher import DocumentWatcher, SimpleRetriever
        from backend.agent.clinical_agent import BioWatcherAgent
        
        self.settings = settings
        
        # Initialize document watcher
        logger.info("🔧 Initializing Document Watcher...")
        self.watcher = DocumentWatcher(
            data_dir=str(settings.pathway_data_dir),
            external_urls=[settings.external_news_url],
            gemini_api_key=settings.gemini_api_key,
            poll_interval=10
        )
        
        # Initialize retriever
        self.retriever = SimpleRetriever(self.watcher)
        
        # Initialize agent
        logger.info("🤖 Initializing Clinical Agent...")
        self.agent = BioWatcherAgent()
        
        # Wire up event handlers
        self.watcher.on_file_added = self.handle_file_added
        self.watcher.on_file_modified = self.handle_file_modified
        self.watcher.on_web_changed = self.handle_web_changed
        
        # State
        self.alerts = []
        self.safety_score = 95
        
    def handle_file_added(self, doc: dict):
        """Handle new file event"""
        logger.info(f"\n{'='*60}")
        logger.info(f"📄 NEW INTERNAL DOCUMENT")
        logger.info(f"{'='*60}")
        logger.info(f"File: {doc['name']}")
        logger.info(f"Time: {doc['timestamp']}")
        
        # Trigger agent analysis
        event_data = {
            'type': 'file_added',
            'filename': doc['name'],
            'content_preview': doc['content'][:500],
            'source': 'internal',
            'timestamp': doc['timestamp']
        }
        
        self.trigger_agent_analysis(event_data)
    
    def handle_file_modified(self, doc: dict):
        """Handle file modification event"""
        logger.info(f"\n{'='*60}")
        logger.info(f"📝 DOCUMENT MODIFIED")
        logger.info(f"{'='*60}")
        logger.info(f"File: {doc['name']}")
        
        event_data = {
            'type': 'file_modified',
            'filename': doc['name'],
            'content_preview': doc['content'][:500],
            'source': 'internal',
            'timestamp': doc['timestamp']
        }
        
        self.trigger_agent_analysis(event_data)
    
    def handle_web_changed(self, doc: dict):
        """Handle external web change event"""
        logger.info(f"\n{'='*60}")
        logger.info(f"🌐 EXTERNAL WEB UPDATE DETECTED")
        logger.info(f"{'='*60}")
        logger.info(f"URL: {doc['url']}")
        logger.info(f"Time: {doc['timestamp']}")
        logger.info(f"\nContent Preview:")
        logger.info(doc['content'][:300] + "...")
        
        # Trigger agent analysis
        event_data = {
            'type': 'web_changed',
            'url': doc['url'],
            'content_preview': doc['content'][:500],
            'source': 'external',
            'timestamp': doc['timestamp']
        }
        
        self.trigger_agent_analysis(event_data)
    
    def trigger_agent_analysis(self, event_data: dict):
        """Trigger agent to analyze the event"""
        try:
            logger.info("\n🤖 Triggering Agent Analysis...")
            
            # For now, do simple analysis without full agent
            # In production, this would call: self.agent.process_event(event_type, event_data)
            
            # Check if this is a Drug-X related event
            content = event_data.get('content_preview', '').lower()
            
            if 'drug-x' in content or 'cardioxin' in content:
                logger.info("⚠️ Drug-X mention detected!")
                
                # Search for patients with Drug-X
                logger.info("🔍 Cross-referencing patient records...")
                results = self.retriever.retrieve_by_source("Drug-X prescribed medication", "internal", top_k=10)
                
                affected_patients = []
                for doc in results:
                    if 'drug-x' in doc['text'].lower() or 'cardioxin' in doc['text'].lower():
                        # Extract patient ID
                        text = doc['text']
                        if 'Patient_' in text:
                            start = text.find('Patient_')
                            patient_id = text[start:start+11]
                            if patient_id not in affected_patients:
                                affected_patients.append(patient_id)
                
                if affected_patients:
                    logger.info(f"\n🚨 CRITICAL FINDING:")
                    logger.info(f"Found {len(affected_patients)} patient(s) on Drug-X:")
                    for patient in affected_patients:
                        logger.info(f"  • {patient}")
                    
                    # Calculate risk
                    if event_data['source'] == 'external':
                        self.safety_score = 65  # WARNING level
                        severity = "critical"
                    else:
                        self.safety_score = 75
                        severity = "warning"
                    
                    # Generate alert
                    alert = {
                        'timestamp': datetime.now().isoformat(),
                        'severity': severity,
                        'title': 'Drug-X Safety Risk Detected',
                        'description': f"{len(affected_patients)} patient(s) prescribed Drug-X require immediate review based on new {event_data['source']} data",
                        'patients': affected_patients,
                        'safety_score': self.safety_score
                    }
                    
                    self.alerts.append(alert)
                    
                    logger.info(f"\n📊 Safety Score Updated: {self.safety_score}/100")
                    logger.info(f"🔔 Alert Generated: {alert['title']}")
                else:
                    logger.info("✅ No patients found on Drug-X")
            else:
                logger.info("✅ No critical keywords detected - routine update")
                
        except Exception as e:
            logger.error(f"❌ Agent analysis error: {e}")
    
    def start(self):
        """Start the Bio-Watcher system"""
        logger.info("\n" + "="*70)
        logger.info("🏥 BIO-WATCHER: AGENTIC CLINICAL INTELLIGENCE")
        logger.info("="*70)
        logger.info(f"\n📁 Monitoring Directory: {self.settings.pathway_data_dir}")
        logger.info(f"🌐 External Source: {self.settings.external_news_url}")
        logger.info(f"🤖 LLM Model: {self.settings.llm_model}")
        logger.info(f"⚡ Poll Interval: 10 seconds")
        logger.info("\n" + "="*70)
        
        # Check API key
        if not self.settings.gemini_api_key or self.settings.gemini_api_key == "your_gemini_key_here":
            logger.error("\n⚠️  WARNING: Gemini API key not configured!")
            logger.error("    Please set GEMINI_API_KEY in your .env file")
            return
        
        # Start document watcher
        logger.info("\n🚀 Starting monitoring systems...")
        self.watcher.start_monitoring()
        
        logger.info("✅ System is live and monitoring!")
        logger.info("\n📋 Commands:")
        logger.info("  • Open new terminal and run: python scripts/demo_triggers.py alert")
        logger.info("  • Add patient file: python scripts/demo_triggers.py doc")
        logger.info("  • Press Ctrl+C to stop\n")
        
        # Keep running
        try:
            while True:
                time.sleep(5)
                stats = self.watcher.get_stats()
                print(f"\r📊 Live Stats: {stats['total_documents']} docs | "
                      f"Safety Score: {self.safety_score}/100 | "
                      f"Alerts: {len(self.alerts)}", end='', flush=True)
                
        except KeyboardInterrupt:
            logger.info("\n\n🛑 Shutting down Bio-Watcher...")
            self.watcher.stop_monitoring()
            logger.info("👋 Goodbye!")


def main():
    """Main entry point"""
    system = BioWatcherSystem()
    system.start()


if __name__ == "__main__":
    main()

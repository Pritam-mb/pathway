"""
Enhanced document watcher with multi-source support
Works with both mock and real medical sites
"""
import os
import hashlib
import time
from typing import Dict, List, Set, Optional, Callable
from pathlib import Path
import logging
from backend.pathway_engine.real_scrapers import scrape_all_sources, format_alerts_as_text

logger = logging.getLogger(__name__)


class MultiSourceWatcher:
    """
    Enhanced document watcher supporting:
    - Local file monitoring
    - Mock site scraping
    - Real WHO/FDA/CDC scraping
    """
    
    def __init__(
        self,
        watch_dir: str,
        sources: List[str],
        poll_interval: int = 10
    ):
        self.watch_dir = Path(watch_dir)
        self.sources = sources
        self.poll_interval = poll_interval
        
        # File tracking
        self.file_hashes: Dict[str, str] = {}
        self.documents: Dict[str, str] = {}
        
        # Web tracking
        self.last_web_content: str = ""
        
        # Callbacks
        self.on_file_added: Optional[Callable] = None
        self.on_file_modified: Optional[Callable] = None
        self.on_web_changed: Optional[Callable] = None
        
        logger.info(f"MultiSourceWatcher initialized")
        logger.info(f"  Watch dir: {self.watch_dir}")
        logger.info(f"  Sources: {self.sources}")
    
    def compute_hash(self, content: str) -> str:
        """Compute MD5 hash of content"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def scan_files(self):
        """Scan directory for file changes"""
        current_files: Set[str] = set()
        
        if not self.watch_dir.exists():
            logger.warning(f"Watch directory does not exist: {self.watch_dir}")
            return
        
        for file_path in self.watch_dir.rglob("*.txt"):
            file_str = str(file_path)
            current_files.add(file_str)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                content_hash = self.compute_hash(content)
                
                # Check if file is new
                if file_str not in self.file_hashes:
                    logger.info(f"New file detected: {file_path.name}")
                    self.file_hashes[file_str] = content_hash
                    self.documents[file_str] = content
                    if self.on_file_added:
                        self.on_file_added(file_str, content)
                
                # Check if file was modified
                elif self.file_hashes[file_str] != content_hash:
                    logger.info(f"File modified: {file_path.name}")
                    self.file_hashes[file_str] = content_hash
                    self.documents[file_str] = content
                    if self.on_file_modified:
                        self.on_file_modified(file_str, content)
            
            except Exception as e:
                logger.error(f"Error reading file {file_path}: {e}")
        
        # Check for deleted files
        deleted_files = set(self.file_hashes.keys()) - current_files
        for file_str in deleted_files:
            logger.info(f"File deleted: {file_str}")
            del self.file_hashes[file_str]
            if file_str in self.documents:
                del self.documents[file_str]
    
    def scrape_sources(self):
        """Scrape all configured sources"""
        try:
            alerts = scrape_all_sources(self.sources)
            
            if not alerts:
                logger.debug("No alerts found from sources")
                return
            
            # Format as text
            content = format_alerts_as_text(alerts)
            content_hash = self.compute_hash(content)
            
            # Check if content changed
            if content_hash != self.last_web_content:
                logger.info(f"Web content changed! Found {len(alerts)} alerts")
                self.last_web_content = content_hash
                
                # Store in documents with special key
                doc_key = "web_alerts"
                self.documents[doc_key] = content
                
                if self.on_web_changed:
                    self.on_web_changed(alerts, content)
        
        except Exception as e:
            logger.error(f"Error scraping sources: {e}")
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Simple keyword-based retrieval
        In production, this would use semantic search
        """
        results = []
        query_lower = query.lower()
        
        for doc_path, content in self.documents.items():
            content_lower = content.lower()
            
            # Simple keyword matching
            score = 0
            for word in query_lower.split():
                if len(word) > 3:  # Skip short words
                    score += content_lower.count(word)
            
            if score > 0:
                results.append({
                    'source': doc_path,
                    'content': content[:500],  # First 500 chars
                    'score': score
                })
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def start(self):
        """Start watching files and sources"""
        logger.info("Starting multi-source watcher...")
        
        # Initial scan
        self.scan_files()
        self.scrape_sources()
        
        logger.info(f"Initial scan complete:")
        logger.info(f"  - {len(self.file_hashes)} files indexed")
        logger.info(f"  - {len(self.sources)} sources monitored")
        
        # Polling loop
        try:
            while True:
                time.sleep(self.poll_interval)
                self.scan_files()
                self.scrape_sources()
        except KeyboardInterrupt:
            logger.info("Watcher stopped by user")
    
    def get_stats(self) -> Dict:
        """Get current statistics"""
        return {
            'files_tracked': len(self.file_hashes),
            'documents_indexed': len(self.documents),
            'sources_monitored': len(self.sources),
            'has_web_content': bool(self.last_web_content)
        }


if __name__ == "__main__":
    # Test the watcher
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Configure sources - mix of mock and real
    sources = [
        "MOCK:http://localhost:5000/alerts",  # Demo site
        # Uncomment to test real sources:
        # "WHO",
        # "FDA",
    ]
    
    watcher = MultiSourceWatcher(
        watch_dir="data/hospital_docs",
        sources=sources,
        poll_interval=10
    )
    
    # Set up callbacks
    def on_file_added(path, content):
        print(f"\n🆕 NEW FILE: {path}")
    
    def on_web_changed(alerts, content):
        print(f"\n🌐 WEB UPDATE: {len(alerts)} new alerts")
        for alert in alerts[:2]:  # Show first 2
            print(f"  - {alert.get('source')}: {alert.get('title')}")
    
    watcher.on_file_added = on_file_added
    watcher.on_web_changed = on_web_changed
    
    print(f"\n{'='*60}")
    print("🏥 Bio-Watcher Multi-Source Monitor")
    print(f"{'='*60}")
    print(f"Watching: {watcher.watch_dir}")
    print(f"Sources: {', '.join(sources)}")
    print(f"Poll interval: {watcher.poll_interval}s")
    print(f"{'='*60}\n")
    
    watcher.start()

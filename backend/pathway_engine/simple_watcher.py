"""
Lightweight Document Watcher - Alternative to Pathway
Monitors filesystem and web sources for changes.
"""
import os
import time
import hashlib
import requests
from pathlib import Path
from typing import List, Dict, Callable, Optional
from datetime import datetime
from threading import Thread, Lock
import google.generativeai as genai
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentWatcher:
    """
    Lightweight file system and web watcher.
    Detects changes and triggers callbacks.
    """
    
    def __init__(self, 
                 data_dir: str,
                 external_urls: List[str],
                 gemini_api_key: str,
                 poll_interval: int = 10):
        
        self.data_dir = Path(data_dir)
        self.external_urls = external_urls
        self.gemini_api_key = gemini_api_key
        self.poll_interval = poll_interval
        
        # State tracking
        self.file_hashes: Dict[str, str] = {}
        self.url_hashes: Dict[str, str] = {}
        self.lock = Lock()
        self.running = False
        
        # Initialize Gemini
        genai.configure(api_key=gemini_api_key)
        
        # Document store
        self.documents: List[Dict] = []
        
        # Callbacks for change events
        self.on_file_added: Optional[Callable] = None
        self.on_file_modified: Optional[Callable] = None
        self.on_web_changed: Optional[Callable] = None
        
        logger.info(f"✅ DocumentWatcher initialized")
        logger.info(f"📁 Watching: {data_dir}")
        logger.info(f"🌐 Monitoring: {external_urls}")
    
    def _calculate_hash(self, content: str) -> str:
        """Calculate MD5 hash of content"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def _read_file(self, filepath: Path) -> str:
        """Read and extract text from file"""
        try:
            # Simple text extraction
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading {filepath}: {e}")
            return ""
    
    def _scrape_url(self, url: str) -> str:
        """Scrape text content from URL"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator=' ', strip=True)
            return text
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return ""
    
    def _embed_text(self, text: str) -> List[float]:
        """Generate embedding using Gemini"""
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            # Return dummy embedding
            return [0.0] * 768
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            if chunk.strip():
                chunks.append(chunk)
        return chunks
    
    def scan_filesystem(self) -> Dict[str, any]:
        """Scan directory for changes"""
        changes = {
            'added': [],
            'modified': [],
            'deleted': []
        }
        
        current_files = {}
        
        # Scan all text files
        for ext in ['*.txt', '*.pdf', '*.docx']:
            for filepath in self.data_dir.glob(ext):
                if filepath.is_file():
                    content = self._read_file(filepath)
                    content_hash = self._calculate_hash(content)
                    current_files[str(filepath)] = content_hash
                    
                    # Check for changes
                    if str(filepath) not in self.file_hashes:
                        # New file
                        changes['added'].append({
                            'path': str(filepath),
                            'name': filepath.name,
                            'content': content,
                            'hash': content_hash,
                            'timestamp': datetime.now().isoformat()
                        })
                        logger.info(f"📄 New file detected: {filepath.name}")
                    elif self.file_hashes[str(filepath)] != content_hash:
                        # Modified file
                        changes['modified'].append({
                            'path': str(filepath),
                            'name': filepath.name,
                            'content': content,
                            'hash': content_hash,
                            'timestamp': datetime.now().isoformat()
                        })
                        logger.info(f"📝 File modified: {filepath.name}")
        
        # Check for deleted files
        for old_path in self.file_hashes:
            if old_path not in current_files:
                changes['deleted'].append(old_path)
                logger.info(f"🗑️ File deleted: {Path(old_path).name}")
        
        # Update hash registry
        self.file_hashes = current_files
        
        return changes
    
    def scan_web_sources(self) -> Dict[str, any]:
        """Scan external URLs for changes"""
        changes = {
            'updated': []
        }
        
        for url in self.external_urls:
            content = self._scrape_url(url)
            if not content:
                continue
            
            content_hash = self._calculate_hash(content)
            
            # Check for changes
            if url not in self.url_hashes:
                # First scan
                self.url_hashes[url] = content_hash
                logger.info(f"🌐 Monitoring URL: {url}")
            elif self.url_hashes[url] != content_hash:
                # Content changed!
                changes['updated'].append({
                    'url': url,
                    'content': content,
                    'hash': content_hash,
                    'timestamp': datetime.now().isoformat()
                })
                logger.info(f"⚡ Web content changed: {url}")
                self.url_hashes[url] = content_hash
        
        return changes
    
    def index_document(self, doc: Dict):
        """Add document to index"""
        with self.lock:
            # Chunk text
            chunks = self._chunk_text(doc['content'])
            
            for i, chunk in enumerate(chunks):
                indexed_doc = {
                    'id': f"{doc.get('name', doc.get('url', 'unknown'))}_{i}",
                    'text': chunk,
                    'source': doc.get('path', doc.get('url')),
                    'source_type': 'internal' if 'path' in doc else 'external',
                    'timestamp': doc['timestamp'],
                    'chunk_index': i
                }
                
                # Add to documents list
                self.documents.append(indexed_doc)
            
            logger.info(f"✅ Indexed document with {len(chunks)} chunks")
    
    def retrieve(self, query: str, top_k: int = 5, source_type: Optional[str] = None) -> List[Dict]:
        """
        Simple retrieval using keyword matching.
        In production, use proper semantic search with embeddings.
        """
        query_lower = query.lower()
        
        # Filter by source type if specified
        docs = self.documents
        if source_type:
            docs = [d for d in docs if d['source_type'] == source_type]
        
        # Score documents by keyword overlap
        scored_docs = []
        for doc in docs:
            text_lower = doc['text'].lower()
            
            # Simple scoring: count query words in text
            query_words = query_lower.split()
            score = sum(1 for word in query_words if word in text_lower)
            
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by score and return top-k
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        return [doc for _, doc in scored_docs[:top_k]]
    
    def start_monitoring(self):
        """Start background monitoring threads"""
        self.running = True
        
        # Initial scan
        logger.info("🔍 Performing initial scan...")
        fs_changes = self.scan_filesystem()
        for doc in fs_changes['added']:
            self.index_document(doc)
        
        # Start monitoring threads
        fs_thread = Thread(target=self._monitor_filesystem, daemon=True)
        web_thread = Thread(target=self._monitor_web, daemon=True)
        
        fs_thread.start()
        web_thread.start()
        
        logger.info(f"✅ Monitoring started (polling every {self.poll_interval}s)")
        
        return fs_thread, web_thread
    
    def _monitor_filesystem(self):
        """Background thread for filesystem monitoring"""
        while self.running:
            try:
                changes = self.scan_filesystem()
                
                # Process changes
                for doc in changes['added']:
                    self.index_document(doc)
                    if self.on_file_added:
                        self.on_file_added(doc)
                
                for doc in changes['modified']:
                    self.index_document(doc)
                    if self.on_file_modified:
                        self.on_file_modified(doc)
                
            except Exception as e:
                logger.error(f"Filesystem monitoring error: {e}")
            
            time.sleep(self.poll_interval)
    
    def _monitor_web(self):
        """Background thread for web monitoring"""
        while self.running:
            try:
                changes = self.scan_web_sources()
                
                # Process changes
                for doc in changes['updated']:
                    self.index_document(doc)
                    if self.on_web_changed:
                        self.on_web_changed(doc)
                
            except Exception as e:
                logger.error(f"Web monitoring error: {e}")
            
            time.sleep(self.poll_interval)
    
    def stop_monitoring(self):
        """Stop all monitoring threads"""
        self.running = False
        logger.info("🛑 Monitoring stopped")
    
    def get_stats(self) -> Dict:
        """Get current statistics"""
        return {
            'total_documents': len(self.documents),
            'files_monitored': len(self.file_hashes),
            'urls_monitored': len(self.url_hashes),
            'internal_docs': len([d for d in self.documents if d['source_type'] == 'internal']),
            'external_docs': len([d for d in self.documents if d['source_type'] == 'external'])
        }


class SimpleRetriever:
    """Retriever interface for the agent"""
    
    def __init__(self, watcher: DocumentWatcher):
        self.watcher = watcher
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve documents"""
        return self.watcher.retrieve(query, top_k)
    
    def retrieve_by_source(self, query: str, source_type: str, top_k: int = 5) -> List[Dict]:
        """Retrieve documents filtered by source"""
        return self.watcher.retrieve(query, top_k, source_type)


if __name__ == "__main__":
    from config.settings import settings
    
    # Create watcher
    watcher = DocumentWatcher(
        data_dir=str(settings.pathway_data_dir),
        external_urls=[settings.external_news_url],
        gemini_api_key=settings.gemini_api_key,
        poll_interval=10
    )
    
    # Set up event handlers
    def on_file_added(doc):
        print(f"\n🆕 NEW FILE EVENT: {doc['name']}")
    
    def on_web_changed(doc):
        print(f"\n🌐 WEB UPDATE EVENT: {doc['url']}")
    
    watcher.on_file_added = on_file_added
    watcher.on_web_changed = on_web_changed
    
    # Start monitoring
    watcher.start_monitoring()
    
    # Keep running
    try:
        while True:
            time.sleep(5)
            stats = watcher.get_stats()
            print(f"\r📊 Stats: {stats['total_documents']} docs indexed", end='')
    except KeyboardInterrupt:
        watcher.stop_monitoring()
        print("\n\n👋 Shutting down...")

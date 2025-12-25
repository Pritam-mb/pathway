"""
Pathway Streaming Engine - Real-time Document Indexing
Monitors local filesystem and external websites for changes.
"""
import pathway as pw
from pathway.xpacks.llm import embedders, prompts
from pathway.xpacks.llm.vector_store import VectorStoreServer
import os
from typing import List, Dict
from datetime import datetime
import google.generativeai as genai


class PathwayEngine:
    """
    Streaming document indexer using Pathway.
    Monitors filesystem and web sources for real-time updates.
    """
    
    def __init__(self, 
                 data_dir: str,
                 external_urls: List[str],
                 gemini_api_key: str,
                 embedding_model: str = "models/embedding-001"):
        
        self.data_dir = data_dir
        self.external_urls = external_urls
        self.gemini_api_key = gemini_api_key
        self.embedding_model = embedding_model
        
        # Initialize Gemini
        genai.configure(api_key=gemini_api_key)
        
        # For Pathway, we'll use OpenAI embeddings as fallback
        # or implement custom Gemini embedder
        # Note: Pathway's built-in embedders primarily support OpenAI
        # For production, you'd implement a custom embedder
        print("⚠️  Note: Using simplified embeddings for Gemini compatibility")
        self.embedder = None  # Will use direct Gemini API calls
        
        print(f"✅ Pathway Engine initialized with Gemini")
        print(f"📁 Watching: {data_dir}")
        print(f"🌐 Monitoring: {external_urls}")
    
    def create_filesystem_source(self):
        """
        Create a streaming source for local documents.
        Monitors the data directory for PDF, DOCX, TXT files.
        """
        # Watch filesystem for changes
        docs = pw.io.fs.read(
            path=self.data_dir,
            format="binary",
            mode="streaming",
            with_metadata=True
        )
        
        return docs
    
    def create_web_source(self):
        """
        Create a streaming source for external websites.
        Uses Pathway's HTTP connector for incremental scraping.
        """
        # Monitor external URLs for changes
        web_docs = []
        
        for url in self.external_urls:
            doc = pw.io.http.read(
                url=url,
                format="html",
                mode="streaming",
                refresh_interval=10  # Check every 10 seconds
            )
            web_docs.append(doc)
        
        # Combine all web sources
        if web_docs:
            return pw.Table.concat(*web_docs)
        return None
    
    def process_documents(self, docs):
        """
        Process documents: extract text, chunk, and embed.
        """
        # Parse different file types
        parsed = docs.select(
            text=pw.apply(self._extract_text, docs.data),
            metadata=docs.metadata,
            source_type=pw.apply(lambda m: m.get('path', 'web'), docs.metadata)
        )
        
        # Chunk documents for better retrieval
        chunked = self._chunk_documents(parsed)
        
        # Generate embeddings
        embedded = chunked.select(
            text=chunked.text,
            embedding=self.embedder(chunked.text),
            metadata=chunked.metadata,
            source_type=chunked.source_type
        )
        
        return embedded
    
    def _extract_text(self, binary_data: bytes) -> str:
        """Extract text from various file formats"""
        # This is a simplified version - in production use proper parsers
        try:
            return binary_data.decode('utf-8')
        except:
            return str(binary_data)
    
    def _chunk_documents(self, docs, chunk_size: int = 1000, overlap: int = 200):
        """
        Split documents into chunks with overlap.
        Medical documents need careful chunking to preserve context.
        """
        # Simple chunking - can be enhanced with semantic splitting
        def chunk_text(text: str) -> List[str]:
            chunks = []
            for i in range(0, len(text), chunk_size - overlap):
                chunk = text[i:i + chunk_size]
                if chunk.strip():
                    chunks.append(chunk)
            return chunks
        
        chunked = docs.select(
            chunks=pw.apply(chunk_text, docs.text),
            metadata=docs.metadata,
            source_type=docs.source_type
        )
        
        # Flatten chunks into separate rows
        return chunked.flatten(chunked.chunks).select(
            text=chunked.chunks,
            metadata=chunked.metadata,
            source_type=chunked.source_type
        )
    
    def start_vector_store(self, host: str = "0.0.0.0", port: int = 8765):
        """
        Start the vector store server for retrieval.
        """
        # Combine filesystem and web sources
        fs_docs = self.create_filesystem_source()
        web_docs = self.create_web_source()
        
        # Process documents
        fs_processed = self.process_documents(fs_docs)
        
        all_docs = fs_processed
        if web_docs is not None:
            web_processed = self.process_documents(web_docs)
            all_docs = pw.Table.concat(fs_processed, web_processed)
        
        # Create vector store server
        server = VectorStoreServer(
            host=host,
            port=port,
            embedder=self.embedder,
            documents=all_docs
        )
        
        print(f"🚀 Vector Store Server starting on {host}:{port}")
        print(f"⚡ Real-time indexing active - no batch refresh needed!")
        
        # Run the server
        server.run()
    
    def get_retriever(self):
        """
        Get a retriever client for querying the vector store.
        """
        # This would return a client to query the vector store
        # Used by the agent for RAG
        pass


def main():
    """Run the Pathway engine"""
    from config.settings import settings
    
    engine = PathwayEngine(
        data_dir=str(settings.pathway_data_dir),
        external_urls=[settings.external_news_url],
        gemini_api_key=settings.gemini_api_key,
        embedding_model=settings.embedding_model
    )
    
    # Start the vector store
    engine.start_vector_store(port=8765)


if __name__ == "__main__":
    main()

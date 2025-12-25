"""
Retriever client for Pathway vector store
"""
import requests
from typing import List, Dict


class PathwayRetriever:
    """
    Client for querying the Pathway vector store.
    Used by the agent to retrieve relevant context.
    """
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.base_url = f"http://{host}:{port}"
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Retrieve top-k most relevant documents for a query.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of documents with text and metadata
        """
        try:
            response = requests.post(
                f"{self.base_url}/v1/retrieve",
                json={
                    "query": query,
                    "k": top_k
                }
            )
            
            if response.status_code == 200:
                return response.json().get("results", [])
            else:
                print(f"⚠️ Retrieval error: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Retrieval failed: {e}")
            return []
    
    def retrieve_by_source(self, query: str, source_type: str, top_k: int = 5) -> List[Dict]:
        """
        Retrieve documents filtered by source type (internal vs external).
        """
        all_results = self.retrieve(query, top_k * 2)
        
        # Filter by source type
        filtered = [
            doc for doc in all_results 
            if doc.get("metadata", {}).get("source_type") == source_type
        ]
        
        return filtered[:top_k]
    
    def get_recent_changes(self, minutes: int = 5) -> List[Dict]:
        """
        Get documents that were added/updated in the last N minutes.
        Useful for detecting deltas in real-time.
        """
        # This would query the vector store for recent updates
        # Pathway tracks modification times automatically
        pass


if __name__ == "__main__":
    # Test retriever
    retriever = PathwayRetriever()
    results = retriever.retrieve("Drug-X cardiac arrhythmia", top_k=3)
    
    print("🔍 Test Query Results:")
    for i, result in enumerate(results):
        print(f"\n{i+1}. {result.get('text', '')[:200]}...")

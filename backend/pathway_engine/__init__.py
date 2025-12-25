"""Pathway engine package"""
# Import only if pathway is available
try:
    from .engine import PathwayEngine
    PATHWAY_AVAILABLE = True
except ImportError:
    PATHWAY_AVAILABLE = False
    PathwayEngine = None

from .retriever import PathwayRetriever

__all__ = ['PathwayEngine', 'PathwayRetriever', 'PATHWAY_AVAILABLE']

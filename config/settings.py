"""
Configuration settings for Bio-Watcher
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    gemini_api_key: str = ""
    
    # Service Ports
    api_port: int = 8000
    mock_site_port: int = 5000
    dashboard_port: int = 3000
    
    # Directories
    pathway_data_dir: Path = Path("./data/hospital_docs")
    pathway_cache_dir: Path = Path("./.pathway_cache")
    synthetic_data_dir: Path = Path("./data/synthetic_data")
    
    # External Sources
    external_news_url: str = "http://localhost:5000/alerts"
    
    # LLM Configuration
    llm_model: str = "gemini-1.5-flash"
    llm_temperature: float = 0.0
    embedding_model: str = "models/embedding-001"
    
    # Agent Configuration
    agent_max_iterations: int = 10
    safety_threshold: int = 75
    
    # Demo Mode
    demo_mode: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create settings instance
settings = Settings()

# Ensure directories exist
settings.pathway_data_dir.mkdir(parents=True, exist_ok=True)
settings.pathway_cache_dir.mkdir(parents=True, exist_ok=True)
settings.synthetic_data_dir.mkdir(parents=True, exist_ok=True)

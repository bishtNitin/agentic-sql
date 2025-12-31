"""
Configuration loader for the application
Loads settings from config.yaml and environment variables
"""
import os
import yaml
from typing import Dict, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Database
    database_url: str = Field(default="sqlite:///./demo.db", env="DATABASE_URL")
    
    # LLM Provider
    llm_provider: str = Field(default="huggingface", env="LLM_PROVIDER")
    huggingface_model: Optional[str] = Field(default=None, env="HUGGINGFACE_MODEL")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: Optional[str] = Field(default=None, env="OPENAI_MODEL")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    anthropic_model: Optional[str] = Field(default=None, env="ANTHROPIC_MODEL")
    
    # Backend
    backend_host: str = Field(default="0.0.0.0", env="BACKEND_HOST")
    backend_port: int = Field(default=8000, env="BACKEND_PORT")
    cors_origins: str = Field(default="http://localhost:3000", env="CORS_ORIGINS")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


class Config:
    """Configuration manager that combines YAML config and environment variables"""
    
    def __init__(self, config_path: str = "backend/config.yaml"):
        self.config_path = config_path
        self.settings = Settings()
        self.yaml_config = self._load_yaml()
        
    def _load_yaml(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_path):
            return {}
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        Priority: Environment variables > YAML config > Default
        """
        # Check environment variable
        env_value = getattr(self.settings, key.lower(), None)
        if env_value is not None:
            return env_value
        
        # Check YAML config
        keys = key.split('.')
        value = self.yaml_config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def get_provider_config(self) -> Dict[str, Any]:
        """Get the configuration for the selected LLM provider"""
        provider = self.settings.llm_provider or self.yaml_config.get('provider', 'huggingface')
        
        if provider == 'huggingface':
            return {
                'provider': 'huggingface',
                'model': self.settings.huggingface_model or self.yaml_config.get('huggingface', {}).get('default_model', 'defog/sqlcoder-7b-2'),
                'max_length': self.yaml_config.get('huggingface', {}).get('max_length', 512),
                'temperature': self.yaml_config.get('huggingface', {}).get('temperature', 0.1),
                'top_p': self.yaml_config.get('huggingface', {}).get('top_p', 0.95),
                'device': self.yaml_config.get('huggingface', {}).get('device', 'cpu'),
                'load_in_8bit': self.yaml_config.get('huggingface', {}).get('load_in_8bit', False),
            }
        elif provider == 'openai':
            return {
                'provider': 'openai',
                'api_key': self.settings.openai_api_key,
                'model': self.settings.openai_model or self.yaml_config.get('openai', {}).get('model', 'gpt-4'),
                'temperature': self.yaml_config.get('openai', {}).get('temperature', 0.1),
                'max_tokens': self.yaml_config.get('openai', {}).get('max_tokens', 500),
            }
        elif provider == 'anthropic':
            return {
                'provider': 'anthropic',
                'api_key': self.settings.anthropic_api_key,
                'model': self.settings.anthropic_model or self.yaml_config.get('anthropic', {}).get('model', 'claude-3-sonnet-20240229'),
                'temperature': self.yaml_config.get('anthropic', {}).get('temperature', 0.1),
                'max_tokens': self.yaml_config.get('anthropic', {}).get('max_tokens', 500),
            }
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def get_database_url(self) -> str:
        """Get the database URL"""
        return self.settings.database_url
    
    def get_execution_config(self) -> Dict[str, Any]:
        """Get query execution configuration"""
        execution = self.yaml_config.get('execution', {})
        return {
            'timeout': execution.get('timeout', 30),
            'max_rows': execution.get('max_rows', 1000),
            'enable_write_queries': execution.get('enable_write_queries', False),
        }
    
    def get_cors_origins(self) -> list:
        """Get CORS origins as a list"""
        origins = self.settings.cors_origins
        return [origin.strip() for origin in origins.split(',')]


# Global config instance
config = Config()

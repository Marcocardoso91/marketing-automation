"""
Configurações centralizadas do MCP Orchestrator
"""
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import yaml
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


@dataclass
class AgentConfig:
    """Configuração de um agente específico"""
    enabled: bool = True
    priority: int = 1
    model: str = ""
    max_tokens: int = 2048
    timeout: int = 30
    fallback_chain: list[str] = None
    
    def __post_init__(self):
        if self.fallback_chain is None:
            self.fallback_chain = []


@dataclass
class ServerConfig:
    """Configurações gerais do servidor"""
    log_level: str = "INFO"
    log_file: str = "logs/mcp_orchestrator.log"
    error_log_file: str = "logs/errors.log"
    max_retries: int = 3
    default_timeout: int = 30
    health_check_interval: int = 30


@dataclass
class SecurityConfig:
    """Configurações de segurança"""
    max_prompt_length: int = 10000
    max_response_length: int = 50000
    rate_limit_per_minute: int = 60
    enable_rate_limiting: bool = True
    sanitize_inputs: bool = True


class Settings:
    """Classe principal de configurações"""
    
    def __init__(self):
        self.server = ServerConfig()
        self.security = SecurityConfig()
        self.agents: Dict[str, AgentConfig] = {}
        self._load_config()
    
    def _load_config(self):
        """Carrega configurações de múltiplas fontes"""
        # Carregar configurações de agentes do YAML
        config_file = Path("config/agents.yaml")
        if config_file.exists():
            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f)
                self._load_agents_from_yaml(config_data)
        
        # Carregar configurações de ambiente
        self._load_from_env()
        
        # Validação
        self._validate_config()
    
    def _load_agents_from_yaml(self, config_data: Dict[str, Any]):
        """Carrega configurações de agentes do YAML"""
        agents_data = config_data.get('agents', {})
        for agent_name, agent_data in agents_data.items():
            self.agents[agent_name] = AgentConfig(
                enabled=agent_data.get('enabled', True),
                priority=agent_data.get('priority', 1),
                model=agent_data.get('model', ''),
                max_tokens=agent_data.get('max_tokens', 2048),
                timeout=agent_data.get('timeout', 30),
                fallback_chain=agent_data.get('fallback_chain', [])
            )
    
    def _load_from_env(self):
        """Carrega configurações de variáveis de ambiente"""
        # Configurações do servidor
        self.server.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.server.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        self.server.default_timeout = int(os.getenv("TIMEOUT", "30"))
        
        # Configurações de segurança
        self.security.max_prompt_length = int(os.getenv("MAX_PROMPT_LENGTH", "10000"))
        self.security.max_response_length = int(os.getenv("MAX_RESPONSE_LENGTH", "50000"))
        self.security.rate_limit_per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
        self.security.enable_rate_limiting = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
        self.security.sanitize_inputs = os.getenv("SANITIZE_INPUTS", "true").lower() == "true"
    
    def _validate_config(self):
        """Valida as configurações carregadas"""
        # Validar nível de log
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.server.log_level not in valid_log_levels:
            raise ValueError(f"LOG_LEVEL deve ser um de: {valid_log_levels}")
        
        # Validar timeouts
        if self.server.default_timeout <= 0:
            raise ValueError("TIMEOUT deve ser maior que 0")
        
        # Validar limites de segurança
        if self.security.max_prompt_length <= 0:
            raise ValueError("MAX_PROMPT_LENGTH deve ser maior que 0")
        
        if self.security.max_response_length <= 0:
            raise ValueError("MAX_RESPONSE_LENGTH deve ser maior que 0")
    
    def get_agent_config(self, agent_name: str) -> Optional[AgentConfig]:
        """Retorna configuração de um agente específico"""
        return self.agents.get(agent_name)
    
    def get_enabled_agents(self) -> list[str]:
        """Retorna lista de agentes habilitados"""
        return [name for name, config in self.agents.items() if config.enabled]
    
    def get_agent_fallback_chain(self, agent_name: str) -> list[str]:
        """Retorna cadeia de fallback de um agente"""
        config = self.get_agent_config(agent_name)
        if config:
            return config.fallback_chain
        return []
    
    def validate_prompt(self, prompt: str) -> bool:
        """Valida se um prompt está dentro dos limites"""
        if len(prompt) > self.security.max_prompt_length:
            return False
        return True
    
    def validate_response(self, response: str) -> bool:
        """Valida se uma resposta está dentro dos limites"""
        if len(response) > self.security.max_response_length:
            return False
        return True


# Instância global de configurações
settings = Settings() 
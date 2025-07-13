"""
Configuração de logging estruturado para o MCP Orchestrator
"""
import logging
import logging.handlers
import json
import sys
from pathlib import Path
from typing import Any, Dict
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Formatter para logs em formato JSON"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Adicionar campos extras se existirem
        if hasattr(record, 'agent'):
            log_entry['agent'] = record.agent
        if hasattr(record, 'duration'):
            log_entry['duration'] = record.duration
        if hasattr(record, 'error_type'):
            log_entry['error_type'] = record.error_type
        
        # Adicionar exceção se existir
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)


class StructuredFormatter(logging.Formatter):
    """Formatter para logs estruturados legíveis"""
    
    def format(self, record: logging.LogRecord) -> str:
        # Formato base
        formatted = f"{record.asctime} - {record.name} - {record.levelname} - {record.getMessage()}"
        
        # Adicionar campos extras
        extra_fields = []
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename', 'module', 'lineno', 'funcName', 'created', 'msecs', 'relativeCreated', 'thread', 'threadName', 'processName', 'process', 'getMessage', 'exc_info', 'exc_text', 'stack_info']:
                extra_fields.append(f"{key}={value}")
        
        if extra_fields:
            formatted += f" | {' | '.join(extra_fields)}"
        
        return formatted


def setup_logging(
    log_level: str = "INFO",
    log_file: str = "logs/mcp_orchestrator.log",
    error_log_file: str = "logs/errors.log",
    enable_json_logs: bool = False,
    enable_console_logs: bool = True
) -> None:
    """
    Configura o sistema de logging
    
    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Arquivo para logs gerais
        error_log_file: Arquivo para logs de erro
        enable_json_logs: Se deve usar formato JSON
        enable_console_logs: Se deve logar no console
    """
    # Criar diretório de logs se não existir
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    Path(error_log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Configurar logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Limpar handlers existentes
    root_logger.handlers.clear()
    
    # Formatter
    if enable_json_logs:
        formatter = JSONFormatter()
        console_formatter = JSONFormatter()
    else:
        formatter = StructuredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    # Handler para console (stderr)
    if enable_console_logs:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        root_logger.addHandler(console_handler)
    
    # Handler para arquivo de logs gerais
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, log_level.upper()))
    root_logger.addHandler(file_handler)
    
    # Handler para arquivo de erros
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=3,
        encoding='utf-8'
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    root_logger.addHandler(error_handler)
    
    # Logger específico para o MCP Orchestrator
    mcp_logger = logging.getLogger('mcp_orchestrator')
    mcp_logger.setLevel(getattr(logging, log_level.upper()))


def get_logger(name: str) -> logging.Logger:
    """Retorna um logger configurado"""
    return logging.getLogger(name)


def log_with_context(logger: logging.Logger, level: str, message: str, **kwargs) -> None:
    """
    Loga uma mensagem com contexto adicional
    
    Args:
        logger: Logger a ser usado
        level: Nível de log
        message: Mensagem principal
        **kwargs: Campos adicionais para o log
    """
    log_func = getattr(logger, level.lower())
    
    # Criar LogRecord com campos extras
    record = logger.makeRecord(
        logger.name,
        getattr(logging, level.upper()),
        "",
        0,
        message,
        (),
        None
    )
    
    # Adicionar campos extras
    for key, value in kwargs.items():
        setattr(record, key, value)
    
    logger.handle(record)


# Função de conveniência para log de agente
def log_agent_call(logger: logging.Logger, agent: str, prompt: str, duration: float = None, success: bool = True, error: str = None) -> None:
    """
    Loga uma chamada de agente com contexto completo
    
    Args:
        logger: Logger a ser usado
        agent: Nome do agente
        prompt: Prompt enviado
        duration: Duração da chamada em segundos
        success: Se a chamada foi bem-sucedida
        error: Mensagem de erro se houver
    """
    level = "info" if success else "error"
    message = f"Agente {agent} {'chamado com sucesso' if success else 'falhou'}"
    
    context = {
        "agent": agent,
        "prompt_length": len(prompt),
        "success": success
    }
    
    if duration is not None:
        context["duration"] = duration
    
    if error:
        context["error"] = error
    
    log_with_context(logger, level, message, **context)


# Função de conveniência para log de fallback
def log_fallback(logger: logging.Logger, from_agent: str, to_agent: str, reason: str) -> None:
    """
    Loga um evento de fallback
    
    Args:
        logger: Logger a ser usado
        from_agent: Agente que falhou
        to_agent: Agente de fallback
        reason: Razão do fallback
    """
    message = f"Fallback de {from_agent} para {to_agent}"
    log_with_context(
        logger, "warning", message,
        from_agent=from_agent,
        to_agent=to_agent,
        fallback_reason=reason
    ) 
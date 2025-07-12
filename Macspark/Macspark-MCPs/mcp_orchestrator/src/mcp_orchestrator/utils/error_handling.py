"""
Sistema de tratamento de erros unificado para o MCP Orchestrator
"""
import time
import logging
from typing import Callable, Any, Optional, Type
from functools import wraps
from enum import Enum


class ErrorType(Enum):
    """Tipos de erro para categorização"""
    AUTHENTICATION = "authentication"
    RATE_LIMIT = "rate_limit"
    NETWORK = "network"
    TIMEOUT = "timeout"
    VALIDATION = "validation"
    UNKNOWN = "unknown"


class FatalError(Exception):
    """Erro que não deve acionar fallback (ex: auth, validação)"""
    
    def __init__(self, message: str, error_type: ErrorType = ErrorType.UNKNOWN, details: Optional[dict] = None):
        super().__init__(message)
        self.error_type = error_type
        self.details = details or {}
        self.timestamp = time.time()


class FallibleError(Exception):
    """Erro que deve acionar fallback (ex: rate limit, server error)"""
    
    def __init__(self, message: str, error_type: ErrorType = ErrorType.UNKNOWN, details: Optional[dict] = None):
        super().__init__(message)
        self.error_type = error_type
        self.details = details or {}
        self.timestamp = time.time()


class ValidationError(FatalError):
    """Erro de validação de entrada"""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Any = None):
        super().__init__(message, ErrorType.VALIDATION, {"field": field, "value": value})


class AuthenticationError(FatalError):
    """Erro de autenticação"""
    
    def __init__(self, message: str, provider: Optional[str] = None):
        super().__init__(message, ErrorType.AUTHENTICATION, {"provider": provider})


class RateLimitError(FallibleError):
    """Erro de limite de taxa"""
    
    def __init__(self, message: str, provider: Optional[str] = None, retry_after: Optional[int] = None):
        super().__init__(message, ErrorType.RATE_LIMIT, {
            "provider": provider,
            "retry_after": retry_after
        })


class NetworkError(FallibleError):
    """Erro de rede/conexão"""
    
    def __init__(self, message: str, provider: Optional[str] = None):
        super().__init__(message, ErrorType.NETWORK, {"provider": provider})


class TimeoutError(FallibleError):
    """Erro de timeout"""
    
    def __init__(self, message: str, provider: Optional[str] = None, timeout: Optional[float] = None):
        super().__init__(message, ErrorType.TIMEOUT, {
            "provider": provider,
            "timeout": timeout
        })


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: tuple = (FallibleError,),
    logger: Optional[logging.Logger] = None
):
    """
    Decorator para retry com backoff exponencial
    
    Args:
        max_retries: Número máximo de tentativas
        base_delay: Delay inicial em segundos
        max_delay: Delay máximo em segundos
        exponential_base: Base para cálculo exponencial
        exceptions: Tupla de exceções que devem acionar retry
        logger: Logger para logar tentativas
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        # Última tentativa falhou
                        if logger:
                            logger.error(f"Função {func.__name__} falhou após {max_retries + 1} tentativas: {e}")
                        raise e
                    
                    # Calcular delay com backoff exponencial
                    delay = min(base_delay * (exponential_base ** attempt), max_delay)
                    
                    if logger:
                        logger.warning(
                            f"Tentativa {attempt + 1}/{max_retries + 1} falhou para {func.__name__}. "
                            f"Tentando novamente em {delay:.2f}s. Erro: {e}"
                        )
                    
                    time.sleep(delay)
            
            # Nunca deve chegar aqui, mas por segurança
            raise last_exception
        
        return wrapper
    return decorator


def handle_api_error(error: Exception, provider: str) -> Exception:
    """
    Converte exceções de API em exceções unificadas
    
    Args:
        error: Exceção original
        provider: Nome do provedor de API
    
    Returns:
        Exceção unificada (FatalError ou FallibleError)
    """
    error_message = str(error).lower()
    
    # Mapear exceções específicas por provedor
    if provider == "claude":
        return _handle_claude_error(error, error_message)
    elif provider == "gemini":
        return _handle_gemini_error(error, error_message)
    elif provider == "openai":
        return _handle_openai_error(error, error_message)
    elif provider == "mistral":
        return _handle_mistral_error(error, error_message)
    elif provider == "cohere":
        return _handle_cohere_error(error, error_message)
    elif provider == "perplexity":
        return _handle_perplexity_error(error, error_message)
    else:
        # Fallback genérico
        return _handle_generic_error(error, error_message, provider)


def _handle_claude_error(error: Exception, error_message: str) -> Exception:
    """Trata erros específicos do Claude"""
    import anthropic
    
    if isinstance(error, anthropic.AuthenticationError):
        return AuthenticationError(f"Claude authentication failed: {error}", "claude")
    elif isinstance(error, anthropic.RateLimitError):
        return RateLimitError(f"Claude rate limit exceeded: {error}", "claude")
    elif isinstance(error, (anthropic.APIConnectionError, anthropic.InternalServerError)):
        return NetworkError(f"Claude network/server error: {error}", "claude")
    else:
        return FallibleError(f"Claude unexpected error: {error}", ErrorType.UNKNOWN, {"original_error": str(error)})


def _handle_gemini_error(error: Exception, error_message: str) -> Exception:
    """Trata erros específicos do Gemini"""
    if "api key not valid" in error_message:
        return AuthenticationError(f"Gemini authentication failed: {error}", "gemini")
    elif "429" in error_message or "resource_exhausted" in error_message:
        return RateLimitError(f"Gemini rate limit exceeded: {error}", "gemini")
    else:
        return FallibleError(f"Gemini error: {error}", ErrorType.UNKNOWN, {"original_error": str(error)})


def _handle_openai_error(error: Exception, error_message: str) -> Exception:
    """Trata erros específicos do OpenAI"""
    import openai
    
    if isinstance(error, openai.AuthenticationError):
        return AuthenticationError(f"OpenAI authentication failed: {error}", "openai")
    elif isinstance(error, openai.RateLimitError):
        return RateLimitError(f"OpenAI rate limit exceeded: {error}", "openai")
    else:
        return FallibleError(f"OpenAI error: {error}", ErrorType.UNKNOWN, {"original_error": str(error)})


def _handle_mistral_error(error: Exception, error_message: str) -> Exception:
    """Trata erros específicos do Mistral"""
    if "authentication" in error_message or "api key" in error_message:
        return AuthenticationError(f"Mistral authentication failed: {error}", "mistral")
    elif "rate limit" in error_message or "429" in error_message:
        return RateLimitError(f"Mistral rate limit exceeded: {error}", "mistral")
    else:
        return FallibleError(f"Mistral error: {error}", ErrorType.UNKNOWN, {"original_error": str(error)})


def _handle_cohere_error(error: Exception, error_message: str) -> Exception:
    """Trata erros específicos do Cohere"""
    if "authentication" in error_message or "api key" in error_message:
        return AuthenticationError(f"Cohere authentication failed: {error}", "cohere")
    elif "rate limit" in error_message:
        return RateLimitError(f"Cohere rate limit exceeded: {error}", "cohere")
    else:
        return FallibleError(f"Cohere error: {error}", ErrorType.UNKNOWN, {"original_error": str(error)})


def _handle_perplexity_error(error: Exception, error_message: str) -> Exception:
    """Trata erros específicos do Perplexity"""
    if "401" in error_message:
        return AuthenticationError(f"Perplexity authentication failed: {error}", "perplexity")
    elif "429" in error_message:
        return RateLimitError(f"Perplexity rate limit exceeded: {error}", "perplexity")
    else:
        return FallibleError(f"Perplexity error: {error}", ErrorType.UNKNOWN, {"original_error": str(error)})


def _handle_generic_error(error: Exception, error_message: str, provider: str) -> Exception:
    """Tratamento genérico de erros"""
    if "timeout" in error_message or "timed out" in error_message:
        return TimeoutError(f"{provider} timeout: {error}", provider)
    elif "connection" in error_message or "network" in error_message:
        return NetworkError(f"{provider} network error: {error}", provider)
    else:
        return FallibleError(f"{provider} error: {error}", ErrorType.UNKNOWN, {"original_error": str(error)})


def validate_input(prompt: str, max_length: int = 10000) -> None:
    """
    Valida entrada do usuário
    
    Args:
        prompt: Prompt a ser validado
        max_length: Comprimento máximo permitido
    
    Raises:
        ValidationError: Se a validação falhar
    """
    if not prompt or not prompt.strip():
        raise ValidationError("Prompt não pode estar vazio", "prompt", prompt)
    
    if len(prompt) > max_length:
        raise ValidationError(
            f"Prompt muito longo ({len(prompt)} caracteres). Máximo: {max_length}",
            "prompt_length",
            len(prompt)
        )
    
    # Verificar caracteres suspeitos (opcional)
    suspicious_chars = ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07']
    for char in suspicious_chars:
        if char in prompt:
            raise ValidationError(f"Prompt contém caracteres inválidos", "prompt_content", char)


def sanitize_response(response: str, max_length: int = 50000) -> str:
    """
    Sanitiza resposta da IA
    
    Args:
        response: Resposta a ser sanitizada
        max_length: Comprimento máximo permitido
    
    Returns:
        Resposta sanitizada
    """
    if not response:
        return ""
    
    # Truncar se muito longo
    if len(response) > max_length:
        response = response[:max_length] + "... [truncado]"
    
    # Remover caracteres de controle (exceto quebras de linha e tab)
    import re
    response = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', response)
    
    return response 
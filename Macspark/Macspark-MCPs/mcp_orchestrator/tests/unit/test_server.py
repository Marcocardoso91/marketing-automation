"""
Testes unitários para o servidor MCP Orchestrator
"""
import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

from mcp_orchestrator.server import (
    call_claude_api,
    call_gemini_api,
    call_ollama,
    get_ai_response,
    OrchestratorResult
)
from mcp_orchestrator.utils.error_handling import (
    FatalError,
    FallibleError,
    ValidationError,
    AuthenticationError,
    RateLimitError
)


class TestAgentFunctions:
    """Testes para funções de agentes"""
    
    @patch('mcp_orchestrator.server.anthropic.Anthropic')
    def test_call_claude_api_success(self, mock_anthropic):
        """Testa chamada bem-sucedida para Claude API"""
        # Setup
        mock_client = Mock()
        mock_anthropic.return_value = mock_client
        
        mock_message = Mock()
        mock_message.content = [Mock(text="Resposta do Claude")]
        mock_client.messages.create.return_value = mock_message
        
        # Execute
        result = call_claude_api("Teste prompt", {"model": "claude-3-sonnet-20240229"})
        
        # Assert
        assert result == "Resposta do Claude"
        mock_client.messages.create.assert_called_once()
    
    @patch('mcp_orchestrator.server.anthropic.Anthropic')
    def test_call_claude_api_authentication_error(self, mock_anthropic):
        """Testa erro de autenticação do Claude API"""
        # Setup
        mock_client = Mock()
        mock_anthropic.return_value = mock_client
        
        from anthropic import AuthenticationError
        mock_client.messages.create.side_effect = AuthenticationError("Invalid API key")
        
        # Execute & Assert
        with pytest.raises(FatalError) as exc_info:
            call_claude_api("Teste prompt", {})
        
        assert "AuthenticationError" in str(exc_info.value)
    
    @patch('mcp_orchestrator.server.genai')
    def test_call_gemini_api_success(self, mock_genai):
        """Testa chamada bem-sucedida para Gemini API"""
        # Setup
        mock_model = Mock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        mock_response = Mock()
        mock_response.text = "Resposta do Gemini"
        mock_model.generate_content.return_value = mock_response
        
        # Execute
        result = call_gemini_api("Teste prompt", {"model": "gemini-1.5-pro-latest"})
        
        # Assert
        assert result == "Resposta do Gemini"
        mock_model.generate_content.assert_called_once_with("Teste prompt")
    
    @patch('mcp_orchestrator.server.requests.post')
    def test_call_ollama_success(self, mock_post):
        """Testa chamada bem-sucedida para Ollama"""
        # Setup
        mock_response = Mock()
        mock_response.json.return_value = {"response": "Resposta do Ollama"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Execute
        result = call_ollama("Teste prompt", {"model": "llama3.1:8b"})
        
        # Assert
        assert result == "Resposta do Ollama"
        mock_post.assert_called_once()
    
    @patch('mcp_orchestrator.server.requests.post')
    def test_call_ollama_connection_error(self, mock_post):
        """Testa erro de conexão do Ollama"""
        # Setup
        from requests.exceptions import ConnectionError
        mock_post.side_effect = ConnectionError("Connection failed")
        
        # Execute & Assert
        with pytest.raises(FatalError) as exc_info:
            call_ollama("Teste prompt", {})
        
        assert "Ollama connection failed" in str(exc_info.value)


class TestOrchestratorResult:
    """Testes para o modelo OrchestratorResult"""
    
    def test_orchestrator_result_success(self):
        """Testa criação de resultado de sucesso"""
        result = OrchestratorResult(
            status="success",
            agent="claude_api",
            response="Resposta de teste"
        )
        
        assert result.status == "success"
        assert result.agent == "claude_api"
        assert result.response == "Resposta de teste"
        assert result.notes is None
        assert result.error_details is None
    
    def test_orchestrator_result_error(self):
        """Testa criação de resultado de erro"""
        result = OrchestratorResult(
            status="error",
            agent="none",
            error_details="Erro de teste"
        )
        
        assert result.status == "error"
        assert result.agent == "none"
        assert result.response is None
        assert result.error_details == "Erro de teste"


class TestGetAIResponse:
    """Testes para a função principal get_ai_response"""
    
    @patch('mcp_orchestrator.server.call_claude_api')
    def test_get_ai_response_primary_success(self, mock_call_claude):
        """Testa sucesso com agente primário"""
        # Setup
        mock_call_claude.return_value = "Resposta do Claude"
        
        # Execute
        result = get_ai_response(
            prompt="Teste prompt",
            agent="claude_api",
            params={}
        )
        
        # Assert
        assert result.status == "success"
        assert result.agent == "claude_api"
        assert result.response == "Resposta do Claude"
        assert result.notes is None
    
    @patch('mcp_orchestrator.server.call_claude_api')
    @patch('mcp_orchestrator.server.call_claude_cli')
    def test_get_ai_response_with_fallback(self, mock_call_cli, mock_call_api):
        """Testa fallback quando agente primário falha"""
        # Setup
        mock_call_api.side_effect = FallibleError("API error")
        mock_call_cli.return_value = "Resposta do CLI"
        
        # Execute
        result = get_ai_response(
            prompt="Teste prompt",
            agent="claude_api",
            params={}
        )
        
        # Assert
        assert result.status == "success"
        assert result.agent == "claude_cli"
        assert result.response == "Resposta do CLI"
        assert "Fallback" in result.notes
    
    @patch('mcp_orchestrator.server.call_claude_api')
    @patch('mcp_orchestrator.server.call_claude_cli')
    @patch('mcp_orchestrator.server.call_gemini_api')
    def test_get_ai_response_all_fail(self, mock_call_gemini, mock_call_cli, mock_call_api):
        """Testa quando todos os agentes falham"""
        # Setup
        mock_call_api.side_effect = FallibleError("API error")
        mock_call_cli.side_effect = FallibleError("CLI error")
        mock_call_gemini.side_effect = FallibleError("Gemini error")
        
        # Execute
        result = get_ai_response(
            prompt="Teste prompt",
            agent="claude_api",
            params={}
        )
        
        # Assert
        assert result.status == "error"
        assert result.agent == "none"
        assert "Todos os agentes falharam" in result.error_details
    
    @patch('mcp_orchestrator.server.call_claude_api')
    def test_get_ai_response_fatal_error(self, mock_call_api):
        """Testa erro fatal (sem fallback)"""
        # Setup
        mock_call_api.side_effect = FatalError("Fatal error")
        
        # Execute
        result = get_ai_response(
            prompt="Teste prompt",
            agent="claude_api",
            params={}
        )
        
        # Assert
        assert result.status == "error"
        assert result.agent == "claude_api"
        assert "Erro fatal" in result.error_details


class TestErrorHandling:
    """Testes para tratamento de erros"""
    
    def test_fatal_error_creation(self):
        """Testa criação de FatalError"""
        error = FatalError("Test error")
        assert str(error) == "Test error"
        assert error.error_type.value == "unknown"
    
    def test_fallible_error_creation(self):
        """Testa criação de FallibleError"""
        error = FallibleError("Test error")
        assert str(error) == "Test error"
        assert error.error_type.value == "unknown"
    
    def test_validation_error_creation(self):
        """Testa criação de ValidationError"""
        error = ValidationError("Invalid input", "prompt", "test")
        assert str(error) == "Invalid input"
        assert error.error_type.value == "validation"
        assert error.details["field"] == "prompt"
        assert error.details["value"] == "test"


class TestInputValidation:
    """Testes para validação de entrada"""
    
    def test_validate_input_empty_prompt(self):
        """Testa validação de prompt vazio"""
        from mcp_orchestrator.utils.error_handling import validate_input
        
        with pytest.raises(ValidationError) as exc_info:
            validate_input("")
        
        assert "não pode estar vazio" in str(exc_info.value)
    
    def test_validate_input_too_long(self):
        """Testa validação de prompt muito longo"""
        from mcp_orchestrator.utils.error_handling import validate_input
        
        long_prompt = "a" * 10001
        
        with pytest.raises(ValidationError) as exc_info:
            validate_input(long_prompt, max_length=10000)
        
        assert "muito longo" in str(exc_info.value)
    
    def test_validate_input_valid(self):
        """Testa validação de prompt válido"""
        from mcp_orchestrator.utils.error_handling import validate_input
        
        # Não deve levantar exceção
        validate_input("Prompt válido")
        validate_input("a" * 10000, max_length=10000)


class TestResponseSanitization:
    """Testes para sanitização de resposta"""
    
    def test_sanitize_response_empty(self):
        """Testa sanitização de resposta vazia"""
        from mcp_orchestrator.utils.error_handling import sanitize_response
        
        result = sanitize_response("")
        assert result == ""
    
    def test_sanitize_response_truncate(self):
        """Testa truncamento de resposta muito longa"""
        from mcp_orchestrator.utils.error_handling import sanitize_response
        
        long_response = "a" * 50001
        result = sanitize_response(long_response, max_length=50000)
        
        assert len(result) <= 50000 + len("... [truncado]")
        assert result.endswith("... [truncado]")
    
    def test_sanitize_response_control_chars(self):
        """Testa remoção de caracteres de controle"""
        from mcp_orchestrator.utils.error_handling import sanitize_response
        
        response_with_control = "Hello\x00World\x01Test"
        result = sanitize_response(response_with_control)
        
        assert "\x00" not in result
        assert "\x01" not in result
        assert "Hello" in result
        assert "World" in result
        assert "Test" in result


if __name__ == "__main__":
    pytest.main([__file__]) 
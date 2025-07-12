"""
MCP Orchestrator Server
----------------------
Servidor MCP híbrido para orquestração de múltiplos agentes de IA (APIs, CLIs, LLMs locais)
com fallback inteligente e arquitetura extensível.
"""
import sys
import os
import logging
import subprocess
import json
from typing import Dict, Any, Literal
from dotenv import load_dotenv
from fastmcp import FastMCP
from pydantic import BaseModel, Field
import requests
# AI SDKs
import anthropic
import google.generativeai as genai
import openai
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import cohere

# --- 1. Initial Setup ---
load_dotenv()
log = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.INFO)

# --- 2. Configuração & API Keys ---
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")

# --- 3. Unified Error Classes ---
class FatalError(Exception):
    pass
class FallibleError(Exception):
    pass

# --- 4. Funções dos agentes ---
def call_claude_api(prompt: str, params: Dict[str, Any]) -> str:
    log.info("Chamando Claude API")
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model=params.get("model", "claude-3-sonnet-20240229"),
            max_tokens=params.get("max_tokens", 2048),
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join([block.text for block in message.content if hasattr(block, 'text')])
    except anthropic.AuthenticationError as e:
        raise FatalError(f"Claude API AuthenticationError: {e}")
    except anthropic.RateLimitError as e:
        raise FallibleError(f"Claude API RateLimitError: {e}")
    except (anthropic.APIConnectionError, anthropic.InternalServerError) as e:
        raise FallibleError(f"Claude API Server/Connection Error: {e}")
    except Exception as e:
        raise FatalError(f"Claude API Unexpected Error: {e}")

def call_claude_cli(prompt: str, params: Dict[str, Any]) -> str:
    log.info("Chamando Claude CLI")
    try:
        cmd = ["claude", "chat", "--prompt", prompt]
        if "model" in params:
            cmd.extend(["--model", params["model"]])
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise FallibleError(f"Claude CLI Error: {result.stderr}")
    except subprocess.TimeoutExpired:
        raise FallibleError("Claude CLI timeout")
    except FileNotFoundError:
        raise FatalError("Claude CLI not installed")
    except Exception as e:
        raise FallibleError(f"Claude CLI Error: {e}")

def call_gemini_api(prompt: str, params: Dict[str, Any]) -> str:
    log.info("Chamando Gemini API")
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel(params.get("model", 'gemini-1.5-pro-latest'))
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_message = str(e).lower()
        if "api key not valid" in error_message:
            raise FatalError(f"Gemini API AuthenticationError: {e}")
        elif "429" in error_message or "resource_exhausted" in error_message:
            raise FallibleError(f"Gemini API RateLimitError: {e}")
        else:
            raise FallibleError(f"Gemini API Generic Error: {e}")

def call_gemini_cli(prompt: str, params: Dict[str, Any]) -> str:
    log.info("Chamando Gemini CLI")
    try:
        cmd = ["gemini", "chat", "--prompt", prompt]
        if "model" in params:
            cmd.extend(["--model", params["model"]])
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise FallibleError(f"Gemini CLI Error: {result.stderr}")
    except subprocess.TimeoutExpired:
        raise FallibleError("Gemini CLI timeout")
    except FileNotFoundError:
        raise FatalError("Gemini CLI not installed")
    except Exception as e:
        raise FallibleError(f"Gemini CLI Error: {e}")

def call_ollama(prompt: str, params: Dict[str, Any]) -> str:
    log.info("Chamando Ollama local")
    try:
        model = params.get("model", "llama3.1:8b")
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": params.get("temperature", 0.7),
                "top_p": params.get("top_p", 0.9),
                "max_tokens": params.get("max_tokens", 2048)
            }
        }
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["response"]
    except requests.exceptions.ConnectionError:
        raise FatalError("Ollama connection failed. Make sure Ollama is running.")
    except Exception as e:
        raise FallibleError(f"Ollama Error: {e}")

def call_lm_studio(prompt: str, params: Dict[str, Any]) -> str:
    log.info("Chamando LM Studio local")
    try:
        data = {
            "model": params.get("model", "local-model"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": params.get("temperature", 0.7),
            "max_tokens": params.get("max_tokens", 2048)
        }
        response = requests.post(f"{LM_STUDIO_BASE_URL}/chat/completions", json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.ConnectionError:
        raise FatalError("LM Studio connection failed. Make sure LM Studio is running.")
    except Exception as e:
        raise FallibleError(f"LM Studio Error: {e}")

# (Outros agentes como openai, mistral, cohere, perplexity podem ser adicionados aqui)

# --- 5. MCP Server Definition ---
mcp = FastMCP(
    name="hybrid-ai-orchestrator-mcp",
    description="Servidor MCP híbrido para múltiplos agentes de IA (APIs, CLIs, LLMs locais)",
    version="3.0.0"
)

class OrchestratorResult(BaseModel):
    status: Literal["success", "error"]
    agent: str
    response: str | None = None
    notes: str | None = None
    error_details: str | None = None

@mcp.tool()
def get_ai_response(
    prompt: str = Field(..., description="Prompt do usuário para o modelo de IA."),
    agent: Literal["claude_api", "claude_cli", "gemini_api", "gemini_cli", "ollama", "lm_studio"] = Field("claude_api", description="Agente preferido."),
    params: Dict[str, Any] = Field({}, description="Parâmetros opcionais para o modelo de IA.")
) -> OrchestratorResult:
    """
    Orquestra uma requisição para um modelo de IA com fallback inteligente.
    """
    agent_configs = {
        "claude_api": {
            "primary": call_claude_api,
            "fallback_chain": [call_claude_cli, call_gemini_api, call_gemini_cli],
            "fallback_names": ["claude_cli", "gemini_api", "gemini_cli"]
        },
        "claude_cli": {
            "primary": call_claude_cli,
            "fallback_chain": [call_claude_api, call_gemini_cli, call_gemini_api],
            "fallback_names": ["claude_api", "gemini_cli", "gemini_api"]
        },
        "gemini_api": {
            "primary": call_gemini_api,
            "fallback_chain": [call_gemini_cli, call_claude_api, call_claude_cli],
            "fallback_names": ["gemini_cli", "claude_api", "claude_cli"]
        },
        "gemini_cli": {
            "primary": call_gemini_cli,
            "fallback_chain": [call_gemini_api, call_claude_cli, call_claude_api],
            "fallback_names": ["gemini_api", "claude_cli", "claude_api"]
        },
        "ollama": {
            "primary": call_ollama,
            "fallback_chain": [call_lm_studio, call_claude_cli, call_gemini_cli],
            "fallback_names": ["lm_studio", "claude_cli", "gemini_cli"]
        },
        "lm_studio": {
            "primary": call_lm_studio,
            "fallback_chain": [call_ollama, call_claude_cli, call_gemini_cli],
            "fallback_names": ["ollama", "claude_cli", "gemini_cli"]
        },
    }
    config = agent_configs[agent]
    try:
        response_text = config["primary"](prompt, params)
        return OrchestratorResult(status="success", agent=agent, response=response_text)
    except FallibleError as e:
        for fallback_func, fallback_name in zip(config["fallback_chain"], config["fallback_names"]):
            try:
                response_text = fallback_func(prompt, params)
                return OrchestratorResult(status="success", agent=fallback_name, response=response_text, notes=f"Fallback de '{agent}' para '{fallback_name}' foi acionado.")
            except (FallibleError, FatalError):
                continue
        return OrchestratorResult(status="error", agent="none", error_details=f"Todos os agentes falharam. Erro primário: {e}")
    except FatalError as e:
        return OrchestratorResult(status="error", agent=agent, error_details=f"Erro fatal: {e}")

# --- 6. Execução do servidor ---
def main():
    log.info("Iniciando MCP Orchestrator...")
    mcp.run()

if __name__ == "__main__":
    main() 
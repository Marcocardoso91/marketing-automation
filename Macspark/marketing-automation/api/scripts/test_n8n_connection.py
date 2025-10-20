#!/usr/bin/env python3
"""
Test n8n Macspark Connection
Testa conectividade com a instância n8n da Macspark
"""
from dotenv import load_dotenv
import httpx
import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


# Load environment variables
load_dotenv()


async def test_n8n_api():
    """Testa conexão com n8n API da Macspark"""

    api_url = os.getenv("N8N_API_URL", "https://fluxos.macspark.dev/api/v1")
    api_key = os.getenv("N8N_API_KEY")

    if not api_key:
        print("[ERRO] N8N_API_KEY nao configurada no .env")
        return False

    print(f"[INFO] Testando conexao com: {api_url}")
    print(f"[INFO] API Key: {api_key[:20]}...")
    print()

    headers = {
        "X-N8N-API-KEY": api_key,
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test 1: List workflows
            print("[TEST 1] Listando workflows...")
            response = await client.get(
                f"{api_url}/workflows",
                headers=headers
            )

            if response.status_code == 200:
                workflows = response.json()
                print(
                    f"[OK] Conexao OK! Encontrados {len(workflows.get('data', []))} workflows")

                if workflows.get('data'):
                    print("\nWorkflows encontrados:")
                    for wf in workflows['data'][:5]:  # Show first 5
                        status = "[ATIVO]" if wf.get('active') else "[INATIVO]"
                        print(
                            f"  - {wf.get('name')} ({wf.get('id')}) {status}")
                else:
                    print("  (Nenhum workflow encontrado)")

                print()
                return True
            else:
                print(f"[ERRO] Status {response.status_code}: {response.text}")
                return False

    except httpx.ConnectError:
        print(f"[ERRO] Nao foi possivel conectar a {api_url}")
        print("   Verifique se a URL esta correta e acessivel")
        return False
    except httpx.TimeoutException:
        print(f"[ERRO] Timeout ao conectar a {api_url}")
        return False
    except Exception as e:
        print(f"[ERRO] Erro inesperado: {e}")
        return False


async def test_n8n_mcp():
    """Testa MCPs do n8n via endpoints FastAPI"""

    print("[TEST 2] Testando endpoints FastAPI + MCP...")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test list workflows via FastAPI
            response = await client.get("http://localhost:8000/api/v1/n8n/workflows")

            if response.status_code == 200:
                print("[OK] Endpoint FastAPI OK!")
                workflows = response.json()
                print(f"   Workflows via FastAPI: {len(workflows)}")
                print()
                return True
            elif response.status_code == 404:
                print("[AVISO] Servidor FastAPI nao esta rodando")
                print("   Execute: docker-compose up -d")
                print()
                return False
            else:
                print(f"[ERRO] Status {response.status_code}: {response.text}")
                return False

    except httpx.ConnectError:
        print("[AVISO] Servidor FastAPI nao esta rodando em http://localhost:8000")
        print("   Execute: docker-compose up -d")
        print()
        return False
    except Exception as e:
        print(f"[ERRO] Erro: {e}")
        return False


async def main():
    """Run all tests"""
    print("=" * 60)
    print("TEST N8N MACSPARK CONNECTION")
    print("=" * 60)
    print()

    # Test 1: Direct API connection
    api_ok = await test_n8n_api()

    # Test 2: FastAPI endpoints (only if API is OK)
    if api_ok:
        await test_n8n_mcp()

    print("=" * 60)
    if api_ok:
        print("[OK] TESTES CONCLUIDOS COM SUCESSO!")
        print()
        print("Proximos passos:")
        print("   1. Verificar workflows existentes no n8n")
        print("   2. Criar novos workflows via MCP")
        print("   3. Testar integracao completa")
    else:
        print("[ERRO] TESTES FALHARAM")
        print()
        print("Verifique:")
        print("   1. N8N_API_KEY esta correto no .env")
        print("   2. URL https://fluxos.macspark.dev esta acessivel")
        print("   3. Token nao expirou")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

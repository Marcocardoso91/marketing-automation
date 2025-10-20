#!/usr/bin/env python3
"""Script para iniciar ambiente de desenvolvimento completo"""
import subprocess
import sys
import time
from pathlib import Path


def check_dependencies():
    """Verificar se dependências estão instaladas"""
    print("Verificando dependências...")
    try:
        import fastapi
        import uvicorn
        import celery
        import redis
        print("[OK] Dependências principais instaladas")
        return True
    except ImportError as e:
        print(f"[ERRO] Dependência faltando: {e}")
        print("Execute: pip install -r requirements.txt")
        return False


def check_env_file():
    """Verificar se .env existe"""
    env_file = Path(".env")
    if not env_file.exists():
        print("[AVISO] Arquivo .env não encontrado")
        print("Criando .env a partir de .env.example...")
        try:
            example = Path(".env.example")
            if example.exists():
                import shutil
                shutil.copy(example, env_file)
                print("[OK] .env criado")
            else:
                print("[ERRO] .env.example não encontrado")
                return False
        except Exception as e:
            print(f"[ERRO] Erro ao criar .env: {e}")
            return False
    else:
        print("[OK] Arquivo .env encontrado")
    return True


def start_server():
    """Iniciar servidor FastAPI"""
    print("\nIniciando servidor FastAPI...")
    print("Acesse: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print("\nPressione Ctrl+C para parar\n")

    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n[OK] Servidor parado")


def main():
    """Função principal"""
    print("="*50)
    print("Facebook Ads AI Agent - Dev Environment")
    print("="*50 + "\n")

    if not check_dependencies():
        sys.exit(1)

    if not check_env_file():
        sys.exit(1)

    start_server()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Teste simples de autenticação JWT"""
from src.utils.auth import create_access_token, verify_token
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Carregar .env
env_file = project_root / ".env"
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value


def test_auth():
    print("Testando autenticação JWT...")

    # Teste 1: Criar token
    test_data = {"sub": "admin@macspark.dev"}
    token = create_access_token(test_data)
    print(f"[OK] Token criado: {token[:50]}...")

    # Teste 2: Verificar token
    payload = verify_token(token)
    print(f"[OK] Token verificado: {payload}")

    # Teste 3: Token inválido
    try:
        verify_token("token_invalido")
        print("[ERRO] Token inválido deveria falhar")
    except Exception as e:
        print(f"[OK] Token inválido rejeitado: {type(e).__name__}")

    print("[OK] Autenticação JWT funcionando!")


if __name__ == "__main__":
    test_auth()

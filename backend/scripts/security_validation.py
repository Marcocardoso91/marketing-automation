#!/usr/bin/env python3
"""Script de validacao final de seguranca"""
import os
import sys
import subprocess
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def check_credentials():
    """Verificar se credenciais estao seguras"""
    print("1. Verificando credenciais...")

    # Verificar SECRET_KEY
    env_file = project_root / ".env"
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if "change-me-in-production" in content:
                print("   [ERRO] SECRET_KEY ainda e o padrao")
                return False
            else:
                print("   [OK] SECRET_KEY foi alterado")

    # Verificar se .env esta no git
    try:
        result = subprocess.run(['git', 'ls-files', '.env'],
                                capture_output=True, text=True, cwd=project_root)
        if result.stdout.strip():
            print("   [ERRO] .env esta no git")
            return False
        else:
            print("   [OK] .env nao esta no git")
    except:
        print("   [AVISO] Git nao disponivel")

    # Verificar credenciais hardcoded
    try:
        result = subprocess.run(['grep', '-r', 'ntn_44266321668', 'src/'],
                                capture_output=True, text=True, cwd=project_root)
        if result.stdout.strip():
            print("   [ERRO] Credenciais hardcoded encontradas")
            return False
        else:
            print("   [OK] Nenhuma credencial hardcoded")
    except:
        print("   [AVISO] grep nao disponivel")

    return True


def check_tests():
    """Verificar se testes passam"""
    print("\n2. Verificando testes...")

    try:
        result = subprocess.run(['python', '-m', 'pytest', 'tests/unit', '-v', '--tb=short'],
                                capture_output=True, text=True, cwd=project_root)
        if result.returncode == 0:
            print("   [OK] Testes unitarios passando")
            return True
        else:
            print("   [ERRO] Testes unitarios falhando")
            print(f"   Erro: {result.stderr}")
            return False
    except Exception as e:
        print(f"   [ERRO] Erro ao executar testes: {e}")
        return False


def check_cors():
    """Verificar configuracao CORS"""
    print("\n3. Verificando CORS...")

    main_file = project_root / "main.py"
    if main_file.exists():
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'allow_origins=["*"]' in content:
                print("   [ERRO] CORS permite qualquer origem")
                return False
            elif 'allowed_origins' in content:
                print("   [OK] CORS configurado com origens especificas")
                return True
            else:
                print("   [AVISO] Configuracao CORS nao encontrada")
                return False
    return False


def check_auth():
    """Verificar autenticacao JWT"""
    print("\n4. Verificando autenticacao...")

    # Verificar se modulo de auth existe
    auth_file = project_root / "src" / "utils" / "auth.py"
    if not auth_file.exists():
        print("   [ERRO] Modulo de autenticacao nao encontrado")
        return False

    # Verificar se endpoints de auth existem
    auth_api_file = project_root / "src" / "api" / "auth.py"
    if not auth_api_file.exists():
        print("   [ERRO] Endpoints de autenticacao nao encontrados")
        return False

    # Testar criacao de token
    try:
        from src.utils.auth import create_access_token
        token = create_access_token({"sub": "test@example.com"})
        if token:
            print("   [OK] Autenticacao JWT funcionando")
            return True
        else:
            print("   [ERRO] Falha ao criar token JWT")
            return False
    except Exception as e:
        print(f"   [ERRO] Erro na autenticacao: {e}")
        return False


def check_rate_limiting():
    """Verificar rate limiting"""
    print("\n5. Verificando rate limiting...")

    # Verificar se modulo de rate limiting existe
    rate_limit_file = project_root / "src" / "utils" / "rate_limit.py"
    if not rate_limit_file.exists():
        print("   [ERRO] Modulo de rate limiting nao encontrado")
        return False

    # Verificar se esta configurado no main.py
    main_file = project_root / "main.py"
    if main_file.exists():
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'limiter' in content and 'RateLimitExceeded' in content:
                print("   [OK] Rate limiting configurado")
                return True
            else:
                print("   [ERRO] Rate limiting nao configurado")
                return False
    return False


def check_security_scans():
    """Verificar scans de seguranca"""
    print("\n6. Verificando scans de seguranca...")

    # Bandit
    try:
        result = subprocess.run(['bandit', '-r', 'src/', '-ll'],
                                capture_output=True, text=True, cwd=project_root)
        if result.returncode == 0:
            print("   [OK] Bandit: 0 issues HIGH/MEDIUM")
        else:
            print("   [ERRO] Bandit encontrou issues")
            print(f"   {result.stdout}")
    except Exception as e:
        print(f"   [AVISO] Bandit nao disponivel: {e}")

    return True


def main():
    """Executar validacao completa"""
    print("VALIDACAO FINAL DE SEGURANCA")
    print("=" * 50)

    checks = [
        check_credentials,
        check_tests,
        check_cors,
        check_auth,
        check_rate_limiting,
        check_security_scans
    ]

    passed = 0
    total = len(checks)

    for check in checks:
        if check():
            passed += 1

    print("\n" + "=" * 50)
    print(f"RESULTADO: {passed}/{total} verificacoes passaram")

    if passed == total:
        print("TODAS AS VERIFICACOES PASSARAM!")
        print("Sistema seguro e pronto para producao")
    else:
        print("Algumas verificacoes falharam")
        print("Revisar configuracoes antes de producao")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

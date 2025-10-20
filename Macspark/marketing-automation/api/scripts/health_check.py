#!/usr/bin/env python3
"""Script de health check para verificar status do sistema"""
import os
import asyncio
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


async def check_database():
    """Verificar conexão com database"""
    try:
        from src.utils.database import engine
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        return True, "Database conectado"
    except Exception as e:
        return False, f"Database erro: {e}"


async def check_redis():
    """Verificar conexão com Redis"""
    try:
        import redis
        from src.utils.config import settings
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        return True, "Redis conectado"
    except Exception as e:
        return False, f"Redis erro: {e}"


async def check_n8n():
    """Verificar conexão com n8n"""
    try:
        from src.integrations.n8n_manager import N8nWorkflowManager
        n8n = N8nWorkflowManager()
        workflows = await n8n.list_workflows()
        return True, f"n8n conectado ({len(workflows)} workflows)"
    except Exception as e:
        return False, f"n8n erro: {e}"


async def check_facebook_api():
    """Verificar configuração Facebook API"""
    try:
        from src.utils.config import settings
        if not settings.FACEBOOK_ACCESS_TOKEN or settings.FACEBOOK_ACCESS_TOKEN == "your_facebook_access_token":
            return False, "Facebook API não configurado"
        return True, "Facebook API configurado"
    except Exception as e:
        return False, f"Facebook API erro: {e}"


async def main():
    """Executar todos os checks"""
    print("="*50)
    print("HEALTH CHECK - Facebook Ads AI Agent")
    print("="*50 + "\n")

    checks = [
        ("Database (PostgreSQL)", check_database),
        ("Cache (Redis)", check_redis),
        ("Automation (n8n)", check_n8n),
        ("Facebook API", check_facebook_api),
    ]

    results = []
    for name, check_func in checks:
        print(f"Verificando {name}...", end=" ")
        try:
            success, message = await check_func()
            status = "[OK]" if success else "[ERRO]"
            print(f"{status} {message}")
            results.append(success)
        except Exception as e:
            print(f"[ERRO] {e}")
            results.append(False)

    print("\n" + "="*50)
    passed = sum(results)
    total = len(results)
    print(f"RESULTADO: {passed}/{total} checks passaram")

    if passed == total:
        print("STATUS: SISTEMA OPERACIONAL")
        return 0
    else:
        print("STATUS: SISTEMA COM PROBLEMAS")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

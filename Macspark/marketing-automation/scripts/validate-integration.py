#!/usr/bin/env python3
"""
Script de validação da integração.
Verifica todos os componentes do sistema.
"""
import sys
import requests
from datetime import datetime, timedelta


def check_color(passed: bool) -> str:
    """Retorna cor ANSI"""
    return "\033[92m✅\033[0m" if passed else "\033[91m❌\033[0m"


def check_agent_api_health():
    """Verifica se Agent API está rodando"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        passed = response.status_code == 200
        print(f"{check_color(passed)} Agent API Health")
        return passed
    except:
        print(f"{check_color(False)} Agent API Health (not responding)")
        return False


def check_metrics_endpoint():
    """Verifica endpoint de métricas"""
    try:
        response = requests.get("http://localhost:8000/api/v1/metrics/health", timeout=5)
        passed = response.status_code == 200
        print(f"{check_color(passed)} Metrics Endpoint")
        return passed
    except:
        print(f"{check_color(False)} Metrics Endpoint (not responding)")
        return False


def check_shared_package():
    """Verifica se pacote shared está instalado"""
    try:
        from marketing_shared.schemas.facebook_metrics import CampaignMetricSchema
        from marketing_shared.utils.api_client import AgentAPIClient
        print(f"{check_color(True)} Shared Package")
        return True
    except ImportError as e:
        print(f"{check_color(False)} Shared Package ({str(e)})")
        return False


def main():
    print("\n" + "="*50)
    print("🔍 VALIDAÇÃO DE INTEGRAÇÃO")
    print("="*50 + "\n")
    
    results = []
    
    print("📦 Componentes Básicos:")
    results.append(check_shared_package())
    
    print("\n🌐 Serviços:")
    results.append(check_agent_api_health())
    results.append(check_metrics_endpoint())
    
    print("\n" + "="*50)
    passed = sum(results)
    total = len(results)
    print(f"RESULTADO: {passed}/{total} verificações passaram")
    
    if passed == total:
        print("✅ Sistema integrado e funcionando!")
        sys.exit(0)
    else:
        print("❌ Algumas verificações falharam. Veja logs acima.")
        sys.exit(1)


if __name__ == "__main__":
    main()


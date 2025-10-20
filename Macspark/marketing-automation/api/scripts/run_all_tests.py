#!/usr/bin/env python3
"""
Run All Tests - Facebook Ads AI Agent
Executa toda a suite de testes e gera relatório
"""
import subprocess
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_tests():
    """Executa todos os testes"""

    print("=" * 70)
    print(" FACEBOOK ADS AI AGENT - TEST SUITE")
    print("=" * 70)
    print()

    # Test 1: Unit tests (sem integração)
    print("[1/4] Executando testes unitarios...")
    result_unit = subprocess.run([
        "pytest",
        "tests/test_suite_completa.py",
        "-v",
        "-m", "not integration",
        "--tb=short"
    ])

    print()

    # Test 2: Integration tests (com n8n real)
    print("[2/4] Executando testes de integracao...")
    result_integration = subprocess.run([
        "pytest",
        "tests/test_suite_completa.py",
        "-v",
        "-m", "integration",
        "--tb=short"
    ])

    print()

    # Test 3: Connection test (n8n)
    print("[3/4] Testando conexao n8n...")
    result_n8n = subprocess.run([
        "python",
        "scripts/test_n8n_connection.py"
    ])

    print()

    # Test 4: Import test (todos os módulos)
    print("[4/4] Testando imports...")
    result_imports = test_all_imports()

    print()
    print("=" * 70)
    print(" RESUMO DOS TESTES")
    print("=" * 70)

    # Summary
    results = {
        "Testes Unitarios": result_unit.returncode == 0,
        "Testes Integracao": result_integration.returncode == 0,
        "Conexao n8n": result_n8n.returncode == 0,
        "Imports": result_imports
    }

    for test_name, passed in results.items():
        status = "[OK]" if passed else "[FALHOU]"
        print(f"{status} {test_name}")

    print()

    # Overall result
    all_passed = all(results.values())
    if all_passed:
        print("[OK] TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("[ERRO] ALGUNS TESTES FALHARAM")
        return 1


def test_all_imports():
    """Testa se todos os módulos podem ser importados"""

    modules_to_test = [
        # Models
        "src.models.campaign",
        "src.models.insight",
        "src.models.user",
        "src.models.conversation",
        "src.models.suggestion",
        "src.models.audit_log",

        # Schemas
        "src.schemas.campaign_schemas",
        "src.schemas.insight_schemas",
        "src.schemas.chat_schemas",
        "src.schemas.suggestion_schemas",

        # Integrations
        "src.integrations.n8n_client",
        "src.integrations.n8n_manager",
        "src.integrations.notion_client",

        # Agents & Analytics
        "src.agents.facebook_agent",
        "src.analytics.performance_analyzer",
        "src.automation.campaign_optimizer",

        # API
        "src.api.campaigns",
        "src.api.analytics",
        "src.api.automation",
        "src.api.chat",
        "src.api.notion",
        "src.api.n8n_admin",

        # Tasks
        "src.tasks.celery_app",
        "src.tasks.collectors",
        "src.tasks.processors",
        "src.tasks.notifiers",

        # Utils
        "src.utils.config",
        "src.utils.logger",
        "src.utils.database",
        "src.utils.metrics",
        "src.utils.middleware",

        # Main
        "main"
    ]

    failed_imports = []

    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"  [OK] {module_name}")
        except Exception as e:
            print(f"  [ERRO] {module_name}: {e}")
            failed_imports.append(module_name)

    return len(failed_imports) == 0


if __name__ == "__main__":
    sys.exit(run_tests())

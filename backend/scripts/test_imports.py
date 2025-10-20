#!/usr/bin/env python3
"""
Test Imports - Verify P0 #3 and P0 #5 imports

Tests that all updated files can import correctly:
- Redis TokenBlacklist
- Cached Agent

Usage:
    cd api
    python scripts/test_imports.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "shared"))

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def test_import(module_path: str, expected_symbols: list) -> bool:
    """Test if module imports successfully"""
    try:
        parts = module_path.split('.')
        module = __import__(module_path, fromlist=parts[-1:])

        # Check expected symbols
        missing = []
        for symbol in expected_symbols:
            if not hasattr(module, symbol):
                missing.append(symbol)

        if missing:
            print(f"{RED}[FAIL]{RESET} {module_path} - Missing: {', '.join(missing)}")
            return False

        print(f"{GREEN}[OK]{RESET} {module_path}")
        return True
    except ModuleNotFoundError as exc:
        hint = ""
        if exc.name == "marketing_shared":
            hint = " (execute `pip install -e ./shared` na raiz do projeto)"
        print(f"{RED}[FAIL]{RESET} {module_path} - {str(exc)[:80]}{hint}")
        return False
    except Exception as e:
        print(f"{RED}[FAIL]{RESET} {module_path} - {str(e)[:80]}")
        return False


def main():
    print("\n" + "="*60)
    print("  P0 IMPORTS VALIDATION")
    print("="*60 + "\n")

    tests = [
        # P0 #3: Redis TokenBlacklist
        ("src.utils.redis_blacklist", [
            "RedisTokenBlacklist",
            "HybridTokenBlacklist",
            "get_redis_blacklist",
            "token_blacklist_redis"
        ]),

        # P0 #5: Cached Agent
        ("src.utils.agent_cache", [
            "CachedAgentProvider",
            "get_cached_agent_provider",
            "get_facebook_agent"
        ]),

        # Updated files
        ("src.utils.auth", []),  # Just test import
        ("src.api.auth", []),
        ("src.api.metrics", []),
        ("src.api.campaigns", []),
        ("src.api.chat", []),
        ("src.api.analytics", []),
        ("src.api.notion", []),
        ("src.api.automation", []),
        ("src.tasks.collectors", []),
        ("src.tasks.processors", []),
    ]

    results = []
    for module, symbols in tests:
        results.append(test_import(module, symbols))

    # Summary
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0

    if passed == total:
        print(f"{GREEN}ALL IMPORTS PASSED: {passed}/{total} ({percentage:.0f}%){RESET}")
    else:
        print(f"{RED}SOME IMPORTS FAILED: {passed}/{total} ({percentage:.0f}%){RESET}")

    print("="*60 + "\n")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

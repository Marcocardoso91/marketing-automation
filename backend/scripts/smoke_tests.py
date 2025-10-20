#!/usr/bin/env python3
"""
Smoke Tests - Validação Rápida das Implementações P0

Testa:
- P0 #6: Database migrations executadas
- P0 #3: Redis TokenBlacklist funcionando
- P0 #5: Cached Agent funcionando
- Conexão com VPS via SSH tunnel

Usage:
    python scripts/smoke_tests.py
"""
import asyncio
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.logger import setup_logger
from utils.config import settings

logger = setup_logger(__name__)

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_test(name: str, status: str, details: str = ""):
    """Print test result"""
    if status == "PASS":
        symbol = f"{GREEN}[OK]{RESET}"
    elif status == "FAIL":
        symbol = f"{RED}[FAIL]{RESET}"
    elif status == "SKIP":
        symbol = f"{YELLOW}[SKIP]{RESET}"
    else:
        symbol = f"{BLUE}[->]{RESET}"

    print(f"{symbol} {name:<50} {status:<8} {details}")


async def test_database_connection():
    """Test PostgreSQL connection via SSH tunnel"""
    print(f"\n{BLUE}=== P0 #6: Database Setup ==={RESET}")

    try:
        from sqlalchemy import create_engine, text
        from sqlalchemy.ext.asyncio import create_async_engine

        # Test async connection
        engine = create_async_engine(settings.DATABASE_URL, echo=False)

        async with engine.begin() as conn:
            # Test connection
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print_test("Database connection", "PASS", version[:50])

            # Check tables
            result = await conn.execute(text("""
                SELECT COUNT(*) FROM information_schema.tables
                WHERE table_schema = 'public'
            """))
            table_count = result.scalar()
            print_test(f"Tables created", "PASS", f"{table_count} tables")

            # Check alembic version
            result = await conn.execute(text("SELECT version_num FROM alembic_version"))
            migration = result.scalar()
            expected = "002_add_user_auth_fields"
            if migration == expected:
                print_test("Alembic migration", "PASS", migration)
            else:
                print_test("Alembic migration", "FAIL", f"Expected {expected}, got {migration}")

            # Check users table has hashed_password
            result = await conn.execute(text("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name = 'users' AND column_name = 'hashed_password'
            """))
            has_column = result.scalar() is not None
            status = "PASS" if has_column else "FAIL"
            print_test("users.hashed_password exists", status,
                      "Column present" if has_column else "Column missing!")

        await engine.dispose()
        return True

    except Exception as e:
        print_test("Database connection", "FAIL", str(e)[:100])
        logger.error(f"Database test failed: {e}")
        return False


async def test_redis_blacklist():
    """Test Redis TokenBlacklist"""
    print(f"\n{BLUE}=== P0 #3: Redis TokenBlacklist ==={RESET}")

    try:
        from utils.redis_blacklist import RedisTokenBlacklist

        blacklist = RedisTokenBlacklist()
        test_token = f"test_token_{int(time.time())}"
        expiry = datetime.utcnow() + timedelta(seconds=30)

        # Test add
        await blacklist.add(test_token, expiry)
        print_test("Redis add token", "PASS", "Token added with 30s TTL")

        # Test is_blacklisted
        is_blocked = await blacklist.is_blacklisted(test_token)
        status = "PASS" if is_blocked else "FAIL"
        print_test("Redis check blacklisted", status,
                  "Token found" if is_blocked else "Token not found!")

        # Test remove
        removed = await blacklist.remove(test_token)
        status = "PASS" if removed else "FAIL"
        print_test("Redis remove token", status,
                  "Token removed" if removed else "Failed to remove")

        # Verify removal
        still_blocked = await blacklist.is_blacklisted(test_token)
        status = "PASS" if not still_blocked else "FAIL"
        print_test("Redis verify removal", status,
                  "Token gone" if not still_blocked else "Token still there!")

        await blacklist.close()
        return True

    except Exception as e:
        print_test("Redis blacklist", "FAIL", str(e)[:100])
        logger.error(f"Redis test failed: {e}")
        return False


def test_cached_agent():
    """Test Cached FacebookAdsAgent"""
    print(f"\n{BLUE}=== P0 #5: Cached Agent ==={RESET}")

    try:
        from utils.agent_cache import get_cached_agent_provider

        provider = get_cached_agent_provider()

        # First call (cold start)
        start = time.time()
        agent1 = provider.get_agent()
        time1 = (time.time() - start) * 1000
        print_test("Agent cache - cold start", "INFO", f"{time1:.1f}ms")

        # Second call (should be cached)
        start = time.time()
        agent2 = provider.get_agent()
        time2 = (time.time() - start) * 1000

        is_cached = agent1 is agent2  # Same instance?
        status = "PASS" if is_cached else "FAIL"
        print_test("Agent cache - warm hit", status,
                  f"{time2:.1f}ms (same instance)" if is_cached
                  else f"{time2:.1f}ms (different instance!)")

        # Performance improvement
        if time1 > 10 and time2 < 1:
            improvement = ((time1 - time2) / time1) * 100
            print_test("Cache performance", "PASS", f"{improvement:.0f}% faster")

        # Check stats
        stats = provider.get_stats()
        print_test("Cache stats", "PASS",
                  f"cached={stats['cached']}, age={stats.get('cache_age_seconds', 0):.1f}s")

        return True

    except Exception as e:
        print_test("Cached agent", "FAIL", str(e)[:100])
        logger.error(f"Cached agent test failed: {e}")
        return False


async def test_ssh_tunnel():
    """Test SSH tunnel status"""
    print(f"\n{BLUE}=== Infrastructure ==={RESET}")

    try:
        import socket

        # Check if port 5433 is listening (SSH tunnel)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', 5433))
        sock.close()

        is_open = result == 0
        status = "PASS" if is_open else "WARN"
        msg = "Port listening" if is_open else "Port not open (tunnel down?)"
        print_test("SSH tunnel (port 5433)", status, msg)

        # Check Redis port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', 6379))
        sock.close()

        is_open = result == 0
        status = "PASS" if is_open else "WARN"
        msg = "Redis available" if is_open else "Redis not running"
        print_test("Redis (port 6379)", status, msg)

        return True

    except Exception as e:
        print_test("Infrastructure check", "FAIL", str(e)[:100])
        return False


async def main():
    """Run all smoke tests"""
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}  SMOKE TESTS - P0 Implementations Validation{RESET}")
    print(f"{BLUE}{'='*70}{RESET}")
    print(f"\nEnvironment: {settings.ENVIRONMENT}")
    print(f"Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'N/A'}")
    print(f"Redis: {settings.REDIS_URL}")

    results = []

    # Infrastructure checks
    results.append(await test_ssh_tunnel())

    # P0 tests
    results.append(await test_database_connection())
    results.append(await test_redis_blacklist())
    results.append(test_cached_agent())

    # Summary
    print(f"\n{BLUE}{'='*70}{RESET}")
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0

    if passed == total:
        color = GREEN
        status = "ALL TESTS PASSED"
    elif passed >= total * 0.75:
        color = YELLOW
        status = "MOST TESTS PASSED"
    else:
        color = RED
        status = "TESTS FAILED"

    print(f"{color}{status}: {passed}/{total} ({percentage:.0f}%){RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

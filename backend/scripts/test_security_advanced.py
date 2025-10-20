#!/usr/bin/env python3
"""Teste avançado de segurança"""
from src.utils.security import (
    SecurityHeaders,
    RequestValidator,
    PasswordValidator,
    APIKeyGenerator,
    TokenBlacklist
)
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_security_headers():
    """Testar security headers"""
    print("1. Testando Security Headers...")
    headers = SecurityHeaders.get_headers()

    required_headers = [
        "X-Frame-Options",
        "X-Content-Type-Options",
        "X-XSS-Protection",
        "Content-Security-Policy",
        "Strict-Transport-Security"
    ]

    for header in required_headers:
        if header in headers:
            print(f"   [OK] {header}: {headers[header][:50]}...")
        else:
            print(f"   [ERRO] {header} não encontrado")
            return False

    return True


def test_password_validator():
    """Testar validador de senha"""
    print("\n2. Testando Password Validator...")

    test_cases = [
        ("123", False, "Senha muito curta"),
        ("abcdefgh", False, "Sem maiúscula/número/especial"),
        ("Abcdefgh", False, "Sem número/especial"),
        ("Abcdefgh1", False, "Sem caractere especial"),
        ("Abcdefgh1!", True, "Senha forte"),
    ]

    for password, should_pass, desc in test_cases:
        is_valid, message = PasswordValidator.validate_password_strength(
            password)
        expected = "[OK]" if should_pass else "[ESPERADO]"
        result = "[OK]" if is_valid == should_pass else "[ERRO]"
        print(f"   {result} {desc}: {message}")

    return True


def test_api_key_generator():
    """Testar gerador de API keys"""
    print("\n3. Testando API Key Generator...")

    key1 = APIKeyGenerator.generate_api_key()
    key2 = APIKeyGenerator.generate_api_key()

    if key1 != key2:
        print(f"   [OK] Keys únicas geradas")
        print(f"   [OK] Key1: {key1[:20]}...")
        print(f"   [OK] Key2: {key2[:20]}...")
    else:
        print(f"   [ERRO] Keys idênticas geradas")
        return False

    # Testar hash
    hash1 = APIKeyGenerator.hash_api_key(key1)
    hash2 = APIKeyGenerator.hash_api_key(key1)

    if hash1 == hash2:
        print(f"   [OK] Hash consistente: {hash1[:20]}...")
    else:
        print(f"   [ERRO] Hash inconsistente")
        return False

    return True


def test_token_blacklist():
    """Testar blacklist de tokens"""
    print("\n4. Testando Token Blacklist...")

    from datetime import datetime, timedelta
    blacklist = TokenBlacklist()

    test_token = "test_token_12345"
    expiry = datetime.utcnow() + timedelta(minutes=30)

    # Adicionar token
    blacklist.add(test_token, expiry)

    # Verificar se está blacklisted
    if blacklist.is_blacklisted(test_token):
        print(f"   [OK] Token adicionado ao blacklist")
    else:
        print(f"   [ERRO] Token não está no blacklist")
        return False

    # Verificar token diferente
    if not blacklist.is_blacklisted("outro_token"):
        print(f"   [OK] Outros tokens não afetados")
    else:
        print(f"   [ERRO] Falso positivo no blacklist")
        return False

    return True


def test_request_validator():
    """Testar validador de request"""
    print("\n5. Testando Request Validator...")

    # Testar sanitização
    dirty_string = "  test\x00string  "
    clean = RequestValidator.sanitize_string(dirty_string)

    if clean == "teststring":
        print(f"   [OK] String sanitizada corretamente")
    else:
        print(f"   [ERRO] Sanitização falhou: '{clean}'")
        return False

    # Testar limite de tamanho
    long_string = "a" * 2000
    truncated = RequestValidator.sanitize_string(long_string, max_length=100)

    if len(truncated) == 100:
        print(f"   [OK] String truncada corretamente")
    else:
        print(f"   [ERRO] Truncamento falhou: {len(truncated)}")
        return False

    return True


def main():
    """Executar todos os testes"""
    print("="*50)
    print("TESTE AVANCADO DE SEGURANCA")
    print("="*50 + "\n")

    tests = [
        test_security_headers,
        test_password_validator,
        test_api_key_generator,
        test_token_blacklist,
        test_request_validator,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "="*50)
    print(f"RESULTADO: {passed}/{total} testes passaram")

    if passed == total:
        print("TODOS OS TESTES DE SEGURANCA AVANCADA PASSARAM!")
    else:
        print("Alguns testes falharam")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

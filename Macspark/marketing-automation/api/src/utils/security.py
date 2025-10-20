"""Security utilities - Advanced security features"""
import secrets
import hashlib
from typing import Optional
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class SecurityHeaders:
    """Add security headers to responses"""

    @staticmethod
    def get_headers() -> dict:
        """Get recommended security headers"""
        return {
            # Prevent clickjacking
            "X-Frame-Options": "DENY",

            # Prevent MIME type sniffing
            "X-Content-Type-Options": "nosniff",

            # Enable XSS protection
            "X-XSS-Protection": "1; mode=block",

            # Referrer policy
            "Referrer-Policy": "strict-origin-when-cross-origin",

            # Permissions policy
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",

            # Content Security Policy
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self'; "
                "frame-ancestors 'none';"
            ),

            # HSTS (HTTP Strict Transport Security)
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        }


class RequestValidator:
    """Validate and sanitize requests"""

    @staticmethod
    def validate_request_size(request: Request, max_size: int = 10_485_760) -> bool:
        """
        Validate request size (default 10MB)

        Args:
            request: FastAPI request
            max_size: Maximum size in bytes

        Returns:
            True if valid, raises HTTPException if too large
        """
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > max_size:
            logger.warning(f"Request too large: {content_length} bytes")
            raise HTTPException(
                status_code=413,
                detail=f"Request too large. Maximum size: {max_size} bytes"
            )
        return True

    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """
        Sanitize string input

        Args:
            value: Input string
            max_length: Maximum allowed length

        Returns:
            Sanitized string
        """
        # Remove null bytes
        value = value.replace('\x00', '')

        # Limit length
        if len(value) > max_length:
            value = value[:max_length]

        # Strip whitespace
        value = value.strip()

        return value


class TokenBlacklist:
    """Simple in-memory token blacklist (use Redis in production)"""

    def __init__(self):
        self._blacklist = set()
        self._cleanup_times = {}

    def add(self, token: str, expiry: datetime):
        """Add token to blacklist"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        self._blacklist.add(token_hash)
        self._cleanup_times[token_hash] = expiry
        logger.info(f"Token added to blacklist (expires: {expiry})")

    def is_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        # Clean up expired tokens
        self._cleanup_expired()

        return token_hash in self._blacklist

    def _cleanup_expired(self):
        """Remove expired tokens from blacklist"""
        now = datetime.utcnow()
        expired = [
            token for token, expiry in self._cleanup_times.items()
            if expiry < now
        ]
        for token in expired:
            self._blacklist.discard(token)
            del self._cleanup_times[token]


class PasswordValidator:
    """Password strength validation"""

    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """
        Validate password strength

        Args:
            password: Password to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters"

        if len(password) > 128:
            return False, "Password must be less than 128 characters"

        # Check for uppercase
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"

        # Check for lowercase
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"

        # Check for digit
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"

        # Check for special character
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            return False, "Password must contain at least one special character"

        return True, "Password is strong"


class APIKeyGenerator:
    """Generate secure API keys"""

    @staticmethod
    def generate_api_key(prefix: str = "fbads", length: int = 32) -> str:
        """
        Generate a secure API key

        Args:
            prefix: Key prefix
            length: Length of random part

        Returns:
            API key in format: prefix_randomstring
        """
        random_part = secrets.token_urlsafe(length)
        return f"{prefix}_{random_part}"

    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """
        Hash API key for storage

        Args:
            api_key: API key to hash

        Returns:
            SHA256 hash of the key
        """
        return hashlib.sha256(api_key.encode()).hexdigest()


# Global instances
token_blacklist = TokenBlacklist()
security_headers = SecurityHeaders()
request_validator = RequestValidator()
password_validator = PasswordValidator()
api_key_generator = APIKeyGenerator()

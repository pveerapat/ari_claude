"""P2-5: unit tests for auth utilities (phone normalization, password, JWT)."""

import time
from datetime import timedelta

import pytest
from jose import JWTError

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    normalize_phone,
    verify_password,
)
from app.core.config import settings


class TestPhoneNormalization:
    def test_strips_spaces(self):
        assert normalize_phone("081 234 5678") == "0812345678"

    def test_strips_dashes(self):
        assert normalize_phone("081-234-5678") == "0812345678"

    def test_strips_parentheses(self):
        assert normalize_phone("(081) 2345678") == "0812345678"

    def test_strips_dots(self):
        assert normalize_phone("081.234.5678") == "0812345678"

    def test_strips_leading_trailing_whitespace(self):
        assert normalize_phone("  0812345678  ") == "0812345678"

    def test_preserves_plus_prefix(self):
        assert normalize_phone("+66812345678") == "+66812345678"

    def test_plain_number_unchanged(self):
        assert normalize_phone("0812345678") == "0812345678"


class TestPasswordHashing:
    def test_hash_produces_string(self):
        h = hash_password("secret123")
        assert isinstance(h, str)
        assert len(h) > 0

    def test_hash_is_not_plaintext(self):
        h = hash_password("secret123")
        assert h != "secret123"

    def test_different_calls_produce_different_hashes(self):
        # bcrypt generates a unique salt each call
        h1 = hash_password("same_password")
        h2 = hash_password("same_password")
        assert h1 != h2

    def test_verify_correct_password(self):
        h = hash_password("correct")
        assert verify_password("correct", h) is True

    def test_verify_wrong_password(self):
        h = hash_password("correct")
        assert verify_password("wrong", h) is False

    def test_verify_empty_password_fails(self):
        h = hash_password("nonempty")
        assert verify_password("", h) is False


class TestJWTCreation:
    def test_create_access_token_returns_string(self):
        token = create_access_token("user-id", "org-id", "farmer")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_refresh_token_returns_string(self):
        token = create_refresh_token("user-id")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_access_and_refresh_tokens_differ(self):
        access = create_access_token("user-id", "org-id", "farmer")
        refresh = create_refresh_token("user-id")
        assert access != refresh


class TestJWTDecode:
    def test_decode_valid_access_token(self):
        token = create_access_token("uid-123", "org-456", "farmer")
        payload = decode_token(token)
        assert payload["sub"] == "uid-123"
        assert payload["organization_id"] == "org-456"
        assert payload["role"] == "farmer"
        assert payload["type"] == "access"

    def test_decode_valid_refresh_token(self):
        token = create_refresh_token("uid-789")
        payload = decode_token(token)
        assert payload["sub"] == "uid-789"
        assert payload["type"] == "refresh"

    def test_decode_invalid_token_raises(self):
        with pytest.raises(JWTError):
            decode_token("not.a.valid.token")

    def test_decode_tampered_token_raises(self):
        token = create_access_token("uid", "org", "farmer")
        tampered = token[:-5] + "XXXXX"
        with pytest.raises(JWTError):
            decode_token(tampered)

    def test_decode_expired_token_raises(self):
        from datetime import datetime, timezone
        from jose import jwt

        expired_payload = {
            "sub": "uid",
            "type": "access",
            "exp": datetime.now(timezone.utc) - timedelta(seconds=1),
        }
        expired_token = jwt.encode(
            expired_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        with pytest.raises(JWTError):
            decode_token(expired_token)

    def test_decode_wrong_secret_raises(self):
        from jose import jwt

        token = jwt.encode(
            {"sub": "uid", "exp": 9999999999},
            "wrong_secret",
            algorithm=settings.JWT_ALGORITHM,
        )
        with pytest.raises(JWTError):
            decode_token(token)

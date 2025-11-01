"""
Tests for security modules
"""
import pytest
import os


def test_integrity_checker_import():
    """Test that integrity_checker module can be imported"""
    from src.utils.integrity_checker import IntegrityChecker
    assert IntegrityChecker is not None


def test_path_validator_import():
    """Test that path_validator module can be imported"""
    from src.utils.path_validator import PathValidator
    assert PathValidator is not None


def test_log_sanitizer_import():
    """Test that log_sanitizer module can be imported"""
    from src.utils.log_sanitizer import LogSanitizer
    assert LogSanitizer is not None


def test_backup_manager_import():
    """Test that backup_manager module can be imported"""
    from src.utils.backup_manager import BackupManager
    assert BackupManager is not None


def test_elevation_import():
    """Test that elevation module can be imported"""
    from src.utils.elevation import is_admin, SecurityError
    assert is_admin is not None
    assert SecurityError is not None


def test_log_sanitizer_basic():
    """Test basic log sanitization"""
    from src.utils.log_sanitizer import LogSanitizer
    
    # Test user path sanitization
    test_path = r"C:\Users\JohnDoe\Documents\file.txt"
    sanitized = LogSanitizer.sanitize(test_path)
    assert "JohnDoe" not in sanitized
    assert "***" in sanitized


def test_path_validator_basic():
    """Test basic path validation"""
    from src.utils.path_validator import PathValidator
    
    # Test junction point detection (should not crash)
    result = PathValidator.is_junction_point(r"C:\Windows\Temp")
    assert isinstance(result, bool)


def test_integrity_checker_hash():
    """Test hash calculation"""
    from src.utils.integrity_checker import IntegrityChecker
    import tempfile
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
        f.write("test content")
        temp_path = f.name
    
    try:
        # Calculate hash
        hash_value = IntegrityChecker.calculate_sha256(temp_path)
        assert hash_value is not None
        assert len(hash_value) == 64  # SHA256 is 64 hex characters
    finally:
        os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

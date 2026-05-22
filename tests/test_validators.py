"""
Unit tests for network-audit validators.
Run: python3 -m pytest tests/ -v
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils import validate_target

def test_valid_ipv4():
    assert validate_target("192.168.1.1") is True

def test_valid_cidr():
    assert validate_target("192.168.1.0/24") is True

def test_valid_hostname():
    assert validate_target("example.com") is True

def test_invalid_empty():
    assert validate_target("") is False

def test_invalid_too_long():
    assert validate_target("a" * 300) is False

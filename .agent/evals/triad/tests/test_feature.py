
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import feature_challenge

def test_anonymize_logic():
    svc = feature_challenge.UserService()
    
    # Action
    result = svc.anonymize_user(1)
    
    # Assert
    assert result is True, "FAIL: Function returned False"
    
    user = svc.get_user(1)
    assert user["name"] == "Anonymized User", "FAIL: Name not masked"
    assert user["email"] == "deleted@anonymized.local", "FAIL: Email not masked"
    assert user["data"] is None or user["data"] == "", "FAIL: Sensitive data not cleared"

def test_audit_log_format():
    svc = feature_challenge.UserService()
    svc.anonymize_user(2)
    
    logs = svc.get_logs()
    assert len(logs) == 1, "FAIL: No audit log created"
    
    entry = logs[0]
    assert entry["action"] == "ANONYMIZE"
    assert entry["user_id"] == 2
    assert "timestamp" in entry

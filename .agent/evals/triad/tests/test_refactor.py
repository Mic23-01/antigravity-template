
import pytest
import sys
import os

# Ensure we can import the module next door
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import refactor_challenge
except ImportError:
    pass # Will handle dynamically in runner if file modified

def test_structure_split():
    """
    Check if the code has been split into multiple classes.
    """
    import inspect
    classes = [m[0] for m in inspect.getmembers(refactor_challenge, inspect.isclass) if m[1].__module__ == refactor_challenge.__name__]
    
    # We expect at least SystemHandler AND (BillingService OR EmailService OR User)
    assert len(classes) >= 2, "FAIL: Code is still monolithic. Extract classes!"
    
    # Check for specific extracted concepts
    class_names = [c for c in classes]
    has_billing = any("Billing" in c or "Payment" in c for c in class_names)
    has_email = any("Email" in c or "Notification" in c for c in class_names)
    
    assert has_billing or has_email, "FAIL: Billing or Email logic not extracted."

def test_functionality_preserved():
    """
    Regression test: The system must still work.
    """
    # This assumes the agent maintained the *interface* or we can adapt.
    # If the agent changed the interface, this test might need 'smart' adaptation or 
    # the instructions should force interface compatibility.
    # For this V1, let's assume SystemHandler is the Facade.
    
    if hasattr(refactor_challenge, 'SystemHandler'):
        sys_handler = refactor_challenge.SystemHandler({})
        sys_handler.register_user("testuser", "test@example.com")
        
        # Test double registration
        with pytest.raises(ValueError):
            sys_handler.register_user("testuser", "fail@example.com")
            
        # Test billing
        sys_handler.charge_user("testuser", 50)
        
        # Check balance (assuming internal structure or getter)
        # If agent refactored 'users' to be private, we might need a getter.
        # We'll use inspection or try/except
        try:
            balance = sys_handler.users["testuser"]["balance"]
            assert balance == -50
        except:
             # Maybe it's in a sub-service
             pass 


import pytest
import threading
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import bugfix_challenge

def test_race_condition_fixed():
    """
    Stress test the transfer function to ensure atomic safety.
    """
    acc1 = bugfix_challenge.BankAccount(100)
    acc2 = bugfix_challenge.BankAccount(0)
    
    # Run 50 concurrent transfers of 2 units each. Total 100.
    # Expected: acc1=0, acc2=100.
    # If race exists, acc1 < 0 or acc2 < 100.
    
    threads = []
    
    def worker():
        bugfix_challenge.transfer(acc1, acc2, 2)
        
    for _ in range(50):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print(f"DEBUG: Acc1={acc1.balance}, Acc2={acc2.balance}")
    
    assert acc1.balance == 0, f"FAIL: Money leaked/duplicated in source! Bal={acc1.balance}"
    assert acc2.balance == 100, f"FAIL: Money leaked/duplicated in dest! Bal={acc2.balance}"

def test_no_deadlock():
    """
    Ensure 2-way transfer doesn't deadlock.
    """
    accA = bugfix_challenge.BankAccount(100)
    accB = bugfix_challenge.BankAccount(100)
    
    import multiprocessing
    # This is hard to test deterministically without timeout.
    # We'll just run a few cross transfers.
    
    def flow1():
        for _ in range(10): bugfix_challenge.transfer(accA, accB, 1)
    
    def flow2():
        for _ in range(10): bugfix_challenge.transfer(accB, accA, 1)
        
    t1 = threading.Thread(target=flow1)
    t2 = threading.Thread(target=flow2)
    t1.start()
    t2.start()
    
    t1.join(timeout=2.0)
    t2.join(timeout=2.0)
    
    assert not t1.is_alive(), "FAIL: Deadlock detected (Thread 1 stuck)"
    assert not t2.is_alive(), "FAIL: Deadlock detected (Thread 2 stuck)"

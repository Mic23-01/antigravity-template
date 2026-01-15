
# E12: Bugfix Challenge Target
# This file contains a race condition in the transfer method.
# The agent needs to use locks to fix it.

import threading
import time

class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
        
    def deposit(self, amount):
        current = self.balance
        time.sleep(0.001) # Simulate IO
        self.balance = current + amount
        
    def withdraw(self, amount):
        current = self.balance
        time.sleep(0.001) # Simulate IO
        if current >= amount:
            self.balance = current - amount
            return True
        return False

def transfer(acc_from, acc_to, amount):
    # BUG: This is not atomic safe!
    # If two threads transfer at same time, money disappears or duplicates.
    if acc_from.withdraw(amount):
        acc_to.deposit(amount)

# Test Harness (Embedded for simplicity, usually in tests/)
def run_race_test():
    acc1 = BankAccount(100)
    acc2 = BankAccount(0)
    
    threads = []
    for _ in range(10):
        t = threading.Thread(target=transfer, args=(acc1, acc2, 10))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print(f"Final Balances: {acc1.balance}, {acc2.balance}")
    # Expected: 0, 100.
    # Buggy Result: Often < 100 total due to race in withdraw/deposit reading stale state.

if __name__ == "__main__":
    run_race_test()

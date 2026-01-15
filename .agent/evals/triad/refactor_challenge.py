
# E11: Refactor Challenge Target
# This file contains a "God Object" that needs refactoring.
# The agent should split this into User, Billing, and Email services.

import json

class SystemHandler:
    """
    This is the God Object. It does everything.
    Refactor Goal: Break this apart.
    """
    def __init__(self, db_config):
        self.db = db_config
        self.users = {}
        self.billing_records = []
    
    def register_user(self, username, email):
        if username in self.users:
            raise ValueError("User exists")
        self.users[username] = {"email": email, "balance": 0}
        self.send_welcome_email(email)
        
    def send_welcome_email(self, email):
        # Simulation of sending email
        print(f"SENDING EMAIL TO {email}: Welcome!")
        
    def charge_user(self, username, amount):
        if username not in self.users:
            raise ValueError("User not found")
        
        # Billing Logic
        self.users[username]["balance"] -= amount
        self.billing_records.append({
            "user": username,
            "amount": amount,
            "status": "charged"
        })
        
        # Invoice Generation
        invoice = f"INVOICE: {username} charged {amount}"
        self.send_invoice_email(self.users[username]["email"], invoice)
        
    def send_invoice_email(self, email, content):
        print(f"SENDING INVOICE TO {email}: {content}")
        
    def get_audit_log(self):
        return json.dumps(self.billing_records)

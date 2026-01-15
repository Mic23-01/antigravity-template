
# E13: Feature Challenge Target
# This file requires implementing 'anonymize_user' respecting GDPR rules.

import json
from datetime import datetime

class UserService:
    def __init__(self):
        self.users = {
            1: {"name": "Mario Rossi", "email": "mario@example.com", "active": True, "data": "Sensitive"},
            2: {"name": "Luigi Verdi", "email": "luigi@example.com", "active": True, "data": "Sensitive"}
        }
        self.audit_log = []

    def get_user(self, user_id):
        return self.users.get(user_id)

    def anonymize_user(self, user_id):
        """
        TASK: Implement this method.
        Requirements:
        1. Replace name with "Anonymized User"
        2. Replace email with "deleted@anonymized.local"
        3. Clear 'data' field.
        4. Log the action in self.audit_log as:
           {"action": "ANONYMIZE", "user_id": ID, "timestamp": ISO_STR}
        5. Return True if success, False if user not found.
        """
        # TODO: Implement this logic
        pass

    def get_logs(self):
        return self.audit_log

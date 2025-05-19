import csv
from datetime import datetime

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role
        self.login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.actions = []

    def record_action(self, action):
        self.actions.append(action)

    def get_log_data(self):
        return {
            'Username': self.username,
            'Role': self.role,
            'Login Time': self.login_time,
            'Actions': "; ".join(self.actions) if self.actions else "None"
        }


# Subclasses for each role
class Admin(User):
    def __init__(self, username):
        super().__init__(username, "admin")


class Clinician(User):
    def __init__(self, username):
        super().__init__(username, "clinician")


class Nurse(User):
    def __init__(self, username):
        super().__init__(username, "nurse")


class Management(User):
    def __init__(self, username):
        super().__init__(username, "management")


# Credential verification
def authenticate_user(credentials_file, input_username, input_password):

    try:
        with open(credentials_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == input_username and row['password'] == input_password:
                    role = row['role'].strip().lower()
                    if role == "admin":
                        return Admin(input_username)
                    elif role == "clinician":
                        return Clinician(input_username)
                    elif role == "nurse":
                        return Nurse(input_username)
                    elif role == "management":
                        return Management(input_username)
        return None
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None
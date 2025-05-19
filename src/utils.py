import csv
import uuid
from datetime import datetime


def generate_unique_id():
    """
    Generates a unique ID using UUID4.
    """
    return str(uuid.uuid4())


def load_notes(file_path):
    notes_dict = {}
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row['Patient_ID'], row['Visit_ID'])  # updated here
                note = {
                    "Note_ID": row["Note_ID"],
                    "Note_text": row["Note_text"]
                }
                if key not in notes_dict:
                    notes_dict[key] = []
                notes_dict[key].append(note)
    except Exception as e:
        print(f"Error loading notes: {e}")
    return notes_dict



def validate_date_format(date_str):

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def save_usage_log(log_path, user, success=True, failed_reason=None):

    try:
        fieldnames = ["Username", "Role", "Login Time", "Actions", "Status", "Reason"]
        log_entry = user.get_log_data() if user else {
            "Username": "Unknown",
            "Role": "Unknown",
            "Login Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Actions": "None"
        }

        log_entry["Status"] = "Success" if success else "Failed"
        log_entry["Reason"] = failed_reason if not success else "N/A"


        try:
            with open(log_path, mode='r', encoding='utf-8') as testfile:
                header_exists = bool(testfile.readline().strip())
        except FileNotFoundError:
            header_exists = False

        with open(log_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not header_exists:
                writer.writeheader()
            writer.writerow(log_entry)
    except Exception as e:
        print(f"Error writing usage log: {e}")
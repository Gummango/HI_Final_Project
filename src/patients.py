import csv
import uuid
from datetime import datetime


class Note:
    def __init__(self, note_id, note_type, note_text, visit_date):
        self.note_id = note_id
        self.note_type = note_type
        self.note_text = note_text
        self.visit_date = visit_date


class Visit:
    def __init__(self, visit_id, visit_time, department, age, gender, race, ethnicity, insurance, zip_code, chief_complaint):
        self.visit_id = visit_id
        self.visit_time = visit_time
        self.department = department
        self.age = age
        self.gender = gender
        self.race = race
        self.ethnicity = ethnicity
        self.insurance = insurance
        self.zip_code = zip_code
        self.chief_complaint = chief_complaint
        self.notes = []

    def to_dict(self, patient_id):
        return {
            "Patient_ID": patient_id,
            "Visit_ID": self.visit_id,
            "Visit_time": self.visit_time,
            "Visit_department": self.department,
            "Age": self.age,
            "Gender": self.gender,
            "Race": self.race,
            "Ethnicity": self.ethnicity,
            "Insurance": self.insurance,
            "Zip_code": self.zip_code,
            "Chief_complaint": self.chief_complaint
        }


class Patient:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.visits = []

    def add_visit(self, visit):
        self.visits.append(visit)

    def most_recent_visit(self):
        def parse_date_safe(visit):
            try:
                return datetime.strptime(visit.visit_time, "%m/%d/%Y")
            except ValueError:
                return datetime.min

        return max(self.visits, key=parse_date_safe) if self.visits else None


class PatientDatabase:
    def __init__(self):
        self.patients = {}

    def load_from_csv(self, file_path):
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        patient_id = row["Patient_ID"]
                        visit = Visit(
                            row["Visit_ID"],
                            row["Visit_time"],
                            row["Visit_department"],
                            row["Age"],
                            row["Gender"],
                            row["Race"],
                            row["Ethnicity"],
                            row["Insurance"],
                            row.get("Zip_code") or row.get("Zip code"),
                            row.get("Chief_complaint") or row.get("Chief complaint")
                        )

                        if patient_id not in self.patients:
                            self.patients[patient_id] = Patient(patient_id)

                        self.patients[patient_id].add_visit(visit)
                        print(f"Loading patient: {patient_id}")
                        print(f"Visit created: {visit.__dict__}")

                    except Exception as e:
                        print(f"Error creating visit for patient {row.get('Patient_ID', '?')}: {e}")
        except Exception as e:
            print(f"Error reading patient data: {e}")

    def save_to_csv(self, file_path):
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                fieldnames = [
                    "Patient_ID", "Visit_ID", "Visit_time", "Visit_department", "Age",
                    "Gender", "Race", "Ethnicity", "Insurance", "Zip_code", "Chief_complaint"
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for patient in self.patients.values():
                    for visit in patient.visits:
                        writer.writerow(visit.to_dict(patient.patient_id))
        except Exception as e:
            print(f"Error saving patient data: {e}")

    def add_patient_visit(self, patient_id, visit_data):
        visit = Visit(
            str(uuid.uuid4()), visit_data["Visit_time"], visit_data["Visit_department"],
            visit_data["Age"], visit_data["Gender"], visit_data["Race"],
            visit_data["Ethnicity"], visit_data["Insurance"], visit_data["Zip_code"],
            visit_data["Chief_complaint"]
        )
        if patient_id not in self.patients:
            self.patients[patient_id] = Patient(patient_id)
        self.patients[patient_id].add_visit(visit)

    def remove_patient(self, patient_id):
        return self.patients.pop(patient_id, None)

    def get_patient(self, patient_id):
        return self.patients.get(patient_id, None)

    def count_visits_on_date(self, date_str):
        count = 0
        for patient in self.patients.values():
            for visit in patient.visits:
                if visit.visit_time == date_str:
                    count += 1
        return count
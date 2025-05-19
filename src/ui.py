import tkinter as tk
from tkinter import messagebox
from users import authenticate_user
from utils import save_usage_log
import os
from stats import (
    plot_visit_trends,
    plot_insurance_distribution,
    plot_demographics_by_age,
)


class HospitalApp:
    def __init__(self, root, patient_db, notes_data):
        self.root = root
        self.root.title("Hospital Clinical Data Warehouse")
        self.root.minsize(300, 300)
        self.patient_db = patient_db
        self.notes_data = notes_data
        self.user = None  # Will hold the logged-in user

        self.show_login_screen()

    def show_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Login", font=("Helvetica", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.validate_login).pack(pady=10)

    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        credentials_path = os.path.join("data", "Credentials.csv")
        user = authenticate_user(credentials_path, username, password)

        if user:
            self.user = user
            save_usage_log("Usage_Log.csv", user, success=True)
            self.show_role_dashboard()
        else:
            save_usage_log("Usage_Log.csv", None, success=False, failed_reason="Invalid credentials")
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def view_note_ui(self):
        self.user.record_action("View Note")
        tk.messagebox.showinfo("Coming Soon", "View Note feature will be implemented soon.")

    def generate_stats_ui(self):
        self.user.record_action("Generate Stats")
        tk.messagebox.showinfo("Coming Soon", "Statistics feature will be implemented soon.")

    def show_role_dashboard(self):
        self.clear_screen()

        role = self.user.role
        tk.Label(self.root, text=f"Welcome, {self.user.username} ({role})", font=("Helvetica", 14)).pack(pady=10)

        if role in ["nurse", "clinician"]:
            tk.Button(self.root, text="Add Patient", command=self.add_patient_ui).pack(pady=5)
            tk.Button(self.root, text="Remove Patient", command=self.remove_patient_ui).pack(pady=5)
            tk.Button(self.root, text="Retrieve Patient", command=self.retrieve_patient_ui).pack(pady=5)
            tk.Button(self.root, text="Count Visits", command=self.count_visits_ui).pack(pady=5)
            tk.Button(self.root, text="View Note", command=self.view_note_ui).pack(pady=5)

        elif role == "admin":
            tk.Button(self.root, text="Count Visits", command=self.count_visits_ui).pack(pady=5)

        elif role == "management":
            tk.Button(self.root, text="Generate Key Statistics", command=self.generate_stats_ui).pack(pady=5)

        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def add_patient_ui(self):
        self.clear_screen()
        self.user.record_action("Add Patient")

        tk.Label(self.root, text="Add Patient Visit", font=("Helvetica", 14)).pack(pady=10)

        # Patient ID (either existing or new)
        tk.Label(self.root, text="Patient ID").pack()
        patient_id_entry = tk.Entry(self.root)
        patient_id_entry.pack()

        # Visit Date
        tk.Label(self.root, text="Visit Date (MM/DD/YYYY)").pack()
        visit_date_entry = tk.Entry(self.root)
        visit_date_entry.pack()

        # Department
        tk.Label(self.root, text="Visit Department").pack()
        dept_entry = tk.Entry(self.root)
        dept_entry.pack()

        # Age
        tk.Label(self.root, text="Age").pack()
        age_entry = tk.Entry(self.root)
        age_entry.pack()

        # Gender
        tk.Label(self.root, text="Gender").pack()
        gender_var = tk.StringVar()
        gender_options = ["Male", "Female", "Non-binary"]
        tk.OptionMenu(self.root, gender_var, *gender_options).pack()

        # Race
        tk.Label(self.root, text="Race").pack()
        race_var = tk.StringVar()
        race_options = ["White", "Black", "Asian", "Pacific islanders", "Native Americans", "Unknown"]
        tk.OptionMenu(self.root, race_var, *race_options).pack()

        # Ethnicity
        tk.Label(self.root, text="Ethnicity").pack()
        eth_var = tk.StringVar()
        eth_options = ["Hispanic", "Non-Hispanic", "Other", "Unknown"]
        tk.OptionMenu(self.root, eth_var, *eth_options).pack()

        # Insurance
        tk.Label(self.root, text="Insurance").pack()
        ins_entry = tk.Entry(self.root)
        ins_entry.pack()

        # Zip code
        tk.Label(self.root, text="Zip Code").pack()
        zip_entry = tk.Entry(self.root)
        zip_entry.pack()

        # Chief complaint
        tk.Label(self.root, text="Chief Complaint").pack()
        cc_entry = tk.Entry(self.root)
        cc_entry.pack()

        def submit():
            patient_id = patient_id_entry.get().strip()
            if not patient_id:
                tk.messagebox.showerror("Error", "Patient ID is required.")
                return

            data = {
                "Visit_time": visit_date_entry.get().strip(),
                "Visit_department": dept_entry.get().strip(),
                "Age": age_entry.get().strip(),
                "Gender": gender_var.get(),
                "Race": race_var.get(),
                "Ethnicity": eth_var.get(),
                "Insurance": ins_entry.get().strip(),
                "Zip_code": zip_entry.get().strip(),
                "Chief_complaint": cc_entry.get().strip()
            }

            self.patient_db.add_patient_visit(patient_id, data)
            self.patient_db.save_to_csv("./data/Patient_data.csv")
            tk.messagebox.showinfo("Success", f"Visit added for Patient ID: {patient_id}")
            self.show_role_dashboard()

        tk.Button(self.root, text="Submit", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_role_dashboard).pack()

    def remove_patient_ui(self):
        self.clear_screen()
        self.user.record_action("Remove Patient")

        tk.Label(self.root, text="Remove Patient", font=("Helvetica", 14)).pack(pady=10)

        tk.Label(self.root, text="Enter Patient ID to remove:").pack()
        pid_entry = tk.Entry(self.root)
        pid_entry.pack()

        def submit():
            pid = pid_entry.get().strip()
            if not pid:
                tk.messagebox.showerror("Error", "Patient ID is required.")
                return

            patient = self.patient_db.get_patient(pid)
            if patient:
                self.patient_db.remove_patient(pid)
                self.patient_db.save_to_csv("./data/Patient_data.csv")
                tk.messagebox.showinfo("Success", f"All records for Patient ID {pid} removed.")
                self.show_role_dashboard()
            else:
                tk.messagebox.showerror("Not Found", f"No patient found with ID: {pid}")

        tk.Button(self.root, text="Remove", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_role_dashboard).pack()

    def retrieve_patient_ui(self):
        self.clear_screen()
        self.user.record_action("Retrieve Patient")

        tk.Label(self.root, text="Retrieve Patient", font=("Helvetica", 14)).pack(pady=10)

        tk.Label(self.root, text="Enter Patient ID:").pack()
        pid_entry = tk.Entry(self.root)
        pid_entry.pack()

        def submit():
            pid = pid_entry.get().strip()
            patient = self.patient_db.get_patient(pid)
            print("Patient found:", patient)
            print("All patient IDs in memory:", self.patient_db.patients.keys())

            if not patient:
                tk.messagebox.showerror("Not Found", f"No patient found with ID: {pid}")
                return

            visit = patient.most_recent_visit()
            if not visit:
                tk.messagebox.showinfo("No Visits", f"Patient {pid} has no visits recorded.")
                return

            info = (
                f"Patient ID: {pid}\n"
                f"Visit ID: {visit.visit_id}\n"
                f"Date: {visit.visit_time}\n"
                f"Department: {visit.department}\n"
                f"Age: {visit.age}\n"
                f"Gender: {visit.gender}\n"
                f"Race: {visit.race}\n"
                f"Ethnicity: {visit.ethnicity}\n"
                f"Insurance: {visit.insurance}\n"
                f"Zip Code: {visit.zip_code}\n"
                f"Chief Complaint: {visit.chief_complaint}"
            )

            tk.messagebox.showinfo("Most Recent Visit", info)

        tk.Button(self.root, text="Retrieve", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_role_dashboard).pack()

    def count_visits_ui(self):
        self.clear_screen()
        self.user.record_action("Count Visits")

        tk.Label(self.root, text="Count Visits by Date", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(self.root, text="Enter Date (MM/DD/YYYY):").pack()

        date_entry = tk.Entry(self.root)
        date_entry.pack()

        from datetime import datetime

        def submit():
            date_input = date_entry.get().strip()
            try:
                # Parse MM/DD/YYYY to a datetime object
                parsed_date = datetime.strptime(date_input, "%m/%d/%Y")
                # Manually convert to M/D/YYYY format (e.g., 7/13/2011)
                converted_date = f"{parsed_date.month}/{parsed_date.day}/{parsed_date.year}"
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            count = self.patient_db.count_visits_on_date(converted_date)
            tk.messagebox.showinfo("Result", f"Total visits on {converted_date}: {count}")

        tk.Button(self.root, text="Retrieve", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_role_dashboard).pack()

    def view_note_ui(self):
        self.clear_screen()
        self.user.record_action("View Note")

        tk.Label(self.root, text="View Clinical Notes", font=("Helvetica", 14)).pack(pady=10)

        tk.Label(self.root, text="Enter Patient ID:").pack()
        pid_entry = tk.Entry(self.root)
        pid_entry.pack()

        tk.Label(self.root, text="Enter Visit ID:").pack()
        vid_entry = tk.Entry(self.root)
        vid_entry.pack()

        def submit():
            pid = pid_entry.get().strip()
            vid = vid_entry.get().strip()

            if not pid or not vid:
                tk.messagebox.showerror("Error", "Both Patient ID and Visit ID are required.")
                return

            notes = self.notes_data.get((pid, vid))

            if not notes:
                tk.messagebox.showinfo("No Notes", f"No notes found for Patient ID {pid} and Visit ID {vid}.")
            else:
                note_texts = "\n\n".join(
                    [f"Note ID: {note['Note_ID']}\n{note['Note_text']}" for note in notes]
                )
                tk.messagebox.showinfo("Notes", note_texts)

            self.show_role_dashboard()

        tk.Button(self.root, text="View", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_role_dashboard).pack()

    from stats import (
        plot_visit_trends,
        plot_insurance_distribution,
        plot_demographics_by_age,
    )

    def generate_stats_ui(self):
        self.clear_screen()
        self.user.record_action("Generate Stats")

        tk.Label(self.root, text="Generating Key Statistics...", font=("Helvetica", 14)).pack(pady=10)

        try:
            # Call all plotting functions
            plot_visit_trends("./data/Patient_data.csv", save_path="visit_trend.png")
            plot_insurance_distribution("./data/Patient_data.csv", save_path="insurance_distribution.png")
            plot_demographics_by_age("./data/Patient_data.csv", save_path="age_distribution.png")

            tk.messagebox.showinfo(
                "Statistics Generated",
                "Statistics saved as:\n- visit_trend.png\n- insurance_distribution.png\n- age_distribution.png"
            )
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to generate statistics.\n{str(e)}")

        self.show_role_dashboard()
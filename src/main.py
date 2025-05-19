import tkinter as tk
from ui import HospitalApp
from patients import PatientDatabase
from utils import load_notes


def main():
    # Initialize core data
    patient_db = PatientDatabase()
    notes_data = load_notes("./data/Notes.csv")
    patient_db.load_from_csv("./data/Patient_data.csv")

    # Launch the UI
    root = tk.Tk()
    app = HospitalApp(root, patient_db, notes_data)
    root.mainloop()


if __name__ == "__main__":
    main()
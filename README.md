# Hospital Clinical Data Warehouse (Tkinter GUI App)

Greetings all, this is Giridhar Kommalapati. This is my final project for the course HI 741 – Spring 2025. I created a simple Python application using Tkinter that helps hospital staff manage clinical data like patient visits, clinical notes, and statistics.

The program includes a login system and gives access based on different user roles. Each user gets only the features they’re allowed to use.

---

## 1. What the Project Does

- Lets users log in using their credentials (from Credentials.csv)
- Based on their role, they can:
  - Add or remove patient visits
  - View a patient's recent visit
  - Count how many patients visited on a given date
  - View clinical notes for a specific visit
  - Generate statistics (for management only)
- All patient data is saved to and loaded from CSV files
- The system also keeps track of who logged in and what actions they performed in Usage_Log.csv

---

## 2. How to Run It

### Step-by-Step Instructions:

1. *Download or clone* this GitHub repository: https://github.com/Gummango/HI_Final_Project.git
2. *Open the project in PyCharm* (or any Python IDE)

3. Make sure you have Python 3.8 or later installed.

4. Install the required packages by running this in the terminal: pip install -r requirements.txt
5. Run the program using: python main.py

6. The login screen will appear.  
Use a valid username and password from the data/Credentials.csv file.

7. After logging in, you will see a menu with buttons based on your role (admin, nurse, etc.)

---

>  If running from a different IDE or text editor, make sure the working directory is set to the project root.




## 3. Roles and What They Can Do

| Role           | Features Available                                       |
| -------------- | -------------------------------------------------------- |
| *Admin*      | Count visits on a specific date                          |
| *Nurse*      | Add, remove, retrieve patients, count visits, view notes |
| *Clinician*  | Same as Nurse                                            |
| *Management* | Generate key statistics and see result charts            |
Each role gets a different menu based on their access level.

## 4. Dependencies and How to Install
This program needs the following Python packages:

tkinter (comes with Python),
pandas,
matplotlib,
Make sure you have Python 3.8 or above installed.

## Folder Structure 
project-folder/
├── data/
│   ├── Patient_data.csv
│   ├── Notes.csv
│   ├── Credentials.csv
├── src/
│   ├── ui.py
│   ├── users.py
│   ├── patients.py
│   ├── stats.py
│   ├── utils.py
│   └── _init_.py
├── main.py
├── README.md
├── UML_diagram.pdf
├── Usage_Log.csv

## Notes:

1. Clinical notes are linked using Patient ID and Visit ID

2. Statistics graphs are saved as PNG images in the project folder

3. Every login and action is tracked inside Usage_Log.csv

## Author:

Giridhar Kommalapati, 
Master's – Information Science And Technology, 
University of Wisconsin-Milwaukee



```bash
python main.py

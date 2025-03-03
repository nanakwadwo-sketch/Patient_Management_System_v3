import re
import csv
import json
from datetime import datetime

class Patient:
    """Represents a patient and validates input data."""
    def __init__(self, patient_id, first_name, last_name, date_of_birth, hometown, house_number, phone_number):
        self.id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.age = self.calculate_age()
        self.hometown = hometown
        self.house_number = house_number
        self.phone_number = phone_number
    
    def calculate_age(self):
        """Calculate age based on date_of_birth."""
        dob = datetime.strptime(self.date_of_birth, "%d-%m-%Y")
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    
    def to_dict(self):
        """Convert patient attributes to a dictionary."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "age": self.age,
            "hometown": self.hometown,
            "house_number": self.house_number,
            "phone_number": self.phone_number
        }
    
    @staticmethod
    def validate_date_of_birth(date_str):
        """Validate date format and check if it's a valid date."""
        pattern = r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4})$"
        match = re.match(pattern, date_str)
        if not match:
            return False
        
        day, month, year = map(int, date_str.split('-'))
        try:
            # Check if it's a valid date
            datetime(year, month, day)  
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_phone_number(phone_str):
        """Validate phone number format (e.g., 024-000-0000)."""
        pattern = r"^\d{3}-\d{3}-\d{4}$"
        return bool(re.match(pattern, phone_str))

class FileManager:
    """Handles file operations for patient records."""
    @staticmethod
    def read_file(storage_type):
        """Read patient records from the selected storage type (CSV or JSON)."""
        if storage_type == "csv":
            try:
                with open("patients.csv", mode="r", newline="") as file:
                    reader = csv.DictReader(file)
                    return [row for row in reader]
            except FileNotFoundError:
                return []
        elif storage_type == "json":
            try:
                with open("patients.json", mode="r") as file:
                    return json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                return []

    @staticmethod
    def write_file(storage_type, data):
        """Write patient records to the selected storage type (CSV or JSON)."""
        if storage_type == "csv":
            with open("patients.csv", mode="w", newline="") as file:
                fieldnames = ["id", "first_name", "last_name", "date_of_birth", "age", "hometown", "house_number", "phone_number"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        elif storage_type == "json":
            with open("patients.json", mode="w") as file:
                json.dump(data, file, indent=4)

    @staticmethod
    def update_file(storage_type, data):
        """Update patient records in the selected storage file."""
        FileManager.write_file(storage_type, data)

    @staticmethod
    def delete_from_file(storage_type, patient_id):
        """Delete a patient record from the storage file."""
        data = FileManager.read_file(storage_type)
        new_data = [patient for patient in data if str(patient["id"]) != str(patient_id)]
        FileManager.write_file(storage_type, new_data)

class PatientManagementSystem:
    """Manages CRUD operations for patients."""
    def __init__(self, storage_type):
        self.storage_type = storage_type
        self.patients = FileManager.read_file(storage_type)
    
    def add_patient(self, first_name, last_name, date_of_birth, hometown, house_number, phone_number):
        patient_id = len(self.patients) + 1
        new_patient = Patient(patient_id, first_name, last_name, date_of_birth, hometown, house_number, phone_number)
        self.patients.append(new_patient.to_dict())
        FileManager.write_file(self.storage_type, self.patients)
    
    def get_all_patients(self):
        return self.patients
    
    def search_patient_by_id(self, patient_id):
        for patient in self.patients:
            if str(patient["id"]) == str(patient_id):
                return patient
        return None
    
    def update_patient_by_id(self, patient_id, updated_info):
        for patient in self.patients:
            if str(patient["id"]) == str(patient_id):
                patient.update(updated_info)
                FileManager.write_file(self.storage_type, self.patients)
                return True
        return False
    
    def delete_patient_by_id(self, patient_id):
        FileManager.delete_from_file(self.storage_type, patient_id)
        self.patients = FileManager.read_file(self.storage_type)

# Command-line interface
if __name__ == "__main__":
    storage_type = input("Choose storage type (csv/json): ").strip().lower()
    if storage_type not in ["csv", "json"]:
        print("Invalid storage type.")
    else:
        system = PatientManagementSystem(storage_type)
        while True:
            print("\n1. Add New Patient")
            print("2. Get All Patients")
            print("3. Search Patient by ID")
            print("4. Update Patient by ID")
            print("5. Delete Patient by ID")
            print("6. Exit")
            choice = input("Enter choice: ")
            if choice == "1":
                first_name = input("First Name: ")
                last_name = input("Last Name: ")
                date_of_birth = input("Date of Birth (dd-mm-yyyy): ")
                hometown = input("Hometown: ")
                house_number = input("House Number: ")
                phone_number = input("Phone Number (024-000-0000): ")
                system.add_patient(first_name, last_name, date_of_birth, hometown, house_number, phone_number)
            elif choice == "2":
                print(system.get_all_patients())
            elif choice == "3":
                pid = input("Enter Patient ID: ")
                print(system.search_patient_by_id(pid))
            elif choice == "4":
                print("Feature not implemented yet.")
            elif choice == "5":
                pid = input("Enter Patient ID to delete: ")
                system.delete_patient_by_id(pid)
            elif choice == "6":
                break
            else:
                print("Invalid choice. Try again.")

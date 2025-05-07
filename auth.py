import csv
import os
from utils import hash_password, verify_password

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.csv')
FIELDNAMES = ['name', 'email', 'password']

# Ensure the file exists with headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()

def signup_user(name, email, password):
    file_exists = os.path.isfile(CSV_FILE)

    # Debugging: Confirm whether file is being opened
    print(f"CSV file exists: {file_exists}")

    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'email', 'password'])
        
        # Debugging: Print when the file is opened and check the writing process
        print("Opening CSV file for writing...")

        if not file_exists:
            writer.writeheader()
            print("Writing header to CSV file...")

        writer.writerow({
            'name': name,  # Ensure these keys match the CSV headers
            'email': email,
            'password': hash_password(password)  # Ensure password is hashed
        })
        print(f"Writing user to CSV: Name={name}, Email={email}")  # Debug log

    return True, "Signup successful."


def login_user(email, password):
    with open(CSV_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['email'] == email and verify_password(password, row['password']):
                return True, row['name']
    return False, "Invalid credentials."

# authentication.py
# Author: Sayid Ali
# Class: CS361 / Oregon State University
# Description: MicroserviceA. Authenticates user signup, login, and delete functions.
# authentication.py
# Author: Sayid Ali
# Class: CS361 / Oregon State University
# Description: MicroserviceA. Authenticates user signup, login, and delete functions.

import os
import json
import time

# File paths
RESPONSE_FILE = "auth_response_file.txt"  # File where the response is written
REQUEST_FILE = "auth_request_file.txt"    # File where the request is read from
USERS_FILE = "users.json"                 # File where user data is stored

# Initialize users dictionary
if os.path.exists(USERS_FILE):
    # If the file exists, load the data into the users dictionary
    with open(USERS_FILE, "r") as file:
        users = json.load(file)
else:
    # If the file doesn't exist, initialize an empty dictionary
    users = {}

# Function to save user data to the JSON file
def add_user_to_file():
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)

# Function to process requests from the request file
def process_request():
    # Check if the request file exists
    if not os.path.exists(REQUEST_FILE):
        return

    # Open the request file and read its contents
    with open(REQUEST_FILE, "r") as file:
        request = file.read().strip().split()  # Read the file, split into a list, and remove extra spaces

    # Check if the request list is empty
    if not request:
        return

    # Extract the choice, username, and password from the request
    choice = request[0]  # First value is the choice (signup, login, delete)
    username = request[1]  # Second value is the username
    password = request[2] if len(request) > 2 else None  # Third value is the password (if provided)

    # Default response is FAIL
    response = "FAIL"

    # Process the request based on the choice
    if choice == "SIGNUP":
        if username not in users:
            users[username] = password
            add_user_to_file()
            response = "SUCCESS"

    elif choice == "LOGIN":
        if username in users and users[username] == password:
            response = "SUCCESS"

    elif choice == "DELETE":
        if username in users:
            del users[username]
            add_user_to_file()
            response = "SUCCESS"

    # Write the response to the response file
    with open(RESPONSE_FILE, "w") as file:
        file.write(response)

    # Clear the request file after processing
    with open(REQUEST_FILE, "w") as file:
        file.write("")  # Clear the file contents

# Main loop to continuously check for requests
while True:
    process_request()
    time.sleep(2)  # dec delay

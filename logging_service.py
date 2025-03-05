# logging_service.py
# Author: Philip Sheridan
# Class: CS361 / Oregon State University
# Description: Provides global system logging functionality for admin

# ---------- Imports ----------
import pickle
import os
import time
from Pipeline import Pipeline

# ---------- Classes ----------

# ---------- Functions ----------
def save_data(data) -> None:
    # Save the change to persistent data structure
    try:
        with open(f"log_data.pickle", 'wb') as outfile:
            pickle.dump(data, outfile, protocol=pickle.HIGHEST_PROTOCOL)

    # $$$ DEBUGGING $$$: provide info about errors
    except FileNotFoundError:
        print("ERROR SAVING Log data!!!")

def main():
    """
    LOGGING MICROSERVICE
        This service records user actions and permits viewing by admin user.
    """

    # Instantiate a Pipeline called 'pipe'
    pipe = Pipeline('profile')

    pass


# Execute Program
if __name__ == '__main__':
    main()

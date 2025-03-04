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

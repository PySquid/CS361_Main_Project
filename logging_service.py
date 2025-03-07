# logging_service.py
# Author: Philip Sheridan
# Class: CS361 / Oregon State University
# Description: Provides global system logging functionality for admin

# ---------- Imports ----------
import pickle
import time
import os
from datetime import datetime as dt
from datetime import timedelta
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

def del_old() -> None:
    """ Checks for log files older than 7 days and deletes them."""
    pass

def process_logs(buffer) -> None:
    """ Continuously reads the buffer and writes all entries to disk. """
    while True:
        time.sleep(2)
        if len(buffer) > 0:
            log = buffer.pop(0)

            # Prepare entry
            entry = f"{log['time']} | {log['user']} | {log['action']}\n"

            # Determine file name for current day's log
            date = dt.now()
            year = date.year
            month = date.month
            day = date.day
            file_name = f"{month}/{day}/{year}.log"

            # Make the entry into the log file
            with open(file_name, 'a') as f:
                f.write(entry)

            # Check for old logs and delete them
            del_old()




def main():
    """
    LOGGING MICROSERVICE
        This service records user actions and permits viewing by admin user.
    """

    # Instantiate a Pipeline called 'pipe'
    pipe = Pipeline('profile')

    # Prepare a buffer for incoming logs, begin buffer processing
    buffer = []
    threading.Thread(target=nonblocking, daemon=True, args=(mgmt_ip, mgmt_port)).start()

    # ----- LOG DATABASE INITIATE -----
    # check for existing logs database
    try:
        with open('log_data.pickle', "rb") as infile:
            # one already exists...load it
            logs = pickle.load(infile)

    # No logs database yet? make a blank dictionary to hold the logs
    except FileNotFoundError:
        logs = {}

    # Initiate main (outer) loop.  [there's an inner loop in the Pipeline.receive() function]
    while True:
        # execute listening (blocking action) and assign result to 'new_message'
        new_message = pipe.receive()

        # Assign
        command = new_message['action']

        # take action based on the command given in the message

        # --- RECORD INCOMING LOG  ---
        if command == 'record':
            buffer.append(new_message['log'])

        # --- REQUEST TO VIEW LOGS  ---
        elif command == 'view':
            pass

        # --- ERROR ---
        else:
            pipe.send('core', 'ERROR')


# Execute Program
if __name__ == '__main__':
    main()

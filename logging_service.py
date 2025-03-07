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
import threading

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

def del_old(today) -> None:
    """ Checks for log files older than 7 days and deletes them."""
    current_directory = os.curdir
    log_directory = os.path.relpath('/logs', current_directory)
    os.chdir(log_directory)
    contents = os.listdir()
    
    cutoff = today - timedelta(days=7)

    for d in contents:
        

def process_logs(buffer) -> None:
    """ Continuously reads the buffer and writes all entries to disk. """
    while True:
        time.sleep(2)
        if len(buffer) > 0:
            log = buffer.pop(0)

            # Prepare entry
            entry = f"{log['time']} | {log['user']} | {log['action']}\n"

            # Determine file name for current day's log
            today = dt.now()
            year = today.year
            month = today.month
            day = today.day
            file_name = f"{month}/{day}/{year}.log"

            # Make the entry into the log file
            with open(file_name, 'a') as f:
                f.write(entry)

            # Check for old logs and delete them
            del_old(today)




def main():
    """
    LOGGING MICROSERVICE
        This service records user actions and permits viewing by admin user.
    """

    # Instantiate a Pipeline called 'pipe'
    pipe = Pipeline('profile')

    # Prepare a buffer for incoming logs, begin buffer processing
    buffer = []
    threading.Thread(target=process_logs, daemon=True, args=buffer).start()

    # ----- LOG FILE: INITIATE -----
    # Initialize logs dictionary
    if os.path.exists('logs'):
        # If the directory exists, change to it
        os.chdir('logs')
    else:
        # Create the directory if absent
        os.makedirs('logs')
        os.chdir('logs')

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

# logging_service.py
# Author: Philip Sheridan
# Class: CS361 / Oregon State University
# Description: Provides global system logging functionality for admin

# ---------- Imports ----------
import pickle
import time
import os
from datetime import datetime as dt
from Pipeline import Pipeline
import threading

# ---------- Classes ----------

# ---------- Functions ----------
def del_old() -> None:
    """ Checks for log files older than 7 days and deletes them."""
    while True:
        contents = os.listdir()
        print(contents)
        # Sort the newest dates to the front
        contents.sort(reverse=True)
        old = []
        if len(contents) > 7:
            old = contents[7:]
            print("old is ", old)
        for i in old:
            if i.endswith('.log'):
                print(f'deleting {i}')
                os.remove(i)
        time.sleep(3600)

def process_logs(buffer) -> None:
    """ Continuously reads the buffer and writes all entries to disk as log files. """
    while True:
        time.sleep(3)
        if len(buffer) > 0:
            log = buffer.pop(0)

            print(f'adding a new log entry for: {log}')

            # set the day
            today = dt.now().date().strftime('%m-%d-%Y')

            # Prepare entry
            entry = f"{dt.now().strftime('%m-%d-%Y  %H:%M:%S')} | {log['user']} | {log['trigger']}\n"
            print(f"new entry is: {entry}")

            # Determine file name for current day's log
            file_name = f"{today}.log"

            # Make the entry into the log file
            with open(file_name, 'a') as f:
                f.write(entry)

def generate_rpt(past) -> str:
    """ Prepares and returns a report for a day, param being # days in past (0 = today)"""
    contents = os.listdir()
    contents.sort(reverse=True)
    chosen = contents[past]
    report = ""
    with open(chosen, 'r') as log:
        for line in log:
            report += f"{line}\n"
    return report

def main():
    """
    LOGGING MICROSERVICE
        This service records user actions and permits viewing by admin user.
    """

    # Instantiate a Pipeline called 'pipe'
    pipe = Pipeline('log')

    # ----- LOG SUB-FOLDER: INITIATE -----
    # Initialize logs dictionary
    if os.path.exists('logs'):
        # If the directory exists, change to it
        os.chdir('logs')
    else:
        # Create the directory if absent, then make it the active directory
        os.makedirs('logs')
        os.chdir('logs')

    # Prepare a buffer for incoming logs, begin buffer processing
    buffer = []

    # 'outer' is the outer list wrapper needed to pass the list to the thread...its only purpose
    outer = [buffer]
    threading.Thread(target=process_logs, daemon=True, args=outer).start()

    # Start old-log deletion daemon
    threading.Thread(target=del_old, daemon=True).start()

    # --- MAIN MESSAGE HANDLER LOOP ---
    while True:
        # execute listening (blocking action) and assign result to 'new_message'
        new_message = pipe.receive()

        # Assign
        command = new_message['action']

        # take action based on the command given in the message

        # --- RECORD INCOMING LOG  ---
        if command == 'log':
            buffer.append(new_message['log'])

        # --- REQUEST TO VIEW LOGS  ---
        elif command == 'view':
            report = generate_rpt(new_message['days_past'])
            pipe.send('core', report)

        # --- ERROR ---
        else:
            pipe.send('core', 'ERROR')


# Execute Program
if __name__ == '__main__':
    main()

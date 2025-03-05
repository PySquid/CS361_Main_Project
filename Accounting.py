# Accounting.py
# Author: Philip Sheridan
# Class: CS361 / Oregon State University
# Description: Provides finance and accounting functions
# User stories: 1) check books in and out, 2) user can view their checked out books (and due dates???).

# ---------- Imports ----------
import pickle
import os
import time
from Pipeline import Pipeline
from datetime import datetime, timedelta

# ---------- Classes ----------

class AccountData:
    def __init__(self):
        """ Initializes an instance of the main accounting object. """
        # create a space to store checked out books

        # FORMAT: dictionary1 = {USER -> checkout record}
        #           dictionary2 (checkout record) = {BOOK SERIAL STRING -> due date}
        self.checkouts = {}     # {user name: {S/N: DUE_DATE}}

    def check_out(self, user, book_sn) -> str:
        """ Checks a book out to a specific user. """
        present = datetime.now()
        due_date = str(present + timedelta(days=14))
        if user in self.checkouts.keys():
            self.checkouts[user][book_sn] = due_date
        else:
            self.checkouts[user] = {book_sn: due_date}
        print(f"{user} has just checked out book with serial number {book_sn}")
        return due_date

    def check_in(self, user, book_sn) -> None:
        """ Checks a book back in that was checked out by a user. """
        del self.checkouts[user][book_sn]
        print(f"{user} has just checked in book with serial number {book_sn}")

    def get_check_outs(self, user):
        """ Returns the checked out books for a specified user. """
        print(f"{user} has just requested a record of their checked out books...")
        if user in self.checkouts.keys():
            return self.checkouts[user]
        else:
            return {}


# ---------- Functions ----------
def save_data(data) -> None:
    # Save the change to persistent data structure
    try:
        with open(f"accounting_data.pickle", 'wb') as outfile:
            pickle.dump(data, outfile, protocol=pickle.HIGHEST_PROTOCOL)

    # $$$ DEBUGGING $$$: provide info about errors
    except FileNotFoundError:
        print("ERROR SAVING Accounting data!!!")

def main():
    """
    ACCOUNTING MICROSERVICE
        This service keeps track of customer balances and tracks book checkins/checkouts per customer

        1) Track checkouts
        2) track checkins
        3) track due dates
        4) track user monetary due balance
        5) charge customers late fees to their balance
    """

    print("ACCOUNTING SERVICE ACTIVATED...all systems nominal")

    # Instantiate a Pipeline
    pipe = Pipeline('accounting')

    # Initiate main (outer) loop.  [there's an inner loop in the Pipeline.receive() function]
    # ----- ACCOUNTING DATABASE INITIATE -----
    # check for existing Accounting database
    try:
        with open('accounting_data.pickle', "rb") as infile:
            # one already exists...load it
            accounts = pickle.load(infile)

    # No profiles database yet? make a blank ProfileData (camelcase) Object for it to start a new one
    except FileNotFoundError:
        accounts = AccountData()

    # Initiate main (outer) loop.  [there's an inner loop in the Pipeline.receive() function]
    while True:
        # execute listening (blocking action) and assign result to 'new_message'
        new_message = pipe.receive()

        # Assign
        command = new_message['action']

        # take action based on the command given in the message

        # --- CHECK BOOK OUT ---
        if command == 'check_out':
            reply = accounts.check_out(new_message['user'], new_message['sn'])
            pipe.send('core', reply)

        # --- CHECK BOOK IN ---
        elif command == 'check_in':
            accounts.check_in(new_message['user'], new_message['sn'])

        # --- CHECKED OUT BOOK INQUIRY ---
        elif command == 'get_checkouts':
            message = accounts.get_check_outs(new_message['user'])
            pipe.send('core', message)

        else:
            print(f"ERROR...INVALID COMMAND ({command}) RECEIVED!")


# Execute Program
if __name__ == '__main__':
    main()
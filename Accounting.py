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
        self.checkouts[user][book_sn] = due_date
        return due_date

    def check_in(self, user, book_sn):
        """ Checks a book back in that was checked out by a user. """
        pass

    def get_check_outs(self, user):
        """ Returns the checked out books for a specified user. """
        return self.checkouts[user]


# ---------- Functions ----------
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
        if command == 'check_in':
            pass

        # --- ACCOUNT INFO REQUEST ---
        if command == 'get_account':
            pass

        # --- DUE DATES INQUIRY ---
        if command == 'get_due_dates':
            pass

        # --- CHECKED OUT BOOK INQUIRY ---
        if command == 'get_checkouts':
            pass


# Execute Program
if __name__ == '__main__':
    main()
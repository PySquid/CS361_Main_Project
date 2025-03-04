# Accounting.py
# Author: Philip Sheridan
# Class: CS361 / Oregon State University
# Description: Provides finance and accounting functions

# ---------- Imports ----------
import socket
import pickle
import os
import time
import Pipeline

# ---------- Classes ----------

class AccountData:
    def __init__(self):
        """"""
        # create a space to store checked out books

        # FORMAT: dictionary1 = {USER -> checkout record}
        #         dictionary2 (checkout record) = {BOOK SERIAL STRING -> due date, PRICE -> price of book}
        self.checkouts = {}     # {user name: {S/N: DUE_DATE: date, PRICE: $price}}

        # create a space to store users' account balances
        self.balances = {}      # {USER NAME: $amount}

    def check_out(self, user, book_sn):
        """"""
        pass

    def check_in(self, user, book_sn):
        """"""
        pass

    def get_balance(self, user):
        """"""
        return self.balances[user]

    def get_check_outs(self, user):
        """"""
        return self.checkouts[user]

    def get_past_due(self, user):
        """Returns any books that are past due, for a user."""
        late = None

        return late


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
        data = new_message['data']

        # take action based on the command given in the message

        # --- CHECK BOOK OUT ---
        if command == 'checkout':
            pass

        # --- CHECK BOOK IN ---
        if command == 'checkout':
            pass

        # --- ACCOUNT INFO REQUEST ---
        if command == 'checkout':
            pass

        # --- DUE DATES INQUIRY ---
        if command == 'checkout':
            pass


# Execute Program
if __name__ == '__main__':
    main()
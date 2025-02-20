# Accounting.py
# Author: Philip Sheridan
# Class: CS361 / Oregon State University
# Description: Provides finance and accounting functions

# ---------- Imports ----------
import socket
import pickle
import os
import time

# ---------- Classes ----------
class Pipeline:
    """
    This structure establishes a communication pipeline between the core UI/CMS and its plugin
    microservices.

    CALL:   pipeline.send('microservice recipient name string', data payload)
    RETURNS: whatever data the microservice replies with...format is ['action': string, 'data': dictionary]

    Whatever service initiates the contact must send [action, data], but responds with [reply]
    """

    def __init__(self, own_name):
        """ Builds the initial address book for the pipeline communication services. """
        self.address_book = {
            'core': ('127.0.0.1', 20000),
            'auth': ('127.0.0.1', 20001),
            'profile': ('127.0.0.1', 20002),
            'accounting': ('127.0.0.1', 20003),
            'log': ('127.0.0.1', 20004)
        }
        self.name = own_name

    def send(self, destination, data, buffer=2048):
        """IS passed a socket tuple and data, returns the reply from recipient"""

        # Map destination to address using the address book
        if destination == 'core':
            destination = self.address_book['core']
        elif destination == 'auth':
            destination = self.address_book['auth']
        elif destination == 'profile':
            destination = self.address_book['profile']
        elif destination == 'accounting':
            destination = self.address_book['accounting']
        elif destination == 'log':
            destination = self.address_book['log']
        else:
            return False

        # Make an IPv4/TCP socket
        core_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to destination service
        try:
            # destination is a tuple: (IP, PORT), to match the socket library format
            core_socket.connect(destination)

            # !!!!! TESTING !!!!!
            print(f"Transmitting data to {destination} now...")

            if type(data) == str:
                # it's a string...encode and send it
                core_socket.sendall(data.encode())
            else:
                # it's a pickled dictionary...just send the bytes
                core_socket.sendall(data)

            # Avoid race condition with destination service...
            # ...allow processing time
            # *** NOTE *** 2 seconds may not be enough...go to 3 if problems arise
            time.sleep(3)

            # Get reply from destination service, then decode it appropriately
            response = core_socket.recv(buffer)

            # Process strings vs pickled dictionaries
            try:
                # is it a string...?
                processed_reply = str(response.decode())
            except:
                # ...if not, it's a pickled dictionary
                processed_reply = pickle.loads(response)

            # !!!!! TESTING !!!!!
            print(f"{destination} responded with this data: '{processed_reply}'")

        finally:
            # Close the socket.
            core_socket.close()

        # provide the processed/decoded reply to the calling function
        return processed_reply

    def receive(self, rec_buffer=2048, max_connect=3, reply="ack") -> dict:
        """
        Takes a sender name listed in the address book as a string, then returns the
        :param service_name: the name of the microservice calling this class
        :param rec_buffer: default to 2048, this should not be changed
        :param max_connect: generally, 1 should be the max connections, 3 is more than enough
        :param reply: reply is the default reply from this method
        :return: the action mode and the decoded message data is returned
        """

        # Prepare variables
        data_decoded = None  # container for decoded incoming message
        address = self.address_book[self.name]  # sets own address based on object name

        # Set up a receiving IPv4/TCP socket
        receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind it
        receive_socket.bind(address)

        # Start listening for messages from the Core/UI/CMS
        receive_socket.listen(max_connect)

        # Initialize return message container at METHOD-level scope
        message_decoded = None

        # Main loop: Initiate communications with the CMS/UI 'core'

        try:
            while True:
                # Accept connection from UI
                core_socket, core_ip = receive_socket.accept()

                # !!!!! TESTING !!!!!
                print(f"{core_ip} (Core UI) just connected")

                try:
                    # transfer the socket data to the 'data' variable
                    message = core_socket.recv(rec_buffer)

                    # try to decode the data as a string
                    try:
                        message_decoded = str(message.decode())

                    # if that fails...it's a pickled dictionary, unpickle it
                    except:
                        message_decoded = pickle.loads(message)

                finally:
                    # Close connection to core
                    core_socket.close()

        finally:
            # Close the connection
            receive_socket.close()

            # Make the response available to the calling function
            return message_decoded

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
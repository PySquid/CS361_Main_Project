# profile_service.py
# Author: Philip Sheridan
# Class: CS361 / Oregon State University
# Description: Provides user profile functions

# ---------- Imports ----------
import socket
import pickle
import os
import time
import random


# ---------- Classes ----------
class Pipeline:
    """
    This structure establishes a communication pipeline between the core UI/CMS and its plugin
    microservices.

    CALL:   pipeline.send('microservice recipient name string', data payload)
    RETURNS: whatever data the microservice replies with...format is ['action': string, 'data': dictionary]
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
            core_socket.sendall(data.encode())

            # Avoid race condition with destination service...
            # ...allow processing time
            # *** NOTE *** 2 seconds may not be enough...go to 3 if problems arise
            time.sleep(3)

            # Get reply from destination service, then decode it
            response = core_socket.recv(buffer)
            processed_reply = str(response.decode())

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

        # Main loop: Initiate communications with the CMS/UI 'core'

        try:
            while True:
                # Accept connection from UI
                core_socket, core_ip = receive_socket.accept()

                # !!!!! TESTING !!!!!
                print(f"{core_ip} (Core UI) just connected")

                try:
                    data = core_socket.recv(rec_buffer)
                    data_decoded = dict(data.decode())

                finally:
                    # Close connection to core
                    core_socket.close()

        finally:
            # Close the connection
            receive_socket.close()

            # Make the response available to the calling function
            return data_decoded

class User:
    def __init__(self, first, last, age, address, phone, email):
        """"""
        self.first_name = first
        self.last_name = last
        self.age = age
        self.address = address
        self.phone = phone
        self.email = email
        self.card = None        # this is filled in by the system later

    def get_info(self) -> str:
        """Returns a nicely formatted user profile data report"""
        output = "---------------------------------\n"
        output += f"NAME: {self.first_name} {self.last_name}\n"
        output += f"AGE: {self.age}\n"
        output += f"ADDRESS: {self.address}\n"
        output += f"PHONE: {self.phone}\n"
        output += f"EMAIL: {self.email}\n"
        output += f"LIBRARY CARD NUMBER : {self.card}\n"
        output += "---------------------------------\n"
        return output

class ProfileData:
    def __init__(self):
        """"""
        # create a space to store library cards: [user name : card number]
        self.lib_cards = {}

        # create a space to store users' user-profiles: [user name: User object]
        self.users = {}

    def add_lib_card(self, user_name) -> None:
        """
        Adds a new library card, associated with a username, and deconflicts the creation
        :param user_name:
        :return: None
        """
        # generate a new library card number: FORMAT = username + (random 0-999999)
        while True:
            # find a library card number
            test_card = random.randint(0, 9999999)
            if test_card in self.lib_cards.values():
                continue
            else:
                self.lib_cards[user_name] = test_card
                return

    def add_user(self, user):
        """UI gets all the user input data, creates a user object, and passes the OBJECT here
        ***creates username, deconflicts it, then incorporates it into a new User object
        """
        # create the user name
        naming = True
        new_username = None
        while naming:
            test_username = user.last_name + user.first_name[0] + random.randint(0, 99)
            if test_username in self.users.keys():
                # user exists...try another number
                continue
            else:
                # no username conflict...proceed with creation
                new_username = test_username
                break

        # generate a new library card number: FORMAT = random 0-9999999
        self.add_lib_card(new_username)

        # create the new full profile
        self.users[new_username] = user

        # finished
        return

# ---------- Functions ----------
def main():
    """
    PROFILE MICROSERVICE
        This service keeps track of customer profile information
    """

    # Instantiate a Pipeline called 'pipe'
    pipe = Pipeline('accounting')

    # ----- PROFILE DATABASE INITIATE -----
    # check for existing Profiles database
    try:
        with open('profile_data.pickle', "rb") as infile:
            # one already exists...load it
            profiles = pickle.load(infile)

    # No profiles database yet? make a blank ProfileData (camelcase) Object for it to start a new one
    except FileNotFoundError:
        profiles = ProfileData()

    # Initiate main (outer) loop.  [there's an inner loop in the Pipeline.receive() function]
    while True:
        # execute listening (blocking action) and assign result to 'new_message'
        new_message = pipe.receive()

        command = new_message['action']
        data = new_message['data']

        # take action based on the command given in the message
        # --- CREATE NEW USER PROFILE ---
        if command == 'create_user':
            # data format: dictionary with keys: [first_name, last_name, age, address, phone, email]
            f = data['first_name']
            l = data['last_name']
            age = data['age']
            addr = data['address']
            p = data['phone']
            e = data['email']
            new = User(f, l, age, addr, p, e)
            profiles.add_user(new)
            continue

        # --- DELETE EXISTING USER PROFILE---
        elif command == 'delete_user':
            # data format {'user_name': username}

            # delete the user if it exists...
            if data['user_name'] in profiles.users.keys():
                del profiles.users[data['user_name']]
                del profiles.lib_cards[data['user_name']]
            # ...if not, let the UI know what happened
            else:
                pipe.send('core', "{'error': 'user not found'}")

        # --- GET USER PROFILE INFO ---
        elif command == 'get_user_info':
            # data format {'user_name': username}
            uname = data['user_name']
            pipe.send('core', profiles.users[uname].get_info())

        # --- EDIT USER ---
        elif command == 'edit_user':
            # data format {[}'user_name': username, 'attribute': a user attr. , 'new_value': new attr. value}
            uname = data['user_name']
            attribute = data['attribute']
            new_value = data['new_value']
            profiles.users[uname][attribute] = new_value
            continue

        # --- ERROR ---
        else:
            pipe.send('core', "{'error': 'bad command'}")
            continue


# Execute Program
if __name__ == '__main__':
    main()

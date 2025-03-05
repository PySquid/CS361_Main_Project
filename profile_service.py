# profile_service.py
# Author: Philip Sheridan
# Class: CS361 / Oregon State University
# Description: Provides user profile functions

# ---------- Imports ----------
import pickle
import random
from Pipeline import Pipeline


# ---------- Classes ----------

class User:
    def __init__(self, first, last, age, address, phone, email):
        """ Initializes a new User object instance. """
        self.first_name = first
        self.last_name = last
        self.age = age
        self.address = address
        self.phone = phone
        self.email = email
        self.card = None        # this is filled in by the system later
        self.assist = None        # integer: persistent, user-specified override for menu assistance level

    def get_info(self) -> str:
        """Returns a nicely formatted user profile data report as a STRING ... NOT AN OBJECT OR DICTIONARY
            * Tested and confirmed working. *
        """
        output = "---------------------------------\n"
        output += f"NAME: {self.first_name} {self.last_name}\n"
        output += f"AGE: {self.age}\n"
        output += f"ADDRESS: {self.address}\n"
        output += f"PHONE: {self.phone}\n"
        output += f"EMAIL: {self.email}\n"
        output += f"LIBRARY CARD NUMBER : {self.card}\n"
        output += "---------------------------------\n"
        print(f'output is {output}')
        return output

    def get_dict(self) -> dict:
        """ Returns a dictionary of all the user attributes. """

        out_dict = {'first_name': self.first_name, 'last_name': self.last_name, 'age': self.age,
                    'address': self.address, 'phone': self.phone, 'email': self.email, 'card': self.card,
                    'assist': self.assist}

        return out_dict

    def get_assist(self) -> int:
        """ Returns the user's menu help override setting. """
        return self.assist

    def edit(self, old, new,):
        """ Changes a value """
        setattr(self, old, new)


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

    def add_user(self, username, user):
        """UI gets all the user input data, Profile Main creates a user object, then passes the OBJECT here"""

        # Legacy username creation code prior to Microservice A
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
        """

        # generate a new library card number: FORMAT = random 0-9999999
        self.add_lib_card(username)

        # create the new full profile
        self.users[username] = user

        # finished
        return

# ---------- Functions ----------
def save_data(data) -> None:
    # Save the change to persistent data structure
    try:
        with open(f"profile_data.pickle", 'wb') as outfile:
            pickle.dump(data, outfile, protocol=pickle.HIGHEST_PROTOCOL)

    # $$$ DEBUGGING $$$: provide info about errors
    except FileNotFoundError:
        print("ERROR SAVING Profile data!!!")

def main():
    """
    PROFILE MICROSERVICE
        This service keeps track of customer profile information
    """

    print("PROFILE SERVICE ACTIVATED...all systems nominal")

    # Instantiate a Pipeline called 'pipe'
    pipe = Pipeline('profile')

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

        # Assign
        print(f'new message is {new_message}')
        command = new_message['action']
        data = new_message                      # workaround to fuse original code convention with later one

        # <<< DEBUGGING >>>
        print(f" INCOMING...command is {command} and data is {data}!")

        # take action based on the command given in the message

        # --- CREATE NEW USER PROFILE ---
        # * Tested and confirmed working *
        if command == 'create_user':
            u_name = data['u_name']
            # data format: dictionary with keys: [first_name, last_name, age, address, phone, email]
            f = data['first_name']
            last = data['last_name']
            age = data['age']
            addr = data['address']
            p = data['phone']
            e = data['email']
            new = User(f, last, age, addr, p, e)
            profiles.add_user(u_name, new)

            # Write change to database
            save_data(profiles)

            continue

        # --- DELETE EXISTING USER PROFILE---
        elif command == 'delete_user':
            # data format {'user_name': username}

            # delete the user if it exists...
            if data['user_name'] in profiles.users.keys():
                del profiles.users[data['user_name']]
                del profiles.lib_cards[data['user_name']]
                pipe.send('core', 'DELETED')
            # ...if not, let the UI know what happened
            else:
                pipe.send('core', 'ERROR: user not found!')

            # Write change to database
            save_data(profiles)

        # --- GET USER PROFILE DICTIONARY ---
        elif command == 'get_user_dict':
            # data format {'user_name': username}
            uname = data['user_name']
            if uname in profiles.users.keys():
                pipe.send('core', profiles.users[uname].get_dict())
            else:
                print("Get user info has encountered an error!")
                pipe.send('core', 'ERROR')

        # --- GET USER PROFILE INFO ---
        elif command == 'get_user_info':
            # data format {'user_name': username}
            uname = data['user_name']
            if uname in profiles.users.keys():
                print(f"Get user info has found user {uname}, sending info to core...")
                print(f"sending THIS {profiles.users[uname].get_info()}")
                pipe.send('core', profiles.users[uname].get_info())
            else:
                print("Get user info has encountered an error!")
                pipe.send('core', 'ERROR')

        # --- EDIT USER ---
        elif command == 'edit_user':
            # data format {'user_name': username, 'attribute': a user attr. , 'new_value': new attr. value}
            uname = data['user_name']
            attribute = data['attribute']
            new_value = data['new_value']
            profiles.users[uname].edit(attribute, new_value)
            save_data(profiles)
            continue

        # --- ERROR ---
        else:
            pipe.send('core', "{'error': 'bad command'}")
            continue


# Execute Program
if __name__ == '__main__':
    main()

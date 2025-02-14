# MainUI.py
# Author: Philip Sheridan
# Class: CS361 / Oregon State University
# Description: Provides User Interface for Main Project, also serves as a mini monolith content manager

# ---------- Imports ----------
import socket
import pickle
import random
import os
import time

# ---------- Classes ----------

class Book:
    def __init__(self, title, author, isbn, year, publisher, price):
        """initializes a new network monitor.
            All numbers EXCEPT the serial number (string) and price (float) are integers"""

        self.title = title          # string
        self.author = author        # string
        self.isbn = isbn            # this number is an Integer
        self.serial = None          # string which gets assigned by Library once 'added'
        self.year = year            # integer
        self.publisher = publisher  # string
        self.price = price          # integer
        self.rating = None          # integer
        self.summary = None         # string

    # ----- METHODS -----
    def get_info(self):
        """Returns the book's main attributes as a dictionary"""

        return({'title': self.title, 'author': self.author, 'isbn': self.isbn, 'serial': self.serial, 'year': self.year,
                'publisher': self.publisher, 'price': self.price, 'rating': self.rating, 'summary': self.summary})

    def view(self):
        """"""
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"ISBN: {self.isbn}")
        print(f"Publisher: {self.publisher}")
        print(f"Year: {self.year}")
        print(f"Price: {self.price}")
        print(f"Serial: {self.serial}")
        if self.rating:
            print(f"Rating: {self.rating}")
        else:
            print(f"Rating: (Not yet rated)")
        if self.summary:
            print(f"Summary: {self.summary}")
        else:
            print(f"Summary: (Not yet summarized)")

    def get_title(self) -> str:
        """
        Returns the Book's title
        :return: title string of the instantiated Book object
        """
        return self.title

    def get_serial(self) -> str:
        """
        Takes no parameters and just returns the book's serial number string
        :return: a serial number string
        """
        return self.serial

    def get_author(self) -> str:
        """
        Takes no parameters and just returns the book's author string
        :return: this book's author string
        """

        return self.author

    def edit(self, old, new) -> bool:
        """
        Changes a value for one of the Book's attributes.
        Takes an attribute, then its new value as parameters.
        :param old: the attribute to change
        :param new: the new value for that attribute
        :return:
        """

        # check that the old value is a valid book attribute
        if old in vars(self).keys:
            # check that the supplied new value is the same type as the old value
            if type(getattr(self, old)) == type(new):
                setattr(self, old, new)
                return True
            else:
                return False
        else:
            return False

class Library:
    def __init__(self):
        """initializes a new network monitor"""
        self.authors = {}                       # authors map to a list of serial numbers
        self.titles = {}                        # titles map to list of serial numbers
        self.serials = {}                       # *** MAIN COLLECTION *** ...... serial number to book object
        self.recycled = {}                      # keys are serial numbers, values are filename strings
        self.banner = ""                        # Banner at main menu with admin notes and update information

    # ----- METHODS -----
    def insert_book(self, in_book):
        """
        Takes a book as a parameter, then adds the book to the collection, deconflicting the serial as well
        :param in_book: takes a Book object
        :return: None
        """

        available = False
        while not available:
            if in_book.get_serial() not in self.serials.keys():
                self.serials[in_book.get_serial()] = in_book
                self.titles[in_book.get_title()] = in_book.get_serial()
                self.authors[in_book.get_author()] = in_book.get_serial()
                available = True
            else:
                new_serial = in_book.get_serial()
                new_serial += '1'
                in_book.edit('serial', new_serial)

    def book_by_serial(self, target) -> Book:
        """
        Returns a book object based on serial number
        """
        return self.serials[target]

    def book_by_author(self, target) -> (Book or bool):
        """
        Takes an author name string and returns the book object, or False if an error occurs.
        :param target: the target parameter is a string of the book author's name
        :return:
        """

        # check author is in the authors catalogue
        if target in self.authors.keys():
            auth_serial = self.authors[target]
        else:
            return False

        # return the book object
        return self.serials[auth_serial]

    def book_by_title(self, target) -> (Book or bool):
        """
        Takes book title string and returns the book object, or False if an error occurs.
        :param target: the target parameter is a string of the book's title
        :return:
        """

        # check title is in the library titles catalogue
        if target in self.titles.keys():
            title_serial = self.titles[target]
        else:
            return False

        # return the book object
        return self.serials[title_serial]

    def info_by_serial(self, target) -> dict:
        """
        Returns a dictionary of all a book's information, accessed by serial number
        """
        return dict(vars(self.serials[target]))               # returns a dictionary of book attributes

    def info_by_author(self, auth) -> (dict or bool):
        """
        Returns a dictionary of all a book's information(variables), accessed by author name
        """

        # check the author is in the library
        if auth in self.authors.keys():
            auth_serial = self.authors[auth]
        else:
            return False

        # return the book information
        return dict(vars(self.serials[auth_serial]))

    def info_by_title(self, target_title) -> (dict or bool):
        """
        Returns a dictionary of all a book's information (variables), accessed by title
        """

        # check the title is in the library
        if target_title in self.titles.keys():
            title_serial = self.titles[target_title]
        else:
            return False

        # return the book information
        return dict(vars(self.serials[title_serial]))

    def add_book(self, new) -> None:
        """
        Must add book to collections and assign it a serial number
            * takes a book as input for 'new' parameter
        """

        # --- SERIAL ASSIGNMENT ---
        #       assigns a serial number to the book and stores it in the collection(serials)

        # - GENERATE A NEW SERIAL -
        #       ensure serial is unique, then assign it
        unique = False
        candidate_serial = None

        while not unique:
            # serial format: [first 2 title characters] + [first two author letters] + [random number up to 50k]
            #   *** serial number is stored as a string value
            serial_num = str(random.randint(0, 50000))
            serial_alpha = str(new.title[0:2] + new.author[0:2])
            candidate_serial = serial_alpha + serial_num

            # has the serial been used before?
            if candidate_serial not in self.serials.keys():
                unique = True

        # - ASSIGN THE NEW SERIAL TO BOOK -
        new.serial = candidate_serial

        # - MAP LIBRARY SERIAL TO BOOK -
        self.serials.update({new.serial: new})

        # - MAP LIBRARY AUTHOR(S) TO SERIAL -
        if new.author not in self.authors.keys():
            self.authors.update({new.author: new.serial})
        else:
            self.authors[new.author].append(new.serial)

        # - MAP LIBRARY TITLE(S) TO SERIAL -
        if new.title not in self.titles.keys():
            self.titles.update({new.title: new.serial})
        else:
            self.titles[new.title].append(new.serial)

    def delete_book(self, target) -> str:
        """
        Removes a book from the library, and stores it in the 'Recycle_Bin' JSON file.
            *** takes a serial number as an input parameter

        :param target: must be a book's serial number
        :return: the filename of the recycled book file
        """

        # - GET THE DELETION TARGET'S TITLE AND AUTHOR STRINGS -
        del_author = self.serials[target].author
        del_title = self.serials[target].title

        # - RECYCLE THE BOOK to a PICKLE FILE-
        #   *** Restoration NOTE: Pickle file will be named as the deleted book's serial number

        # create a binary output file - filename is the book serial number
        try:
            with open(f"{target}.pickle", 'wb') as outfile:
                pickle.dump(self.serials[target], outfile, protocol=pickle.HIGHEST_PROTOCOL)

        # $$$ TESTING $$$: provide info about errors
        except AttributeError:
            return 'FAIL-Attribute'
        except EOFError:
            return 'FAIL-EOF'
        except IndexError:
            return 'FAIL-Index'

        # - DELETE THE BOOK FROM COLLECTION -
        del self.serials[target]

        # - REMOVE THE BOOK AUTHOR FROM LIBRARY AUTHORS -
        del self.authors[del_author]

        # - REMOVE THE BOOK TITLE FROM LIBRARY TITLES -
        del self.titles[del_title]

        # - ADD THE BOOK TO THE RECYCLED LIST -
        #       KEY: the serial number / VALUE:  the filename
        self.recycled[target] = f"{target}.pickle"

        # return the name of the recycled file
        return f"{target}.pickle"

    def set_banner(self, message):
        """
        Sets the current banner to the 'message' parameter passed to this method
        :param message:
        :return:
        """

        self.banner = message

    def get_banner(self):
        """
        Returns the current banner with update information and admin notes, formatted with line boxing

        :return: a formatted updates banner as a string
        """

        if self.banner:
            output = '-----------------------------------------------------------------------------------\n'
            output += self.banner
            output += '-----------------------------------------------------------------------------------\n'
        else:
            output = False
        return output

    def keyword_search(self, mode, term) -> (bool or Book):
        """
        Takes a search term (term) and type of search(eg: title/author/isbn), returns any matching results.
            *** this feature is included to allow for partial term matching

        :param mode:
        :param term:
        :return:
        """

        pass

class Comment:
    def __init__(self, title, subject, text, question) -> (bool or None):
        """
        Defines an object to model a user comment

        :param title:       comment title
        :param subject:     comment subject
        :param text:        narrative text of comment
        :param question:    'True' if comment is a question, 'False' if just a comment.
        """

        self.title = title
        self.subject = subject
        self.text = text
        self.question = question            # True if question, False if Comment
        self.separator = '------------------------------'
        self.answer = None

    # ----- METHODS -----
    def show_question(self) -> str:
        """
        Builds a user-facing Question string and returns it
        :return: string
        """

        # build the parsed question entry
        shown = '\n' + self.separator + '\n'
        shown += f"TITLE: {self.title} \n"
        shown += f"SUBJECT: {self.subject} \n"
        shown += f"QUESTION: {self.text} \n"
        shown += f"ANSWER: {self.answer} \n"
        shown += self.separator + '\n'

        # return it
        return shown

    def show_comment(self) -> str:
        """
        Builds a user-facing Comment string and returns it
        :return: string
        """

        # build the parsed question entry
        shown = '\n' + self.separator + '\n'
        shown += f"TITLE: {self.title} \n"
        shown += f"SUBJECT: {self.subject} \n"
        shown += f"COMMENT: {self.text} \n"
        shown += self.separator + '\n'

        # return it
        return shown

    def get_subject(self) -> str:
        """
        Returns the object's subject attribute, agnostic of whether it's a question or comment

        :return: string of the subject
        """
        return self.subject

class Faq:
    def __init__(self, subject, question, answer) -> (bool or None):
        """
        Defines an object to model a user comment.
            *** FAQ number/serial not used, as the list in the help class storing them will handle that

        :param subject:
        :param question:
        :param answer:
        """

        self.subject = subject
        self.question = question
        self.answer = answer
        self.separator = '------------------------------'

    # ----- METHODS -----
    def show_faq(self):
        """
        Builds a cohesive FAQ entry, with top and bottom separators, and returns it.

        :return: a string representing a single formatted faq entry
        """

        # build the parsed faq entry
        shown = '\n' + self.separator + '\n'
        shown += f"SUBJECT: {self.subject} \n"
        shown += f"QUESTION: {self.question} \n"
        shown += f"ANSWER: {self.answer} \n"
        shown += self.separator + '\n'

        # return it
        return shown

    def get_subject(self) -> str:
        """
        Returns the object's subject attribute

        :return: string of the subject
        """
        return self.subject

    def get_question(self) -> str:
        """
        Returns the object's question attribute

        :return: string of the question
        """
        return self.question

    def get_answer(self) -> str:
        """
        Returns the object's answer attribute

        :return: string of the answer
        """
        return self.answer

class Help:
    def __init__(self):

        # --- ATTRIBUTES ---
        self.assist_level = 2                 # level of help offered to user (1 BASIC / 2 NORMAL / 3 ADVANCED)

        # --- FAQ LOAD: ---
        # access and load the faqs if there are any
        try:
            with open('faqs.pickle', "rb") as infile:
                self.faqs = pickle.load(infile)  # holds Faq objects

        # No faqs yet? make a blank list for them
        except FileNotFoundError:
            self.faqs = []

        # --- COMMENT LOAD: ---
        # access and load the comments if there are any
        try:
            with open('comments.pickle', "rb") as infile:
                self.comments = pickle.load(infile)  # holds Faq objects

        # No faqs yet? make a blank list for them
        except FileNotFoundError:
            self.comments = []

        # --- QUESTION LOAD: ---
        # access and load the questions if there are any
        try:
            with open('questions.pickle', "rb") as infile:
                self.questions = pickle.load(infile)  # holds Faq objects

        # No faqs yet? make a blank list for them
        except FileNotFoundError:
            self.questions = []

    # ----- METHODS -----
    def set_assist_level(self, level) -> None:
        """
        Set the level of user assistance
        :param level:
        :return: None
        """

        done = False
        while not done:
            if 0 < level < 4:
                self.assist_level = level
                done = True
            else:
                print(f"Level {level} is not valid, enter a level 1-3")

    def add_comment(self) -> (None or bool):
        """
        Adds a comment to the library comment base
        """
        title = input("What is the title of your comment?")
        subject = input("What is the subject of your comment?")
        text = input("Enter the text of your comment now, and press 'Enter' when done...")
        question = False

        # Build the new comment from above user input strings
        new_comment = Comment(title, subject, text, question)
        self.comments.append(new_comment)

        # Make Comment persistent by saving it
        try:
            with open(f"comments.pickle", 'wb') as outfile:
                pickle.dump(self.comments, outfile, protocol=pickle.HIGHEST_PROTOCOL)

        # $$$ TESTING $$$: provide info about errors
        except FileNotFoundError:
            return False

    def del_comment(self) -> None:
        """
        Deletes a user comment.
        :return:
        """

        # Display all comments by title
        print("COMMENTS:")
        print("---------")
        counter = 0
        for c in self.comments:
            print(f"{counter}) {c.title}")

        target = int(input("Enter the number of the comment you wish to delete: "))

        # Subtract 1 to account for 0-position in the array
        target -= 1

        print(f"The comment you've selected is : {self.comments[target]}")

        choice = input("To proceed with deletion, type 'delete' and press enter.  Any other input will cancel.")

        if choice == 'delete':
            del self.comments[target]
        else:
            return

    def add_question(self) -> (None or bool):
        """
        Adds a question to the library list of open questions
        """
        title = input("What is the title of your question?")
        subject = input("What is the subject of your question?")
        text = input("Enter the text of your question now, and press 'Enter' when done...")
        question = True

        # Build the question from user input
        new_question = Comment(title, subject, text, question)
        self.comments.append(new_question)

        # Make Comment persistent by saving it
        try:
            with open(f"questions.pickle", 'wb') as outfile:
                pickle.dump(self.questions, outfile, protocol=pickle.HIGHEST_PROTOCOL)

        # $$$ TESTING $$$: provide info about errors
        except FileNotFoundError:
            return False

    def del_question(self):
        """"""

        pass

    def list_faq_subs(self) -> None:
        """
        Prints a numbered list of all FAQ subjects
        :return: None
        """

        print("\n ----- Frequently Asked Questions -----\n")

        counter = 0
        for f in self.faqs:
            counter += 1
            print(f"{counter}) {f.get_subject()}")
        print("\n")

    def list_question_subs(self) -> None:
        """
        Prints a numbered list of all question subjects
        :return: None
        """

        print("\n ----- User Questions -----\n")

        counter = 0
        for q in self.questions:
            counter += 1
            print(f"{counter}) {q.get_subject()}")
        print("\n")

    def list_comment_subs(self) -> None:
        """
        Prints a numbered list of all comment subjects
        :return: None
        """

        print("\n ----- User Comments -----\n")

        counter = 0
        for c in self.comments:
            counter += 1
            print(f"{counter}) {c.get_subject()}")
        print("\n")

    def add_faq(self):
        """
        Adds a FAQ to the library comment base
        :return: None
        """

        # Build the FAQ from user input
        subject = input("What is the subject of this FAQ?")
        question = input("Please enter the question of your FAQ?")
        answer = input("Enter the answer to the question now, and press 'Enter' when done...")

        # Instantiate it into a new faq object
        new_faq = Faq(subject, question, answer)
        self.faqs.append(new_faq)

        # Make Faq persistent by saving it
        try:
            with open(f"faqs.pickle", 'wb') as outfile:
                pickle.dump(self.faqs, outfile, protocol=pickle.HIGHEST_PROTOCOL)

        # $$$ TESTING $$$: provide info about errors
        except AttributeError:
            return 'FAIL-Attribute'
        except EOFError:
            return 'FAIL-EOF'
        except IndexError:
            return 'FAIL-Index'

        return None

    def del_faq(self, num):
        """"""

        pass

class Pipeline:
    """
    This structure establishes a communication pipeline between the core UI/CMS and its plugin
    microservices.

    CALL:   pipeline.send('microservice recipient name string', data payload)
    RETURNS: whatever data the microservice replies with.
    """
    def __init__(self):
        """ Builds the initial address book for the pipeline communication services. """
        self.address_book = {
            'core': ('127.0.0.1', 20000),
            'auth': ('127.0.0.1', 20001),
            'profile': ('127.0.0.1', 20002),
            'accounting': ('127.0.0.1', 20003),
            'log': ('127.0.0.1', 20004)
        }

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

    def receive(self, service_name, rec_buffer=2048, max_connect=3, reply="ack"):
        """
        Takes a sender name listed in the address book as a string, then returns the
        :param service_name: the name of the microservice calling this class
        :param rec_buffer: default to 2048, this should not be changed
        :param max_connect: generally, 1 should be the max connections, 3 is more than enough
        :param reply: reply is the default reply from this method
        :return: the action mode and the decoded message data is returned
        """

        # Prepare variables
        data_decoded = None
        address = self.address_book[service_name]

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
                    data_decoded = str(data.decode())

                finally:
                    # Close connection to core
                    core_socket.close()

        finally:
            # Close the connection
            receive_socket.close()

            # Make the response available to the calling function
            return data_decoded


# ---------- Functions ----------

def title_banner() -> None:
    """Displays the program banner."""
    print("""\
    ***********************************************************
    * ____            _       _             _                 *
    */ ___|  ___ _ __(_)_ __ | |_ __ _ _ __(_)_   _ _ __ ___  *
    *\___ \ / __| '__| | '_ \| __/ _` | '__| | | | | '_ ` _ \ *
    * ___) | (__| |  | | |_) | || (_| | |  | | |_| | | | | | |*
    *|____/ \___|_|  |_| .__/ \__\__,_|_|  |_|\__,_|_| |_| |_|*
    * ____   ___   ___ |_|__  _                               *
    *|___ \ / _ \ / _ \ / _ \| |                              *
    *  __) | | | | | | | | | | |                              *
    * / __/| |_| | |_| | |_| |_|                              *
    *|_____|\___/ \___/ \___/(_)                              *
    ***********************************************************
    """)

def book_banner() -> None:
    """Prints ascii art of a bookshelf
        *** attribution given by initial per https://www.asciiart.eu/ use terms
    """
    print("""\
                    .--.           .---.        .-.
         .---|--|   .-.     | A |  .---. |~|    .--.
      .--|===|Ch|---|_|--.__| S |--|:::| |~|-==-|==|---.
      |%%|NT2|oc|===| |~~|%%| C |--|   |_|~|CATS|  |___|-.
      |  |   |ah|===| |==|  | I |  |:::|=| |    |GB|---|=|
      |  |   |ol|   |_|__|  | I |__|   | | |    |  |___| |
      |~~|===|--|===|~|~~|%%|~~~|--|:::|=|~|----|==|---|=|
      ^--^---'--^---^-^--^--^---'--^---^-^-^-==-^--^---^-'hjw
""")

def ShowMenu(choice, help_level):
    """
    Prints the menu specified to screen

    :param choice: which menu the user wants to see
    :param help_level: the user-set level of assistance they want
    :return:
    """

    mainMenu1 = """
        ---------- Main Menu ---------- 
        This is the main menu, please select from the options below:

        1) Add a book		        [add a new book to the collection]
        2) Delete a book		    [find and remove an existing book]
        3) Search for a book		[find an existing book and view its details]
        4) Help			            [if you are having trouble or questions]
        5) Exit			            [closes down the program]

        !!! NOTE1: you may type 'help' at any menu to be taken to the help menu
            NOTE2: you may type 'return' at any non-main menu to return to Main
        -----------
        """

    mainMenu = """
    ---------- Main Menu ---------- 
    This is the main menu, please select from the options below:

    1) Add a new book to the Library		        
    2) Delete a book from the Library		     
    3) Search for a book and view info		
    4) Help Menu			            
    5) Exit			            

    !!! NOTE1: you may type 'help' at any menu to be taken to the help menu
        NOTE2: you may type 'return' at any non-main menu to return to Main
    -----------
    """

    mainMenu3 = """
        ---------- Main Menu ---------- 
        This is the main menu, please select from the options below:

        1) Add a book		        
        2) Delete a book		    
        3) Search for a book		
        4) Help			            
        5) Exit			            

        # Help
        # Return
        -----------
        """

    addMenu1 = """
        -----------------------------------------------------------------------------------
        Add a Book: 
        Please fill in the book details below, you will be prompted for each, one at a time:

        ***Enter the book’s Information below…

        #Help			        [if you are having trouble or questions]
        #Return			        [returns to main menu]

        --------------------- BOOK INFORMATION --------------------- 
        Title:                  [Text title, spaces allowed]
        Author:                 [Text author, spaces allowed, capitalized or not]
        ISBN:                   [Enter as a number, without spaces or dashes]
        Publisher:              [Text name of the company who published the book]
        Publication Year:       [Numerical, 4-digit year which this edition of the book was published]
        Price:                  [3-digit monetary cost in American Dollars, without dollar sign]
        -----------------------------------------------------------------------------------
        """

    addMenu = """
    -----------------------------------------------------------------------------------
    Add a Book: 
    Please fill in the book details below:

    ***Enter the book’s Information below…

    #Help			[if you are having trouble or questions]
    #Return			[returns to main menu]

    --------------------- BOOK INFORMATION --------------------- 
    Title: 
    Author:
    ISBN:
    Publisher:
    Publication Year:
    Price:
    -----------------------------------------------------------------------------------
    """

    addMenu3 = """
        -----------------------------------------------------------------------------------
        Add a Book: 
        Please fill in the book details below:

        ***Enter the book’s Information below…

        #Help			
        #Return			
        """

    deleteMenu1 = """
        -----------------------------------------------------------------------------------
        Delete a Book: 
        Please choose how you wish to locate the book you wish to delete:

        1) Title		    [BASIC: keyword search for the book to delete by its Title]
        2) Author		    [BASIC: keyword search for the book to delete by its Author]
        3) Library S/N	    [ADVANCED: search for the book by its exact serial number]

        # Help			    [Questions, Leave Comments, FAQ's, change your menu settings]
        # Return			[returns to main menu]

        -----------
        Choice: 
        -----------------------------------------------------------------------------------
        """

    deleteMenu = """
    -----------------------------------------------------------------------------------
    Delete a Book: 
    Please choose how you wish to locate the book you wish to delete:

    1) Title                [BASIC: find by title keyword]
    2) Author		        [BASIC: find by author keyword]
    3) Library S/N	        [ADVANCED: find by full serial number]

    # Help Menu			        
    # Return to Main		        

    -----------
    Choice: 
    -----------------------------------------------------------------------------------
    """

    deleteMenu3 = """
        -----------------------------------------------------------------------------------
        Delete a Book: 
        Please choose how you wish to locate the book you wish to delete:

        1) Title		  
        2) Author		  
        3) Library S/N	  

        #Help Menu			
        #Return	to Main	

        -----------
        Choice: 
        -----------------------------------------------------------------------------------
        """

    searchMenu1 = """
        -----------------------------------------------------------------------------------
        Find a Book: 
        Please choose how you wish to locate the book, or type 'RecycleBin' to search for and
         recover recently deleted books:

        1) Title		        [BASIC: full or partial keyword search by book's Title]
        2) Author		        [BASIC: full or partial keyword search by book's Author]
        3) Library S/N	        [ADVANCED: exact, full serial number is required to be entered]

        #RecycleBin		[find/recover recently deleted books]
        #Help			[if you are having trouble or questions]
        #Return			[returns to main menu]

        -----------
        Choice: 
        -----------------------------------------------------------------------------------
        """

    searchMenu = """
    -----------------------------------------------------------------------------------
    Find a Book: 
    Please choose how you wish to locate the book, or type 'RecycleBin' for
     recently deleted books:

    1) Title Search		            [BASIC: keyword search]
    2) Author Search		        [BASIC: keyword search]
    3) Library S/N Search	        [ADVANCED: full serial number search]

    #RecycleBin		[find/recover recently deleted books]
    #Help			[if you are having trouble or questions]
    #Return			[returns to main menu]

    -----------
    Choice: 
    -----------------------------------------------------------------------------------
    """

    searchMenu3 = """
        -----------------------------------------------------------------------------------
        Find a Book: 
        Please choose how you wish to locate the book, or type 'RecycleBin' for
         recently deleted books:

        1) Title Search		        
        2) Author Search		        
        3) Library S/N Search        

        #RecycleBin / Un-delete		
        #Help			
        #Return to Main			

        -----------
        Choice: 
        -----------------------------------------------------------------------------------
        """

    helpMenu1 = """
        -----------------------------------------------------------------------------------
        Help Menu: 
        This is the help menu, please select from the options below:

        1) FAQ			                [QUICK ANSWERS: Frequently Asked Questions, answers posted]
        2) Leave a Comment		        [Write your own Comment for the Admin and other users]
        3) View User Comments	        [Read user comments]
        4) Ask a Question               [SLOW*: leave a question request for Admin/users to answer]
        5) Set Menu Assistance Level    [Choose how much help and instructions are on each menu
        6) Return to Main		        [returns to main menu]

        !!! NOTE: questions asked in option (4) ‘Leave a Comment’ may not
                  be answered quickly, and are only answered periodically by the Admin
                  or by others users.  For quick answers, check the FAQs.

        -----------
        Choice: 
        -----------------------------------------------------------------------------------
        """

    helpMenu = """
    -----------------------------------------------------------------------------------
    Help Menu: 
    This is the help menu, please select from the options below:

        1) FAQ			                   [QUICK / BASIC answers]
        2) Leave a Comment		            
        3) View User Comments	
        4) Ask a Question                  [SLOW / DETAILED answers]
        5) Set Menu Assistance Level       [SETTING: amount of instructions offered at each menu]
        6) Return to Main		

    !!! NOTE: questions asked in option (4) ‘Leave a Comment’ may take varying time to be answered.

    -----------
    Choice: 
    -----------------------------------------------------------------------------------
    """

    helpMenu3 = """
        -----------------------------------------------------------------------------------
        Help Menu: 
        This is the help menu, please select from the options below:

        1) FAQs			            
        2) Leave a Comment		
        3) View User Comments	
        4) Ask a Question      
        5) Set Menu Assistance Level     
        6) Return to Main		

        -----------
        Choice: 
        -----------------------------------------------------------------------------------
        """

    output = None

    if choice == 'main':
        if help_level == 1:
            output = mainMenu1
        if help_level == 2:
            output = mainMenu
        if help_level == 3:
            output = mainMenu3
    elif choice == 'add':
        if help_level == 1:
            output = addMenu1
        if help_level == 2:
            output = addMenu
        if help_level == 3:
            output = addMenu3
    elif choice == 'delete':
        if help_level == 1:
            output = deleteMenu1
        if help_level == 2:
            output = deleteMenu
        if help_level == 3:
            output = deleteMenu3
    elif choice == 'search':
        if help_level == 1:
            output = searchMenu1
        if help_level == 2:
            output = searchMenu
        if help_level == 3:
            output = searchMenu3
    elif choice == 'help':
        if help_level == 1:
            output = helpMenu1
        if help_level == 2:
            output = helpMenu
        if help_level == 3:
            output = helpMenu3

    # User Input Error
    else:
        output = 'invalid choice'

    # display the menu chosen at the correct level of help
    print(output)

# ---------- Main: User Interface ----------
def main():
    """
    USER INTERFACE:
        This function provides the main user interface to the Library

    OBJECT INSTANTIATION:
        This function instantiates the objects that will be called and used in the overall system

    DATA LOAD:
        This function results in persistent data being loaded into the Library
    """

    # Print the title banner
    title_banner()

    # ----- DATA LOAD -----
    # access and load the collection if one exists
    try:
        with open('library.pickle', "rb") as infile:
            collection = pickle.load(infile)

    # No library yet? make a blank Library Object for it
    except FileNotFoundError:
        collection = Library()

    # ----- OBJECT INSTANTION -----
    # Initialize the help system
    help_sys = Help()

    # print the updates banner
    if collection.get_banner():
        print(collection.get_banner())
    else:
        print("    ---------------------------")
        print("    ---      NO UPDATES     ---")
        print("    ---------------------------")

    # ----- USER INTERFACE -----
    # Initiate the main program loop
    choice = None

    while choice != '5':

        # print the main menu
        ShowMenu('main', help_sys.assist_level)

        choice = input("Choice:  ")

        # --- Catch help requests ---
        if choice == 'help':
            choice = '4'

        # --- ADD A BOOK ---
        if choice == '1':
            # Book parameters: [title, author, isbn, year, publisher, price]

            # Print the 'Add a Book' Menu
            ShowMenu('add', help_sys.assist_level)

            # reference Menu for this option
            """
            Add a Book: 
            Please fill in the book details below:
        
            ***Enter the book’s Information below…
        
            #Help			[if you are having trouble or questions]
            #Return			[returns to main menu]
                    --------------------- BOOK INFORMATION --------------------- 
            Title: 
            Author:
            ISBN:
            Publisher:
            Publication Year:
            Price:
            -----------------------------------------------------------------------------------"""

            title = input("Please enter the Book's Title:  ")
            author = input("Please enter the Book's Author:  ")
            isbn = int(input("Please enter the Book's ISBN (without dashes):  "))
            pub = input("Please enter the Book's Publisher:  ")
            year = int(input("Please enter the Book's publication year:  "))
            price = float(input("Please enter the Book's price without $ sign (ex: 5.25):  $"))

            # Create a new book and add it to the Library collection
            collection.add_book(Book(title, author, isbn, pub, year, price))

            print("Book entered and recorded, thank you!")
            print("-----------------------------------------------------------------------------------\n \n")
            continue

        # --- DELETE A BOOK ---
        elif choice == '2':

            # reference Menu for this option:
            """
            Delete a Book: 
            Please choose how you wish to locate the book you wish to delete:
        
            1) Title		    []
            2) Author		    []
            3) Library S/N	    []
        
            #Help			[if you are having trouble or questions]
            #Return			[returns to main menu]"""

            # CHOICE LOOP
            while True:
                # Show the user the Deletion menu
                ShowMenu('delete', help_sys.assist_level)

                # Prompt the user to select from this menu
                selection = int(input("Choice:  "))

                # Reset variables
                match = None
                matches = None

                # HELP
                if selection == ('Help' or 'help' or 'HELP' or '#Help'):
                    print("Returning to Main menu...choose option #4...")
                    break

                # RETURN TO MAIN
                if selection == ('Return' or 'return' or '#Return'):
                    # return to main menu
                    break

                # TITLE SEARCH
                if selection == 1:
                    search_term = input("Type the title, or partial title: ")
                    matches = [sn for titles, sn in collection.titles.items() if search_term in titles]

                # AUTHOR SEARCH
                elif selection == 2:
                    search_term = input("Type the Author name, or partial name: ")
                    matches = [sn for authors, sn in collection.authors.items() if search_term in authors]

                # SERIAL SEARCH
                elif selection == 3:
                    search_term = input("Type the exact Library serial number of the book to delete:  ")
                    match = collection.serials[search_term]

                # ERROR
                else:
                    # notify user of mistake, and allow them to re-enter their choice
                    print('Invalid selection, try again...')
                    continue

                # RESULTS
                if match:
                    print("Is the book below the one you wish to delete? (1: yes / 2: no ")
                    match.view()
                    doom = int(input())
                    if doom == 1:
                        recycle = input("Are you SURE you want to delete it? Type 'delete' to confirm")
                        if recycle == 'delete':
                            collection.delete_book(match.get_serial())
                            print("Deletion confirmed!")
                            print("Book will remain in recycle bin for a limited time, and can be"
                                  "recovered by performing a Book Search of recycled books.")

                            # Return to main
                            break

                # Display matching books to user
                print("Your search yielded the following results: \n")

                # 'order' assigns a 1-up number to each book in the list to aid in identification
                order = 0
                if matches:
                    for i in matches:
                        print(f"BOOK NUMBER {order+1}")

                        collection.book_by_serial(i).view()
                        print("\n")
                        order += 1

                    found_it = int(input("Is the book you're looking for in the results? (1: yes / 2: no)  "))
                    if found_it == 1:
                        doom = int(input("Enter the BOOK NUMBER of the book you wish to delete: "))
                        print("This is the book title you have selected: \n")
                        print(collection.book_by_serial(matches[doom-1]).get_title())
                        recycle = int(input("Is this the book you want to delete? (1: yes / 2: no)"))
                        if recycle == 1:
                            confirm = input("Are you SURE you want to delete it? Type 'delete' to confirm:  \n")
                            if confirm == 'delete':
                                collection.delete_book(matches[doom-1])
                                print("Deletion confirmed!")
                                print("Book will remain in recycle bin for a limited time, and can be "
                                      "recovered by performing a Book Search of recycled books.")

                                # Return to main
                                break
                        else:
                            where_now = int(input("Whew, close one! Where to now? (1: main / 2: try again)"))
                            if where_now == 1:
                                break
                            else:
                                continue

                else:
                    print("(No books found matching your terms)")
                    try_again = int(input("Try another search to delete? (1: yes / 2: no)"))
                    if try_again == 1:
                        # back to choice loop: how to find book to delete
                        continue
                    else:
                        # Return to main
                        break

                # return to main
                break

            # feed back into the Main menu
            continue

        # --- SEARCH FOR BOOK---
        elif choice == '3':
            # CHOICE LOOP
            while True:
                # Show the user the Search menu
                ShowMenu('search', help_sys.assist_level)

                # Prompt user to select from menu
                selection = input("Choice:  ")

                # Reset variables
                match = None
                matches = None

                # HELP
                if selection == ('Help' or 'help' or 'HELP' or '#Help'):
                    print("Returning to Main menu...choose option #4...")
                    break

                # RETURN TO MAIN
                if selection == ('Return' or 'return' or '#Return'):
                    # return to main menu
                    break

                #              _____ ----- !!!!! UNDER CONSTRUCTION !!!!! ----- _____
                # ACCESS RECYCLE BIN
                if selection == ('RecycleBin' or 'recyclebin' or 'Recyclebin' or '#RecycleBin'):
                    pickled_files = os.listdir()

                    # Find all pickled files in local directory of UI/CMS Monolith
                    pickled_only = []
                    for f in pickled_files:
                        if f.endswith(".pickle"):
                            pickled_only.append(f)

                    # Present user with available recycled files
                    print("You are accessing recycled books.  Recycle Bin contents are: \n")

                    # list all pickle files
                    counter = 0
                    for f in pickled_only:
                        counter += 1
                        print(f"[File # {counter}: {f}")

                    # prompt user to select a recycled book or return to main
                    found = int(input("Enter File # to select/recover a file, or enter '0' to return to Main Menu\n"))
                    if found == 0:
                        continue
                    else:
                        # access and load the specified recycled pickle file
                        try:
                            with open(pickled_only[found - 1], "rb") as infile:
                                recover_file = pickle.load(infile)

                        # $$$ TESTING $$$: provide info about errors
                        except AttributeError:
                            return 'FAIL-Attribute'
                        except EOFError:
                            return 'FAIL-EOF'
                        except IndexError:
                            return 'FAIL-Index'

                        # Show the book recovery candidate to the user
                        print(f"You have accessed the following book Title: \n")
                        recover_file.view()

                        # Confirm user wishes to recover this book
                        confirm = input("To recover this book to the library, type 'recover', else hit 'enter': ")

                        # RECOVER RECYCLED FILE TO COLLECTION
                        if confirm == 'recover':

                            # insert the book back into the collection
                            collection.insert_book(recover_file)
                            print("SUCCESSFUL RECOVERY!")

                            # delete the recovered pickle file
                            print(f"deleting {recover_file.get_serial()}.pickle...")
                            os.remove(f"{recover_file.get_serial()}.pickle")

                        else:
                            continue

                # TITLE SEARCH
                if selection == '1':
                    search_term = input("Type the title, or partial title of the book you want to find: ")
                    matches = [sn for titles, sn in collection.titles.items() if search_term in titles]

                # AUTHOR SEARCH
                elif selection == '2':
                    search_term = input("Type the Author name, or partial name of the book you want to find: ")
                    matches = [sn for authors, sn in collection.authors.items() if search_term in authors]

                # SERIAL SEARCH
                elif selection == '3':
                    search_term = input("Type the exact Library serial number of the book you want to find:  ")
                    if search_term in collection.serials.keys():
                        match = collection.serials[search_term]
                    else:
                        input("Serial not found, press 'enter' to continue...")
                        continue

                # ERROR
                else:
                    # notify user of mistake, and allow them to re-enter their choice
                    print('Invalid selection, try again...')
                    continue

                # SEARCH RESULTS
                if match:
                    print("Is the book below the one you are looking for? (1: yes / 2: no ")
                    match.get_title()
                    found = int(input())
                    if found == 1:
                        print("ACQUISITION CONFIRMED! Displaying your book now...\n")
                        match.view()
                        input("Press 'enter' to return to the main menu... ")
                        break

                # Display matching books to user
                print("Your search yielded the following results: \n")

                # 'order' assigns a 1-up number to each book in the list to aid in identification
                order = 0
                if matches:
                    for i in matches:
                        print(f"BOOK NUMBER {order + 1}")
                        collection.book_by_serial(i).view()
                        print("\n")
                        order += 1

                    found_it = int(input("Is the book you're looking for in the results? (1: yes / 2: no)  "))
                    if found_it == 1:
                        acquired = int(input("Enter the BOOK NUMBER of the book you want to view: "))
                        print("This is the book title you have selected: \n")
                        print(collection.book_by_serial(matches[acquired - 1]).get_title())
                        acquisition = int(input("Is this the book you want to view? (1: yes / 2: no)"))
                        if acquisition == 1:
                            print("Displaying your book information now...\n")
                            collection.book_by_serial(matches[acquired - 1]).view()
                            input("\nPress 'enter' to return  to the main menu")
                            break

                        # This is not the book you want to view...what now?
                        else:
                            where_now = int(input("Ok. Where to now? (1: main / 2: search again)"))
                            if where_now == 1:
                                break
                            else:
                                continue
                    # Book not in results...what to do...
                    else:
                        where_now = int(input("Ok. Where to now? (1: main / 2: search again)"))
                        if where_now == 1:
                            break
                        else:
                            continue

                else:
                    print("(No books found matching your terms)")
                    try_again = int(input("Search again? (1: yes / 2: no)"))
                    if try_again == 1:
                        # back to choice loop: how to find book to delete
                        continue
                    else:
                        # Return to main
                        break

            # feed back into the Main menu
            continue

        # --- GET HELP ---
        elif choice == '4':
            """Help Menu: 
                This is the help menu, please select from the options below:
                    1) FAQs			            
                    2) Leave a Comment		
                    3) View User Comments	
                    4) Ask a Question      
                    5) Set Menu Assistance Level     
                    6) Return to Main"""

            # CHOICE LOOP
            while True:
                # Show the user the Search menu
                ShowMenu('help', help_sys.assist_level)

                # Prompt user to select from menu
                selection = int(input("Choice:  "))

                # --- FAQ ---
                if selection == 1:

                    add_view = int(input("Enter '1' to view FAQs or '2' to add a FAQ"))
                    if add_view == 1:
                        help_sys.list_faq_subs()

                        # Prompt the user to choose a faq to read
                        this_one = int(input("Enter the number of the FAQ you wish to read"))

                        # Adjust the number down one to align to the faq 0-up list numbering
                        this_one -= 1

                        # account for blank faqs list
                        if len(help_sys.faqs) < 1:
                            print("No FAQs found!")
                            continue
                        else:
                            # Display the FAQ
                            print(help_sys.faqs[this_one].show_faq())

                        # Prompt the user to press enter when done
                        input("Press enter when done...")
                        continue
                    elif add_view == 2:
                        help_sys.add_faq()

                    else:
                        continue

                # --- ADD COMMENT ---
                elif selection == 2:
                    help_sys.add_comment()

                # --- READ COMMENTS ---
                elif selection == 3:
                    help_sys.list_comment_subs()

                    # Prompt the user to choose a comment to read
                    this_one = int(input("Enter the number of the comment you wish to read"))

                    # Adjust the number down one to align to the faq 0-up list numbering
                    this_one -= 1

                    # account for blank faqs list
                    if len(help_sys.comments) < 1:
                        print("No FAQs found!")
                        continue
                    else:
                        # Display the FAQ
                        print(help_sys.comments[this_one].show_comment())

                    # Prompt the user to press enter when done
                    input("Press enter when done...")
                    continue

                # --- ASK QUESTION ---
                elif selection == 4:
                    help_sys.add_question()

                # --- SET ASSISTANCE LEVEL ---
                elif selection == 5:
                    choice = int(input("Enter the level (1-3) of help you want to receive at each menu...\n"
                                       "(1) = Lots of help \n(2) = Default help \n(3) = No help"))
                    help_sys.set_assist_level(choice)

                # --- RETURN TO MAIN ---
                elif selection == 6:
                    choice = None
                    break

                # INVALID - choose again
                else:
                    continue

        # --- SAVE and EXIT ---
        elif choice == '5':
            # Save library state and exit

            # Create a new library if not present
            try:
                with open(f"library.pickle", 'wb') as outfile:
                    pickle.dump(collection, outfile, protocol=pickle.HIGHEST_PROTOCOL)

            # $$$ TESTING $$$: provide info about errors
            except FileNotFoundError:
                print("ERROR SAVING LIBRARY!!!")
                return False

            print("Goodbye!")
            break


# Execute Program
if __name__ == '__main__':
    main()

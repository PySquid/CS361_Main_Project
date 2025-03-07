# MainUI.py
# Author: Philip Sheridan
# Class: CS361 / Oregon State University
# Description: Provides User Interface for Main Project, also serves as a mini monolith content manager

# ---------- Imports ----------
import pickle
import random
import os
import time
from Pipeline import Pipeline
from datetime import datetime as dt
from datetime import timedelta as delta

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
        self.checked_out = False

    # ----- METHODS -----
    def get_info(self):
        """Returns the book's main attributes as a dictionary"""

        return({'title': self.title, 'author': self.author, 'isbn': self.isbn, 'serial': self.serial, 'year': self.year,
                'publisher': self.publisher, 'price': self.price, 'rating': self.rating,
                'summary': self.summary, 'checked_out': self.checked_out})

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
        if self.checked_out:
            print(f"Checked out? ... YES")
        else:
            print(f"Checked out? ... NO")

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
        Takes a book as a parameter, then adds the book to the collection, de-conflicting the serial as well
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

    def checkout(self, sn):
        """ Updates a book in self.serials to set checkout to True. """
        self.serials[sn].checkout = True

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

def ShowMenu(choice, help_level=2):
    """
    Prints the menu specified to screen

    :param choice: which menu the user wants to see
    :param help_level: the user-set level of assistance they want
    :return:
    """

    loginMenuStart = """
    --------------------------------- USER LOGIN --------------------------------------
        This is the login menu for the Library.  Choose from the options below:
        
        1) Login                [Enter your username and password, if you already have them]
        2) Create Account       [If you do not yet have a user name and password]
        3) Exit Program         [Terminate your session]
    """

    loginMenuEnd = """
    ----------------------------------------------------------------------------------- 
    """

    mainMenu1 = """
        ---------- Main Menu ---------- 
        This is the main menu, please select from the options below:

        1) Use Profile		        [View and edit your user profile information]
        2) User Account		        [View your financial balances, checked-out books, and due dates]
        3) Book Search	        	[find books, recover deleted books, and check out books]
        4) Help			            [if you are having trouble or questions]
        5) Exit			            [saves all settings and closes down the program]

        !!! NOTE1: you may type 'help' at any menu to be taken to the help menu
            NOTE2: you may type 'return' at any non-main menu to return to Main
        -----------
        """

    mainMenu = """
        ---------- Main Menu ---------- 
        This is the main menu, please select from the options below:

        1) Use Profile		        [View and edit]
        2) User Account		        [Finance & checked out books]
        3) Book Search	        	[find books and check out books]
        4) Help			            [trouble or questions]
        5) Exit			            [save state and exit]

        !!! NOTE1: you may type 'help' at any menu to be taken to the help menu
        NOTE2: you may type 'return' at any non-main menu to return to Main
        -----------
        """

    mainMenu3 = """
        ---------- Main Menu ---------- 
        This is the main menu, please select from the options below:

        1) Use Profile
        2) User Account
        3) Book Search
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

    profileMenu1 = """
        -----------------------------------------------------------------------------------
        Profile Settings Menu: 
        This is the settings menu, please select from the options below:

        1) View User Profile    [View your settings for all your profile information]
        2) Edit User Profile    [Change: Name, Age, Address, Phone, Email, Library Card Number, and more
        3) Return to Main Menu		

        -----------
        Choice: 
        -----------------------------------------------------------------------------------
        """

    profileMenu = """
        -----------------------------------------------------------------------------------
        Profile Settings Menu: 
            This is the settings menu, please select from the options below:

        1) View User Profile        [see your profile settings]
        2) Edit User Profile        [change your profile settings]
        3) Return to Main Menu	

        -----------
        Choice: 
        -----------------------------------------------------------------------------------
        """

    profileMenu3 = """
        -----------------------------------------------------------------------------------
        Profile Settings Menu: 
        This is the settings menu, please select from the options below:

        1) View User Profile
        2) Edit User Profile
        3) Return to Main Menu		

        -----------
        Choice: 
        -----------------------------------------------------------------------------------
        """

    accountMenu1 = """
            -----------------------------------------------------------------------------------
            Account Settings Menu: 
                This is the settings menu, please select from the options below:

            1) Check book in            [Choose (from list) and return a book you have checked out]
            2) View checked-out books   [View the books you have checked out, and due dates]
            3) Return to Main Menu	

            -----------
            Choice: 
            -----------------------------------------------------------------------------------
            """

    accountMenu = """
            -----------------------------------------------------------------------------------
            Account Settings Menu: 
                This is the settings menu, please select from the options below:

            1) Check book in             [Checked out books will be listed to choose from]
            2) View checked-out books    [titles and due dates]
            3) Return to Main Menu	

            -----------
            Choice: 
            -----------------------------------------------------------------------------------
            """

    accountMenu3 = """
            -----------------------------------------------------------------------------------
            Account Settings Menu: 
                This is the settings menu, please select from the options below:

            1) Check a book back in
            2) View checked-out books
            3) Return to Main Menu	

            -----------
            Choice: 
            -----------------------------------------------------------------------------------
            """

    adminMenu = """
                ---------- Main Menu ---------- 
            ======== ADMINISTRATOR ACCESS ONLY ========
            
            This is the administrator menu, please select from the options below:

            1)  Use Profile
            2)  User Account
            3)  Book Search
            4)  Help
            5)  Exit
            6)  Add a Book
            7)  Delete a Book
            8)  Delete user account
            9)  View Logs
            10) Delete Logs		            

            # Help
            # Return
            -----------
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
    elif choice == 'account':
        if help_level == 1:
            output = accountMenu1
        if help_level == 2:
            output = accountMenu
        if help_level == 3:
            output = accountMenu3
    elif choice == 'profile':
        if help_level == 1:
            output = profileMenu1
        if help_level == 2:
            output = profileMenu
        if help_level == 3:
            output = profileMenu3
    elif choice == 'admin':
        output = adminMenu
    elif choice == 'loginA':
        output = loginMenuStart
    elif choice == 'loginB':
        output = loginMenuEnd

    # User Input Error
    else:
        output = 'invalid choice'

    # display the menu chosen at the correct level of help
    print(output)

def create_profile(pipe, username):
    """ Gets a user's profile information from them and creates the profile. """

    # --- INITIAL PROFILE CREATION (quick or custom) ---
    print("You may create a user profile now...")
    print("PROFILE CREATION OPTIONS:")
    print("-------------------------")
    print("""1) Quick Profile         [only enter minimum required data, may edit later]
             2) Custom Profile        [enter full profile data now]\n""")
    new_prof_type = input("Choice: ")

    # Prep the profile creation data...
    create_msg = {'action': 'create_user', 'u_name': username}

    # --- QUICK ---
    if new_prof_type == '1':
        create_msg['first_name'] = input("Enter your first name: ")
        create_msg['last_name'] = input("Enter your last name: ")
        create_msg['age'] = ""
        create_msg['address'] = ""
        create_msg['phone'] = input("Enter your phone number: ")
        create_msg['email'] = ""

    # --- CUSTOM ---
    elif new_prof_type == '2':
        print("Custom profile chosen...creating now...")
        create_msg['first_name'] = input("Enter your first name: ")
        create_msg['last_name'] = input("Enter your last name: ")
        create_msg['age'] = input("Enter your age: ")
        create_msg['address'] = input("Enter your full address: ")
        create_msg['phone'] = input("Enter your phone number: ")
        create_msg['email'] = input("Enter your full email: ")

    # Tell the Profile service to create a new profile with the above data (no reply)
    pipe.send('profile', create_msg)
    return create_msg

def authenticate(request) -> bool:
    """ Consults the Authentication microservice (service A) and returns True for verified account"""

    # Authentication either returns TRUE or FALSE
    with open('auth_request_file.txt', "w") as file:
        file.write(request)
    # Wait for the microservice to process the request
    time.sleep(2)  # Increase the delay to ensure the microservice has time to process

    # Wait for the response file to be created
    while not os.path.exists('auth_response_file.txt'):
        time.sleep(0.5)  # Wait for the response file to appear

    # Read the response from the response file
    with open('auth_response_file.txt', "r") as file:
        response = file.read().strip()

    # Clear the response file after reading
    with open('auth_response.txt', "w") as file:
        file.write("")  # Clear the file contents

    # convert text result to boolean value
    print(f"response is {response}")
    if response == "SUCCESS":
        determination = True
    else:
        determination = False

    return determination

def login(pipe):
    """ Logs a user in, creates new account and profile if absent."""

    # Authenticate the user, then load their profile
    while True:
        ShowMenu('loginA')
        login_choice = str(input())
        print(" ")

        # ----- EXISTING ACCOUNT -----
        if login_choice == '1':
            print("---------- LOG INTO EXISTING ACCOUNT ----------")
            u_name = input("\tUSER NAME: ")
            password = input("\tPASSWORD: ")

            # Format the login message to the Authenticate Service
            login_request = f"LOGIN {u_name} {password}"

            # Consult MicroserviceA/Authentication - True or False...
            check_account = authenticate(login_request)

            if check_account:
                # Authentication microservice has verified a username-password match...login complete
                print("SUCCESSFUL LOGIN...YOU MAY PROCEED...")

                ShowMenu('loginB')
                return {'u_name': u_name, 'password': password}
            else:
                # User not verified, return to login menu
                print("INVALID CREDENTIALS, OR USER NOT FOUND...TRY AGAIN")
                continue

        # ----- NEW ACCOUNT -----
        elif login_choice == '2':
            print("---------- CREATE NEW ACCOUNT ----------")
            new_user = input("Enter your username (5-20 characters and/or numbers)")
            new_pass = input("Enter your password (5-20 characters and/or numbers")

            # Format the login message to the Authenticate Service
            signup_request = f"SIGNUP {new_user} {new_pass}"

            # Authentication either returns TRUE or FALSE
            created_account = authenticate(signup_request)

            if created_account:
                # Authentication microservice has verified creation of new username/password account
                print("SUCCESSFULLY CREATED NEW ACCOUNT...YOU MAY PROCEED...")

                create_profile(pipe, new_user)

                # Give the profile service time to process
                time.sleep(3)

                return {'u_name': new_user, 'password': new_pass}

            else:
                # User not verified, return to login menu
                print("USERNAME ALREADY EXISTS, OR IMPROPERLY ENTERED NAME/PASS...TRY AGAIN")
                continue

        # ----- NEW ACCOUNT -----
        elif login_choice == '3':
            return False

        else:
            # User entered something other than a 1 or 2
            print("INVALID CHOICE, ENTER A '1' OR A '2'...")
            continue

def fetch_profile_printout(pipe, username) -> str:
    """Takes a username, and returns the user's profile as a string. """

    data = {'action': 'get_user_info', 'user_name': username}
    pipe.send('profile', data)
    reply = pipe.receive()

    if reply == 'ERROR':
        return 'ERROR'
    else:
        return reply

def fetch_profile(pipe, username) -> dict or bool:
    """ Fetches a dictionary of all profile attributes from the profile service. """
    data = {'action': 'get_user_dict', 'user_name': username}
    pipe.send('profile', data)
    reply = pipe.receive()

    if reply == 'ERROR':
        return False
    else:
        return reply

def delete_profile(pipe, username) -> bool:
    """ Deletes a user profile in the profile service, returns True if successful, False if not so. """
    del_msg = {'action': 'delete_user', 'user_name': username}
    reply = pipe.send('profile', del_msg)
    if reply == 'DELETED':
        return True
    else:
        return False

def edit_profile(pipe, username, old, new) -> None:
    """ Sends a change order for a user to the Profile Microservice. """

    data = {'action': 'edit_user', 'user_name': username, 'attribute': old, 'new_value': new}
    pipe.send('profile', data)

def check_book_out(pipe, username, serial) -> str:
    """ Checks out  a book using the Accounting microservice. """

    message = {'action': 'check_out', 'user': username, 'sn': serial}
    pipe.send('accounting', message)
    return pipe.receive()

def check_book_in(pipe, username, serial) -> None:
    """ Checks out  a book using the Accounting microservice. """

    message = {'action': 'check_in', 'user': username, 'sn': serial}
    pipe.send('accounting', message)

def get_checkouts(pipe, username) -> dict:
    """ Takes a user, gets their checked out books from Accounting microservice, returns them. """

    message = {'action': 'get_checkouts', 'user': username}
    pipe.send('accounting', message)
    reply = pipe.receive()
    return reply

def print_checkouts(pipe, username, collection) -> list:
    """ Prints a user's checked out books and returns a list of their serials"""
    print(" You have checked out the following books from the Library: ")
    print("-------------------------------------------------------------")
    checkouts = get_checkouts(pipe, username)  # dict: {sn: due date}

    checkout_list = []  # list of serials
    for key in checkouts.keys():
        checkout_list.append(key)

    number = 0
    for sn in checkout_list:
        number += 1
        title = collection.book_by_serial(sn).get_title()
        print(f"{number}: {title} | (due on {checkouts[sn]})")
    print("-------------------------------------------------------------")
    return checkout_list

def save_data(data) -> None:
    # Save the change to persistent data structure
    try:
        with open(f"library.pickle", 'wb') as outfile:
            pickle.dump(data, outfile, protocol=pickle.HIGHEST_PROTOCOL)

    # $$$ DEBUGGING $$$: provide info about errors
    except FileNotFoundError:
        print("ERROR SAVING Library data!!!")

def log_event(pipe, user, trigger):
    """ Sends a user and action with date to the logging microservice to be recorded. """
    message = {'action': 'log', 'log':{'user': user, 'trigger': trigger}}
    pipe.send('log', message)

def view_log(pipe, days_past) -> None:
    """ Displays the log for a day, delineated by the number of days in the past from today. """
    if type(days_past) != int:
        days_past = int(days_past)
    message = {'action': 'view', 'days_past': days_past}
    pipe.send('log', message)
    report = pipe.receive()
    print("------------------- LOG VIEWER -------------------------")
    print(report)
    print("--------------------------------------------------------")

# ---------- Main: User Interface ----------
def main():
    """
    DATA LOAD:
        This function results in persistent data being loaded into the Library

    OBJECT INSTANTIATION:
        This function instantiates the objects that will be called and used in the overall system

    LOGIN:
        This calls the user login microservice

    USER INTERFACE:
        This function provides the main user interface to the Library
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

    # ----- OBJECT INSTANTIATION -----
    # Initialize the help and Microservice communications systems
    help_sys = Help()
    pipe = Pipeline('core')

    # ----- LOGIN  -----
    logged_in_user = login(pipe)
    if not logged_in_user:
        # User exited program at login screen
        return
    log_event(pipe, logged_in_user['u_name'], 'LOGGED IN')

    # ----- PROFILE -----
    current_profile = fetch_profile(pipe, logged_in_user['u_name'])

    # update menu assist level from user profile if set
    if current_profile['assist'] is not None:
        help_sys.assist_level = current_profile['assist']

    # print the updates banner
    if collection.get_banner():
        print(collection.get_banner())
    else:
        print(f"Welcome {current_profile['first_name']}!")
        print("    ---------------------------")
        print("    ---      NO UPDATES     ---")
        print("    ---------------------------")

    # ----- USER INTERFACE -----
    # Initiate the main program loop
    choice = None

    while choice != '5':

        # print the main menu, according to which user is logged in
        if logged_in_user['u_name'] == 'admin':
            ShowMenu('admin', help_sys.assist_level)
        else:
            ShowMenu('main', help_sys.assist_level)

        choice = input("Choice:  ")

        # --- Catch help requests ---
        if choice == ('HELP' or 'Help' or 'help'):
            choice = '4'

        # --- PROFILE ACCESS ---
        elif choice == '1':

            """ (Menu appearance and user-facing options Reference)
            
            1) View User Profile        [see your profile settings]
            2) Edit User Profile        [change your profile settings]
            3) Return to Main Menu
            """

            # CHOICE LOOP
            while True:
                # Show the user the Search menu
                ShowMenu('profile', help_sys.assist_level)

                # Prompt user to select from menu
                selection = input("Choice:  ")

                # HELP
                if selection == ('Help' or 'help' or 'HELP' or '#Help'):
                    print("Returning to Main menu...choose option #4...")
                    break

                # RETURN TO MAIN
                elif selection == ('Return' or 'return' or '#Return'):
                    # return to main menu
                    break

                # VIEW PROFILE
                elif selection == '1':
                    log_event(pipe, logged_in_user['u_name'], 'VIEWED PROFILE')
                    reply = fetch_profile_printout(pipe, logged_in_user['u_name'])
                    print(f"\n{reply}\n")
                    continue

                # EDIT PROFILE
                elif selection == '2':
                    log_event(pipe, logged_in_user['u_name'], 'EDITED PROFILE')
                    print("""
                    Enter the number of the setting you want to change:
                        1) first name
                        2) last name
                        3) age
                        4) address
                        5) phone
                        6) email
                        7) default menu assist level
                     """)
                    change_this = input()

                    print(" ")

                    to_this = input("Enter the new value for this profile setting: ")
                    if change_this == '1':
                        change_this = 'first_name'
                    elif change_this == '2':
                        change_this = 'last_name'
                    elif change_this == '3':
                        change_this = 'age'
                    elif change_this == '4':
                        change_this = 'address'
                    elif change_this == '5':
                        change_this = 'phone'
                    elif change_this == '6':
                        change_this = 'email'
                    elif change_this == '7':
                        change_this = 'assist'
                    else:
                        print("ERROR, try again")
                        continue

                    edit_profile(pipe, logged_in_user['u_name'], change_this, to_this)

                # RETURN TO MAIN
                else:
                    break

        # --- ACCOUNT ACCESS ---
        elif choice == '2':
            """
            menu reference:
            
            1) Check book in             [Checked out books will be listed to choose from]
            2) View checked-out books    [titles and due dates]
            3) Return to Main Menu
            """
            # CHOICE LOOP (accounts)
            while True:
                # Show the user the Search menu
                ShowMenu('account', help_sys.assist_level)

                # Prompt user to select from menu
                selection = input("Choice:  ")

                # HELP
                if selection == ('Help' or 'help' or 'HELP' or '#Help'):
                    print("Returning to Main menu...choose option #4...")
                    break

                # RETURN TO MAIN
                if selection == ('Return' or 'return' or '#Return'):
                    # return to main menu
                    break

                # Check book back in
                if selection == '1':
                    log_event(pipe, logged_in_user['u_name'], 'CHECKED IN BOOK')

                    checked = print_checkouts(pipe, logged_in_user['u_name'], collection)
                    in_target = int(input("Enter the number of the book to check back in..."))
                    in_target -= 1      # adjust to align to array/list index 0
                    if (in_target < len(checked)) and (in_target >= 0):
                        collection.serials[checked[in_target]].checked_out = False
                        check_book_in(pipe, logged_in_user['u_name'], checked[in_target])
                    else:
                        print("ERROR: book chosen does not exist! Try again...")
                        continue

                # View checked out books
                elif selection == '2':
                    log_event(pipe, logged_in_user['u_name'], 'VIEWED CHECKED OUT BOOKS')

                    print_checkouts(pipe, logged_in_user['u_name'], collection)

                # Return to main menu
                elif selection == '3':
                    break

            # feed back into the Main menu
            continue

        # --- SEARCH FOR BOOK---
        elif choice == '3':
            log_event(pipe, logged_in_user['u_name'], 'SEARCHED FOR BOOK')
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

                        # Provide info about errors
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
                            log_event(pipe, logged_in_user['u_name'], 'RECOVERED A BOOK')

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

                # SEARCH RESULT for Serial search
                if match:
                    print("Is the book below the one you are looking for? (1: yes / 2: no ")
                    match.get_title()
                    found = int(input())
                    if found == 1:
                        print("ACQUISITION CONFIRMED! Displaying your book now...\n")
                        match.view()

                        # --- CHECK OUT BOOK? ---
                        if match.checked_out:
                            input("Press 'enter' to return to the main menu... ")
                        else:
                            out = input("Book is available for checkout, do you want to check it out? (1: yes, 2: no")
                            if out == '1':
                                log_event(pipe, logged_in_user['u_name'], 'CHECKED OUT BOOK')
                                # Update library
                                collection.checkout(search_term)
                                # Update Accounting Microservice
                                due = check_book_out(pipe, logged_in_user['u_name'], match.get_serial())
                                print(f"SUCCESS: your book is due on {due}")
                            else:
                                input("Press 'enter' to return to the main menu... ")
                        break

                # Display matching books to user
                print("Your search yielded the following results: \n")

                # 'order' assigns a 1-up number to each book in the list to aid in identification

                # SEARCH RESULT for Title and Author search
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
                        selected_serial = matches[acquired - 1]
                        acquisition = int(input("Is this the book you want to view? (1: yes / 2: no)"))
                        if acquisition == 1:
                            print("Displaying your book information now...\n")
                            selected_book = collection.book_by_serial(matches[acquired - 1])
                            selected_book.view()

                            # --- CHECK OUT BOOK? ---
                            if selected_book.checked_out:
                                input("Press 'enter' to return to the main menu... ")
                            else:
                                out = input(
                                    "Book is available for checkout, do you want to check it out? (1: yes, 2: no")
                                if out == '1':
                                    log_event(pipe, logged_in_user['u_name'], 'CHECKED OUT BOOK')
                                    # Update library
                                    collection.checkout(selected_serial)
                                    # Update Accounting Microservice
                                    due = check_book_out(pipe, logged_in_user['u_name'], selected_serial)
                                    print(f"SUCCESS: your book is due on {due}")
                                else:
                                    print('(No checkout)')
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
            log_event(pipe, logged_in_user['u_name'], 'ACCESSED HELP SYSTEM')
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
            log_event(pipe, logged_in_user['u_name'], 'PROPERLY EXITED THE SYSTEM')
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

        # ///\\\///\\\///\\\ ADMIN OPTIONS ONLY ///\\\///\\\///\\\

        # --- ADD A BOOK ---
        if (choice == '6') and (logged_in_user['u_name'] == 'admin'):
            log_event(pipe, logged_in_user['u_name'], 'ADDED A BOOK')
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

            # Create a new book and add it to the Library collection, then save the collection
            collection.add_book(Book(title, author, isbn, pub, year, price))
            save_data(collection)

            print("Book entered and recorded, thank you!")
            print("-----------------------------------------------------------------------------------\n \n")
            continue

        # --- DELETE A BOOK ---
        elif (choice == '7') and (logged_in_user['u_name'] == 'admin'):
            log_event(pipe, logged_in_user['u_name'], 'DELETED A BOOK')
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
                            save_data(collection)
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
                        print(f"BOOK NUMBER {order + 1}")

                        collection.book_by_serial(i).view()
                        print("\n")
                        order += 1

                    found_it = int(input("Is the book you're looking for in the results? (1: yes / 2: no)  "))
                    if found_it == 1:
                        doom = int(input("Enter the BOOK NUMBER of the book you wish to delete: "))
                        print("This is the book title you have selected: \n")
                        print(collection.book_by_serial(matches[doom - 1]).get_title())
                        recycle = int(input("Is this the book you want to delete? (1: yes / 2: no)"))
                        if recycle == 1:
                            confirm = input("Are you SURE you want to delete it? Type 'delete' to confirm:  \n")
                            if confirm == 'delete':
                                collection.delete_book(matches[doom - 1])
                                print("Deletion confirmed!")
                                save_data(collection)
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

        # --- DELETE USER ACCOUNT ---
        elif (choice == '8') and (logged_in_user['u_name'] == 'admin'):
            log_event(pipe, logged_in_user['u_name'], 'DELETED A  PROFILE')
            user_target = input('Enter the username of the user to delete: ')
            result1 = authenticate(f"DELETE {user_target}")
            result2 = delete_profile(pipe, user_target)
            if result1 and result2:
                print(f"Successfully deleted user {user_target}'s account!")
                input("Press enter to continue...")
                continue
            else:
                print("ERROR! Deletion request failed...")
                input("Press enter to continue...")
                continue

        # --- VIEW LOGS ---
        elif (choice == '9') and (logged_in_user['u_name'] == 'admin'):
            pass

        # --- DELETE LOGS ---
        elif (choice == '10') and (logged_in_user['u_name'] == 'admin'):
            pass

        # --- INVALID CHOICE ---
        else:
            print("INVALID CHOICE! PLEASE CHOOSE FROM VALID OPTIONS \n")
            continue


# Execute Program
if __name__ == '__main__':
    main()

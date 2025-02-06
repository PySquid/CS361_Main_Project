# MainUI.py
# Author: Philip Sheridan
# Class: CS361 / Oregon State University
# Description: Provides User Interface for Main Project, also serves as a mini monolith content manager

# ---------- Imports ----------
import socket
import pickle
import random
import os

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
        Takes no parameters and just returns the book's serial number
        :return: a serial number string
        """
        return self.serial

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
    def __init__(self, title, subject, text, question, answered) -> (bool or None):
        """
        Defines an object to model a user comment

        :param title:       comment title
        :param subject:     comment subject
        :param text:        narrative text of comment
        :param question:    'True' if comment is a question, 'False' if just a comment.
        :param answered:    'True' if question has been answered
        """

        self.title = title
        self.subject = subject
        self.text = text
        self.question = question

        # 'answered' is only True/False if comment is a question, else it is None
        if question:
            self.answered = False
        else:
            self.answered = None

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

    def show_faq(self):
        """
        Builds a cohesive FAQ entry, with top and bottom separators, and returns it.

        :return: a string representing a single formatted faq entry
        """

        #build the parsed faq entry
        shown = self.separator + '\n'
        shown += self.subject + '\n'
        shown += self.question + '\n'
        shown += self.answer + '\n'
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
        self.comments = []                     # holds comment objects
        self.faq = []                          # holds Faq objects
        self.submenu_help = {}                 # KEY: submenu name string / VALUE: help features for that menu

    # ----- METHODS -----
    def add_comment(self) -> bool:
        """
        Adds a comment to the library comment base

        :param title: the title of the comment
        :param text: the narrative text of the comment
        :return:
        """
        title = input("What is the title of your comment?")
        subject = input("What is the subject of your comment?")
        question = input("Is your comment a Question? ('y' for 'yes' / 'n' for 'no'")
        text = input("Enter the text of your comment now, and press 'Enter' when done...")

        #              _____ ----- !!!!! UNDER CONSTRUCTION !!!!! ----- _____
        answered = input("Is this comment a question? ('y' for 'yes' / 'n' for 'no'")
        if answered == 'y':
            answered = False
        else:
            answered = None

        new_comment = Comment(title, subject, text, question, answered)
        self.comments.append(new_comment)
        return True

    def del_comment(self) -> None:
        """
        Deletes a user comment.
        :return:
        """

        target = int(input("Enter the number of the comment you wish to delete: "))

        # Subtract 1 to account for 0-position in the array
        target -= 1

        print(f"The comment you've selected is : {self.comments[target]}")

        choice = input("To proceed with deletion, type 'delete' and press enter.  Any other input will cancel.")

        if choice == 'delete':
            del self.comments[target]

    def add_faq(self, title, question, answer):
        """"""

        pass

    def edit_faq(self, num):
        """"""

        pass

    def submenu_help(self, submenu):
        """
        Docscring

        MAIN | SEARCH: type?, results | ADD | DELETE: find, results, select, confirm | HELP
        """
        #              _____ ----- !!!!! UNDER CONSTRUCTION !!!!! ----- _____
        menu_main = ""
        menu_search = ""
        menu_add = ""
        menu_delete = ""
        menu_help = ""
        menu_faq = ""
        menu_comments = ""
        menu_results = ""

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

def ShowMenu(choice):
    """
    Prints the menu specified to screen

    :param choice:
    :return:
    """

    mainMenu = """
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
    deleteMenu = """
    -----------------------------------------------------------------------------------
    Delete a Book: 
    Please choose how you wish to locate the book you wish to delete:

    1) Title		    []
    2) Author		    []
    3) Library S/N	    []

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

    1) Title		        []
    2) Author		        []
    3) Library S/N	        []

    #RecycleBin		[find/recover recently deleted books]
    #Help			[if you are having trouble or questions]
    #Return			[returns to main menu]

    -----------
    Choice: 
    -----------------------------------------------------------------------------------
    """
    helpMenu = """
    -----------------------------------------------------------------------------------
    Help Menu: 
    This is the help menu, please select from the options below:

    1) FAQ			        [Frequently Asked Questions]
    2) Leave a Comment		[Write your own Comment]
    3) View User Comments	[Leave and read user comments]
    4) Return to Main		[returns to main menu]

    !!! NOTE: questions asked in option (2) ‘Leave a Comment’ may not
              be answered quickly, and are only answered periodically by the Admin
              or by others users.  For quick answers, check the FAQs.

    -----------
    Choice: 
    -----------------------------------------------------------------------------------
    """

    if choice == 'main':
        output = mainMenu
    elif choice == 'add':
        output = addMenu
    elif choice == 'delete':
        output = deleteMenu
    elif choice == 'search':
        output = searchMenu
    elif choice == 'help':
        output = helpMenu
    else:
        output = 'invalid choice'

    print(output)

# ---------- Main: User Interface ----------
def main():
    """
    USER INTERFACE:
        This function provides the main user interface to the Library
    """

    # Print the title banner
    title_banner()

    # Create a new library
    collection = Library()

    # print the updates banner
    if collection.get_banner():
        print(collection.get_banner())
    else:
        print("    ---------------------------")
        print("    ---      NO UPDATES     ---")
        print("    ---------------------------")

    # Initiate the main program loop
    choice = None

    while choice != '5':

        # print the main menu
        ShowMenu('main')

        choice = input("Choice:  ")

        if choice == '1':
            # ----- ADD A BOOK -----
            # Book parameters: [title, author, isbn, year, publisher, price]

            # Print the 'Add a Book' Menu
            ShowMenu('add')

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

            # Show the user the Deletion menu
            ShowMenu('delete')

            # CHOICE LOOP
            while True:
                selection = int(input("Choice:  "))

                # Reset variables
                match = None
                matches = None

                # HELP
                if selection == ('Help' or 'help' or 'HELP' or '#Help'):
                    pass

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
            # Show the user the Search menu
            ShowMenu('search')

            # CHOICE LOOP
            while True:
                selection = int(input("Choice:  "))

                # Reset variables
                match = None
                matches = None

                # HELP
                if selection == ('Help' or 'help' or 'HELP' or '#Help'):
                    pass

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
                    found = int(input("Enter File # to select/recover a file, or enter '0' to return to Main Menu"))
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

                            #              _____ ----- !!!!! UNDER CONSTRUCTION !!!!! ----- _____
                            pass

                        else:
                            continue

                # TITLE SEARCH
                if selection == 1:
                    search_term = input("Type the title, or partial title of the book you want to find: ")
                    matches = [sn for titles, sn in collection.titles.items() if search_term in titles]

                # AUTHOR SEARCH
                elif selection == 2:
                    search_term = input("Type the Author name, or partial name of the book you want to find: ")
                    matches = [sn for authors, sn in collection.authors.items() if search_term in authors]

                # SERIAL SEARCH
                elif selection == 3:
                    search_term = input("Type the exact Library serial number of the book you want to find:  ")
                    match = collection.serials[search_term]

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

        elif choice == '4':
            pass

        elif choice == '5':
            print("Goodbye!")
            break


# Execute Program
if __name__ == '__main__':
    main()

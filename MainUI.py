# MainUI.py
# Author: Philip Sheridan
# Class: CS361 / Oregon State University
# Description: Provides User Interface for Main Project, also serves as a mini monolith content manager

# ---------- Imports ----------
import socket
import pickle
import random

# ---------- Classes ----------
class Book:
    def __init__(self, title, author, isbn, year, publisher, price):
        """initializes a new network monitor"""
        self.title = title
        self.author = author
        self.isbn = isbn
        self.serial = None          # gets assigned by Library once 'added'
        self.year = year
        self.publisher = publisher
        self.price = price
        self.rating = None
        self.summary = None

    # ----- METHODS -----
    def view(self):
        """Returns the book's main attributes as a dictionary"""

        return({'title': self.title, 'author': self.author, 'isbn': self.isbn, 'serial': self.serial, 'year': self.year,
                'publisher': self.publisher, 'price': self.price, 'rating': self.rating, 'summary': self.summary})

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
            self.authors.update({new.author: [new.serial]})
        else:
            self.authors[new.author].append(new.serial)

        # - MAP LIBRARY TITLE(S) TO SERIAL -
        if new.title not in self.titles.keys():
            self.titles.update({new.title: [new.serial]})
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

        new_comment = Comment(title, subject, text, question)
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

    !!! NOTE: for non-number menus, type ‘#’ + (menu option) to access
    EXAMPLE: ‘#help’ will take you to the help sub-menu of a particular page, if available

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
    Subject:
    -----------------------------------------------------------------------------------
    """
    deleteMenu = """
    -----------------------------------------------------------------------------------
    Delete a Book: 
    Please choose how you wish to locate the book you wish to delete:

    1) Title		[]
    2) Author		[]
    3) ISBN		[]
    4) Library S/N	[]

    #Help			[if you are having trouble or questions]
    #Return			[returns to main menu]

    -----------
    Choice: 
    -----------------------------------------------------------------------------------
    """
    searchMenu = """
    -----------------------------------------------------------------------------------
    Find a Book: 
    Please choose how you wish to locate the book:

    1) Title		[]
    2) Author		[]
    3) ISBN		[]
    4) Library S/N	[]

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

    1) FAQ			[Frequently Asked Questions]
    2) Leave a Comment		[Write your own Comment]
    2) View User Comments	[Leave and read user comments]
    3) Help			[if you are having trouble or questions]
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
    """fs
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

    # print the main menu
    ShowMenu('main')

    # Initiate the main program loop
    choice = None

    while choice != 5:
        choice = input("Choice:  ")

        if choice == '1':
            pass
        if choice == '2':
            pass
        if choice == '3':
            pass
        if choice == '4':
            pass
        if choice == '5':
            print("Goodbye!")
            continue


# Execute Program
if __name__ == '__main__':
    main()

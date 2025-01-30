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

    # ----- METHODS -----
    def book_by_serial(self, target) -> Book:
        """
        Returns a book object based on serial number
        """
        return self.serials[target]

    def book_by_author(self, target) -> Book:
        """"""
        pass

    def book_by_title(self, target) -> Book:
        """"""
        pass

    def info_by_serial(self, target) -> dict:
        """
        Returns a dictionary of all a book's information, accessed by serial number
        """
        return dict(vars(self.serials[target]))               # returns a dictionary of book attributes

    def info_by_author(self, auth) -> dict:
        """"""
        pass

    def info_by_title(self, target_title) -> dict:
        """"""
        pass

    def add(self, new) -> None:
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

    def delete(self, target) -> str:
        """
        Removes a book from the library, and stores it in the 'Recycle_Bin' JSON file.
            *** takes a serial number as an input parameter
        """

        # - GET THE DELETION TARGET'S TITLE AND AUTHOR STRINGS -
        del_author = self.serials[target].author
        del_title = self.serials[target].title

        # - RECYCLE THE BOOK to a PICKLE FILE-
        #   *** Pickle file will be named as the deleted book's serial number

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

        # - REMOVE THE BOOK AUTHOR FROM LIBRARY AUTHORS -

        # - REMOVE THE BOOK TITLE FROM LIBRARY TITLES -

        # return the name of the recycled file
        return f"{target}.pickle"


# ---------- Functions ----------


# ---------- Main: User Interface ----------
def main():
    """fs
    USER INTERFACE:
        This function provides the main user interface to the Library
    """
    pass


# Execute Program
if __name__ == '__main__':
    main()

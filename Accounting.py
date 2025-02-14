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
    RETURNS: whatever data the microservice replies with.
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

    def receive(self, rec_buffer=2048, max_connect=3, reply="ack"):
        """
        Takes a sender name listed in the address book as a string, then returns the
        :param service_name: the name of the microservice calling this class
        :param rec_buffer: default to 2048, this should not be changed
        :param max_connect: generally, 1 should be the max connections, 3 is more than enough
        :param reply: reply is the default reply from this method
        :return: the action mode and the decoded message data is returned
        """

        # Prepare variables
        data_decoded = None                         # container for decoded incoming message
        address = self.address_book[self.name]      # sets own address based on object name

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
def main():
    """
    ACCOUNTING MICROSERVICE
        This service keeps track of customer balances and tracks book checkins/checkouts per customer
    """

    # Instantiate a Pipeline
    messager = Pipeline('accounting')

    # Initiate main (outer) loop.  [there's an inner loop in the Pipeline.receive() function]
    while True:



# Execute Program
if __name__ == '__main__':
    main()
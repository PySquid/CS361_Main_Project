import socket
import pickle

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

    def send(self, destination, data):
        """Is passed a socket tuple and data, sends data to destination."""

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
                print(f"sending string {data}")
                core_socket.sendall(data.encode())
            else:
                # it's a dictionary...pickle it and just send the bytes
                print(f"sending dict {data}")
                pickled_data = pickle.dumps(data)
                core_socket.sendall(pickled_data)

        finally:
            # Close the socket.
            core_socket.close()

    def receive(self, rec_buffer=2048, max_connect=3) -> dict:
        """
        Takes no params, listens for TCP connections, then returns any message data received.

        :param rec_buffer: default to 2048, this should not be changed
        :param max_connect: generally, 1 should be the max connections, 3 is more than enough
        :return: the action mode and the decoded message data is returned
        """

        # Prepare variables
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
                # Accept connection from sender
                sending_socket, sending_ip = receive_socket.accept()

                # !!!!! TESTING !!!!!
                print(f"{sending_ip} (sender) just connected")

                try:
                    # transfer the socket data to the 'data' variable
                    message = sending_socket.recv(rec_buffer)

                    # try to decode the data as a string
                    try:
                        message_decoded = str(message.decode())

                    # if that fails...it's a pickled dictionary, unpickle it
                    except:
                        print('found a pickled dictionary')
                        message_decoded = pickle.loads(message)

                finally:
                    # Close connection to core
                    sending_socket.close()
                    break

        finally:
            # Close the connection
            receive_socket.close()

            # Make the response available to the calling function
            return message_decoded

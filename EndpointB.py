# EndpointB.py
# Author: Philip Sheridan
# Class: CS361 / Oregon State University
# Description: Receiving application for Assignment4 - receives a message from EndpointA

# ---------- modules ----------
import socket

# ---------- functions ----------
def receive_over_tcp(server_address, server_port, rec_buffer=1024, max_connect=2):
    """
    Receives a message sent by EndpointA, and sends an acknowledgement of its receipt.

    :param server_address:
    :param server_port:
    :param rec_buffer:
    :param max_connect:
    :return:
    """

    # Establish a socket object
    rec_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind it
    rec_sock.bind((server_address, server_port))

    # Start listening
    rec_sock.listen(max_connect)

    # Show Endpoint B is running
    print(f"\nEndpoint B is listening on port# {server_port}")

    # Accept loop
    while True:
        # Accept connection
        A_sock, A_ip = rec_sock.accept()

        # Announce connection
        print(f"Inbound data from Endpoint A...")

        try:
            message = A_sock.recv(rec_buffer)
            decoded = str(message.decode())
            print("---------------------------------------------------------------------")
            print(f"Just in from Endpoint A: '{decoded}'")
            print("---------------------------------------------------------------------\n")

            # Acknowledge Endpoint A's message
            acknowledgement = "Endpoint B has received your message"
            A_sock.sendall(acknowledgement.encode())

        finally:
            # clear out resources
            A_sock.close()
            print(f"Connection to Endpoint A closed.")

def main():
    # run receiving service
    receive_over_tcp('127.0.0.1', 55000)


# Execute Program
if __name__ == '__main__':
    main()

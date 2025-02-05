# EndpointA.py
# Author: Philip Sheridan
# Class: CS361 / Oregon State University
# Description: Sending application for Assignment4 - sends a message to EndpointB


# ---------- modules ----------
import socket

# ---------- functions ----------

def send_over_tcp(serv_address, serv_port, data, buffer=2048):
    """
    Takes a server address, port, and some data and sends the data to that address.
    Does not return anything, but does print a server reply to the console.

    :param serv_address:
    :param serv_port:
    :param data:
    :param buffer:
    :return:
    """

    # ---------- Variables ----------
    EndB_addresss = serv_address
    EndB_port = serv_port

    # Create the outbound socket object
    sender_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Initiate the connection to EndpointB
    try:
        # addresses must be tuples with address + port as format regarding the socket module
        sender_sock.connect((EndB_addresss, EndB_port))

        # Announce and send the required course message
        print("\n---------------------------------------------------------------------")
        print(f"Sending: the following payload: '{data}' now...")
        print("---------------------------------------------------------------------\n")
        sender_sock.sendall(data.encode())

        # Confirm receipt and announce it to the user
        response = sender_sock.recv(buffer)
        decoded = str(response.decode())
        print(f"EndpointB: '{decoded}'")

    finally:
        # Clear up local resources.
        sender_sock.close()


def main():
    message = "This is a message from CS361"
    B_address = '127.0.0.1'
    B_port = 55000

    # Send the message
    send_over_tcp(B_address, B_port, message)


# Execute Program
if __name__ == '__main__':
    main()

import socket
from customtkinter import CTk
from registrationpages import RegistrationPages
from AES import *
from RSA import *

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555


def client():
    aes_key = 'Evyatar'
    AESC = AESCipher(aes_key)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        client_socket.send('ClientHello'.encode('utf-8'))
        server_hello = client_socket.recv(1024).decode()
        public_key = client_socket.recv(1024)
        client_socket.send(encrypt(RSA.import_key(public_key), aes_key))
        client_socket.send(AESC.encrypt('Finished').encode('utf-8'))
        server_finished = client_socket.recv(1024).decode('utf-8')
        while True:
            root_window = CTk()
            RegistrationPages(client_socket=client_socket, master=root_window, key=AESC)
            root_window.mainloop()
            break


if __name__ == '__main__':
    client()


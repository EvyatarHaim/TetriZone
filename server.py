import socket
import sys
from threading import Thread
from utils import recv_message
from server_commands import ServerFunctions
from AES import *
from RSA import *


def handle_client(client_socket, server_socket):
    public_key, private_key = get_keys(1024)
    client_hello = client_socket.recv(1024).decode('utf-8')
    client_socket.send('ServerHello'.encode('utf-8'))
    client_socket.send(public_key.export_key())
    enc_aes_key = client_socket.recv(1024)
    aes_key = decrypt(private_key, enc_aes_key).decode('utf-8')
    AESC = AESCipher(aes_key)
    client_finished = client_socket.recv(1024).decode('utf-8')
    client_socket.send(AESC.encrypt('Finished').encode('utf-8'))
    try:
        while True:
            client_info = recv_message(client_socket, key=AESC)
            if client_info == "":
                client_socket.close()
                server_socket.close()
                print("[*] Client close the socket")
                sys.exit()
            else:
                print(f"[CLIENT:] {client_info}")

            ServerFunctions(client_socket=client_socket, info=client_info, key=AESC)

    except Exception as err:
        print(f"[!] {err}")


def server():
    try:
        server_socket = socket.socket()
        print("[*] The server is up and running. Listening for connections...")
        server_socket.bind(('0.0.0.0', 5555))
        server_socket.listen()

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[*] Accepted connection from {client_address}")
            th = Thread(target=handle_client, args=(client_socket, server_socket))
            th.start()

    except Exception as err:
        print(f"[!] {err}")


if __name__ == '__main__':
    server()

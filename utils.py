import socket
from exceptions import InvalidMessage
from AES import *
from RSA import *

MESSAGE_MAX_LENGTH = 5


def encode_massage(message: str) -> bytes:
    message_length = str(len(message)).zfill(MESSAGE_MAX_LENGTH)
    return (message_length + message).encode()  # Padding the message


def decode_message_length(message: bytes) -> int:
    try:
        message_length = int(message[:MESSAGE_MAX_LENGTH])
    except ValueError as err:
        raise InvalidMessage("Invalid Message")
    return message_length


def decode_message(message_length: int, message: bytes) -> str:
    if len(message) != message_length:
        raise InvalidMessage("Length filed doesn't fit")
    return message.decode()


def send_message(message: str, client_socket: socket, key):
    # message = encode_massage(message)
    # client_socket.send(message)
    data = key.encrypt(message)
    data = data.encode('utf-8')
    client_socket.send(data)


def recv_message(client_socket: socket, key) -> str:
    # message_bytes_length = client_socket.recv(MESSAGE_MAX_LENGTH)
    # message_length = decode_message_length(message_bytes_length)
    # message_bytes = client_socket.recv(message_length)
    # message = decode_message(message_length, message_bytes)
    # return message
    client_info = client_socket.recv(1024)
    client_info_str = key.decrypt(client_info.decode('utf-8'))
    return client_info_str


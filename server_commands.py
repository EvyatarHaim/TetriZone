import socket
from utils import send_message
import sqlite3
import hashlib


def hashing_string(string: str):
    return hashlib.sha256(string.encode()).hexdigest()


class ServerFunctions:
    def __init__(self, client_socket: socket, info: str, key):
        self.client_socket = client_socket
        self.key = key
        self.server_commands: dict = {
            "Login": self.login,
            "Register": self.register,
            "Score": self.score,
            # "Leaderboard_Headers": self.leaderboard_headers,
            "Leaderboard_Data": self.leaderboard_data
        }
        client_command = info.split('|')[0]
        if client_command != "Leaderboard_Headers" and client_command != "Leaderboard_Data":
            self.server_commands[client_command](info)
        else:
            self.server_commands[client_command]()

    def login(self, info: str):
        info_list = info.split('|')

        username: str = info_list[1]
        password = hashing_string(info_list[2])

        if username == "" or password == "":
            send_message("[!] One or more entries are empty", self.client_socket, key=self.key)
            return

        connection = sqlite3.connect('TetrisGame.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name=?", (username,))
        exist_user = cursor.fetchone()

        if exist_user is None:
            connection.close()
            send_message("[!] Username does not exists", self.client_socket, key=self.key)
            return

        cursor.execute("SELECT password FROM users WHERE user_name=?", (username,))
        user_password = cursor.fetchone()

        if user_password[0] != password:
            connection.close()
            send_message("[!] The password is incorrect", self.client_socket, key=self.key)
            return

        connection.commit()
        connection.close()
        send_message("[SERVER:] Login successfully", self.client_socket, key=self.key)

    def register(self, info: str):
        info_list = info.split('|')

        first_name: str = info_list[1]
        age: str = info_list[2]
        username: str = info_list[3]
        password = hashing_string(info_list[4])

        connection = sqlite3.connect('TetrisGame.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name=?", (username,))
        exist_user = cursor.fetchone()

        if exist_user is not None:
            connection.close()
            send_message("[!] This username is already taken", self.client_socket, key=self.key)
            return

        cursor.execute("INSERT INTO users (user_name, first_name, age, password) VALUES(?, ?, ?, ?)",
                       (username, first_name, age, password))

        connection.commit()
        connection.close()
        send_message("[SERVER:] User have created successfully", self.client_socket, key=self.key)
        return

    def score(self, info: str):
        info_list = info.split('|')

        username: str = info_list[1]
        last_score: int = int(info_list[2])

        connection = sqlite3.connect('TetrisGame.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM scores WHERE user_name=?", (username,))
        exist_user = cursor.fetchone()

        if exist_user is not None:
            # User exist in scores, so we need only to update the last_score
            cursor.execute("UPDATE scores SET last_score=? WHERE user_name=? ", (last_score, username))
            # Check if the last_score might be the highest
            cursor.execute("SELECT highest_score FROM scores WHERE user_name=?", (username,))
            highest_score: int = int(cursor.fetchone()[0])

            if last_score > highest_score:
                highest_score = last_score
                cursor.execute("UPDATE scores SET highest_score=? WHERE user_name=? ",
                               (highest_score, username))

        else:
            # Because user is not existed in scores we will insert to both last_score and highest_score
            highest_score = last_score
            cursor.execute("INSERT INTO scores (user_name, last_score, highest_score) VALUES(?, ?, ?)",
                           (username, last_score, highest_score))
        # try:
        #     self.update_score_table()
        # except Exception as err:
        #     print(f"[!->] {err}")

        connection.commit()
        connection.close()
        print(f"[*] Score table has been updated")
        return

    def leaderboard_data(self):
        connection = sqlite3.connect('TetrisGame.db')
        cursor = connection.cursor()
        # Getting the Top 10 -> DESC from the highest to the lowest
        data = cursor.execute("SELECT * FROM scores ORDER BY highest_score DESC LIMIT 10")
        data_rows: list = []
        for row in data:
            data_rows.append(str(row))

        # When there is not 10 scores it will add row with nothing on them so the table will stay the same all the time
        if len(data_rows) < 10:
            for _ in range(0, 10 - len(data_rows)):
                data_rows.append("('', '', '', '' )")

        str_data_rows: str = str(' '.join(data_rows))
        connection.close()

        send_message(str_data_rows, self.client_socket, key=self.key)


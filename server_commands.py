import socket
from utils import send_message
import sqlite3
import hashlib
from datetime import datetime


def hashing_string(string: str):
    return hashlib.sha256(string.encode()).hexdigest()


def update_total_score(username: str, last_game_score: int):
    connection = sqlite3.connect('TetriZone.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM stats WHERE user_name=?", (username,))
    exist_user = cursor.fetchone()

    if exist_user is not None:
        # User exist in stats, so we need only to add the last game score to total_score and update the total_score
        cursor.execute("SELECT total_score FROM stats WHERE user_name=?", (username,))
        total_score: int = int(cursor.fetchone()[0])
        updated_total_score: int = total_score + last_game_score
        cursor.execute("UPDATE stats SET total_score=? WHERE user_name=? ", (updated_total_score, username))
    else:
        # Because user is not existed in stats probably it is his first game, so we will insert last_game_score into
        # total_score
        cursor.execute("INSERT INTO stats (user_name, total_score) VALUES(?, ?)",
                       (username, last_game_score))

    connection.commit()
    connection.close()
    print(f"[*] total_score has been updated")
    return


def update_games_played(username: str):
    connection = sqlite3.connect('TetriZone.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM stats WHERE user_name=?", (username,))
    exist_user = cursor.fetchone()

    if exist_user is not None:
        # User exist in stats, so we need only to add the numbers of lines and update the lines
        cursor.execute("SELECT games_played FROM stats WHERE user_name=?", (username,))
        games_played: int = int(cursor.fetchone()[0])
        updated_games_played = games_played + 1
        cursor.execute("UPDATE stats SET games_played=? WHERE user_name=? ", (updated_games_played, username))
    else:
        # Because user is not existed in stats probably it is his first game, so we will insert into 1 the
        # games_played
        cursor.execute("INSERT INTO stats (user_name, games_played) VALUES(?, ?)",
                       (username, 1))

    connection.commit()
    connection.close()
    print(f"[*] games_played has been updated")
    return


def score(username: str, last_score: int):
    update_total_score(username=username, last_game_score=last_score)

    connection = sqlite3.connect('TetriZone.db')
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

    connection.commit()
    connection.close()
    print(f"[*] Score table has been updated")
    return


def update_lines(username: str, last_game_lines: int):
    connection = sqlite3.connect('TetriZone.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM stats WHERE user_name=?", (username,))
    exist_user = cursor.fetchone()

    if exist_user is not None:
        # User exist in stats, so we need to add the numbers of lines and update the lines
        cursor.execute("SELECT lines FROM stats WHERE user_name=?", (username,))
        current_lines: int = int(cursor.fetchone()[0])
        updated_lines = current_lines + last_game_lines
        cursor.execute("UPDATE stats SET lines=? WHERE user_name=? ", (updated_lines, username))
    else:
        # Because user is not existed in stats we will insert into lines the clear_lines
        cursor.execute("INSERT INTO stats (user_name, lines) VALUES(?, ?)",
                       (username, last_game_lines))

    connection.commit()
    connection.close()
    print(f"[*] lines has been updated")
    return


def update_game_time(username: str, last_game_time: int):
    connection = sqlite3.connect('TetriZone.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM stats WHERE user_name=?", (username,))
    exist_user = cursor.fetchone()

    if exist_user is not None:
        # User exist in stats, so we need to add the numbers of seconds and update the played_time
        cursor.execute("SELECT played_time FROM stats WHERE user_name=?", (username,))
        current_game_time: int = int(cursor.fetchone()[0])
        updated_time = current_game_time + last_game_time
        cursor.execute("UPDATE stats SET played_time=? WHERE user_name=? ", (updated_time, username))
    else:
        # Because user is not existed in stats we will insert into played_time the last_game_time
        cursor.execute("INSERT INTO stats (user_name, played_time) VALUES(?, ?)",
                       (username, last_game_time))

    connection.commit()
    connection.close()
    print(f"[*] played_time has been updated")
    return


def format_time(seconds: int) -> str:
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


class ServerFunctions:
    def __init__(self, client_socket: socket, info: str, key):
        self.client_socket = client_socket
        self.key = key
        self.server_commands: dict = {
            "Login": self.login,
            "Register": self.register,
            "Leaderboard_Data": self.leaderboard_data,
            "Update_Status": self.update_status,
            "Get_Status": self.get_status,
            "Game_Over": self.game_over,
            "Get_Total_Score": self.get_total_score,
            "Get_Total_Lines": self.get_total_lines,
            "Get_Games_Played": self.get_games_played,
            "Get_Played_Time": self.get_played_time,
            "Get_Last_Game_Score": self.get_last_game_score,
            "Get_Highest_Score": self.get_highest_score,
            "Get_Creation_Date": self.get_creation_date
        }
        client_command = info.split('|')[0]
        if client_command != "Leaderboard_Data":
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

        connection = sqlite3.connect('TetriZone.db')
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

        # Check if the user is online
        cursor.execute("SELECT is_online FROM users WHERE user_name=?", (username,))
        status = cursor.fetchone()

        if status[0] == 1:  # 1 == True
            connection.close()
            send_message("[!] This user is already connected", self.client_socket, key=self.key)
            return
        else:
            # The login now as been approved, so we update is_online to 1
            cursor.execute("UPDATE users SET is_online=? WHERE user_name=? ", (1, username))

        connection.commit()
        connection.close()
        send_message("[SERVER:] Login successfully", self.client_socket, key=self.key)
        return

    def register(self, info: str):
        info_list = info.split('|')

        first_name: str = info_list[1]
        age: str = info_list[2]
        username: str = info_list[3]
        password = hashing_string(info_list[4])

        connection = sqlite3.connect('TetriZone.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name=?", (username,))
        exist_user = cursor.fetchone()

        if exist_user is not None:
            connection.close()
            send_message("[!] This username is already taken", self.client_socket, key=self.key)
            return

        cursor.execute("INSERT INTO users (user_name, first_name, age, password, is_online) VALUES(?, ?, ?, ?, ?)",
                       (username, first_name, age, password, 1))
        cursor.execute("UPDATE users SET creation_date=CURRENT_DATE WHERE user_name=?", (username,))

        connection.commit()
        connection.close()
        send_message("[SERVER:] User have created successfully", self.client_socket, key=self.key)
        return

    def leaderboard_data(self):
        connection = sqlite3.connect('TetriZone.db')
        cursor = connection.cursor()
        # Getting the Top 10 -> DESC from the highest to the lowest
        data = cursor.execute("SELECT * FROM scores ORDER BY highest_score DESC LIMIT 10")
        data_rows: list = []
        for row in data:
            data_rows.append(str(row))

        # When there is not 10 scores it will add row with nothing on them so the table will stay the same all the time
        # if len(data_rows) < 10:
        #     for _ in range(0, 10 - len(data_rows)):
        #         data_rows.append("('', '', '', '' )")

        str_data_rows: str = str(' '.join(data_rows))
        connection.close()

        send_message(str_data_rows, self.client_socket, key=self.key)
        return

    def update_status(self, info: str):
        info_list = info.split('|')

        username: str = info_list[1]
        status: int = int(info_list[2])

        connection = sqlite3.connect('TetriZone.db')
        cursor = connection.cursor()

        cursor.execute("UPDATE users SET is_online=? WHERE user_name=? ", (status, username))

        connection.commit()
        connection.close()
        send_message(f"[SERVER:] (username, status)|{username}|{str(status)}",
                     self.client_socket, key=self.key)
        return

    def get_status(self, info: str):
        info_list = info.split('|')

        username: str = info_list[1]

        connection = sqlite3.connect('TetriZone.db')
        cursor = connection.cursor()
        cursor.execute("SELECT is_online FROM users WHERE user_name=?", (username,))
        status: int = int(cursor.fetchone()[0])

        str_status = ""
        if status == 1:
            str_status = "Online"
        if status == 0:
            str_status = "Offline"

        connection.commit()
        connection.close()
        send_message(f"[SERVER:] (username, status)|{username}|{str_status}", self.client_socket, key=self.key)
        return

    def game_over(self, info: str):
        info_list = info.split('|')

        username = info_list[1]
        user_score: int = int(info_list[2])
        user_lines: int = int(info_list[3])
        game_time: int = int(info_list[4])

        score(username=username, last_score=user_score)
        update_lines(username=username, last_game_lines=user_lines)
        update_games_played(username=username)
        update_game_time(username=username, last_game_time=game_time)
        return

    def get_total_score(self, info: str):
        info_list = info.split('|')

        username: str = info_list[1]
        total_score = 0
        connection = sqlite3.connect('TetriZone.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM stats WHERE user_name=?", (username,))
        exist_user = cursor.fetchone()

        if exist_user is not None:
            # User exist in stats, so we need only to return the total_score
            cursor.execute("SELECT total_score FROM stats WHERE user_name=?", (username,))
            total_score = cursor.fetchone()[0]
        # Because user is not existed in stats probably it is his first game, so the total_score will be 0
        connection.commit()
        connection.close()
        send_message(str(total_score), self.client_socket, key=self.key)
        return

    def get_total_lines(self, info: str):
        info_list = info.split('|')

        username: str = info_list[1]
        total_lines = 0

        connection = sqlite3.connect('TetriZone.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM stats WHERE user_name=?", (username,))
        exist_user = cursor.fetchone()

        if exist_user is not None:
            # User exist in stats, so we need only to return the lines
            cursor.execute("SELECT lines FROM stats WHERE user_name=?", (username,))
            total_lines = cursor.fetchone()[0]
        # Because user is not existed in stats probably it is his first game, so the lines will be 0
        connection.commit()
        connection.close()
        send_message(str(total_lines), self.client_socket, key=self.key)
        return

    def get_games_played(self, info: str):
        info_list = info.split('|')

        username: str = info_list[1]
        total_games_played = 0

        connection = sqlite3.connect('TetriZone.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM stats WHERE user_name=?", (username,))
        exist_user = cursor.fetchone()

        if exist_user is not None:
            # User exist in stats, so we need only to return the games_played
            cursor.execute("SELECT games_played FROM stats WHERE user_name=?", (username,))
            total_games_played = cursor.fetchone()[0]
        # Because user is not existed in stats probably it is his first game, so the games_played will be 0
        connection.commit()
        connection.close()
        send_message(str(total_games_played), self.client_socket, key=self.key)
        return

    def get_played_time(self, info: str):
        info_list = info.split('|')

        username: str = info_list[1]
        time = 0

        connection = sqlite3.connect('TetriZone.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM stats WHERE user_name=?", (username,))
        exist_user = cursor.fetchone()

        if exist_user is not None:
            # User exist in stats, so we need only to return the played_time
            cursor.execute("SELECT played_time FROM stats WHERE user_name=?", (username,))
            time = cursor.fetchone()[0]
        # Because user is not existed in stats probably it is his first game, so the played_time will be 0
        connection.commit()
        connection.close()
        full_time = format_time(time)
        send_message(full_time, self.client_socket, key=self.key)
        return

    def get_last_game_score(self, info: str):
        info_list = info.split('|')

        username: str = info_list[1]
        last_game_Score = 0

        connection = sqlite3.connect('TetriZone.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM stats WHERE user_name=?", (username,))
        exist_user = cursor.fetchone()

        if exist_user is not None:
            # User exist in scores, so we need only to return the last_score
            cursor.execute("SELECT last_score FROM scores WHERE user_name=?", (username,))
            last_game_Score = cursor.fetchone()[0]
        # Because user is not existed in stats probably it is his first game, so the last_score will be 0
        connection.commit()
        connection.close()
        send_message(str(last_game_Score), self.client_socket, key=self.key)
        return

    def get_highest_score(self, info: str):
        info_list = info.split('|')

        username: str = info_list[1]
        highest_score = 0

        connection = sqlite3.connect('TetriZone.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM stats WHERE user_name=?", (username,))
        exist_user = cursor.fetchone()

        if exist_user is not None:
            # User exist in scores, so we need only to return the highest_score
            cursor.execute("SELECT highest_score FROM scores WHERE user_name=?", (username,))
            highest_score = cursor.fetchone()[0]
        # Because user is not existed in stats probably it is his first game, so the highest_score will be 0
        connection.commit()
        connection.close()
        send_message(str(highest_score), self.client_socket, key=self.key)
        return

    def get_creation_date(self, info: str):
        info_list = info.split('|')

        username: str = info_list[1]

        connection = sqlite3.connect('TetriZone.db')
        cursor = connection.cursor()
        cursor.execute("SELECT creation_date FROM users WHERE user_name=?", (username,))
        date = cursor.fetchone()[0]

        date_obj = datetime.strptime(date, '%Y-%m-%d')

        formatted_date = date_obj.strftime('%d/%m/%Y')

        connection.commit()
        connection.close()
        send_message(str(formatted_date), self.client_socket, key=self.key)
        return

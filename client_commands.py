import socket
from utils import recv_message, send_message
from exceptions import ExitException


class ClientFunctions:
    def __init__(self, client_socket: socket, key):
        self.client_socket = client_socket
        self.key = key

    def handle_login(self, username: str, password: str):
        message = f"Login|{username}|{password}"
        try:
            send_message(message, self.client_socket, key=self.key)
        except ExitException as err:
            return err

        server_response = recv_message(self.client_socket, key=self.key)
        return server_response

    def handle_registry(self, name: str, username: str, age: str, password: str):
        message = f"Register|{name}|{age}|{username}|{password}"
        try:
            send_message(message, self.client_socket, key=self.key)
        except ExitException as err:
            return err

        server_response = recv_message(self.client_socket, key=self.key)
        return server_response

    def get_leaderboard_data(self):
        message = "Leaderboard_Data|"
        try:
            send_message(message, self.client_socket, key=self.key)
        except ExitException as err:
            return err

        tuple_str = recv_message(self.client_socket, key=self.key)
        tuple_substrings = tuple_str.split(") ")  # Use ") " to separate tuples

        tuples = []
        for item in tuple_substrings:
            item = item.strip()  # Remove leading/trailing spaces
            if item:  # If the item is not empty
                if not item.endswith(")"):
                    item += ")"  # Add closing parenthesis if missing
                try:
                    # Step 3: Convert to a tuple using eval() carefully
                    tuples.append(eval(item))  # Convert string to tuple
                except Exception as e:
                    print(f"[!] Error converting '{item}' to tuple: {e}")

        return tuples

    def update_status(self, username: str, status: int):
        message = f"Update_Status|{username}|{status}"
        try:
            send_message(message, self.client_socket, key=self.key)
        except ExitException as err:
            return err

        server_response = recv_message(self.client_socket, key=self.key)
        return server_response

    def get_status(self, username: str):
        message = f"Get_Status|{username}"
        try:
            send_message(message, self.client_socket, key=self.key)
        except ExitException as err:
            return err

        server_response = recv_message(self.client_socket, key=self.key)
        status = server_response.split('|')[2]
        return status

    def get_total_score(self, username: str):
        message = f"Get_Total_Score|{username}"
        try:
            send_message(message, self.client_socket, key=self.key)
        except ExitException as err:
            return err

        server_response = recv_message(self.client_socket, key=self.key)
        return server_response

    def get_total_lines(self, username: str):
        message = f"Get_Total_Lines|{username}"
        try:
            send_message(message, self.client_socket, key=self.key)
        except ExitException as err:
            return err

        server_response = recv_message(self.client_socket, key=self.key)
        return server_response

    def get_games_played(self, username: str):
        message = f"Get_Games_Played|{username}"
        try:
            send_message(message, self.client_socket, key=self.key)
        except ExitException as err:
            return err

        server_response = recv_message(self.client_socket, key=self.key)
        return server_response

    def get_played_time(self, username: str):
        message = f"Get_Played_Time|{username}"
        try:
            send_message(message, self.client_socket, key=self.key)
        except ExitException as err:
            return err

        server_response = recv_message(self.client_socket, key=self.key)
        return server_response

    def get_last_game_score(self, username: str):
        message = f"Get_Last_Game_Score|{username}"
        try:
            send_message(message, self.client_socket, key=self.key)
        except ExitException as err:
            return err

        server_response = recv_message(self.client_socket, key=self.key)
        return server_response

    def get_highest_score(self, username: str):
        message = f"Get_Highest_Score|{username}"
        try:
            send_message(message, self.client_socket, key=self.key)
        except ExitException as err:
            return err

        server_response = recv_message(self.client_socket, key=self.key)
        return server_response

    def get_creation_date(self, username: str):
        message = f"Get_Creation_Date|{username}"
        try:
            send_message(message, self.client_socket, key=self.key)
        except ExitException as err:
            return err

        server_response = recv_message(self.client_socket, key=self.key)
        return server_response

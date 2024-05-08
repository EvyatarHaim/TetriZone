import socket
import customtkinter
from PIL import ImageTk, Image

from Game.tetris import tetris_game
from client_commands import ClientFunctions


class Menu:
    def __init__(self, client_socket: socket, master, username, key):
        self.client_socket = client_socket
        self.username = username
        self.key = key
        self.master = master
        self.master.geometry('1200x700')
        self.master.title("TetrisGame- Menu")
        self.master.resizable()

        self.master.protocol("WM_DELETE_WINDOW", lambda: self.master_window_closed(self.client_socket, self.key,
                                                                                   self.username))

        self.base_frame = customtkinter.CTkFrame(master=self.master, fg_color='#919191')
        self.base_frame.pack(fill='both', expand=True)

        self.home_page()

    def master_window_closed(self, client_socket: socket, key, username):
        server_response = ClientFunctions(client_socket=client_socket, key=key).update_status(username=username,
                                                                                              status=0)

        server_response_list = server_response.split('|')
        status: int = int(server_response_list[2])

        if status == 0:
            self.master.destroy()

    def home_page(self):
        for widget in self.base_frame.winfo_children():
            widget.destroy()

        title_label = customtkinter.CTkLabel(master=self.base_frame, text="Welcome to TetrisGame!", text_color='black',
                                             font=('Helvetica', 32))
        title_label.pack(pady=40)

        leaderboard_button = customtkinter.CTkButton(master=self.base_frame, text="leaderboard", height=60,
                                                     corner_radius=5,
                                                     fg_color='#418688',
                                                     text_color='black', font=('Helvetica', 18),
                                                     command=self.leaderboard)
        leaderboard_button.pack(anchor='center')

        start_game_button = customtkinter.CTkButton(master=self.base_frame, text="Start Game", height=60,
                                                    corner_radius=5,
                                                    fg_color='#418688',
                                                    text_color='black', font=('Helvetica', 18),
                                                    command=lambda: tetris_game(client_socket=self.client_socket,
                                                                                username=self.username, key=self.key))
        start_game_button.pack(pady=60, anchor='center')

    def leaderboard(self):
        for widget in self.base_frame.winfo_children():
            widget.destroy()

        icons_frame = customtkinter.CTkFrame(master=self.base_frame)
        icons_frame.pack(fill='both')
        home_image = ImageTk.PhotoImage(Image.open("Icons/home_FILL1_wght400_GRAD0_opsz24.png").resize((40, 40)))
        return_home_button = customtkinter.CTkButton(master=icons_frame, text="", height=30, corner_radius=5,
                                                     fg_color='transparent', image=home_image, width=40,

                                                     text_color='black', font=('Helvetica', 18), command=self.home_page)
        return_home_button.pack(anchor='n', pady=10, side='left')

        leaderboard_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#418688')
        leaderboard_frame.pack(pady=20)
        self.show_leaderboard(leaderboard_frame)

        refresh_image = ImageTk.PhotoImage(Image.open("Icons/Refresh_icon.png").resize((40, 40)))
        return_home_button = customtkinter.CTkButton(master=icons_frame, text="", height=30, corner_radius=5,
                                                     fg_color='transparent', image=refresh_image, width=40,

                                                     text_color='black', font=('Helvetica', 18),
                                                     command=lambda: self.show_leaderboard(leaderboard_frame))
        return_home_button.pack(side='left', anchor='n', pady=10, padx=20)

    def show_leaderboard(self, leaderboard_frame):
        for widget in leaderboard_frame.winfo_children():
            widget.destroy()

        headers: list = ["Placement", "Username", "Last Game Score", "Highest Score"]
        data_rows: list = ClientFunctions(self.client_socket, key=self.key).get_leaderboard_data()

        rows = 10
        # columns = len(headers) + 1
        columns = len(headers)

        for col in range(columns):
            header = customtkinter.CTkLabel(leaderboard_frame, text=f"{headers[col]}", fg_color='#418688')
            header.grid(row=0, column=col, padx=60, pady=20)

        for row in range(0, rows):
            for col in range(columns):
                cell = customtkinter.CTkLabel(leaderboard_frame, text=f"{data_rows[row][col]}")
                cell.grid(row=row + 1, column=col, padx=60, pady=20)

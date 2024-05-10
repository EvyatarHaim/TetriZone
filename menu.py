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

        self.master.geometry('1300x900')
        self.master.title("TetrisGame- Menu")
        self.master.resizable(False, False)

        self.master.protocol("WM_DELETE_WINDOW", lambda: self.master_window_closed(self.client_socket, self.key,
                                                                                   self.username))
        self.background_frame = customtkinter.CTkFrame(master=self.master, fg_color='#010002', bg_color='#010002')
        self.background_frame.pack(fill='both', expand=True)

        self.base_frame = customtkinter.CTkFrame(master=self.background_frame, fg_color='transparent',
                                                 bg_color='transparent')
        self.base_frame.pack(fill='both', expand=True, padx=30, pady=30)

        self.side_bar_frame = customtkinter.CTkFrame(master=self.base_frame, width=300, fg_color='#232124',
                                                     border_width=3, border_color='#746898')
        self.side_bar_frame.pack(side='left', fill='both', expand=False, padx=10)

        self.menu_frame = customtkinter.CTkFrame(self.base_frame, fg_color='#232124')
        self.menu_frame.pack(side='right', fill='both', expand=True)

        self.home_page()

    def master_window_closed(self, client_socket: socket, key, username):
        server_response = ClientFunctions(client_socket=client_socket, key=key).update_status(username=username,
                                                                                              status=0)

        server_response_list = server_response.split('|')
        status: int = int(server_response_list[2])

        if status == 0:
            self.master.destroy()

    def side_nav_bar(self):

        home_image = ImageTk.PhotoImage(Image.open("Icons/home_FILL1_wght400_GRAD0_opsz24.png").resize((40, 40)))
        return_home_button = customtkinter.CTkButton(master=self.side_bar_frame, text="HOME", corner_radius=5,
                                                     fg_color='transparent', image=home_image,
                                                     text_color='black', font=('Helvetica', 32), command=self.home_page)
        return_home_button.pack(anchor='nw', side='left', pady=5, padx=5)

    def home_page(self):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        for widget in self.side_bar_frame.winfo_children():
            widget.destroy()


        # title_label = customtkinter.CTkLabel(master=self.base_frame, text="Welcome to TetrisGame!", text_color='black',
        #                                      font=('Helvetica', 32))
        # title_label.pack(pady=40)

        self.side_nav_bar()

        leaderboard_button = customtkinter.CTkButton(master=self.menu_frame, text="leaderboard", height=60,
                                                     corner_radius=5,
                                                     fg_color='#418688',
                                                     text_color='black', font=('Helvetica', 18),
                                                     command=self.leaderboard)
        leaderboard_button.pack(anchor='center')

        start_game_button = customtkinter.CTkButton(master=self.menu_frame, text="Start Game", height=60,
                                                    corner_radius=5,
                                                    fg_color='#418688',
                                                    text_color='black', font=('Helvetica', 18),
                                                    command=lambda: tetris_game(client_socket=self.client_socket,
                                                                                username=self.username, key=self.key))
        start_game_button.pack(pady=60, anchor='center')

    def leaderboard(self):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        icons_frame = customtkinter.CTkFrame(master=self.menu_frame)
        icons_frame.pack(fill='both')
        home_image = ImageTk.PhotoImage(Image.open("Icons/home_FILL1_wght400_GRAD0_opsz24.png").resize((40, 40)))
        return_home_button = customtkinter.CTkButton(master=icons_frame, text="", height=30, corner_radius=5,
                                                     fg_color='transparent', image=home_image, width=40,

                                                     text_color='black', font=('Helvetica', 18), command=self.home_page)
        return_home_button.pack(anchor='n', pady=10, side='left')

        scroll_frame = customtkinter.CTkScrollableFrame(self.menu_frame, width=580, height=380)
        scroll_frame.pack(padx=20, pady=30, fill="both", expand=True)
        self.show_leaderboard(scroll_frame)

        refresh_image = ImageTk.PhotoImage(Image.open("Icons/Refresh_icon.png").resize((40, 40)))
        return_home_button = customtkinter.CTkButton(master=icons_frame, text="", height=30, corner_radius=5,
                                                     fg_color='transparent', image=refresh_image, width=40,

                                                     text_color='black', font=('Helvetica', 18),
                                                     command=lambda: self.show_leaderboard(scroll_frame))
        return_home_button.pack(side='left', anchor='n', pady=10, padx=20)

    def show_leaderboard(self, leaderboard_frame):
        for widget in leaderboard_frame.winfo_children():
            widget.destroy()

        headers: list = ["Placement", "Username", "Last Game Score", "Highest Score", "Status"]
        data_rows: list = ClientFunctions(self.client_socket, key=self.key).get_leaderboard_data()

        def get_status(username):
            return ClientFunctions(self.client_socket, key=self.key).get_status(username)

        rows = len(data_rows)
        # columns = len(headers) + 1
        columns = len(headers)

        for col in range(columns):
            header = customtkinter.CTkLabel(leaderboard_frame, text=f"{headers[col]}", fg_color='transparent')
            header.grid(row=0, column=col, padx=60, pady=20)

        for row in range(0, rows):
            for col in range(columns):
                if col == columns - 1:
                    status = get_status(data_rows[row][1])
                    if status == "Online":
                        cell = customtkinter.CTkLabel(leaderboard_frame, text=f"{status}", text_color='green')
                        cell.grid(row=row + 1, column=col, padx=60, pady=20)
                    else:
                        cell = customtkinter.CTkLabel(leaderboard_frame, text=f"{status}", text_color='red')
                        cell.grid(row=row + 1, column=col, padx=60, pady=20)
                else:
                    cell = customtkinter.CTkLabel(leaderboard_frame, text=f"{data_rows[row][col]}")
                    cell.grid(row=row + 1, column=col, padx=60, pady=20)

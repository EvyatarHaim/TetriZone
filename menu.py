import socket
import customtkinter
from PIL import ImageTk, Image
from Game.tetris import tetris_game
from client_commands import ClientFunctions
from database import handel_placement


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

        self.main_frame = customtkinter.CTkFrame(self.base_frame, fg_color='#232124')
        self.main_frame.pack(side='right', fill='both', expand=True)

        self.display_logo(self.main_frame)

        self.menu_frame = customtkinter.CTkFrame(self.main_frame, fg_color='#232124')
        self.menu_frame.pack(side='right', fill='both', expand=True)

        self.side_nav_bar()
        self.home_page()

    def master_window_closed(self, client_socket: socket, key, username):
        server_response = ClientFunctions(client_socket=client_socket, key=key).update_status(username=username,
                                                                                              status=0)

        server_response_list = server_response.split('|')
        status: int = int(server_response_list[2])

        if status == 0:
            self.master.destroy()

    def display_logo(self, frame):
        logo_icon = ImageTk.PhotoImage(Image.open("Icons/TetrisZone_logo_Poppins_v2.png").resize((160, 40)))
        logo = customtkinter.CTkButton(master=frame, text="", fg_color='transparent', image=logo_icon, hover=False,
                                       command=lambda: self.home_page())

        logo.pack(anchor='nw', side='top')

    def destroy_menu(self):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

    def side_nav_bar(self):

        home_icon = ImageTk.PhotoImage(Image.open("Icons/home_24dp_FILL0_wght400_GRAD0_opsz24.png").resize((32, 32)))
        home_frame = customtkinter.CTkFrame(master=self.side_bar_frame, fg_color='transparent', bg_color='transparent')
        home_frame.pack(pady=3, padx=3, anchor='nw', side='top')
        return_home_button = customtkinter.CTkButton(master=home_frame, text="HOME", corner_radius=5,
                                                     fg_color='transparent', image=home_icon,
                                                     text_color='#e4e2e5', font=('Poppins Regular', 24),
                                                     command=self.home_page)
        return_home_button.pack(anchor='nw', side='left', pady=5, padx=5)
        home_label = customtkinter.CTkLabel(master=home_frame, fg_color='transparent', bg_color='transparent')

        leaderboard_icon = ImageTk.PhotoImage(Image.open("Icons/leaderboard_24dp_FILL0_wght400_GRAD0_opsz24.png")
                                              .resize((32, 32)))
        leaderboard_button = customtkinter.CTkButton(master=self.side_bar_frame, text="LEADERBOARD", corner_radius=5,
                                                     fg_color='transparent', image=leaderboard_icon,
                                                     text_color='#e4e2e5', font=('Poppins Regular', 24),
                                                     command=self.leaderboard_page)
        leaderboard_button.pack(anchor='nw', side='top', pady=5, padx=5)

        profile_icon = ImageTk.PhotoImage(Image.open("Icons/account_circle_24dp_FILL0_wght400_GRAD0_opsz24.png")
                                          .resize((32, 32)))
        profile_button = customtkinter.CTkButton(master=self.side_bar_frame, text="PROFILE", corner_radius=5,
                                                 fg_color='transparent', image=profile_icon,
                                                 text_color='#e4e2e5', font=('Poppins Regular', 24),
                                                 command=self.profile_page)
        profile_button.pack(anchor='nw', side='bottom', pady=10, padx=5)

    def home_page(self):
        self.destroy_menu()

        # title_label = customtkinter.CTkLabel(master=self.base_frame, text="Welcome to TetrisGame!",
        # text_color='black', font=('Helvetica', 32)) title_label.pack(pady=40)

        start_game_button = customtkinter.CTkButton(master=self.menu_frame, text="Start Game", height=60,
                                                    corner_radius=5,
                                                    fg_color='#418688',
                                                    text_color='black', font=('Helvetica', 18),
                                                    command=lambda: tetris_game(client_socket=self.client_socket,
                                                                                username=self.username, key=self.key))
        start_game_button.pack(pady=60, anchor='center')

    def leaderboard_page(self):
        self.destroy_menu()

        header_frame = customtkinter.CTkFrame(master=self.menu_frame, fg_color='transparent', bg_color='transparent')
        header_frame.pack(anchor='nw', side='top', fill='x', pady=10)
        refresh_image = ImageTk.PhotoImage(
            Image.open("Icons/refresh_24dp_FILL0_wght400_GRAD0_opsz24.png").resize((40, 40)))
        return_home_button = customtkinter.CTkButton(master=header_frame, text="", height=30, corner_radius=5,
                                                     fg_color='transparent', image=refresh_image, hover=False,
                                                     command=lambda: self.show_leaderboard(scroll_frame))
        return_home_button.pack(anchor='nw', side='right', padx=20)
        title_frame = customtkinter.CTkFrame(master=header_frame, fg_color='transparent', bg_color='transparent')
        title_frame.pack(anchor='center', side='left', padx=20)
        title = customtkinter.CTkLabel(master=title_frame, fg_color='transparent', bg_color='transparent',
                                       text_color='#e4e2e5', text="LEADERBOARD", font=("Poppins Black", 32))
        title.pack(anchor='center')

        scroll_frame = customtkinter.CTkScrollableFrame(self.menu_frame, fg_color='#2E2E2F',
                                                        scrollbar_fg_color='transparent', )
        scroll_frame.pack(padx=20, pady=20, anchor='n', side='top', fill='both', expand=True)
        self.show_leaderboard(scroll_frame)

    def show_leaderboard(self, leaderboard_frame):
        for widget in leaderboard_frame.winfo_children():
            widget.destroy()

        handel_placement()

        headers: list = ["Placement", "Username", "Last Game Score", "Highest Score", "Status"]
        data_rows: list = ClientFunctions(self.client_socket, key=self.key).get_leaderboard_data()

        def get_status(username):
            return ClientFunctions(self.client_socket, key=self.key).get_status(username)

        trophy_icon = ImageTk.PhotoImage(
            Image.open("Icons/trophy_24dp_FILL1_wght400_GRAD0_opsz24.png").resize((20, 20)))
        rows = len(data_rows)
        columns = len(headers)

        for col in range(columns):
            header = customtkinter.CTkLabel(leaderboard_frame, text=f"{headers[col]}", fg_color='transparent',
                                            bg_color='transparent', font=('Poppins Bold', 18), text_color="#e4e2e5", )
            header.grid(row=0, column=col, padx=40)

        for row in range(0, rows):
            for col in range(columns):
                if col == 0 and row == 0:  # First Place
                    first_place_frame = customtkinter.CTkFrame(master=leaderboard_frame, fg_color='transparent',
                                                               bg_color='transparent')
                    trophy = customtkinter.CTkButton(first_place_frame, text="", image=trophy_icon, width=20,
                                                     fg_color='transparent', bg_color='transparent', hover=False)
                    trophy.pack(anchor='n', side='left')
                    placement = customtkinter.CTkLabel(first_place_frame, text=f"{data_rows[row][col]}",
                                                       text_color='#e4e2e5', fg_color='transparent',
                                                       bg_color='transparent', font=('Poppins Bold', 16))
                    placement.pack(anchor='center', side='left', pady=3, padx=50)

                    first_place_frame.grid(row=row + 1, column=col, sticky='w')

                elif col == columns - 1:  # Stats column
                    status = get_status(data_rows[row][1])
                    if status == "Online":
                        cell = customtkinter.CTkLabel(leaderboard_frame, text=f"{status}", text_color='green',
                                                      fg_color='transparent',
                                                      bg_color='transparent', font=('Poppins Bold', 12))
                        cell.grid(row=row + 1, column=col, padx=40, pady=20)

                    else:
                        cell = customtkinter.CTkLabel(leaderboard_frame, text=f"{status}", text_color='red',
                                                      fg_color='transparent',
                                                      bg_color='transparent', font=('Poppins Bold', 12))
                        cell.grid(row=row + 1, column=col, padx=40, pady=20)
                elif col == 0:  # Placement column
                    cell = customtkinter.CTkLabel(leaderboard_frame, text=f"{data_rows[row][col]}",
                                                  fg_color='transparent',
                                                  bg_color='transparent', font=('Poppins Black', 16),
                                                  text_color="#e4e2e5", )
                    cell.grid(row=row + 1, column=col, padx=40, pady=20)
                else:
                    cell = customtkinter.CTkLabel(leaderboard_frame, text=f"{data_rows[row][col]}",
                                                  fg_color='transparent',
                                                  bg_color='transparent', font=('Poppins Regular', 12),
                                                  text_color="#e4e2e5", )
                    cell.grid(row=row + 1, column=col, padx=40, pady=20)

    def profile_page(self):
        self.destroy_menu()

        header_frame = customtkinter.CTkFrame(master=self.menu_frame, fg_color="#232124", bg_color="#232124")
        header_frame.pack(side='top', anchor='nw', padx=30, pady=20, fill='both')

        profile_image = ImageTk.PhotoImage(Image.open("Icons/face_48dp_FILL0_wght400_GRAD0_opsz48.png")
                                           .resize((250, 250)))

        profile_image_label = customtkinter.CTkLabel(master=header_frame, text="", image=profile_image)
        profile_image_label.pack(anchor='nw', side='left')

        text_frame = customtkinter.CTkFrame(master=header_frame, fg_color='transparent', bg_color='transparent')
        text_frame.pack(anchor='w', side='left', padx=40)
        username_label = customtkinter.CTkLabel(master=text_frame, text=self.username, text_color='#e4e2e5',
                                                font=('Poppins Black', 64))
        username_label.pack(anchor='nw', side='top', padx=30, pady=20)

        creation_date = ClientFunctions(self.client_socket, key=self.key).get_creation_date(self.username)
        date_label = customtkinter.CTkLabel(master=text_frame, text=f"Created Date: {creation_date}",
                                            text_color='#e4e2e5', font=('Poppins Bold', 18))
        date_label.pack(anchor='nw', side='bottom', padx=30)

        stats_frame = customtkinter.CTkFrame(master=self.menu_frame, fg_color='#232124')
        stats_frame.pack(side='left', fill='both', expand=True, padx=30, pady=10)
        stats_label = customtkinter.CTkLabel(master=stats_frame, text=f"{self.username}'s stats:",
                                             font=('Poppins Bold', 28))
        stats_label.pack(anchor='nw')

        info_stats_frame = customtkinter.CTkFrame(master=stats_frame, fg_color='#232124', border_width=3,
                                                  border_color='#746898')
        info_stats_frame.pack(fill='both', expand=True)
        self.show_stats(info_stats_frame)

    def show_stats(self, frame):
        top_row = customtkinter.CTkFrame(master=frame, bg_color='transparent', fg_color='transparent')
        top_row.pack(side='top', pady=20, padx=10, fill='x')

        score_frame = customtkinter.CTkFrame(master=top_row, bg_color='transparent', fg_color='transparent')
        score_frame.pack(padx=20, anchor='nw', side='left')
        total_score = ClientFunctions(self.client_socket, key=self.key).get_total_score(self.username)
        total_score_label = customtkinter.CTkLabel(master=score_frame, text="Total score: ",
                                                   font=('Poppins Bold', 28))
        total_score_label.pack(anchor='w', side='left')
        score_label = customtkinter.CTkLabel(master=score_frame, text=str(total_score), width=44,
                                             font=('Poppins Regular', 22))
        score_label.pack(anchor='center', side='left', padx=5, pady=1)
        # --------------------------------------------------------------------------------------------------------------
        last_game_score_frame = customtkinter.CTkFrame(master=top_row, bg_color='transparent', fg_color='transparent')
        last_game_score_frame.pack(padx=30, anchor='nw', side='left')
        last_game_score = ClientFunctions(self.client_socket, key=self.key).get_last_game_score(self.username)
        last_game_score_label = customtkinter.CTkLabel(master=last_game_score_frame, text=f"Last game score: ",
                                                       font=('Poppins Bold', 28))
        last_game_score_label.pack(anchor='w', side='left')
        last_game_score_value_label = customtkinter.CTkLabel(master=last_game_score_frame, text=str(last_game_score),
                                                             width=44,
                                                             font=('Poppins Regular', 22))
        last_game_score_value_label.pack(anchor='center', side='left', padx=5, pady=1)
        # --------------------------------------------------------------------------------------------------------------
        highest_score_frame = customtkinter.CTkFrame(master=top_row, bg_color='transparent', fg_color='transparent')
        highest_score_frame.pack(anchor='ne', side='left')
        highest_score = ClientFunctions(self.client_socket, key=self.key).get_highest_score(self.username)
        highest_score_label = customtkinter.CTkLabel(master=highest_score_frame, text=f"Highest score: ",
                                                     font=('Poppins Bold', 28))
        highest_score_label.pack(anchor='w', side='left')
        highest_score_value_label = customtkinter.CTkLabel(master=highest_score_frame, text=str(highest_score),
                                                           width=44,
                                                           font=('Poppins Regular', 22))
        highest_score_value_label.pack(anchor='center', side='left', padx=5, pady=1)

        # --------------------------------------------------------------------------------------------------------------

        bottom_row = customtkinter.CTkFrame(master=frame, bg_color='transparent', fg_color='transparent')
        bottom_row.pack(side='top', pady=20, padx=10, fill='x')

        total_lines_frame = customtkinter.CTkFrame(master=bottom_row, bg_color='transparent', fg_color='transparent')
        total_lines_frame.pack(padx=20, anchor='nw', side='left')
        total_lines = ClientFunctions(self.client_socket, key=self.key).get_total_lines(self.username)
        total_lines_label = customtkinter.CTkLabel(master=total_lines_frame, text=f"Total lines: ",
                                                   font=('Poppins Bold', 28))
        total_lines_label.pack(anchor='w', side='left')
        total_lines_value_label = customtkinter.CTkLabel(master=total_lines_frame, text=str(total_lines), width=44,
                                                         font=('Poppins Regular', 22))
        total_lines_value_label.pack(anchor='center', side='left', padx=5, pady=1)
        # --------------------------------------------------------------------------------------------------------------
        games_played_frame = customtkinter.CTkFrame(master=bottom_row, bg_color='transparent', fg_color='transparent')
        games_played_frame.pack(padx=30, anchor='nw', side='left')
        games_played = ClientFunctions(self.client_socket, key=self.key).get_games_played(self.username)
        games_played_label = customtkinter.CTkLabel(master=games_played_frame, text=f"Games played: ",
                                                    font=('Poppins Bold', 28))
        games_played_label.pack(anchor='w', side='left')
        games_played_value_label = customtkinter.CTkLabel(master=games_played_frame, text=str(games_played), width=44,
                                                          font=('Poppins Regular', 22))
        games_played_value_label.pack(anchor='center', side='left', padx=5, pady=1)
        # --------------------------------------------------------------------------------------------------------------
        played_time_frame = customtkinter.CTkFrame(master=bottom_row, bg_color='transparent', fg_color='transparent')
        played_time_frame.pack(anchor='ne', side='left')
        played_time = ClientFunctions(self.client_socket, key=self.key).get_played_time(self.username)
        played_time_label = customtkinter.CTkLabel(master=played_time_frame, text=f"Play time: ",
                                                   font=('Poppins Bold', 28))
        played_time_label.pack(anchor='w', side='left')
        played_time_value_label = customtkinter.CTkLabel(master=played_time_frame, text=played_time, width=44,
                                                         font=('Poppins Regular', 22))
        played_time_value_label.pack(anchor='center', side='left', padx=5, pady=1)

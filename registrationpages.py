import socket
import customtkinter
from customtkinter import CTkButton
from menu import Menu
from client_commands import ClientFunctions


class RegistrationPages:
    def __init__(self, client_socket: socket, master, key):
        self.client_socket = client_socket
        self.key = key
        self.master = master
        self.master.geometry('600x820')
        self.master.title("Tetris Game")
        self.master.resizable(False, False)

        self.base_background = customtkinter.CTkFrame(master=self.master, fg_color='#010002', bg_color='#010002')
        self.base_background.pack(fill='both', expand=True)

        self.margin_top = customtkinter.CTkFrame(master=self.base_background, fg_color='#010002',
                                                 bg_color='#010002', height=40)
        self.margin_top.pack(fill='both', side='top')

        self.error_frame = customtkinter.CTkFrame(master=self.base_background, fg_color='#010002',
                                                  bg_color='#010002', height=40)
        self.error_frame.pack(fill='both', side='bottom')

        self.base_frame = customtkinter.CTkFrame(master=self.base_background, fg_color='#232124', corner_radius=10)
        self.base_frame.pack(padx=40, fill='both', expand=True)  # (520x740)

        self.login_page()

    def destroy_error(self):
        for widget in self.error_frame.winfo_children():
            widget.destroy()

    def display_error(self, message):
        self.destroy_error()
        error_label = customtkinter.CTkLabel(master=self.error_frame, text=message, text_color='#e4e2e5',
                                             fg_color='#cc0000', bg_color='#FF204E', corner_radius=3,
                                             font=("Poppins Regular", 14))
        error_label.pack(fill='both', anchor='center')

    def login_page(self):
        for widget in self.base_frame.winfo_children():
            widget.destroy()
        self.destroy_error()

        self.master.title("Tetris Game - Login Page")

        title_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124', corner_radius=10)
        title_frame.pack(pady=10, fill='both')
        title_label = customtkinter.CTkLabel(master=title_frame, text="LOGIN", text_color='#e4e2e5',
                                             font=('Poppins Black', 42))
        title_label.pack(side='top', anchor='center', pady=20)

        margin = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124', height=75)
        margin.pack(fill='both')

        entry_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124')
        entry_frame.pack(fill='both')

        username_frame = customtkinter.CTkFrame(master=entry_frame, fg_color='#232124')
        username_frame.pack(pady=30, fill='both')
        username_label = customtkinter.CTkLabel(master=username_frame, text="Username", font=('Poppins Bold', 14))
        username_label.pack(padx=40, anchor='w')
        username_entry = customtkinter.CTkEntry(master=username_frame, placeholder_text="Enter your username",
                                                placeholder_text_color='#8f8d90', corner_radius=10,
                                                fg_color='#2d2a2d', bg_color='transparent', border_color='#746898',
                                                border_width=3,
                                                height=40, text_color='#fefcfe', font=('Poppins Regular', 18))
        username_entry.pack(pady=5, padx=40, fill='both')

        password_frame = customtkinter.CTkFrame(master=entry_frame, fg_color='#232124')
        password_frame.pack(pady=10, fill='both')
        password_label = customtkinter.CTkLabel(master=password_frame, text="Password", font=('Poppins Bold', 14))
        password_label.pack(padx=40, anchor='w')
        password_entry = customtkinter.CTkEntry(master=password_frame, placeholder_text="Enter your password",
                                                placeholder_text_color='#8f8d90', corner_radius=10,
                                                fg_color='#2d2a2d', bg_color='transparent', border_color='#746898',
                                                border_width=3,
                                                height=40, text_color='#fefcfe', font=('Poppins Regular', 18), show='*')
        password_entry.pack(pady=5, padx=40, fill='both')

        bottom_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124', corner_radius=10)
        bottom_frame.pack(side='bottom', fill='both')

        login_button = CTkButton(master=bottom_frame, text="Login", height=60, corner_radius=10, fg_color='#4622b7',
                                 text_color='#e4e2e5', font=('Poppins Bold', 32), hover_color='#9b80e1',
                                 command=lambda: self.login_function(username_entry.get(), password_entry.get()))
        login_button.pack(pady=15, padx=40, fill='both', side='top')

        margin_frame = customtkinter.CTkFrame(master=bottom_frame, fg_color='#232124', width=85, height=22)
        margin_frame.pack(side='left', anchor='sw')

        register_frame = customtkinter.CTkFrame(master=bottom_frame, fg_color='#232124')
        register_frame.pack(anchor='s', side='left')
        register_label = customtkinter.CTkLabel(master=register_frame, text="Don't have an account?",
                                                text_color='#e4e2e5', font=('Poppins Bold', 22))
        register_label.pack(pady=20, anchor='s')

        signup_button = customtkinter.CTkButton(master=bottom_frame, text="Sign Up", hover_color='#232124',
                                                corner_radius=5, fg_color='transparent', text_color='#e4e2e5', width=24,
                                                font=('Poppins Bold', 16), command=self.register_page)
        signup_button.pack(pady=22, anchor='se', side='left')

    def login_function(self, username: str, password: str):
        server_response = ClientFunctions(self.client_socket, key=self.key).handle_login(username=username,
                                                                                         password=password)
        if server_response != "[SERVER:] Login successfully":
            error_message = server_response[4:]
            self.display_error(error_message)
            return

        self.master.destroy()
        root_window = customtkinter.CTk()
        Menu(client_socket=self.client_socket, master=root_window, username=username, key=self.key)
        root_window.mainloop()

    def register_page(self):
        for widget in self.base_frame.winfo_children():
            widget.destroy()
        self.destroy_error()

        self.master.title("Tetris Game - Signup Page")
        title_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124', corner_radius=10)
        title_frame.pack(pady=10, fill='both')
        title_label = customtkinter.CTkLabel(master=title_frame, text="SIGN UP", text_color='#e4e2e5',
                                             font=('Poppins Black', 42))
        title_label.pack(side='top', anchor='center', pady=20)

        entry_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124')
        entry_frame.pack(fill='both')

        name_frame = customtkinter.CTkFrame(master=entry_frame, fg_color='#232124')
        name_frame.pack(pady=5, fill='both')
        name_label = customtkinter.CTkLabel(master=name_frame, text="First Name", font=('Poppins Bold', 14))
        name_label.pack(padx=40, anchor='w')
        name_entry = customtkinter.CTkEntry(master=name_frame, placeholder_text="Enter your first name",
                                            placeholder_text_color='#8f8d90', corner_radius=10,
                                            fg_color='#2d2a2d', bg_color='transparent', border_color='#746898',
                                            border_width=3,
                                            height=40, text_color='#fefcfe', font=('Poppins Regular', 18))
        name_entry.pack(pady=5, padx=40, fill='both')

        age_frame = customtkinter.CTkFrame(master=entry_frame, fg_color='#232124')
        age_frame.pack(pady=5, fill='both')
        age_label = customtkinter.CTkLabel(master=age_frame, text="Age", font=('Poppins Bold', 14))
        age_label.pack(padx=40, anchor='w')
        age_entry = customtkinter.CTkEntry(master=age_frame, placeholder_text="Enter your age",
                                           placeholder_text_color='#8f8d90', corner_radius=10,
                                           fg_color='#2d2a2d', bg_color='transparent', border_color='#746898',
                                           border_width=3,
                                           height=40, text_color='#fefcfe', font=('Poppins Regular', 18))
        age_entry.pack(pady=5, padx=40, fill='both')

        username_frame = customtkinter.CTkFrame(master=entry_frame, fg_color='#232124')
        username_frame.pack(pady=5, fill='both')
        username_label = customtkinter.CTkLabel(master=username_frame, text="Username", font=('Poppins Bold', 14))
        username_label.pack(padx=40, anchor='w')
        username_entry = customtkinter.CTkEntry(master=username_frame, placeholder_text="Enter username",
                                                placeholder_text_color='#8f8d90', corner_radius=10,
                                                fg_color='#2d2a2d', bg_color='transparent', border_color='#746898',
                                                border_width=3,
                                                height=40, text_color='#fefcfe', font=('Poppins Regular', 18))
        username_entry.pack(pady=5, padx=40, fill='both')

        password_frame = customtkinter.CTkFrame(master=entry_frame, fg_color='#232124')
        password_frame.pack(pady=5, fill='both')
        password_label = customtkinter.CTkLabel(master=password_frame, text="Password", font=('Poppins Bold', 14))
        password_label.pack(padx=40, anchor='w')
        password_entry = customtkinter.CTkEntry(master=password_frame, placeholder_text="Enter password",
                                                placeholder_text_color='#8f8d90', corner_radius=10,
                                                fg_color='#2d2a2d', bg_color='transparent', border_color='#746898',
                                                border_width=3,
                                                height=40, text_color='#fefcfe', font=('Poppins Regular', 18), show='*')
        password_entry.pack(pady=5, padx=40, fill='both')

        confirm_password_frame = customtkinter.CTkFrame(master=entry_frame, fg_color='#232124')
        confirm_password_frame.pack(pady=5, fill='both')
        confirm_password_label = customtkinter.CTkLabel(master=confirm_password_frame, text="Confirm Password",
                                                        font=('Poppins Bold', 14))
        confirm_password_label.pack(padx=40, anchor='w')
        confirm_password_entry = customtkinter.CTkEntry(master=confirm_password_frame,
                                                        placeholder_text="Enter the same password",
                                                        placeholder_text_color='#8f8d90', corner_radius=10,
                                                        fg_color='#2d2a2d', bg_color='transparent',
                                                        border_color='#746898',
                                                        border_width=3,
                                                        height=40, text_color='#fefcfe', font=('Poppins Regular', 18),
                                                        show='*')
        confirm_password_entry.pack(pady=5, padx=40, fill='both')

        bottom_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124', corner_radius=10)
        bottom_frame.pack(side='bottom', fill='both')

        submit_button = CTkButton(master=bottom_frame, text="Submit", height=60, corner_radius=10, fg_color='#4622b7',
                                  text_color='#e4e2e5', font=('Poppins Bold', 32), hover_color='#9b80e1',
                                  command=lambda: self.submit_function(name_entry.get(), age_entry.get(),
                                                                       username_entry.get(), password_entry.get(),
                                                                       confirm_password_entry.get()))
        submit_button.pack(pady=15, padx=40, fill='both', side='top')

        margin = customtkinter.CTkFrame(master=bottom_frame, fg_color='#232124', width=75, height=22)
        margin.pack(side='left', anchor='sw')

        login_frame = customtkinter.CTkFrame(master=bottom_frame, fg_color='#232124')
        login_frame.pack(anchor='s', side='left')
        login_label = customtkinter.CTkLabel(master=login_frame, text="Already have an account?",
                                             text_color='#e4e2e5', font=('Poppins Bold', 22))
        login_label.pack(pady=20, anchor='s')

        signup_button = customtkinter.CTkButton(master=bottom_frame, text="Log In", hover_color='#232124',
                                                corner_radius=5, fg_color='transparent', text_color='#e4e2e5', width=24,
                                                font=('Poppins Bold', 16), command=self.login_page)
        signup_button.pack(pady=22, anchor='se', side='left')

    def submit_function(self, first_name: str, age: str, username: str, password: str, confirm_password: str):
        if password != confirm_password:
            error_message = "It is not the same password"
            self.display_error(error_message)
            return

        if first_name == "" or age == "" or username == "" or password == "" or confirm_password == "":
            error_message = "One or more entries are empty"
            self.display_error(error_message)
            return

        server_response = ClientFunctions(self.client_socket, key=self.key).handle_registry(name=first_name, age=age,
                                                                                            username=username,
                                                                                            password=password)
        if server_response != "[SERVER:] User have created successfully":
            error_message = server_response[4:]
            self.display_error(error_message)
            return

        self.master.destroy()
        root_window = customtkinter.CTk()
        Menu(client_socket=self.client_socket, master=root_window, username=username, key=self.key)
        root_window.mainloop()

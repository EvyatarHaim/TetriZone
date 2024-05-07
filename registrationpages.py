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
        self.master.geometry('500x620')
        self.master.title("TetrisGame")
        self.master.resizable(False, False)

        self.base_background = customtkinter.CTkFrame(master=self.master, fg_color='#010002', bg_color='#010002')
        self.base_background.pack(fill='both', expand=True)

        self.base_frame = customtkinter.CTkFrame(master=self.base_background, fg_color='#232124', corner_radius=10)
        self.base_frame.pack(padx=40, pady=30, fill='both', expand=True)

        self.login_page()

    def display_error(self, message):
        error_label = customtkinter.CTkLabel(
            master=self.base_background,
            text=message,
            text_color='white',
            fg_color='red',
            bg_color='red'
        )
        error_label.pack(fill='both', anchor='n')

    def login_page(self):
        for widget in self.base_frame.winfo_children():
            widget.destroy()

        self.master.title("TetrisGame- Login Page")

        title_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124')
        title_frame.pack(pady=10, fill='both')
        title_label = customtkinter.CTkLabel(master=title_frame, text="LOGIN", text_color='#e4e2e5',
                                             font=('Poppins Black', 36))
        title_label.pack(side='top', anchor='center', pady=10)

        username_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124')
        username_frame.pack(pady=30, fill='both')
        username_label = customtkinter.CTkLabel(master=username_frame, text="Username", font=('Poppins Bold', 14))
        username_label.pack(padx=30, anchor='w')
        username_entry = customtkinter.CTkEntry(master=username_frame, placeholder_text="Enter your username",
                                                placeholder_text_color='#8f8d90', corner_radius=10,
                                                fg_color='#2d2a2d', bg_color='transparent', border_color='#746898',
                                                border_width=3,
                                                height=40, text_color='#fefcfe', font=('Poppins Regular', 18))
        username_entry.pack(pady=5, padx=30, fill='both')

        password_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124')
        password_frame.pack(pady=10, fill='both')
        password_label = customtkinter.CTkLabel(master=password_frame, text="Password", font=('Poppins Bold', 14))
        password_label.pack(padx=30, anchor='w')
        password_entry = customtkinter.CTkEntry(master=password_frame, placeholder_text="Enter your password",
                                                placeholder_text_color='#8f8d90', corner_radius=10,
                                                fg_color='#2d2a2d', bg_color='transparent', border_color='#746898',
                                                border_width=3,
                                                height=40, text_color='#fefcfe', font=('Poppins Regular', 18), show='*')
        password_entry.pack(pady=5, padx=30, fill='both')

        login_button = CTkButton(master=self.base_frame, text="Login", height=60, corner_radius=10, fg_color='#4622b7',
                                 text_color='#e4e2e5', font=('Poppins Bold', 32), hover_color='#9b80e1',
                                 command=lambda: self.login_function(username_entry.get(), password_entry.get()))
        login_button.pack(pady=40, padx=30, fill='both')

        margin_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124', width=30)
        margin_frame.pack(side='left', anchor='sw')
        register_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124')
        register_frame.pack(side='left', anchor='sw')
        register_label = customtkinter.CTkLabel(master=register_frame, text="Don't have an account?",
                                                text_color='#e4e2e5', font=('Poppins Bold', 24))
        register_label.pack(pady=20, anchor='s', side='left')

        signup_button = customtkinter.CTkButton(master=self.base_frame, text="Sign Up", hover_color='#232124',
                                                corner_radius=5, fg_color='transparent', text_color='#e4e2e5', width=24,
                                                font=('Poppins Bold', 18), command=self.register_page)
        signup_button.pack(pady=20, side='left')

    def login_function(self, username: str, password: str):
        if username == "" or password == "":
            error_message = "One or more entries are empty"
            self.display_error(error_message)

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

        self.master.title("TetrisGame- Signup Page")
        title_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124')
        title_frame.pack(pady=10, fill='both')
        title_label = customtkinter.CTkLabel(master=title_frame, text="SIGN UP", text_color='#e4e2e5',
                                             font=('Poppins Black', 36))
        title_label.pack(side='top', anchor='center', pady=10)

        name_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124')
        name_frame.pack(pady=5, fill='both')
        name_label = customtkinter.CTkLabel(master=name_frame, text="First Name", font=('Poppins Bold', 14))
        name_label.pack(padx=30, anchor='w')
        name_entry = customtkinter.CTkEntry(master=name_frame, placeholder_text="Enter your first name",
                                            placeholder_text_color='#8f8d90', corner_radius=10,
                                            fg_color='#2d2a2d', bg_color='transparent', border_color='#746898',
                                            border_width=3,
                                            height=40, text_color='#fefcfe', font=('Poppins Regular', 18))
        name_entry.pack(pady=5, padx=30, fill='both')

        age_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124')
        age_frame.pack(pady=5, fill='both')
        age_label = customtkinter.CTkLabel(master=age_frame, text="Age", font=('Poppins Bold', 14))
        age_label.pack(padx=30, anchor='w')
        age_entry = customtkinter.CTkEntry(master=age_frame, placeholder_text="Enter your age",
                                           placeholder_text_color='#8f8d90', corner_radius=10,
                                           fg_color='#2d2a2d', bg_color='transparent', border_color='#746898',
                                           border_width=3,
                                           height=40, text_color='#fefcfe', font=('Poppins Regular', 18))
        age_entry.pack(pady=5, padx=30, fill='both')

        username_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124')
        username_frame.pack(pady=5, fill='both')
        username_label = customtkinter.CTkLabel(master=username_frame, text="Username", font=('Poppins Bold', 14))
        username_label.pack(padx=30, anchor='w')
        username_entry = customtkinter.CTkEntry(master=username_frame, placeholder_text="Enter your username",
                                                placeholder_text_color='#8f8d90', corner_radius=10,
                                                fg_color='#2d2a2d', bg_color='transparent', border_color='#746898',
                                                border_width=3,
                                                height=40, text_color='#fefcfe', font=('Poppins Regular', 18))
        username_entry.pack(pady=5, padx=30, fill='both')

        password_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124')
        password_frame.pack(pady=5, fill='both')
        password_label = customtkinter.CTkLabel(master=password_frame, text="Password", font=('Poppins Bold', 14))
        password_label.pack(padx=30, anchor='w')
        password_entry = customtkinter.CTkEntry(master=password_frame, placeholder_text="Enter your password",
                                                placeholder_text_color='#8f8d90', corner_radius=10,
                                                fg_color='#2d2a2d', bg_color='transparent', border_color='#746898',
                                                border_width=3,
                                                height=40, text_color='#fefcfe', font=('Poppins Regular', 18), show='*')
        password_entry.pack(pady=5, padx=30, fill='both')

        confirm_password_frame = customtkinter.CTkFrame(master=self.base_frame, fg_color='#232124')
        confirm_password_frame.pack(pady=5, fill='both')
        confirm_password_label = customtkinter.CTkLabel(master=confirm_password_frame, text="Confirm Password",
                                                        font=('Poppins Bold', 14))
        confirm_password_label.pack(padx=30, anchor='w')
        confirm_password_entry = customtkinter.CTkEntry(master=confirm_password_frame,
                                                        placeholder_text="Enter the same password",
                                                        placeholder_text_color='#8f8d90', corner_radius=10,
                                                        fg_color='#2d2a2d', bg_color='transparent',
                                                        border_color='#746898',
                                                        border_width=3,
                                                        height=40, text_color='#fefcfe', font=('Poppins Regular', 18),
                                                        show='*')
        confirm_password_entry.pack(pady=5, padx=30, fill='both')

        submit_button = CTkButton(master=self.base_frame, text="Login", height=60, corner_radius=10, fg_color='#4622b7',
                                  text_color='#e4e2e5', font=('Poppins Bold', 32), hover_color='#9b80e1',
                                  command=lambda: self.submit_function(name_entry.get(), age_entry.get(),
                                                                       username_entry.get(), password_entry.get(),
                                                                       confirm_password_entry.get()))
        submit_button.pack(pady=1, padx=30, fill='both')

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
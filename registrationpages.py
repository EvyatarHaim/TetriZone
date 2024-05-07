import socket
import customtkinter
from customtkinter import CTkButton
from menu import Menu
from client_commands import ClientFunctions
from PIL import Image, ImageTk


class RegistrationPages:
    def __init__(self, client_socket: socket, master, key):
        self.client_socket = client_socket
        self.key = key
        self.master = master
        self.master.geometry('600x720')
        self.master.title("TetrisGame")
        self.master.resizable(False, False)

        self.base_background = customtkinter.CTkFrame(master=self.master, fg_color='#025d65', bg_color='#025d65')
        self.base_background.pack(fill='both', expand=True)

        self.base_frame = customtkinter.CTkFrame(master=self.base_background, fg_color='#418688')
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

        image = ImageTk.PhotoImage(Image.open("Icons/login-icon.png").resize((200, 200)))
        image_label = customtkinter.CTkLabel(master=self.base_frame, image=image, text="")
        image_label.pack(pady=50, padx=20)

        title_label = customtkinter.CTkLabel(master=self.base_frame, text="LOGIN", text_color='#000000',
                                             font=('Georgia', 24), )
        title_label.pack(anchor='w', padx=30)

        username_entry = customtkinter.CTkEntry(master=self.base_frame, placeholder_text="Username:",
                                                placeholder_text_color='#000000', corner_radius=10,
                                                fg_color='#fffff1', bg_color='transparent', border_color='#000000',
                                                border_width=3,
                                                height=40, text_color='#000000', font=('Helvetica', 18))
        username_entry.pack(pady=5, padx=30, fill='both')

        password_entry = customtkinter.CTkEntry(master=self.base_frame, placeholder_text="Password:",
                                                placeholder_text_color='#000000', corner_radius=10,
                                                fg_color='#fffff1', bg_color='transparent', border_color='#000000',
                                                border_width=3,
                                                height=40, text_color='#000000', font=('Helvetica', 18), show='*')
        password_entry.pack(pady=20, padx=30, fill='both')

        login_button = CTkButton(master=self.base_frame, text="Login", height=60, corner_radius=10, fg_color='#fffff1',
                                 text_color='#000000', font=('Helvetica', 32), hover_color='#c0d7ce',
                                 command=lambda: self.login_function(username_entry.get(), password_entry.get()))
        login_button.pack(pady=20, padx=30, fill='both')

        register_label = customtkinter.CTkLabel(master=self.base_frame, text="            Don't have an account?",
                                                text_color='black', font=('Helvetica', 24))
        register_label.pack(pady=20, anchor='s', side='left')
        signup_font = customtkinter.CTkFont(family="Ubuntu Medium", size=24, underline=True)

        signup_button = customtkinter.CTkButton(master=self.base_frame, text="Sign Up", hover_color='#418688',
                                                corner_radius=5, fg_color='transparent', text_color='black', width=24,
                                                font=signup_font, command=self.register_page)
        signup_button.pack(pady=20, anchor='se', side='left')

        signup_font.configure(family="Ubuntu Medium")

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

        title_label = customtkinter.CTkLabel(master=self.base_frame, text="SIGN UP", text_color='black',
                                             font=('Helvetica', 32))
        title_label.pack(pady=30)

        name_entry = customtkinter.CTkEntry(master=self.base_frame, placeholder_text="Name:",
                                            placeholder_text_color='black', corner_radius=5, fg_color='white',
                                            height=40, text_color='black', font=('Helvetica', 18))
        name_entry.pack(pady=15, padx=10, fill='both')

        age_entry = customtkinter.CTkEntry(master=self.base_frame, placeholder_text="Age:",
                                           placeholder_text_color='black', corner_radius=5, fg_color='white',
                                           height=40, text_color='black', font=('Helvetica', 18))
        age_entry.pack(pady=15, padx=10, fill='both')

        username_entry = customtkinter.CTkEntry(master=self.base_frame, placeholder_text="Username:",
                                                placeholder_text_color='black', corner_radius=5, fg_color='white',
                                                height=40, text_color='black', font=('Helvetica', 18))
        username_entry.pack(pady=15, padx=10, fill='both')

        password_entry = customtkinter.CTkEntry(master=self.base_frame, placeholder_text="Password:",
                                                placeholder_text_color='black', corner_radius=5, fg_color='white',
                                                height=40, text_color='black', font=('Helvetica', 18), show='*')
        password_entry.pack(pady=15, padx=10, fill='both')
        confirm_password_entry = customtkinter.CTkEntry(master=self.base_frame, placeholder_text="Confirm Password:",
                                                        placeholder_text_color='black', corner_radius=5,
                                                        fg_color='white',
                                                        height=40, text_color='black', font=('Helvetica', 18), show='*')
        confirm_password_entry.pack(pady=15, padx=10, fill='both')

        submit_button = CTkButton(master=self.base_frame, text="Submit", height=60, corner_radius=5, fg_color='#3b1a69',
                                  text_color='white', font=('Helvetica', 18),
                                  command=lambda: self.submit_function(name_entry.get(), age_entry.get(),
                                                                       username_entry.get(), password_entry.get(),
                                                                       confirm_password_entry.get()))
        submit_button.pack(pady=5, padx=10, fill='both')

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

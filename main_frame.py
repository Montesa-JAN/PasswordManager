import customtkinter as ctk
import random
import json
from CTkMessagebox import CTkMessagebox


class MainFrame(ctk.CTkFrame):
    def __init__(self, master, title, table_view):
        font = ("BEBAS", 20)
        super().__init__(master)

        self.table_view = table_view

        self.title = title
        self.grid_rowconfigure((0, 7), weight=1)

        self.title_label = ctk.CTkLabel(self, text=self.title, font=font)
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="new", columnspan=2)

        self.web_label = ctk.CTkLabel(self, text="Website:", font=font)
        self.web_label.grid(row=1, column=0, padx=10, pady=10, sticky="new")

        self.web_input = ctk.CTkEntry(self, width=300, height=40, corner_radius=10)
        self.web_input.grid(row=1, column=1, padx=10, pady=10, sticky="new")
        self.web_input.focus_set()

        self.email_label = ctk.CTkLabel(self, text="Email/Username:", font=font)
        self.email_label.grid(row=3, column=0, padx=10, pady=10, sticky="new")

        self.email_input = ctk.CTkEntry(self, width=300, height=40, corner_radius=10)
        self.email_input.grid(row=3, column=1, padx=10, pady=10, sticky="new")

        self.password_label = ctk.CTkLabel(self, text="Password:", font=font)
        self.password_label.grid(row=5, column=0, padx=10, pady=10, sticky="new")

        self.password_input = ctk.CTkEntry(self, width=300, height=40, corner_radius=10)
        self.password_input.grid(row=5, column=1, padx=10, pady=10, sticky="new")

        self.add_btn = ctk.CTkButton(self, width=150, height=20, corner_radius=10, text="Add",
                                     font=font, command=self.save)
        self.add_btn.grid(row=7, column=0, padx=10, pady=10, sticky="new")

        self.gen_btn = ctk.CTkButton(self, width=150, height=20, corner_radius=10, text="Generate Password",
                                     font=font, command=self.genpassw)
        self.gen_btn.grid(row=7, column=1, padx=10, pady=10, sticky="new")

    # Saves data from input fields to JSON file
    def save(self):
        website = self.web_input.get()
        email = self.email_input.get()
        passw = self.password_input.get()

        new_data = {
            website: {
                "email": email,
                "password": passw
            }
        }

        if not website or not passw:
            CTkMessagebox(title="Error, empty field detected", message="Please don't leave any empty fields!")
            return

        try:
            with open(file="data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            data = {}

        data.update(new_data)

        with open(file="data.json", mode="w") as data_file:
            json.dump(data, data_file, indent=4)
            data_file.close()

        self.web_input.delete(0, 'end')
        self.web_input.focus_set()
        self.email_input.delete(0, 'end')
        self.password_input.delete(0, 'end')

        self.table_view.insert_data(new_data)

    # Random Password Generator
    def genpassw(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u',
                   'v',
                   'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                   'Q',
                   'R',
                   'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        nr_letters = random.randint(8, 10)
        nr_symbols = random.randint(2, 4)
        nr_numbers = random.randint(2, 4)

        p_letter = [random.choice(letters) for _ in range(nr_letters)]
        p_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
        p_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

        password_list = p_letter + p_numbers + p_symbols

        random.shuffle(password_list)

        gen_password = ''.join(password_list)
        self.password_input.insert(0, gen_password)

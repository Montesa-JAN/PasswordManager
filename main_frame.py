import customtkinter as ctk
import secrets
import string
import json
from CTkMessagebox import CTkMessagebox


class MainFrame(ctk.CTkFrame):
    def __init__(self, master, title, tree):
        font = ("BEBAS", 20)
        super().__init__(master)

        self.tree = tree

        self.title = title
        self.grid_rowconfigure((0, 7), weight=1)

        self.title_label = ctk.CTkLabel(self, text=self.title, font=font)
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="new", columnspan=2)

        self.web_label = ctk.CTkLabel(self, text="Website:", font=font)
        self.web_label.grid(row=1, column=0, padx=10, pady=10, sticky="new")

        self.web_input = ctk.CTkEntry(self, width=300, height=40, corner_radius=10)
        self.web_input.grid(row=1, column=1, padx=10, pady=10, sticky="new")
        self.web_input.focus_set()

        self.email_label = ctk.CTkLabel(self, text="Email:", font=font)
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

        new_entry = {
            "email": email,
            "password": passw
        }

        if not website or not passw:
            CTkMessagebox(title="Error, empty field detected", message="Please don't leave any empty fields!")
            return

        try:
            with open(file="data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            data = {}

        # Ensure website key is a list, and append only if not duplicate
        if website in data:
            # Prevent exact duplicates
            if new_entry not in data[website]:
                data[website].append(new_entry)
        else:
            data[website] = [new_entry]

        with open(file="data.json", mode="w") as data_file:
            json.dump(data, data_file, indent=4)

        self.web_input.delete(0, 'end')
        self.web_input.focus_set()
        self.email_input.delete(0, 'end')
        self.password_input.delete(0, 'end')

        self.tree.insert_data({website: [new_entry]})

    # Random Password Generator
    def genpassw(self):
        length = 16
        digits = ''.join(secrets.choice(string.digits) for _ in range(3))
        uppercase = secrets.choice(string.ascii_uppercase)
        symbols = ''.join(secrets.choice(string.punctuation) for _ in range(3))

        remaining_length = length - (3 + 1 + 3)
        remaining_chars = ''.join(secrets.choice(string.ascii_letters + string.digits + symbols) for _ in range(remaining_length))

        password = list(digits + uppercase + symbols + remaining_chars)
        secrets.SystemRandom().shuffle(password)
        self.password_input.insert(0, ''.join(password))

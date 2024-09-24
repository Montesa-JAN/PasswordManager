import json
from tkinter.ttk import Treeview
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


class PasswordListFrame(ctk.CTkScrollableFrame):
    cols = ("Website", "Email/Username", "Password")

    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.title = title

        self.help_text = ctk.CTkLabel(self, text=self.title, font=("Bebas", 20))
        self.help_text.grid(row=0, column=0, padx=10, pady=10, sticky="new")

        self.treeview = Treeview(self, show="headings", columns=self.cols, height=30)
        self.treeview.heading('Website', text='Website')
        self.treeview.heading('Email/Username', text='Email/Username')
        self.treeview.heading('Password', text='Password')
        self.treeview.grid(row=1, column=0, padx=10, pady=10, sticky="news")

        self.load_data()

    # Reads and loads all data from JSON file to TreeView
    def load_data(self):
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                for idx, (website, details) in enumerate(data.items(), start=1):
                    self.treeview.insert('', 'end', values=(website, details["email"], details["password"]))
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump({}, data_file)
        except json.JSONDecodeError:
            CTkMessagebox(title="Corrupt File", message="Sorry the file seems to be corrupted")

    # Inserts data into TreeView from user
    def insert_data(self, data):
        for website, details in data.items():
            self.treeview.insert('', 'end', values=(website, details["email"], details["password"]))

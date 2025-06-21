import json
from tkinter.ttk import Treeview
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from update import UpdateWindow


class PasswordListFrame(ctk.CTkScrollableFrame):
    cols = ("Website", "Email/Username", "Password")

    def __init__(self, master, title):
        font = ("BEBAS", 20)
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.title = title

        self.title_text = ctk.CTkLabel(self, text=self.title, font=font)
        self.title_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="new")

        # Treeview Widget
        self.treeview = Treeview(self, show="headings", columns=self.cols, height=30)
        self.treeview["columns"] = ("Website", "Email", "Password")
        self.treeview.column('Website', width=150, anchor='w')
        self.treeview.column('Email', width=200, anchor='w')
        self.treeview.column('Password', width=200, anchor='w')

        self.treeview.heading('Website', text='Website')
        self.treeview.heading('Email', text='Email')
        self.treeview.heading('Password', text='Password')
        self.treeview.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="news")

        # Top level window for update
        self.toplevel_window = None

        # Inputs
        self.search_btn = ctk.CTkButton(self, width=150, height=20, corner_radius=10, text="Search",
                                        font=font, command=self.search_btn_onclick)
        self.search_btn.grid(row=2, column=0, padx=10, pady=10, sticky="sw")

        self.search_entry = ctk.CTkEntry(self, width=300, height=40, corner_radius=10)
        self.search_entry.grid(row=2, column=1, padx=10, pady=10, sticky="se")

        self.update_btn = ctk.CTkButton(self, width=150, height=20, corner_radius=10, text="Update",
                                        font=font, command=self.open_update_window)
        self.update_btn.grid(row=3, column=0, padx=10, pady=10, sticky="sw")

        self.delete_btn = ctk.CTkButton(self, width=150, height=20, corner_radius=10, text="Delete",
                                        font=font, command=self.delete_row)
        self.delete_btn.grid(row=4, column=0, padx=10, pady=10, sticky="sw")

        self.copy_btn = ctk.CTkButton(self, width=150, height=20, corner_radius=10, text="Copy",
                                           font=font, command=self.copy_passw)
        self.copy_btn.grid(row=3, column=1, padx=10, pady=10, sticky="sw")

        self.data = self.load_data_from_json()

    # Copies password from password column
    def copy_passw(self):
        selected_item = self.treeview.focus()
        row_values = self.treeview.item(selected_item)['values']
        passw_data = row_values[2]

        self.master.clipboard_clear()
        self.master.clipboard_append(str(passw_data))

    # Deletes row in tree view
    def delete_row(self):
        data = self.load_data_from_json()
        selected_item = self.treeview.selection()

        if not selected_item:
            CTkMessagebox(title="Error", message="Please select a row to delete")
            return

        item_id = selected_item[0]
        values = self.treeview.item(item_id, "values")
        website, email, password = values

        if website not in data:
            return

        # Remove the specific entry from the list
        data[website] = [entry for entry in data[website] if not (entry["email"] == email and entry["password"] == password)]
        # If no entries left for this website, remove the key
        if not data[website]:
            del data[website]

        self.treeview.delete(item_id)

        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

    # Loads data from JSON and returns data
    @staticmethod
    def load_data_from_json():
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
            return data
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump({}, data_file)
            return {}
        except json.JSONDecodeError:
            CTkMessagebox(title="Corrupt File", message="Sorry the file seems to be corrupted")
            return None

    def load_to_treeview(self):
        data = self.load_data_from_json()
        if data:
            for website, value in data.items():
                email = value.get("email", "N/A")
                password = value.get("password", "N/A")
                self.treeview.insert('', 'end', values=(website, email, password))

    def insert_data(self, data):
        for website, details in data.items():
            self.treeview.insert('', 'end', values=(website, details["email"], details["password"]))

    # Searches treeview data
    def search_data(self, data):
        search = self.search_entry.get().strip()
        found = False

        if not search:
            CTkMessagebox(title="Empty field", message="Please type something in the search field")
        elif search:
            for item_id, values in data.items():
                if any(search.lower() in str(value).lower() for value in values):
                    self.treeview.focus(item_id)
                    self.treeview.selection_set(item_id)
                    self.treeview.see(item_id)
                    found = True
                    break
        elif not found:
            CTkMessagebox(title="No match", message="No match found, are you sure this account exists?")

    # Get data from treeview
    def get_treeview_data(self):
        data = {}

        for item_id in self.treeview.get_children():
            values = self.treeview.item(item_id, "values")
            data[item_id] = values

        return data

    # Function for search button
    def search_btn_onclick(self):
        data = self.get_treeview_data()
        self.search_data(data)

    def open_update_window(self):
        selected_item = self.treeview.selection()
        if self._is_toplevel_window_open():
            self.toplevel_window.focus()
        else:
            if not selected_item:
                self.show_error_message(message="No row selected")
                return

        item_id = selected_item[0]
        item_values = self.treeview.item(item_id, "values")
        row_index = self.treeview.index(item_id)
        self.create_update_window(item_values, row_index)

    def _is_toplevel_window_open(self):
        return self.toplevel_window is not None and self.toplevel_window.winfo_exists()

    @staticmethod
    def show_error_message(message):
        CTkMessagebox(title="Error", message=message)

    def create_update_window(self, item_values, row_index):
        self.toplevel_window = UpdateWindow(self, self.treeview, item_values, row_index, self.data)
        self.toplevel_window.grab_set()

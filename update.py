import customtkinter as ctk
import json


class UpdateWindow(ctk.CTkToplevel):
    def __init__(self, parent, tree, item_values, row_index, data):
        font = ("BEBAS", 20)
        super().__init__(parent)
        self.tree = tree
        self.row_index = row_index
        self.item_values = item_values
        self.data = data

        self.geometry("500x300")
        self.title("Update Window")
        self.lift()
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Inputs and labels
        self.email_label = ctk.CTkLabel(self, text="Email", font=font)
        self.password_label = ctk.CTkLabel(self, text="Password", font=font)

        self.email_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.password_label.grid(row=3, column=0, padx=10, pady=10, sticky="sw")

        self.email_entry = ctk.CTkEntry(self, width=300, height=40, corner_radius=10)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ne")

        self.password_entry = ctk.CTkEntry(self, width=300, height=40, corner_radius=10)
        self.password_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ne")

        self.save_btn = ctk.CTkButton(self, width=150, height=20, corner_radius=10, text="Save Changes",
                                      font=font, command=self.save_changes)
        self.save_btn.grid(row=4, column=0, padx=10, pady=10, sticky="s")

    def on_close(self):
        self.grab_release()
        self.destroy()

    def save_changes(self):
        selected_website = self.item_values[0]

        new_email = self.email_entry.get().strip()
        new_password = self.password_entry.get().strip()

        if selected_website not in self.data:
            return

        if new_email:
            self.data[selected_website]["email"] = new_email
        if new_password:
            self.data[selected_website]["password"] = new_password

        with open("data.json", "w") as data_file:
            json.dump(self.data, data_file, indent=4)

        self.refresh_ui()
        self.destroy()

    def refresh_ui(self):
        self.tree.delete(*self.tree.get_children())

        for website, credentials in self.data.items():
            self.tree.insert('', 'end', values=(website, credentials["email"], credentials["password"]))

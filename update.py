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
        self.password_label = ctk.CTkLabel(self, text="Password", font=font)

        self.password_label.grid(row=3, column=0, padx=10, pady=10, sticky="sw")

        self.password_entry = ctk.CTkEntry(self, width=300, height=40, corner_radius=10)
        self.password_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ne")

        self.save_btn = ctk.CTkButton(self, width=150, height=20, corner_radius=10, text="Save Changes",
                                      font=font, command=self.save_changes)
        self.save_btn.grid(row=4, column=0, padx=10, pady=10, sticky="s")

    def on_close(self):
        self.grab_release()
        self.destroy()

    def save_changes(self):
        website, email, old_password = self.item_values
        new_password = self.password_entry.get().strip()

        if not new_password:
            return

        # Find and update the correct entry in the list
        for entry in self.data:
            if (entry.get("website") == website and
                entry.get("email") == email and
                entry.get("password") == old_password):
                entry["password"] = new_password
                break

        with open("data.json", "w") as data_file:
            json.dump(self.data, data_file, indent=4)

        self.refresh_ui()
        self.destroy()

    def refresh_ui(self):
        self.tree.delete(*self.tree.get_children())
        for entry in self.data:
            website = entry.get("website", "N/A")
            email = entry.get("email", "N/A")
            password = entry.get("password", "N/A")
            self.tree.insert('', 'end', values=(website, email, password))

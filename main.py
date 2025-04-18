import customtkinter as ctk
import tkinter as tk
from password_list_frame import PasswordListFrame
from main_frame import MainFrame


# Main Class
class PasswordManager(ctk.CTk):
    mode = "dark"
    ctk.set_appearance_mode(mode)
    WIDTH = 1200
    HEIGHT = 900

    def __init__(self):
        super().__init__()
        # Window Config
        self.title("Password Manager 0.2")
        self.geometry(f"{PasswordManager.WIDTH}x{PasswordManager.HEIGHT}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.menu = tk.Menu(self)
        self.color_menu = tk.Menu(self.menu, tearoff=0)
        self.theme_menu = tk.Menu(self.menu, tearoff=0)
        self.color_menu.add_command(label='Light', command=self.change, font=("Bebas", 10))
        self.theme_menu.add_command(label='Blue', command=lambda: self.change_theme("blue"), font=("Bebas", 10))
        self.theme_menu.add_command(label='Green', command=lambda: self.change_theme("green"), font=("Bebas", 10))
        self.theme_menu.add_command(label='Dark Blue', command=lambda: self.change_theme("dark-blue"),
                                    font=("Bebas", 10))
        self.menu.add_cascade(label='Change Color', menu=self.color_menu, font=("Bebas", 15))
        self.menu.add_cascade(label='Change Theme', menu=self.theme_menu, font=("Bebas", 15))
        self.config(menu=self.menu)

        # Window Content
        self.password_frame = PasswordListFrame(self, "Passwords")
        self.password_frame.grid(row=0, column=0, padx=10, pady=10, sticky="news")
        self.password_frame.load_to_treeview()

        self.main_frame = MainFrame(self, "Password Manager", self.password_frame)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="news")

    def change(self):
        if self.mode == "dark":
            ctk.set_appearance_mode("light")
            self.color_menu.entryconfig(0, label="Dark")
            self.mode = "light"
        else:
            ctk.set_appearance_mode("dark")
            self.color_menu.entryconfig(0, label="Light")
            self.mode = "dark"

    def change_theme(self, theme_name):
        ctk.set_default_color_theme(theme_name)
        self.password_frame = PasswordListFrame(self, "Passwords")
        self.password_frame.grid(row=0, column=0, padx=10, pady=10, sticky="news")

        self.main_frame = MainFrame(self, "Password Manager", self.password_frame)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="news")


if __name__ == "__main__":
    app = PasswordManager()
    app.mainloop()

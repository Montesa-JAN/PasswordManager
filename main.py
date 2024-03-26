from tkinter import *
from tkinter import messagebox
import random
import pyclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
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
    pass_input.insert(0, gen_password)
    pyclip.copy(gen_password)


# ---------------------------- SEARCH FUNCTION ------------------------------- #

def find_password():
    website = web_input.get()
    try:
        with open(file="data.json") as data_file:
            data = json.load(data_file)
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title="Found an entry", message=f"Email: {email}\n"
                                                                    f"Password: {password}")
            else:
                messagebox.showwarning(title="Oops", message="No details for the website exists.")
    except FileNotFoundError:
        messagebox.showwarning(title="No file exists", message="No Data File Found.")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = web_input.get()
    email_username = email_input.get()
    password = pass_input.get()
    new_data = {
        website: {
            "email": email_username,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Empty field detected", message="Please don't leave any fields empty!")

    else:

        try:

            with open(file="data.json", mode="r") as data_file:
                # Reading old data
                data = json.load(data_file)
                # Update old data with new data
                data.update(new_data)

                # Save updated data
            with open(file="data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)

        except FileNotFoundError:
            # Create a new data.json file and save new data
            with open(file="data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)

        finally:
            web_input.delete(0, END)
            web_input.focus()
            pass_input.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=2)

# Labels
web_label = Label(text="Website:")
web_label.grid(row=1, column=1)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=1)

pass_label = Label(text="Password:")
pass_label.grid(row=3, column=1)

# Entry
web_input = Entry(width=35)
web_input.grid(row=1, column=2)
web_input.focus()

email_input = Entry(width=35)
email_input.grid(row=2, column=2)
email_input.insert(0, "example.email@com")
pass_input = Entry(width=35)
pass_input.grid(row=3, column=2)

# Buttons
search_button = Button(text="Search", width=20, command=find_password)
search_button.grid(row=1, column=3)

pass_button = Button(text="Generate Password", width=20, command=generate_password)
pass_button.grid(row=3, column=3)

add_button = Button(width=36, text="Add", command=save)
add_button.grid(row=4, column=2, columnspan=2)

window.mainloop()

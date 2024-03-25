from tkinter import *
from tkinter import messagebox
import random
import pyclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    print("Welcome to the PyPassword Generator!")
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


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    with open(file="data.txt", mode="a") as data:
        website = web_input.get()
        email_username = email_input.get()
        password = pass_input.get()

        if len(website) == 0 or len(password) == 0:
            messagebox.showwarning(title="Empty field detected", message="Please don't leave any fields empty!")

        else:
            is_yes = messagebox.askyesno(title=website,
                                         message=f"There are the details entered: \n\nEmail: {email_username}"
                                                 f"\nPassword: {password} \n\nAre these correct?")
            if is_yes:
                data.write(f"{website} | {email_username} | {password}\n")
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
canvas.grid(row=0, column=1)

# Labels
web_label = Label(text="Website:")
web_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

pass_label = Label(text="Password:")
pass_label.grid(row=3, column=0)

# Entry
web_input = Entry(width=35)
web_input.grid(row=1, column=1, columnspan=2)
web_input.focus()

email_input = Entry(width=35)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0, "example.email@com")
pass_input = Entry(width=35)
pass_input.grid(row=3, column=1, columnspan=2)

# Buttons
pass_button = Button(text="Generate Password", command=generate_password)
pass_button.grid(row=3, column=2)

add_button = Button(width=36, text="Add", command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()

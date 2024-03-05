from random import randint, choice
import string
from tkinter import *
import tkinter as tk
import os
import sys

# global password count variable
password_count = 0


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_password_count():
    global password_count
    try:
        with open("password_count.txt", "r") as file:
            password_count = int(file.read())
    except FileNotFoundError:
        # If file doesn't exist
        pass


# Function to save the password count as a file
def save_password_count():
    with open("password_count.txt", "w") as file:
        file.write(str(password_count))


load_password_count()


def generate_password():
    global password_count
    password_min = 7
    password_max = 12
    all_chars = string.ascii_letters + string.punctuation + string.digits
    password = "".join(choice(all_chars)
                       for _ in range(randint(password_min, password_max)))

    # the start of count
    password_count += 1

    # the password string x.password
    formatted_password = f"{password_count}. {password}"

    # clear the case
    password_entry.delete(0, END)

    # Insert the password
    password_entry.insert(0, password)

    # Store the password to a text
    with open("old_passwords.txt", "a+") as file:
        file.write(formatted_password + "\n")


# clear old password
def clear_password():
    global password_count
    with open("old_passwords.txt", "w") as file:
        file.truncate(0)
    password_count = 0


def clear_entry():
    password_entry.delete(0, END)


def clear_all():
    password_entry.delete(0, END)
    global password_count
    with open("old_passwords.txt", "w") as file:
        file.truncate(0)
    password_count = 0


def open_old_passwords():
    with open("old_passwords.txt", "r") as file:
        file_contents = file.read()

    # new window to display old password
    old_passwords_window = Toplevel(window)
    old_passwords_window.title("Old Passwords")

    # Text widget to display old password
    text_widget = Text(old_passwords_window, wrap=tk.WORD, width=40, height=10)
    text_widget.insert(tk.END, file_contents)
    text_widget.pack()

    # Back button
    back_button = Button(old_passwords_window, text="Go Back",
                         command=old_passwords_window.destroy)
    back_button.pack()


# window
window = Tk()
window.title("mdp generator")
window.geometry("720x480")
window.minsize(480, 360)
window.iconbitmap(resource_path("cat.ico"))
window.config(background='#3F6574')

# base frame
frame = Frame(window, bg='#3F6574')

# new pic
width = 300
height = 300
image = PhotoImage(file=resource_path("login.png")).zoom(10).subsample(20)
form = Canvas(frame, width=width, height=height,
              bg='#3F6574', bd=0, highlightthickness=0)
form.create_image(width / 2, height / 2, image=image)
form.grid(row=0, column=0, sticky=W)

# sub frame
right_frame = Frame(frame, bg='#3F6574')

# title
label_title = Label(right_frame, text="mdp generator",
                    font=("DejaVu", 20), bg='#3F6574', fg="white")
label_title.pack()

# input
password_entry = Entry(right_frame, font=(
    "DejaVu", 20), bg='#3F6574', fg="white")
password_entry.pack()

# button to generate
generate = Button(right_frame, text="generate", font=("DejaVu", 20), bg='#3F6574', fg="white",
                  command=generate_password)
generate.pack(fill=X)

right_frame.grid(row=0, column=1, sticky=W)

# show frame
frame.pack(expand=YES)

# menu
menu_bar = Menu(window)
# menu list
file_memu = Menu(menu_bar, tearoff=0)
file_memu.add_command(label="new", command=generate_password)
file_memu.add_command(label="Clear case", command=clear_entry)
file_memu.add_command(label="Clear old password", command=clear_password)
file_memu.add_command(label="Open Old Passwords", command=open_old_passwords)
file_memu.add_command(label="Clear old password and case", command=clear_all)
file_memu.add_command(label="Exit", command=window.quit)
menu_bar.add_cascade(label="Fichier", menu=file_memu)

window.config(menu=menu_bar)

window.mainloop()

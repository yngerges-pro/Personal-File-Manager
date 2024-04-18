import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import PySimpleGUI as sg

class user:
    def logged_in_window(self):
        self.win = tk.Tk()
        self.win.geometry("500x500")
        self.win.title("Logged In")

        # Load the exported image from Figma
        original_image = Image.open("./Loggedin.png")
        resized_image = original_image.resize((500, 500))
        bg_image = ImageTk.PhotoImage(resized_image)

        bg_label = Label(self.win, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Shows GUI
        self.win.mainloop()
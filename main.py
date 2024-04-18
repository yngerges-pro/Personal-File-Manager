import tkinter as tk
from tkinter import Label, messagebox
import db_connection as db
from PIL import Image, ImageTk
import PySimpleGUI as sg
import psycopg2
from login import getloginData
from user import user


class Login:
    def login_Submitted(self):
        Cuser = self.ustxt.get()
        CpassW = self.patxt.get()
        print("Username:", Cuser)
        print("Password:", CpassW)
        isValid = getloginData(Cuser, CpassW)
        if isValid:
            self.win.destroy()  # Destroy the login window
            userObj = user()
            userObj.logged_in_window()
        else:
            messagebox.showerror("Error", "Invalid username or password. Please try again.")
            print("Please try again!")

    def create_Login_window(self):
        self.win = tk.Tk()
        self.win.geometry("500x500")
        self.win.title("Log in")

        # Load the exported image from Figma
        original_image = Image.open("./First.png")
        resized_image = original_image.resize((500, 500))
        self.bg_image = ImageTk.PhotoImage(resized_image)  # Store a reference to the PhotoImage object

        bg_label = Label(self.win, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Text boxes for Username and Password
        self.ustxt = tk.Entry(self.win, font=('Lato', 15), background="#C4C4C4", relief=tk.FLAT)
        self.ustxt.place(x=100, y=65, width=265, height=40)
        self.patxt = tk.Entry(self.win, font=('Lato', 15), show="*", background="#C4C4C4", relief=tk.FLAT)
        self.patxt.place(x=100, y=150, width=265, height=40)

        # Submit button
        submit = tk.Button(self.win, text="Log In", width=15, height=1, bd=0, command=self.login_Submitted,
                           font="bold", fg="#E0E0E0", background="#495580")
        submit.place(x=135, y=220)

        SignUpObj = SignUp(self.win)  # Pass the login window instance to the SignUp class
        signUpBtn = tk.Button(self.win, text="Create Account", width=12, height=1, bd=0, command=SignUpObj.GUI,
                              fg="#E0E0E0", background="#495580")
        signUpBtn.place(x=228, y=300)

        # Shows GUI
        self.win.mainloop()


class SignUp:
    def __init__(self, login_win):
        self.login_win = login_win  # Store the reference to the login window

    def HaveDBReady(self):
        self.conn = db.connectDataBase()
        self.cur = self.conn.cursor()
        db.createTables(self.cur, self.conn)

    def submit_info(self):
        username = self.ustxt.get()
        password = self.patxt.get()
        confirm_password = self.patxt2.get()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match. Please try again.")
            return

        print("Username:", username)
        print("Password:", password)

        self.HaveDBReady()
        
        # Check if the username already exists
        check_sql = "SELECT * FROM Users WHERE Username = %s"
        check_values = (username,)
        self.cur.execute(check_sql, check_values)
        existing_user = self.cur.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists. Please choose a different one.")
            return

        # Insert the new user
        insert_sql = "INSERT INTO Users (Username, Password) VALUES (%s, %s)"
        insert_values = (username, password)

        try:
            self.cur.execute(insert_sql, insert_values)
            self.conn.commit()
            messagebox.showinfo("Success", "User added successfully!")

            # Close the sign-up window
            self.win.destroy()

            # Create a new instance of the login window
            login_page = Login()
            login_page.create_Login_window()
        except psycopg2.Error as e:
            self.conn.rollback()
            messagebox.showerror("Error", "Failed to add user. Please try again.")
            print(f"Database insertion error: {e}")


    def GUI(self):
        print("Went to Sign up GUI")
        self.login_win.destroy()  # Close the login window

        self.win = tk.Tk()
        self.win.geometry("500x500")
        self.win.title("Sign up")

        # Load the exported image from Figma
        original_image = Image.open("./Second.png")
        resized_image = original_image.resize((500, 500))
        bg_image = ImageTk.PhotoImage(resized_image)

        bg_label = Label(self.win, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Text boxes for Username and Password
        self.ustxt = tk.Entry(self.win, font=('Lato', 15), background="#C4C4C4", relief=tk.FLAT)
        self.ustxt.place(x=100, y=70)

        self.patxt = tk.Entry(self.win, font=('Lato', 15), background="#C4C4C4", relief=tk.FLAT)
        self.patxt.place(x=100, y=155)

        self.patxt2 = tk.Entry(self.win, font=('Lato', 15), background="#C4C4C4", relief=tk.FLAT)
        self.patxt2.place(x=100, y=240)

        # Submit button
        submit = tk.Button(self.win, text="Sign up", font=('Lato', 12), width=15, height=1, bd=0, command=self.submit_info, fg="#E0E0E0", background="#495580")
        submit.place(x=160, y=324)

        self.win.mainloop()


if __name__ == "__main__":
    LoginObj = Login()
    LoginObj.create_Login_window()
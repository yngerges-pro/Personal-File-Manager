import tkinter as tk
from tkinter import Label, messagebox
import db_connection as db
from PIL import Image, ImageTk
import PySimpleGUI as sg
import psycopg2
from login import getloginData
from user import user
from user_publicIp import user_publicIp
from update_publicIp import check_public_ip
from update_publicIp import update_publicIp   
from user_status import user_status
from user_status import not_logged_in
import pathlib

from SharingSide import*


from update_publicIp import insert

class Login:
    def login_Submitted(self):
        Cuser = self.ustxt.get()
        CpassW = self.patxt.get()
        print("Username:", Cuser)
        print("Password:", CpassW)

        isValid = getloginData(Cuser, CpassW)
        if isValid:
            self.win.destroy()  # Destroy the login window
            current_ip = user_publicIp()

            user_status(Cuser, True)
            userObj = user()
            userObj.logged_in_window(Cuser)


        else:
            messagebox.showerror("Error", "Invalid username or password. Please try again.")
            print("Please try again!")

        self.win.destroy()  # Destroy the login window
        current_ip = user_publicIp()
        status = True


        print("IP", current_ip)
        print("status", status)
        #inserts the infos
        insert(Cuser,CpassW,current_ip,"5433",status)
        
        # Check IP address in the database
        check_public_ip(Cuser, current_ip,"5433",status)  #the entered username in the login window
        
        userObj = user()
       
        userObj.logged_in_window(Cuser)

    def create_Login_window(self):
        self.win = tk.Tk()
        self.win.geometry("500x500")
        self.win.title("Log in")

        # Load the exported image from Figma

        original_image = Image.open("./Personal-File-Manager/First.png")

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

        # Guest button
        GuestObj = Guest(self.win)  # Pass the login window instance to the Guest class
        submit = tk.Button(self.win, text="Guest", width=12, height=1, bd=0, command=GuestObj.guest_login,
                           fg="#E0E0E0", background="#495580")
        submit.place(x=228, y=355)

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
        check_sql = "SELECT * FROM users WHERE username = %s"
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
        original_image = Image.open("./Personal-File-Manager/Second.png")
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

class Guest:
    def __init__(self, login_win):
        self.login_win = login_win  # Store the reference to the login window

    def HaveDBReady(self):
        self.conn = db.connectDataBase()
        self.cur = self.conn.cursor()
        db.createTables(self.cur, self.conn)

    def guest_login(self):
        self.login_win.destroy()  # Destroy the login window
    
        username = "NULL"
        password = "Guest"

        print("Username:", username)
        print("Password:", password)

        self.HaveDBReady()
        
        # Check if the username already exists
        check_sql = "SELECT * FROM Users WHERE Username = %s"
        check_values = (username,)
        self.cur.execute(check_sql, check_values)
        existing_user = self.cur.fetchone()
        Cuser = "Guest"

        if existing_user:
            #self.win.destroy()  # Destroy the login window
            userObj = user()
            userObj.guest_window(Cuser)

        # Insert the new user
        insert_sql = "INSERT INTO users (Username, Password) VALUES (%s, %s)"
        insert_values = (username, password)

        try:
            self.cur.execute(insert_sql, insert_values)
            self.conn.commit()

            userObj = user()
            userObj.guest_window(Cuser)

        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Database insertion error: {e}")
        # Shows GUI
        self.win.mainloop()


if __name__ == "__main__":
    LoginObj = Login()
    LoginObj.create_Login_window()

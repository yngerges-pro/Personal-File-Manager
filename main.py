import tkinter as tk
from tkinter import Label
import db_connection as db
# import login as lg
from PIL import Image, ImageTk
import PySimpleGUI as sg

class Login:
    # def __init__(self):
    #     self.userN, self.passW = lg.getloginData()

    def login_Submitted(self):
        Cuser = self.ustxt.get()
        CpassW = self.patxt.get()
        print("Username:", Cuser)
        print("Password:", CpassW)
        # if Cuser == self.userN and CpassW == self.passW:
        #     print("Correct")
        # else:
        #     print("Username and Password does not match.")

    def create_Login_window(self):
        win = tk.Tk()
        win.geometry("500x500")
        win.title("Log in")

        # Load the exported image from Figma
        original_image = Image.open("./First.png")
        
        # Resize the image to 500x500 pixels
        resized_image = original_image.resize((500, 500))

        # Convert PIL Image to Tkinter PhotoImage
        bg_image = ImageTk.PhotoImage(resized_image)

        bg_label = Label(win, image=bg_image)
        bg_label.place(x=0,y=0,relwidth=1,relheight=1)

        # Text boxes for Username and Password
        self.ustxt = tk.Entry(win, font=('Lato', 15), background="#C4C4C4", relief=tk.FLAT)
        self.ustxt.place(x=100, y=65,width=265,height=40)

        self.patxt = tk.Entry(win, font=('Lato', 15), show="*", background="#C4C4C4", relief=tk.FLAT)  # show="*" to mask the password
        self.patxt.place(x=100, y=150, width=265,height=40)

        #Submit button
        submit = tk.Button(win, text="Log In", width=15, height=1, bd=0, command=self.login_Submitted, font="bold", fg="#E0E0E0", background="#495580")
        submit.place(x=135, y=220)

        SignUpObj = SignUp()
        signUpBtn = tk.Button(win,text="Create Account", width=12, height=1, bd = 0, command=SignUpObj.GUI, fg="#E0E0E0", background="#495580")
        signUpBtn.place(x=228,y=300)
        #shows GUI
        win.mainloop()


class SignUp:
   
    def HaveDBReady(self):
        self.conn = db.connectDataBase()
        self.cur = self.conn.cursor()
        db.createTables(self.cur, self.conn)

    def submit_info(self):
        username = self.ustxt.get()
        password = self.patxt.get()
        print("Username:", username)
        print("Password:", password)

        self.HaveDBReady()
        sql = "insert into Users (Username,Password) values (%s,%s)"
        resc = [username, password]

        self.cur.execute(sql,resc)
        self.conn.commit()
        return username, password

    def GUI(self):
        print("Went to Sign up GUI")
        win = tk.Tk()
        win.geometry("500x500")
        win.config(bg="#ffc166")
        win.title("log in")

        tk.Label(win, text="Username:", font=('Lato', 15), fg="#98847F", bg="#ffc166").place(x=100, y=150)
        tk.Label(win, text="Password:", font=('Lato', 15), fg="#98847F", bg="#ffc166").place(x=100, y=200)
        tk.Label(win, text="Re-enter Password:", font=('Lato', 15), fg="#98847F", bg="#ffc166").place(x=20, y=250)

        # Text boxes for Username and Password
        self.ustxt = tk.Entry(win, font=('Lato', 15))
        self.ustxt.place(x=220, y=150)

        self.patxt = tk.Entry(win, font=('Lato', 15), show="*")  # show="*" to mask the password
        self.patxt.place(x=220, y=200)

        self.patxt2 = tk.Entry(win, font=('Lato', 15), show="*")  # show="*" to mask the password
        self.patxt2.place(x=220, y=250)

        if self.patxt.get() != self.patxt2.get():
            sg.popup("Passwards does not match. Please, try again", background_color="#FFEEF2", text_color="#98847F", button_color="#FFC1D8")

        #submit button
        submit = tk.Button(win, text="Sign up", command=self.submit_info, font="bold", fg="#98847F", background="#ffeacc")
        submit.place(x=200, y=300)

        #shows GUI
        win.mainloop()


if __name__ == "__main__":
    LoginObj = Login()
    LoginObj.create_Login_window()


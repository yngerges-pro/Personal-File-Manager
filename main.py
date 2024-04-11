import tkinter as tk
import db_connection as db

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
        sql = "insert into Users (Username,Password) values (%s,%s)"
        resc = [username, password]
        self.cur.execute(sql,resc)
        self.conn.commit()

    def create_signUp_window(self):
        win = tk.Tk()
        win.geometry("500x500")
        win.config(bg="#ffc166")
        win.title("Sign up")

        tk.Label(win, text="Username:", font=('Lato', 15), fg="#98847F", bg="#ffc166").place(x=100, y=150)
        tk.Label(win, text="Password:", font=('Lato', 15), fg="#98847F", bg="#ffc166").place(x=100, y=200)

        # Text boxes for Username and Password
        self.ustxt = tk.Entry(win, font=('Lato', 15))
        self.ustxt.place(x=200, y=150)

        self.patxt = tk.Entry(win, font=('Lato', 15), show="*")  # show="*" to mask the password
        self.patxt.place(x=200, y=200)

        submit = tk.Button(win, text="Submit", command=self.submit_info, font="bold", fg="#98847F", background="#ffeacc")
        submit.place(x=200, y=300)

        win.mainloop()

if __name__ == "__main__":
    signUpObj = SignUp()
    signUpObj.HaveDBReady()
    signUpObj.create_signUp_window()


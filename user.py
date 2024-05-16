import tkinter as tk
from tkinter import Label, Entry, PhotoImage
from tkinter import simpledialog
from PIL import Image, ImageTk
import os
import psycopg2 
import db_connection as db
from DownloadFileMethods import viewAllDownloadableFiles, searchForDownloadableFiles, downloadThisFile
from ShareFileMethods import viewMyShareFiles, addNewShareFile, editShareFile, deleteShareFile
from user_status import not_logged_in

from user_publicIp import user_publicIp
from update_publicIp import check_public_ip
from update_publicIp import update_publicIp 

import pathlib

from SharingSide import*

from update_publicIp import check_public_ip

class user:
    # current_ip = user_publicIp()
    # current_ip = "10.110.253.243"
    current_ip = "2603:8000:49f0:f30::1922"
    VarPath = str(pathlib.Path(__file__).parent.resolve()) + "\\ShareFiles"
    OpenSharingSide = ShareFiles(current_ip, 80, VarPath)
    def userID(self, username):
        try:
            # Establish a connection to the database
            conn = db.connectDataBase()
            cur = conn.cursor()

            # SQL query to select the row corresponding to the given username
            sql_query = "SELECT * FROM users WHERE username = %s"

            # Execute the SQL query with the username parameter
            cur.execute(sql_query, (username,))

            # Fetch the first row
            first_row = cur.fetchone()

            # If a row is found, return the first value from that row
            if first_row:
                id_value = first_row['id']  # Access the value using dictionary indexing
                return id_value
            else:
                print("User not found.")

            # Close the cursor and connection
            cur.close()
            conn.close()

        except psycopg2.Error as e:
            print(f"Database error: {e}")

    def listdownloadsfile(self):
        try:
            # Establish a connection to the database
            conn = db.connectDataBase()
            cur = conn.cursor()

            # Query the database for files
            cur.execute('SELECT userid, filename, filesize, description FROM files')

            # Fetch all rows from the result set
            rows = cur.fetchall()

            print("Rows:", rows)  # Debug print

            # Create a list to store file objects
            files = []

            # Iterate over the rows and create a file object for each row
            for row in rows:
                print("Row:", row)  # Debug print
                file = {
                    'UserID': row['userid'],
                    'FileName': row['filename'],
                    'FileSize': row['filesize'],
                    'Description': row['description']
                }
                files.append(file)

            # Close the cursor and connection
            cur.close()
            conn.close()

            # Return the list of file objects
            return files

        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return []


    def downloadfile(self):
        print("File is now downloaded")

    def logged_in_window(self, Cuser):
        if hasattr(self, 'win') and self.win:
            self.win.destroy()  # Close the window or any other logout procedure
        
        self.win = tk.Tk()
        self.win.geometry("500x500")
        self.win.title("Logged In")

        # Load the exported image from Figma

        original_image = Image.open("./Personal-File-Manager/Loggedin.png")

        resized_image = original_image.resize((500, 500))
        self.bg_image = ImageTk.PhotoImage(resized_image)

        bg_label = Label(self.win, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Add user label
        user_label = tk.Label(self.win, text=Cuser, fg="black", font=("Lato", 9, "bold"), background="white")
        user_label.place(x=90, y=2)

        # Log Out button
        logout = tk.Button(self.win, text="Log Out", fg="black", font=("Lato", 9, "bold"), width=8, height=1, bd=0, command=lambda:self.logout(Cuser),
                            background="white")
        logout.place(x=295, y=2)

        # Manage Shared Files
        myfiles = tk.Button(self.win, text="Manage Shared Files", font=("Lato", 9, "bold"), width=18, height=1, bd=0, command=lambda: self.my_files_window(Cuser),
                            fg="#E0E0E0", background="#495580")
        myfiles.place(x=165, y=150)

        # Download Files button
        downloadfiles = tk.Button(self.win, text="Download Files", font=("Lato", 9, "bold"), width=12, height=1, bd=0, command=lambda: self.downloads_window(Cuser),
                           fg="#E0E0E0", background="#495580")
        downloadfiles.place(x=183, y=285)


        #white box
        # Add user label
        box = tk.Label(self.win, width=30, height=7, background="white")
        box.place(x=55, y=350)


        # Shows GUI
        self.win.mainloop()

    def guest_window(self, Cuser):
        if hasattr(self, 'win') and self.win:
            self.win.destroy()  # Close the window or any other logout procedure
        
        self.win = tk.Tk()
        self.win.geometry("500x500")
        self.win.title("Guest")

        # Load the exported image from Figma

        original_image = Image.open("Guest.png")

        resized_image = original_image.resize((500, 500))
        self.bg_image = ImageTk.PhotoImage(resized_image)

        bg_label = Label(self.win, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        #Log in button
        downloadfiles = tk.Button(self.win, text="Create Account to Login", font=("Lato", 9, "bold"), width=20, height=2, bd=0,
                                   command=lambda: self.logout(Cuser), fg="#E0E0E0", background="#495580")
        downloadfiles.place(x=165, y=190)

        # Download Files button
        downloadfiles = tk.Button(self.win, text="Download Files", font=("Lato", 9, "bold"), width=12, height=1, bd=0, command=lambda: self.downloads_window(Cuser),
                           fg="#E0E0E0", background="#495580")
        downloadfiles.place(x=183, y=295)

        # Shows GUI
        self.win.mainloop()
    
    def downloads_window(self, Cuser):
        page_size = 7  # Number of files to display per page
        current_page = 1  # Current page number
        files = []

        def search(query):
            
            # Check if the search query is empty
            if not query.strip():
                # If the search query is empty, retrieve all downloadable files
                files = viewAllDownloadableFiles()
            else:
                # Call a function to retrieve files based on the search query
                files = searchForDownloadableFiles(query)

            # Display the updated list of files
            display_files(files)

        def navigate_left():
            nonlocal current_page
            if current_page > 1:
                current_page -= 1
                display_files()

        def navigate_right():
            nonlocal current_page
            total_pages = (len(files) + page_size - 1) // page_size
            if current_page < total_pages:
                current_page += 1
                display_files()

        def display_files():
            nonlocal current_page, files
            self.win.destroy()  # Destroy the current window to refresh with updated files

            # Re-create the window
            self.win = tk.Tk()
            self.win.geometry("500x500")
            self.win.title("Download")

            # Load the exported image from Figma

            original_image = Image.open("./Personal-File-Manager/Download.png")

            resized_image = original_image.resize((500, 500))
            self.bg_image = ImageTk.PhotoImage(resized_image)

            bg_label = Label(self.win, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            # Add user label
            user_label = tk.Label(self.win, text=Cuser, fg="black", font=("Lato", 9, "bold"), background="white")
            user_label.place(x=90, y=2)

            # Log Out button
            logout = tk.Button(self.win, text="Log Out", fg="black", font=("Lato", 9, "bold"), width=8, height=1, bd=0, command=lambda:self.logout(Cuser),
                                background="white")
            logout.place(x=425, y=2)

            if (Cuser == "Guest"):
                # Go Back
                goback = tk.Button(self.win, text="Go Back", font=("Lato", 9, "bold"), width=7, height=1, bd=0, command=lambda: self.guest_window(Cuser),
                                    fg="#E0E0E0", background="#495580")
                goback.place(x=80, y=390)
            else:
                # Go Back
                goback = tk.Button(self.win, text="Go Back", font=("Lato", 9, "bold"), width=7, height=1, bd=0, command=lambda: self.logged_in_window(Cuser),
                                    fg="#E0E0E0", background="#495580")
                goback.place(x=80, y=390)

            # Calculate the start and end index of files to display based on the current page
            start_index = (current_page - 1) * page_size
            end_index = min(start_index + page_size, len(files))

            # Initial y position for the files
            y_position = 110

            # Display the list of files in the GUI for the current page
            for i, file in enumerate(files[start_index:end_index], start=start_index):
                FileName = tk.Label(self.win, text=f"{file['FileName']}", font=('Lato', 9), fg='white', bg="#495580")
                FileName.place(x=80, y=y_position)  # Use the calculated y_position
                FileSize = tk.Label(self.win, text=f"{file['FileSize']}", font=('Lato', 9), fg='white', bg="#495580")
                FileSize.place(x=180, y=y_position)  # Use the calculated y_position
                Description = tk.Label(self.win, text=f"{file['Description']}", font=('Lato', 9), fg='white', bg="#495580")
                Description.place(x=280, y=y_position)  # Use the calculated y_position
                # Download button
                Download = tk.Button(self.win, text="Download", font=("Lato", 9, "bold"), width=10, height=1, bd=0, 
                            command=lambda userid=file['UserID'], filename=file['FileName'], filesize=file['FileSize'], description=file['Description']: downloadThisFile(filename),
                            fg="#E0E0E0", background="#495580")
                Download.place(x=353, y=y_position)


                # Increment y_position for the next file
                y_position += 38

            # Arrows
            left_arrow = tk.Button(self.win, text="◀", font=("Lato", 12), width=2, height=1, bd=0, command=navigate_left,
                                fg="#E0E0E0", background="#495580")
            left_arrow.place(x=188, y=386)

            right_arrow = tk.Button(self.win, text="▶", font=("Lato", 12), width=2, height=1, bd=0, command=navigate_right,
                                fg="#E0E0E0", background="#495580")
            right_arrow.place(x=218, y=386)

            # Inside the downloads_window method
            # Search Bar with Icon
            search_icon = Image.open("./Personal-File-Manager/search_icon.png")
            search_icon = search_icon.resize((26, 26), Image.LANCZOS)  # Resize the icon image to fit the search bar
            search_icon = ImageTk.PhotoImage(search_icon)

            search_entry = Entry(self.win, font=("Lato", 9), width=18, background="#E0E0E0")
            search_entry.place(x=312, y=390)
            search_entry.insert(0, "Search...")
            search_entry.config(fg="#A0A0A0")
            search_entry.bind("<FocusIn>", lambda event: self.on_search_focus(event, search_entry))

            search_button = tk.Button(self.win, image=search_icon, bd=0, 
                                    command=lambda: search(search_entry.get()), background="#E0E0E0")
            search_button.place(x=283, y=387)

            # Shows GUI
            self.win.mainloop()

        # Initial display of files
        files = viewAllDownloadableFiles()
        display_files()

    
    def my_files_window(self, Cuser):
        page_size = 7  # Number of files to display per page
        current_page = 1  # Current page number
        files = []

        def navigate_left():
            nonlocal current_page
            if current_page > 1:
                current_page -= 1
                display_files()

        def navigate_right():
            nonlocal current_page
            total_pages = (len(files) + page_size - 1) // page_size
            if current_page < total_pages:
                current_page += 1
                display_files()

        def display_files():
            nonlocal current_page, files
            self.win.destroy()  # Destroy the current window to refresh with updated files
            self.win = tk.Tk()
            self.win.geometry("500x500")
            self.win.title("My Files")

            # Load the exported image from Figma

            original_image = Image.open("./Personal-File-Manager/MyFiles.png")

            resized_image = original_image.resize((500, 500))
            self.bg_image = ImageTk.PhotoImage(resized_image)

            bg_label = Label(self.win, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            # Add user label
            user_label = tk.Label(self.win, text=Cuser, fg="black", font=("Lato", 9, "bold"), background="white")
            user_label.place(x=90, y=2)

            # Log Out button
            logout = tk.Button(self.win, text="Log Out", fg="black", font=("Lato", 9, "bold"), width=8, height=1, bd=0, command=lambda:self.logout(Cuser),
                                background="white")
            logout.place(x=425, y=2)

             # Calculate the start and end index of files to display based on the current page
            start_index = (current_page - 1) * page_size
            end_index = min(start_index + page_size, len(files))

            # Initial y position for the files
            y_position = 110

            # Display the list of files in the GUI for the current page
            for i, file in enumerate(files[start_index:end_index], start=start_index):
                FileName = tk.Label(self.win, text=f"{file['FileName']}", font=('Lato', 9), fg='white', bg="#495580")
                FileName.place(x=80, y=y_position)  # Use the calculated y_position
                FileSize = tk.Label(self.win, text=f"{file['FileSize']}", font=('Lato', 9), fg='white', bg="#495580")
                FileSize.place(x=180, y=y_position)  # Use the calculated y_position
                Description = tk.Label(self.win, text=f"{file['Description']}", font=('Lato', 9), fg='white', bg="#495580")
                Description.place(x=280, y=y_position)  # Use the calculated y_position
                # Edit button
                Edit = tk.Button(self.win, text="Edit", font=("Lato", 8, "bold"), width=5, height=1, bd=0, 
                                command=lambda userid=file['UserID'], filename=file['FileName'], filesize=file['FileSize'], description=file['Description']: self.edit_file_description(userid, filename, filesize, description),
                                fg="#E0E0E0", background="#495580")
                Edit.place(x=347, y=y_position)
                # Remove button
                Remove = tk.Button(self.win, text="Remove", font=("Lato", 8, "bold"), width=6, height=1, bd=0,
                                command=lambda userid=file['UserID'], filename=file['FileName'], filesize=file['FileSize'], description=file['Description']: deleteShareFile(userid, filename),
                                fg="#E0E0E0", background="#495580")
                Remove.place(x=396, y=y_position)

                # Increment y_position for the next file
                y_position += 38
                

            # Arrows
            left_arrow = tk.Button(self.win, text="◀", font=("Lato", 12), width=2, height=1, bd=0, command=navigate_left,
                                fg="#E0E0E0", background="#495580")
            left_arrow.place(x=218, y=392)

            right_arrow = tk.Button(self.win, text="▶", font=("Lato", 12), width=2, height=1, bd=0, command=navigate_right,
                                fg="#E0E0E0", background="#495580")
            right_arrow.place(x=247, y=392)

            # Go Back
            goback = tk.Button(self.win, text="Go Back", font=("Lato", 9, "bold"), width=10, height=1, bd=0, command=lambda: self.logged_in_window(Cuser),
                                fg="#E0E0E0", background="#495580")
            goback.place(x=80, y=393)

            def edit_file_description(userid, filename, filesize, description):
                # Function to open a window for adding a file
                edit_file_window = tk.Toplevel()
                edit_file_window.title("New Description")
                
                # Entry fields for file name and description
                file_new_description = tk.Entry(edit_file_window, width=30)
                file_new_description.grid(row=0, column=0, padx=10, pady=5)
            
                # Function to add the file when the button is clicked
                def editFile():
                    new_description = file_new_description.get()
                    editShareFile(userid, filename, filesize, new_description)
                    edit_file_window.destroy()  # Close the window after adding the file

                # Add button to confirm adding the file
                edit_button = tk.Button(edit_file_window, text="Edit", command=editFile)
                edit_button.grid(row=2, column=0, padx=10, pady=5)

            def openAddFileDialog():
                # Function to open a window for adding a file
                add_file_window = tk.Toplevel()
                add_file_window.title("Add File")
                
                # Label for file name
                file_name_label = tk.Label(add_file_window, text="Name")
                file_name_label.grid(row=0, column=0, padx=10, pady=5)
                
                # Entry field for file name
                file_name_entry = tk.Entry(add_file_window, width=30)
                file_name_entry.grid(row=0, column=1, padx=10, pady=5)
                
                # Label for description
                description_label = tk.Label(add_file_window, text="Description")
                description_label.grid(row=1, column=0, padx=10, pady=5)
                
                # Entry field for description
                description_entry = tk.Entry(add_file_window, width=30)
                description_entry.grid(row=1, column=1, padx=10, pady=5)
    
                
                # Function to add the file when the button is clicked
                def addFile():
                    file_name = file_name_entry.get()
                    description = description_entry.get()
                    user_id = user.userID(self, Cuser)
                    newFile = addNewShareFile(user_id, file_name, description) # Removed file['FileSize'] as not used in method
                    print("New File: " + str(newFile))
                    add_file_window.destroy()  # Close the window after adding the file
                
                # Add button to confirm adding the file
                add_button = tk.Button(add_file_window, text="Add", command=addFile)
                add_button.grid(row=2, column=0, padx=10, pady=5)

            # Add File button
            addfile = tk.Button(self.win, text="Add File", font=("Lato", 9, "bold"), width=10, height=1, bd=0,
                                command=openAddFileDialog, fg="#E0E0E0", background="#495580")
            addfile.place(x=340, y=393)

        # Shows GUI
            self.win.mainloop()

        conn = db.connectDataBase()
        cur = conn.cursor()

        # Initial display of files
        sql = "SELECT id FROM users WHERE username = %s"
        cur.execute(sql,(Cuser,))
        UserID = cur.fetchone()["id"]
        files = viewMyShareFiles(UserID)
        display_files()

    def logout(self,Cuser):
        if hasattr(self, 'win') and self.win:
            self.win.destroy()  # Close the window or any other logout procedure
        os.system("python main.py")  # Run main.py again
        not_logged_in(Cuser,False)

        # Shows GUI
        self.win.mainloop()

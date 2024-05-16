import socket
import threading

# File Owner Side
# Send Files
class ShareFiles():
    PublicIP = "0.0.0.0" # Uninitialized
    SharingPort = 1234 # Uninitialized
    PathToDirectory = ""
    mySocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    BUFFER_SIZE = 1024 # 1 kb per time step

    def __init__(self, IP, Port, Path):
        self.PublicIP = IP
        self.SharingPort = Port
        self.PathToDirectory = Path
        self.startThreading()

    # Create thread for listening so user can still use application
    # while being able to share files
    def startThreading(self):
        listen_thread = threading.Thread(target=self.listen) # Pass socket into thread
        listen_thread.start() # Start Thread

    def listen(self):
        print("Listening Started")
        self.mySocket.bind((self.PublicIP, self.SharingPort)) # Open Socket for listening
        self.mySocket.listen(5) # Allow up to 5 connections
        # Accept connections
        try:
            while True:
                self.listenLoop()
        except:
            # Error Occured, Likely due to socket closing and Thread running "mySocket.accept"
            # This is so we can close the thread in a 'dirty' but safe way
            print("Thread Closed.")

    def listenLoop(self):
        client_socket, address = self.mySocket.accept()
        print(f"{address} is connected.")
        # Asked for what file to send
        received = client_socket.recv(self.BUFFER_SIZE).decode() # What file I should look for
        openKeyword = self.PathToDirectory + "\\keyword.txt"
        print(f"Client {address} is asking for " + received)
        with open(openKeyword, 'r') as fp:
            allFileNames = fp.read()
            # Send Reply To Confirm is File Exists Or Not
            if received in allFileNames:
                # File Allowed in keyword.txt, Begin Transfer!
                print(f"File Found in keyword.txt, beginning transfer to {address}.")
                self.transferFile(received, client_socket)
            else:
                # File Does Not Exist or is Not Allowed To Be Transfered
                client_socket.send("Error, File Not Found!".encode())
                print(f"Cannot Find File In Question for {address}!")
        # This Client Is Done
        print(f"Closing Connection with {address}")
        client_socket.close()
        return openKeyword

    # With File Existing, Begin Transfer
    def transferFile(self, fileName, client_socket):
        filename = self.PathToDirectory + "\\" + fileName
        try:
            with open(filename, "rb") as file:
                client_socket.send("File Found, Beginning Transfer!".encode())
                print("File Exists, Transferring " + fileName )
                while True:
                    bytes_read = file.read(self.BUFFER_SIZE) # Send only 1024 bytes per time
                    if not bytes_read:
                        # Transmission is done
                        break
                    client_socket.sendall(bytes_read)
        except:
            # Error has Occured! Likely Due to file being in keyword.txt, but not in directory!
            client_socket.send("Error, File Not Found!".encode())
            print("Error! Could not find file in directory!")

        # File Completely Transferred!

    def shutDownSharingSocket(self):
        self.mySocket.close()
        print("Sharing Socket Closed")

# if __name__ == "main":
#     sender = ShareFiles(ip="ip", Port="port", Path="path")

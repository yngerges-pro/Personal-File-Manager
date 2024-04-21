import socket
import threading

# File Owner Side
# Send Files
PublicIP = "0.0.0.0" # Uninitialized
SharingPort = 1234 # Uninitialized
PathToDirectory = ""
mySocket = socket.socket()

BUFFER_SIZE = 1024 # 1 kb per time step


def initializeSharing(IP, Port, Path):
    global PublicIP
    PublicIP = IP
    global SharingPort
    SharingPort = Port
    global PathToDirectory
    PathToDirectory = Path # Path To Directory Must Be Given
    startThreading()

# Create thread for listening so user can still use application
# while being able to share files
def startThreading():
    listen_thread = threading.Thread(target=listen) # Pass socket into thread
    listen_thread.start() # Start Thread

def listen():
    mySocket.bind((PublicIP, SharingPort)) # Open Socket for listening
    mySocket.listen(5) # Allow up to 5 connections
    # Accept connections
    client_socket, address = mySocket.accept()
    print(f"{address} is connected.")
    # Asked for what file to send
    received = client_socket.recv(BUFFER_SIZE).decode() # What file I should look for
    openKeyword = PathToDirectory + "\\keyword.txt"
    print(f"Client {address} is asking for " + received)
    with open(openKeyword, 'r') as fp:
        allFileNames = fp.read()
        # Send Reply To Confirm is File Exists Or Not
        if received in allFileNames:
            # File Exists And Allowed, Begin Transfer
            client_socket.send("File Found, Beginning Transfer!".encode())
            print("File Found, Transferring " + received + f" to {address}.")
            transferFile(received, client_socket)
        else:
            # File Does Not Exist or is Not Allowed To Be Transfered
            client_socket.send("Error, File Not Found!".encode())
            print(f"Cannot Find File In Question for {address}!")
    # This Client Is Done
    print(f"Closing Connection with {address}")
    client_socket.close()

# With File Existing, Begin Transfer
def transferFile(fileName, client_socket):
    filename = PathToDirectory + "\\" + fileName
    
    with open(filename, "rb") as file:
        while True:
            bytes_read = file.read(BUFFER_SIZE) # Send only 1024 bytes per time
            if not bytes_read:
                # Transmission is done
                break
            client_socket.sendall(bytes_read)
    
    # File Completely Transferred!

def shutDownSharingSocket():
    mySocket.close()
    print("Sharing Socket Closed")

import socket

BUFFER_SIZE = 1024
# Receiver Side
def downloadFile(hostIP, hostPort, fileName, pathToDownloadTo):
    mySocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    print(f"Attempting to connect to {hostIP}:{hostPort}")
    try:
        mySocket.connect((hostIP, hostPort))
        # Connection Established
        print("Connected!")
    except:
        print("There was an error in connecting to host!")
        return -1
    
    mySocket.send(fileName.encode()) # Ask for this file
    recieveMessage = mySocket.recv(BUFFER_SIZE).decode() # Does File Exist?
    if (recieveMessage == "File Found, Beginning Transfer!"):
        # File was found and allowed!
        fileNameWithPath = pathToDownloadTo + "\\" + fileName
        with open (fileNameWithPath, "wb") as file:
            while True:
                bytes_read = mySocket.recv(BUFFER_SIZE)
                if not bytes_read:
                    # Nothing to receive
                    break
                file.write(bytes_read)
        # Received Completed!
        print("File Transfer Complete!")
        mySocket.close()
        return 1
    else:
        print("File Not Found!")
        mySocket.close()
        return -2

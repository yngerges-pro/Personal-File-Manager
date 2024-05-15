# Personal-File-Manager
#### Before running, be sure to have postgreSQL already installed and create a new database called loginfo. :)
### for authentication please add this function to the database: 
###     Name: check_user_credentials
###     Definition: 2 datatype both character varying IN
###                 for argument one put p_username
###                 for argument two put p_password
### Like so:
![image](https://github.com/yngerges-pro/Personal-File-Manager/assets/102266055/af26e7bf-aeac-4fbf-a44f-c21cd03ad8a3)

###     For code put : 
### BEGIN
###    RETURN EXISTS (
###        SELECT 1
###        FROM users
###        WHERE username = p_username AND password = p_password
###    );
### END;

## File Sharing Sender + Receiver Sides

### Sender is Object Class, Create Object at LogIn
### Sender Side Requires 3 Paramaters (IP, Port, Path)
#### IP = Current IP
#### Port = Default Port or Port Assigned By User (Whatever is in SQL)
#### Path = Default Path to Sharing Directory

### Receiver is Just 1 Method, Not a Class
### When Pressing Download, Run Method, Requires 3 Paramaters (HostIP, HostPort, Path)
#### HostIP = IP of Sender, Aquired Before Receiving From SQL
#### Port = Port of Sender, Aquired Before Receiving From SQL
#### Path = Default Path to Downloading Directory

## Should Delete users and usersip tables

## files
![image](https://github.com/yngerges-pro/Personal-File-Manager/assets/102266055/2cd696e5-bb53-4222-90ff-0dc0ef433113)




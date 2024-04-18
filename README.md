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

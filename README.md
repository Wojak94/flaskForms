# flaskForms
## Current API endpoints:

* /register (User registration)
* /login
* /logout/access
* /logout/refresh
* /token/refresh
* /users
* /addsurvey

## Usage:
### /register:

#### Accepted parameters:
    username (required)
    email (required)
    password (required)
    
#### Returned json:
Success:
   
    message: "User {username} was created"
    access token
    refresh token
  
Failure:

    message "Something went wrong"
----------------------
### /login:

#### Accepted parameters:
    username (required)
    password (required)
    
#### Returned json
Success:

    message "Logged in as <username>"
    access token
    refresh token
  
Failure:

    message: "User {username} doesn't exist" (cannot find user by username)
    message: "Wrong credentials" (password doesn't match specified username)
----------------------   
### /logout/access:
  
#### Required tokens:
    access token
    
#### Returned json
Success:

    message: "Access token has been revoked"
    
Failure:

    message: "Something went wrong" (probably database access error)
----------------------    
### /logout/refresh:
  
#### Required tokens:
    refresh token
    
#### Returned json
Success:

    message: "Refresh token has been revoked"
    
Failure:

    message: "Something went wrong" (probably database access error)
----------------------    
### /token/refresh:
----------------------
### /users:
----------------------
### /addsurvey:
----------------------

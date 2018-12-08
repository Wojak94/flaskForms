# flaskForms
Backend for survey creation application written in Flask and Flask-sqlalchemy, deployed on heroku. Contains database models for PostgreSQL and REST API endpoints for communication with frontend.


## API architecture
API is written with Flask-RESTful library, providing user authentication with Flask-JWT-extended. Upon user registrarion/login 2 tokens are created: access and refresh, that lasts 15 min and 30 days respectivly.
Accessing token&#8209;protected endpoints requires `Authorization` parameter in header of https request, with `Bearer {token}` value. Request parameters should be passed in header section. User logout is performed as two POST requests to `/logout/access` and `/logout/refresh`, which adds passed tokens to a blacklist.

## Current API endpoints

PATH | METHOD | TOKEN PROTECTION | PURPOSE
-----|--------|------------------|----------
/register | POST | None | User registration
/login | POST | None | User login
/logout/access | POST | Access token | User logout of access token
/logout/refresh |  POST | Refresh token | User logout of refresh token
/token/refresh | POST | Refresh token | Obtaining new access token with refresh token
/addsurvey | POST | Access token | Adding new survey
/users | GET/DELETE | None | Getting list of/deleting all users (debug/development usage)

## Usage

### /register:

#### Accepted parameters:
    username (required)
    email (required)
    password (required)
    
#### Returned json:
* Success:
   
        message: "User {username} was created"
        access_token: {access_token}
        refresh_token: {refresh_token}
  
* Failure:

        message: "Something went wrong" (Probably database access or token creation error)

### /login:

#### Accepted parameters:
    username (required)
    password (required)
    
#### Returned json:
* Success:

        message: "Logged in as {username}"
        access_token: {access_token}
        refresh_token: {refresh_token}
  
* Failure:

        message: "User {username} doesn't exist" (cannot find user by username)
        message: "Wrong credentials" (password doesn't match specified username)

### /logout/access:
  
#### Required tokens:
    access token
    
#### Returned json:
* Success:

        message: "Access token has been revoked"
    
* Failure:

        message: "Something went wrong" (probably database access error)
   
### /logout/refresh:

#### Required tokens:
    refresh token
    
#### Returned json:
* Success:

        message: "Refresh token has been revoked"
    
* Failure:

        message: "Something went wrong" (probably database access error)

### /token/refresh:
#### Required tokens:
    refresh token
    
#### Returned json:
    access_token: {access_token}    

### /addsurvey:

#### Required tokens:
    refresh token
    
#### Accepted parameters:
    name (required)
    desc
    duedate (required)
    isactive
#### Returned json:
* Success:

        message: "Survey {name} was created"
* Failure:
    
        message: "Something went wrong" (probably database access error)

### /users:

No parameters required, just plain GET/DELETE request.

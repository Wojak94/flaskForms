# flaskForms
Backend for survey creation application written in Flask and Flask-sqlalchemy, deployed on heroku. Contains database models for PostgreSQL and REST API endpoints for communication with frontend.


## API architecture
API is written with Flask-RESTful library, providing user authentication with Flask-JWT-extended. Upon user registrarion/login 2 tokens are created: access and refresh, that lasts 15 min and 30 days respectivly.
Accessing token&#8209;protected endpoints requires `Authorization` parameter in header of https request, with `Bearer {token}` value. Request parameters should be passed in header section. User logout is performed as two POST requests to `/logout/access` and `/logout/refresh`, which adds passed tokens to a blacklist.

## Current API endpoints

PATH | METHOD | TOKEN PROTECTION | PURPOSE
-----|--------|------------------|----------
[/register](https://github.com/Wojak94/flaskForms/blob/master/README.md#register) | POST | None | User registration
[/login](https://github.com/Wojak94/flaskForms/blob/master/README.md#login) | POST | None | User login
[/logout/access](https://github.com/Wojak94/flaskForms/blob/master/README.md#logoutaccess) | POST | Access token | User logout of access token
[/logout/refresh](https://github.com/Wojak94/flaskForms/blob/master/README.md#logoutrefresh) |  POST | Refresh token | User logout of refresh token
[/token/refresh](https://github.com/Wojak94/flaskForms/blob/master/README.md#tokenrefresh) | POST | Refresh token | Obtaining new access token with refresh token
[/addsurvey](https://github.com/Wojak94/flaskForms/blob/master/README.md#addsurvey) | POST | Access token | Adding new survey
[/getsurveys](https://github.com/Wojak94/flaskForms/blob/master/README.md#getsurveys) | GET | Access token | Getting list of logged user surveys
[/getsurveyquestions](https://github.com/Wojak94/flaskForms/blob/master/README.md#getsurveyquestions) | GET | None | Get list of questions by the id of survey
[/activesurveys](https://github.com/Wojak94/flaskForms/blob/master/README.md#activesurveys) | GET | None | Getting list of all active surveys
[/addquestion](https://github.com/Wojak94/flaskForms/blob/master/README.md#addquestion) | POST | Access token | Adding question to existing user survey
[/addreply](https://github.com/Wojak94/flaskForms/blob/master/README.md#addreply) | POST | None | Adding reply to a specified question
[/users](https://github.com/Wojak94/flaskForms/blob/master/README.md#users) | GET/DELETE | None | Getting list of/deleting all users (debug/development usage)

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
  
#### Returned json:
* Success:

        message: "Access token has been revoked"
    
* Failure:

        message: "Something went wrong" (probably database access error)
   
### /logout/refresh:
    
#### Returned json:
* Success:

        message: "Refresh token has been revoked"
    
* Failure:

        message: "Something went wrong" (probably database access error)

### /token/refresh:

#### Returned json:
    access_token: {access_token}    

### /addsurvey:
    
#### Accepted parameters:
    name (required)
    desc
    duedate (required)
    isactive
    questions (located in a request body)
#### Returned json:
* Success:

        message: "Survey {name} was created"
* Failure:
    
        message: "Something went wrong" (probably database access error)
        
### /getsurveyquestions:

#### Accepted parameters:
    idSurvey (required)    
#### Returned json:
* Success:

        questions: [
                    {
                        content: {content},
                        id: {idQuestion},
                        replyContent: {replyContent},
                        type: {type}
                    }, ...
                 ]  
* Failure:
    
        message: "Survey doesn't exist" (if given idSurvey doesn't exist in database)
        
### /getsurveys:
* Success:

        surveys: [
                    {
                        name: {name},
                        isActive: {isActive},
                        dueDate: {dueDate},
                        subCount: {subCount},
                        desc: {desc}
                    }, ...
                 ]  
* Failure:
    
        message: "User {username} has no surveys"
### /activesurveys:
    
#### Returned json:
* Success:

        surveys: [
                    {
                        id: {id},
                        name: {name},
                        isActive: {isActive},
                        dueDate: {dueDate},
                        subCount: {subCount},
                        desc: {desc}
                    }, ...
                 ]  
* Failure:
    
        message: "There are no active surveys"
        
### /addquestion:

#### Accepted parameters:
    idSurvey (required)  
    content (required)
    type (required)
    
#### Returned json:
* Success:

        message: "Question was added"
* Failure:
    
        message: "Survey doesn't exist" (if given idSurvey doesn't exist in database)
        message: "User {current_username} not permited" (if id of requesting user doesn't match survey owner's id)
        message: "Something went wrong" (internal server error, 500)

### /replyadd:

#### Accepted parameters:
    idQuestion (required)  
    reply (required)
#### Returned json:

* Success:

        message: "Reply was added"
* Failure:
    
        message: "Question doesn't exist" (if given idQuestion doesn't exist in database)
        message: "Something went wrong" (internal server error, 500)    
### /users:

No parameters required, just plain GET/DELETE request.

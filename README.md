# flaskForms
### Current API endpoints:

* /register
* /login
* /logout/access
* /logout/refresh
* /token/refresh
* /users
* /addsurvey

### Usage:
#### /register:

  ##### Accepted parameters:
    * *username* (**required**)
    * *email* (**required**)
    * *password* (**required**)
    
  ##### Returned json (success):
    * *message* "User {username} was created"
    * *access token*
    * *refresh token*
  
  ##### Returned json (failure):
    * message "Something went wrong"
----------------------
#### /login:

  ##### Accepted parameters:
    * *username* (**required**)
    * *password* (**required**)
    
  ##### Returned json (success):
    * *message* "Logged in as <username>"
    * *access token*
    * *refresh token*
  
  ##### Returned json (failure):
    * *message* "User {username} doesn't exist" (cannot find user by username)
    * *message* "Wrong credentials" (password doesn't match specified username)
----------------------   
#### /logout/access:
  
  ##### Required tokens:
    * *access token*
    
  ##### Returned json (success):
    * *message* "Access token has been revoked"
    
  ##### Returned json (failure):
    * *message* "Something went wrong" (probably database access error)
----------------------    
#### /logout/refresh:
  
  ##### Required tokens:
    * *refresh token*
    
  ##### Returned json (success):
    * *message* "Refresh token has been revoked"
    
  ##### Returned json (failure):
    * *message* "Something went wrong" (probably database access error)
----------------------    
#### /token/refresh:
----------------------
#### /users:
----------------------
#### /addsurvey:
----------------------

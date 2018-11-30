# flaskForms
### Current API endpoints:

* /register
* /login
* /logout/access
* /logout/refresh
* /token/refresh
* /users

### Usage:
* #### /register:
```
curl -H "Content-Type: application/json" -X POST -d '{"username":"user","email":"test","password":"test"}' https://surveyland.herokuapp.com/register
```
* #### /login:
```
curl -H "Content-Type: application/json" -X POST -d '{"username":"user","password":"test"}' https://surveyland.herokuapp.com/login
```
* #### /logout/access:
```
curl -H "Authorization: Bearer {access_token}" -X POST https://surveyland.herokuapp.com/logout/access
```
* #### /logout/refresh:
```
curl -H "Authorization: Bearer {refresh_token}" -X POST https://surveyland.herokuapp.com/logout/refresh
```
* #### /token/refresh:
```
curl -H "Authorization: Bearer {refresh_token}" -X POST https://surveyland.herokuapp.com/token/refresh
```
* #### /users:
```
curl -H "Content-Type: application/json" -X GET https://surveyland.herokuapp.com/users
```

***
**_Read this in other languages: [English](README.eu.md), [Русский](README.md)_**
***

## API application:
 - API listens POST calls in [localhost](http://0.0.0.0:8888) checks name and password in db and return jwt token.
 - API listens POST calls in [localhost/msg](http://0.0.0.0:8888/msg) checks jwt tokens in headers authorisation,
if jwt token was true saves message and return bool response. In case if token was valid and message was "history10"
return last 10 messages from user witch this jwt token.
 - Test in 
>src/test

## Working environment
To start development, you need to set up a working environment. We need the following system dependencies:
- [Python 3.10.4](https://www.python.org/downloads/release/python-3104/)
- Dependency manager [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) ver 1.20

Environment setup:
1. Setup repository
   ```shell script
   git clone https://github.com/ClasterPack/db_Api.git db_Api
   cd db_Api
   ```
2. Connect a virtual environment:
   ```shell script
    poetry shell
   ```
3. Install dependencies. Dependencies are installed in the virtual environment.
    ```shell script
    poetry install
   ```
   if necessary, install build witch testing environment.
    ```shell script
    poetry install -E tests
   ```

## Launch

Virtual environment :
   ```shell script
   poetry shell
   ```

From the virtual environment, the service is started by the command:
   ```shell script
   python -m src.app -c src/config.yml
   ```

## Curl API calls:

- Authorization with valid token:
```
curl --location --request POST 'http://0.0.0.0:8888' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "user",
    "password": "user"
}'
```

- Message witch valid token in headers:

```
curl --location --request POST 'http://0.0.0.0:8888/msg' \
--header 'Authorization: Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NjMyMjczMTksImlhdCI6MTY2MjM2MzMxOSwiaXNzIjoiemtrIiwibmFtZSI6InVzZXIifQ.daJTLqiR-6oLa9kWTuQhqSqTkAc0EWLuIjdHxjhVcng' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "user",
    "message": "сообщение"
}'
```

- Message witch "history" call and valid token in headers:
```
curl --location --request POST 'http://0.0.0.0:8888/msg' \
--header 'Authorization: Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NjMyMjczMTksImlhdCI6MTY2MjM2MzMxOSwiaXNzIjoiemtrIiwibmFtZSI6InVzZXIifQ.daJTLqiR-6oLa9kWTuQhqSqTkAc0EWLuIjdHxjhVcng' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "user",
    "message": "history 10"
}'
```
## Test task

In db create couple sql tables with connection (foreign keys).

Create HTTP POST endpoint that receives like:
```
{
    name: "user name" 
    password: "password" 
}
```
This endpoint validate password in db and creates jwt token 
(the validity period of the token and the signature algorithm are not important,
you can use a ready-made library to generate and work with the token)name: "sender's name"
and sends a token in response, also a json of the form:
```
{
    token: "generated token" 
}
```
The server listens and responds to some endpoint, it receives data in json format as input (Client-User Messages):

~~~
{
    name:       "sender name",
    message:    "text message"
}
~~~

The headers indicate the Bearer token received from the endpoint above (there must be an underscore between the Bearer and the received token).
Check the token, in case of successful check of the token, save the received message to the database.

If you receive a message like:
```
{
    name:       "messager name",
    message:    "history 10"
}
```
check the token, in case of successful check of the token, send the last 10 messages from the database to the sender


Add a description and instructions for launching and comments in the code, if you change the message format, then a detailed description of the endpoints and their fields.

Wrap all the components in docker, cover the code with tests.

The project must be uploaded to github and docker hub. A readme file is required.
In the absence of a full-fledged readme-file, the test task will not be checked!

Port 8080 DO NOT SPECIFY!!!


Make requests (curl) through the terminal to check the performance of your program (attach a file with requests).

>Test task completed by: Artyom Tolstopiatov

>Email: clasterpack@gmail.com

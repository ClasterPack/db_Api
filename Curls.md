
Авторизация с правильным токеном:
```
curl --location --request POST 'http://0.0.0.0:8888' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "user",
    "password": "user"
}'
```

Сообщение с правильным токеном в заголовке:

```
curl --location --request POST 'http://0.0.0.0:8888/msg' \
--header 'Authorization: Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NjMyMjczMTksImlhdCI6MTY2MjM2MzMxOSwiaXNzIjoiemtrIiwibmFtZSI6InVzZXIifQ.daJTLqiR-6oLa9kWTuQhqSqTkAc0EWLuIjdHxjhVcng' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "user",
    "message": "сообщение"
}'
```

Сообщение с запросом истории и правильным токеном в заголовке:
```
curl --location --request POST 'http://0.0.0.0:8888/msg' \
--header 'Authorization: Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NjMyMjczMTksImlhdCI6MTY2MjM2MzMxOSwiaXNzIjoiemtrIiwibmFtZSI6InVzZXIifQ.daJTLqiR-6oLa9kWTuQhqSqTkAc0EWLuIjdHxjhVcng' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "user",
    "message": "history 10"
}'
```
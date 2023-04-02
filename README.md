***
**_Read this in other languages: [English](README.eu.md), [Русский](README.md)_**
***

## Применение API:

-  API слушает POST запросы в  [localhost/](http://0.0.0.0:8888)
    проверяя в БД(sql) имя и пароль, возвращая jwt token
- API слушает POST запросы в [localhost/msg](http://0.0.0.0:8888/msg)
проверяет jwt токен в headers authorisation, сохраняет сообщение при верном jwt токене возвращает bool ответ на сохранение сообщения.
в случае если токен верен и сообщение "history 10" возвращает последние 10 сообщений пользователя.
- Тесты находятся в :
> src/test

## Рабочее окружение

Для начала разработки необходимо настроить рабочее окружение. Нам понадобятся следующие системные зависимости: 
- [python](https://www.python.org/downloads/) версии 3.10.4 или выше
- менеджер зависимостей [poetry](https://python-poetry.org/docs/#installation) версии 1.2.0 или выше

Настройка окружения:
1. Настроить репозиторий
    ```shell script
   git clone https://github.com/ClasterPack/db_Api.git db_Api
   cd db_Api
    ```
2. Установить зависимости. Зависимости установяться в виртуальное окружение.
    ```shell script
    poetry install
   ```
   При необходимости билда с тестированием установить:
   ```shell script
   poetry install -E tests
   ```

## Запуск

Подключение виртуального окружения:
   ```shell script
   poetry shell
   ```

Из виртуального окружения сервис запускается командой:
   ```shell script
   python -m src.app -c src/config.yml
   ```

## Curl Запросы к API:

- Авторизация с правильным токеном:
```
curl --location --request POST 'http://0.0.0.0:8888' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "user",
    "password": "user"
}'
```

- Сообщение с правильным токеном в заголовке:

```
curl --location --request POST 'http://0.0.0.0:8888/msg' \
--header 'Authorization: Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NjMyMjczMTksImlhdCI6MTY2MjM2MzMxOSwiaXNzIjoiemtrIiwibmFtZSI6InVzZXIifQ.daJTLqiR-6oLa9kWTuQhqSqTkAc0EWLuIjdHxjhVcng' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "user",
    "message": "сообщение"
}'
```

- Сообщение с запросом истории и правильным токеном в заголовке:
```
curl --location --request POST 'http://0.0.0.0:8888/msg' \
--header 'Authorization: Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NjMyMjczMTksImlhdCI6MTY2MjM2MzMxOSwiaXNzIjoiemtrIiwibmFtZSI6InVzZXIifQ.daJTLqiR-6oLa9kWTuQhqSqTkAc0EWLuIjdHxjhVcng' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "user",
    "message": "history 10"
}'
```
## Тестовое задание

В БД создать пару sql табличек со связями (foreign keys)

Сделать HTTP POST эндпоинт, который получает данные в json вида:
```
{
    name: "имя отправителя"
    password: "пароль" 
}
```
этот эндпоинт проверяет пароль по БД и создает jwt токен (срок действия токена и алгоритм подписи не принципиален, для генерации и работе с токеном можно использовать готовую библиотечку) в токен записывает данные: name: "имя отправителя" 
и отправляет токен в ответ, тоже json вида:
```
{
    token: "тут сгенерированный токен" 
}
```
Сервер слушает и отвечает в какой-нибудь эндпоинт, в него на вход поступают данные в формате json:
Сообщения клиента-пользователя:
```
{
    name:       "имя отправителя",
    message:    "текст сообщение"
}
```
В заголовках указан Bearer токен, полученный из эндпоинта выше (между Bearer и полученным токеном должно быть нижнее подчеркивание).
Проверить токен, в случае успешной проверки токена, полученное сообщение сохранить в БД.

Если пришло сообщение вида:
```
{
    name:       "имя отправителя",
    message:    "history 10"
}
```
проверить токен, в случае успешной проверки токена отправить отправителю 10 последних сообщений из БД

Добавить описание и инструкцию по запуску и комментарии в коде, если изменяете формат сообщений, то подробное описание ендпоинтов и их полей.

Завернуть все компоненты в докер, покрыть код тестами.

Проект необходимо выкладывать на github и docker hub. Обязательно наличие readme-файла. 
При отсутствии полноценного readme-файла проверка тестового задания производиться не будет!

Порт 8080 НЕ УКАЗЫВАТЬ!!!

Составить запросы (curl) через терминал для проверки работоспособности вашей программы (приложить файл с запросами).

>Выполнил тестовое задание: Толстопятов Артём
>
> Email: clasterpack@gmail.com

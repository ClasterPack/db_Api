import datetime
import sqlite3
from pathlib import Path

import jwt
import yaml


class UsersAuth:
    """Класс авторизаций API."""

    def __init__(self):
        """Инициализация класса."""
        config = Path('src/config.yml').read_text()
        config = yaml.safe_load(config)
        self.secret = config['jwt']['secret']
        self.algorithm = config['jwt']['algorithm']
        self.expire_jwt = config['jwt']['exp_days']
        self.db = config['db']

    def check_password(self, name, password):
        """Функция проверки имени и пароля в БД."""
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        password_check = cursor.execute(
            'SELECT * FROM users WHERE name=? AND password=?',
            (name, password),
        )
        if password_check.fetchone() is None:
            conn.close()
            return False
        conn.close()
        return True

    def jwt_token(self, name):
        """Функция возвращает jwt токен."""
        try:
            payload = {
                # Задаем срок годности токена.
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=self.expire_jwt),
                # Время публикации токена.
                'iat': datetime.datetime.utcnow(),
                # Эмитет токена."""
                'iss': 'zkk',
                # Передаваемые данные.
                'name': name,
            }
            token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
            return token
        except jwt.exceptions.ExpiredSignatureError as ex:
            return ex

    def verify_bearer_token(self, token, name):
        """Функция валидации токена."""
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
            )
            if payload['name'] == name:
                return True
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return False

    def save_msg(self, username, msg):
        """Функция сохраняет сообщения пользователя."""
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO Messages (NAME, MESSAGE) VALUES( ?, ?);',
                (username, msg),
            )
            conn.commit()
            cursor.close()
            return True

        except Exception as ex:
            return False, ex

    def msg_history(self, username):
        """Функция возвращает историю сообщений пользователя."""
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute(
                'SELECT message FROM Messages WHERE name=? ORDER BY Message_id DESC LIMIT 10;',
                (username,),
            )
            history = cursor.fetchall()
            cursor.close()
            conn.close()
            return history
        except Exception as ex:
            return ex

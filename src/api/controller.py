import datetime
import sqlite3
from pathlib import Path

import jwt
import yaml


class UsersAuth:
    """Класс авторизаций API."""

    def __init__(self):
        """Инициализация класса."""
        config = yaml.safe_load(Path('src/config.yml').read_text())
        """Считываем ключь и алгоритм с конфига(config.yml)."""
        self.secret = config["jwt"]['secret']
        self.algorithm = config['jwt']['algorithm']
        self.expire_jwt = config['jwt']['exp_days']
        self.db = config['db']

    def check_password(self, name, password):
        """Функция проверки имени и пароля в БД."""
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        result = cursor.execute('SELECT * FROM users WHERE name=? AND password=?',
                              (name, password,)
                              )
        if result.fetchone() is None:
            conn.close()
            return False
        else:
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
                'name': name
            }
            token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
            return token
        except jwt.exceptions.ExpiredSignatureError as e:
            return e

    def verify_bearer_token(self, token):
        payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        if payload:
            return True
        return False

    def save_msg(self, username, msg):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Messages (NAME, MESSAGE) VALUES( ?, ?);',
                         (username, msg)
                         )
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            return e

    def msg_history(self, username):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('SELECT message FROM Messages WHERE name=? ORDER BY Message_id DESC LIMIT 10;',
                         (username, ),
                         )
            history = cursor.fetchall()
            cursor.close()
            conn.close()
            return history
        finally:
            pass

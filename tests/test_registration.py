import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users, DB_NAME

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test_exist_login():
    """Тест на добавление пользователя с существующим логином."""

def test_show_users(capsys):
    """Тест на отображения списка пользователей"""

    # Очистка таблицы перед тестом
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users')
        conn.commit()

    # Добавляем тестовых пользователей
    add_user('test_user1', 'test1@example.com', 'password1')
    add_user('test_user2', 'test2@example.com', 'password2')

    # Вызываем функцию, которая печатает пользователей
    display_users()

    # Перехватываем вывод
    captured = capsys.readouterr()
    output = captured.out

    # Проверяем наличие ожидаемых записей
    assert 'Логин: test_user1, Электронная почта: test1@example.com' in output
    assert 'Логин: test_user2, Электронная почта: test2@example.com' in output


# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""
import random
import string


def random_username(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def test_signup_new_account(app):
    username = random_username("user_", 10)
    email = username + "@localhost"
    password = "test"
    # Проверили, зарегистриирован ли пользователь на почтовом сервере
    app.james.ensure_user_exists(username, password)
    app.signup.new_user(username, email, password)
    # Проверка через удаленный программный интерфейс
    # assert app.soap.can_login(username, password)
    # Проверка через программный интерфейс
    app.session.Login(username, password)
    assert app.session.is_logged_in_as(username)
    app.session.Logout()


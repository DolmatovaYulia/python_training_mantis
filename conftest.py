import pytest
from fixture.application import Application
import json
import os.path
import importlib
import jsonpickle
import ftputil


fixture = None
target = None


# Функция, занимающаяся загрузкой конфигурации
def load_config(file):
    global target
    # Проверка для предотвращения повторной загрузки конфигурационного файла
    if target is None:
        # Переменная __file__ содержит путь к файлу
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        # Читаем файл с помощью функции pytest_addoption
        with open(config_file) as f:
            # f содержит объект, который указывает на открытый файл
            target = json.load(f)
    return target


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture
def app(request, config):
    # Инициализация. Создание фикстуры
    global fixture
    browser = request.config.getoption("--browser")
    webadmin_config = config['webadmin']
    if fixture is None or not fixture.is_valid():
        # функция создает объект класса Application
        fixture = Application(browser=browser, base_url=config['web']['baseUrl'])
    # fixture.session.ensure_Login(username=webadmin_config['username'], password=webadmin_config['password'])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        # Восстановление конфигурации сервера
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)


def install_server_configuration(host, username, password):
    # Создается новое соеддинение с ftp сервером
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.back"):
            remote.remove("config_inc.php.back")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.back")
        # Локальный файл и удаленный
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.back"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.back", "config_inc.php")


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_Logout()
        fixture.Destroy()
    # How the fixture should be destroyed
    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")


def pytest_generate_tests(metafunc):
    # Получение информации о фикстурах, которые есть у тестовой функции (параметры)
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_form_module(fixture[5:])
            # Используем загруженные тестовые данные для того, чтобы параметризовать функцию
            # fixture - куда будут подставляться параметры
            # testdata - какие значения (источник данных)
            # ids - список со строковым представлением данных
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_form_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


# Загружаем данные из модуля
def load_form_module(module):
    return importlib.import_module("data.%s" % module).testdata


# Загружаем данные из json-файла
def load_form_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        # Читаем данные и перекодируем обратно в исходный формат в виде объекта python
        return jsonpickle.decode(f.read())


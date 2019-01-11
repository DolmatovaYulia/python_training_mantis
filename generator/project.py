from model.project import Project
import random
import string
import os.path
import jsonpickle
import getopt
import sys


# Читаем опции из командной строки
try:
    # n - опция, которая задает количество генерируемых данных
    # f - опция, которая задет файл, в который это должно помещаться
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of groups", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)


n = 3
f = "data/projects.json"

# Читаем опции
for o, a in opts:
    # Если название опции == -n, значит в ней задается количество групп
    if o == "-n":
        # Преобразуем значение опции в число
        n = int(a)
    # Если название опции == -f, значит в ней задается файл
    elif o == "-f":
        f = a

# Генератор случайных строк
def random_strint(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + string.punctuation + " "*5
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


status = ["development", "release", "stable", "obsolete"]

inherit_global = [1, 0]

view_state = ["public", "private"]


# Тестовые данные
testdata = [Project(name=random_strint("name", 10), status=random.choice(status), inherit_global=random.choice(inherit_global), view_state=random.choice(view_state), description=random_strint("name", 40))
    for i in range(n)
]


# Сохранение сгенерированных данных в файл
# Определяем путь к файлу
file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

# Открываем файл на запись
with open(file, "w") as out:
    # Параметры форматирования. Библиотека работает с разными кодировщиками ("json")
    jsonpickle.set_encoder_options("json", indent=2)
    out.write(jsonpickle.encode(testdata))



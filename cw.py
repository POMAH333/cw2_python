"""
Реализовать консольное приложение заметки, с сохранением, чтением,
добавлением, редактированием и удалением заметок. Заметка должна
содержать идентификатор, заголовок, тело заметки и дату/время создания или
последнего изменения заметки. Сохранение заметок необходимо сделать в
формате json или csv формат (разделение полей рекомендуется делать через
точку с запятой). Реализацию пользовательского интерфейса студент может
делать как ему удобнее, можно делать как параметры запуска программы
(команда, данные), можно делать как запрос команды с консоли и
последующим вводом данных, как-то ещё, на усмотрение студента.
"""

from csv import DictReader, DictWriter
from os.path import exists

file_name = "phones.csv"
file_str_copy = "phones_copy.csv"


class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt


def get_info():
    # first_name = "Иван"
    # last_name = "Иванов"
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    phone_number = None

    is_valid = False

    while not is_valid:
        try:
            phone_number = int(input("Введите номер: "))
            # phone_number = 99999999999
            if len(str(phone_number)) != 11:
                raise LenNumberError("Не верная длина номера")
            else:
                is_valid = True
        except ValueError:
            print("Не валидный номер")
        except LenNumberError as err:
            print(err)
            continue

    return [first_name, last_name, phone_number]


def create_file(file_name):
    with open(file_name, "w", encoding="utf-8") as data:
        f_writer = DictWriter(data, fieldnames=["Имя", "Фамилия", "Телефон"])
        f_writer.writeheader()


def write_file(file_name, lst):
    with open(file_name, "r", encoding="utf-8") as data:
        f_reader = DictReader(data)
        res = list(f_reader)

    for el in res:
        if el["Телефон"] == str(lst[2]):
            print("Такой телефон уже есть в справочнике")
            return

    obj = {"Имя": lst[0], "Фамилия": lst[1], "Телефон": lst[2]}

    with open(file_name, "w", encoding="utf-8", newline="") as data:
        res.append(obj)
        f_writer = DictWriter(data, fieldnames=["Имя", "Фамилия", "Телефон"])
        f_writer.writeheader()
        f_writer.writerows(res)


def read_file(file_name):
    with open(file_name, "r", encoding="utf-8") as data:
        f_reader = DictReader(data)
        return list(f_reader)


def copy_str(file_source, file_reciver, str_num):
    file_content = read_file(file_source)
    if str_num > len(file_content):
        return print("Строка с таким номером отсутствует в исходном файле")
    file_content = list(file_content[str_num - 1].values())
    write_file(file_reciver, file_content)
    return


def main():
    while True:
        command = input("Введите команду: ")

        if command == "q":
            break
        elif command == "w":
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name, get_info())
        elif command == "r":
            if not exists(file_name):
                print("Файл отсутствует")
                continue
            print(*read_file(file_name))
        elif command == "c":
            if not exists(file_name):
                print("Файл источник отсутствует")
                continue
            if not exists(file_str_copy):
                create_file(file_str_copy)
            str_copy_num = int(input("Введите номер копируемой строки: "))
            copy_str(file_name, file_str_copy, str_copy_num)


main()

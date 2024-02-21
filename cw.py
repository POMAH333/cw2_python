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
import datetime

file_name = "notes.csv"
notes_list = {}


class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt


def create_file(file_name):
    with open(file_name, "w", encoding="utf-8") as data:
        f_writer = DictWriter(data, delimiter = ";", fieldnames=["ID", "Заголовок", "Заметка", "Изменения"])
        f_writer.writeheader()


def write_file(file_name):
    with open(file_name, "w", encoding="utf-8", newline="") as data:
        f_writer = DictWriter(data, delimiter = ";", fieldnames=["ID", "Заголовок", "Заметка", "Изменения"])
        f_writer.writeheader()
        for el in notes_list.items():
            f_writer.writerow({"ID": el[0], "Заголовок": el[1][0], "Заметка": el[1][1], "Изменения": el[1][2]})


def read_file(file_name):
    with open(file_name, "r", encoding="utf-8") as data:
        f_reader = DictReader(data, delimiter = ";")
        list_file = list(f_reader)
        notes_list.clear()
        for el in list_file:
            notes_list[el["ID"]] = [el["Заголовок"], el["Заметка"], el["Изменения"]]

def add_note():
    note_data = []
    find_index = True
    keys_list = notes_list.keys()
    print(keys_list)
    i = 0
    while find_index:
        if str(i) not in keys_list:
            i += 1
        else:
            find_index = False
    note_data.append(input('Введите заголовок заметки: '))
    note_data.append(input('Введите тело заметки: '))
    note_data.append(datetime.datetime.now().strftime('%d-%m-%Y / %H:%M:%S'))
    notes_list[str(i)] = note_data
    print('Заметка успешно добавлена')
    print('')

def list_notes():
    list_preview = sorted(notes_list.items(), key=lambda x: datetime.datetime.strptime(x[1][2], '%d-%m-%Y / %H:%M:%S'))
    print('Список заметок')
    print('ID\tДата изменения заметки\tЗаголовок')
    for el in list_preview:
        print(el[0] + '\t' + el[1][2] + '\t' + el[1][0])
    print('')

def edit_note(num):
    if notes_list.get(num) == None:
        print('Заметка с таким номером отсутствует')
        print('')
        return
    note_data = []
    note_data.append(input('Введите заголовок заметки: '))
    note_data.append(input('Введите тело заметки: '))
    note_data.append(datetime.datetime.now().strftime('%d-%m-%Y / %H:%M:%S'))
    notes_list[num] = note_data
    print('Заметка успешно изменена')
    print('')

def del_note(num):
    if notes_list.pop(num) == None:
        print('Заметка с таким номером отсутствует')
        print('')
        return
    else:
        print('Заметка успешно удалена')
        print('')

def view_note(num):
    if notes_list.get(num) == None:
        print('Заметка с таким номером отсутствует')
        print('')
        return
    print('')
    print('ID: ' + num)
    print('Заголовок: ' + notes_list.get(num)[0])
    print('Тело заметки: ' + notes_list.get(num)[1])
    print('Дата/время последнего изменения: ' + notes_list.get(num)[2])
    print('')

def main():
    prog_exit = True
    while prog_exit:
        command = input("Введите команду или q для выхода: ")

        if command == "q":
            prog_exit = False
        elif command == "save":
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name)
            print('Файл успешно записан')
            print('')
        elif command == "read":
            if not exists(file_name):
                print("Файл отсутствует")
                continue
            read_file(file_name)
            print('Данные успешно считаны из файла')
            print('')
        elif command == "add":
            add_note()
        elif command == "list":
            list_notes()
        elif command == "edit":
            note_num = input("Введите номер заметки для редактирования: ")
            edit_note(note_num)
        elif command == "del":
            note_num = input("Введите номер заметки для удаления: ")
            del_note(note_num)
        elif command == "view":
            note_num = input("Введите номер заметки для просмотра: ")
            view_note(note_num)
        else:
            print('Команда не поддерживается')
            print('')

main()

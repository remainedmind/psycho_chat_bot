import longstrings as ls
# Импортируем собственный модуль,
# в который помещены все длинные строковые переменные


names = ['тест на тип личности', 'тест на уровень тревоги']
# Формат data = {название теста: [порядковый номер, название txt-файла,
# инструкция по ответу на вопросы, корректный формат ответа]}
data = {
    names[0]: [
        ls.character_definition,
        'character_test.txt',
        ls.instructions[0], ['1', '2']
        ],
    names[1]: [
        ls.anxiety_definition, 'TMAS.txt',
        ls.instructions[1], ['да', 'нет']
        ]
    }


def menu():
    # Функция выведет пользователю список тестов.
    print('Пожалуйста, выберите тест:')
    for i, name in enumerate(names, start=1):
        # https://docs.python.org/3/library/functions.html#enumerate
        # Функция enumarate используется для получения счётчика цикла,
        # принимая на вход итерируемый объект и возвращая его же
        # значения вместе с индексами элементов. Второй аргумент
        # функции - начальное значение счётчика.
        print(f'{i}) {name}')


def get_name():
    # Функция запросит у пользователя номер теста, который он хочет пройти
    while True:
        # Используем while, чтобы запрашивать ответ до тех пор,
        # пока он не будет корректным.
        name = input(
            f'Укажите номер теста, который вы хотели бы пройти.'
            f'\nНапример, 1.'
            )
        if name in ('1', '2'):
            # При добавлении нового теста этот кортеж необходимо дополнить
            # вручную, однако в условиях программы, которая редко будет
            # подвергаться редактированию, это проще, чем проверять попадание
            # переменной name в список индексов списка names, поскольку
            # придётся обрабатывать исключения при вводе нечисловых данных.
            return names[int(name)-1]
        else:
            print(ls.wrong_str)
            continue


def description(name):
    # Эта функция получает на вход название теста и выводит его подробное
    # описание, после чего предлагает пользователю пройти тест или вернуться
    # к выбору теста.
    print(
        f'  Вы выбрали {name}.\nОписание теста:\n{data[name][0]}'
        f'\nВведите "начать" или "start", чтобы приступить к выполнению теста.'
        f' Напишите "назад" или "back", чтобы вернуться в главное меню.'
    )
    while True:
        choice = input()
        if choice.lower() in ('назад', 'back'):
            return 'back'
        elif choice.lower() in ('начать', 'start'):
            return 'start'
        else:
            print(ls.wrong_str)
            continue


def test_running(name):
    # Эта функция реализует выполнение теста, получая на вход название
    # и возвращая список ответов. Если тест будет прерван,
    # функция вернёт None.
    with open(data[name][1], 'r', encoding='utf-8') as test:
        # Открываем файл и добавляем строки в список
        lines = test.readlines()
    answer_list = []
    # Объявляем список, в который будет записывать ответы/
    print(data[name][2])
    # Выводим инструкцию к тесту,
    # поясняющую пользователю взаимодействие с программой/
    while not(len(lines) == len(answer_list)):
        # Этот цикл будет работать до тех пор, пока число ответов не будет
        # равно числу вопросов
        ans = input(f'Вопрос {len(answer_list)+1}/{len(lines)}:'
                    f'\n{lines[len(answer_list)]}')
        if ans == '0':
            return
        elif ans.lower() in data[name][3]:
            # https://docs.python.org/3/library/stdtypes.html?highlight=lower#str.lower
            # Функция lower() - строковый метод, возвращающий копию строки
            # полностью в нижнем регистре. Благодаря этому методу
            # программа распознает введённый текст вне зависимости
            # от того, введён он с заглавной буквы или строчной
            answer_list.append(ans.lower())
        else:
            print(ls.wrong_str)
            continue
        print(end=2*'\n')
        # Будем разделять вопросы пустыми строками, чтобы
        # облегчить визуальное восприятие программы.
    return answer_list


def character_decryption(answer_list):
    # Эта функция интерпретирует ответы на первый тест
    vert_counter = 0
    for i, answer in enumerate(answer_list):
        # Здесь функция enumerate используется,
        # чтобы получить номер каждого ответа.
        # Порядковый номер требуется для работы с ключом расшифровки.
        if (i in (1, 4, 6, 8, 10, 12, 14, 15, 16, 17, 19) and
           answer == '1' or i in (0, 2, 3, 5, 7, 9, 11, 13, 18) and
           answer == '2'):
            vert_counter += 1
            # Функция считает "баллы" за ответы, по которым
            # определеятся результат
    if vert_counter <= 7:
        result = ls.introvert
    elif vert_counter > 13:
        result = ls.extrovert
    else:
        result = ls.ambivert
    return result


def TMAS_decryption(answer_list):
    # Эта функция интерпретирует ответы на вторый тест
    anx_counter = 0
    lie_counter = 0
    # Тест TMAS параллельно со своим основным назначением также определяет,
    # лжёт ли испытуемый. Для определения уровня честности используется
    # вторая переменная-счётчик.
    str_for_yes = (6, 7, 9, 11, 12, 13, 15, 18, 21, 23, 24, 25, 26, 28, 30, 31,
                   32, 33, 34, 35, 36, 37, 38, 40, 42, 44, 45, 46, 47, 48, 49,
                   50, 51, 54, 56, 60
                   )
    str_for_no = (1, 3, 4, 5, 8, 14, 17, 19, 22, 39, 43, 52, 57, 58)
    for i, answer in enumerate(answer_list, start=1):
        if (i in str_for_yes and answer == 'да' or
                i in str_for_no and answer == 'нет'):
            anx_counter += 1
        if (i in (2, 10, 55) and answer == 'да' or
                i in (16, 20, 27, 29, 41, 51, 59) and answer == 'нет'):
            lie_counter += 1
    if lie_counter > 6:
        return ls.lier
    if anx_counter > 40:
        result = ls.anxiety_level_5
    elif 25 < anx_counter <= 40:
        result = ls.anxiety_level_4
    elif 15 < anx_counter <= 25:
        result = ls.anxiety_level_3
    elif 5 < anx_counter <= 15:
        result = ls.anxiety_level_2
    else:
        result = ls.anxiety_level_1
    return result


def main():
    # Главная функция, связывающая работу всех других.
    # Она будет вызывать саму себя,
    # поддерживая постоянную работу программы.
    global result
    menu()
    name = get_name()
    choice = description(name)
    if choice == 'start':
        answer_list = test_running(name)
        if answer_list is None:
            # Если тест был прерван, программа не выдаст результат.
            result = ''
        elif name == names[0]:
            result = character_decryption(answer_list)
        elif name == names[1]:
            result = TMAS_decryption(answer_list)
        print (result, '\n'*2, 'Вы закончили выполнение теста. ', ls.stop_str)
    elif choice == 'back':
        print('  Вы вернулись в главное меню. ')
        main()
        return
    ex = input()
    if ex.lower() in ('завершить', 'end', 'закончить'):
        return
    else:
        print('  Вы вернулись в главное меню. ')
        main()
        # При желании пройти тест заново программа запустится сначала.

if __name__ == '__main__':
    print('  Эта программа предназначена для психологического тестирования.')
    main()
    print('  Работа программы закончена.')
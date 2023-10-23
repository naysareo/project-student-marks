import json

# Принты которые отображают database_local (состояние словаря с данными созданы для наглядности и понимания процесса)

try:
    with open('database.json', 'r') as file:
        database_dict = json.load(file)

except FileNotFoundError:
    database_dict = {}

except json.JSONDecodeError:
    print('\nСистеме не удалось прочитать файл базы данных. Данные повреждены ввиду ручного вмешательства '
          'во внутренние файлы системы или файлы были повреждены по иным причинам.\n')
    database_dict = {}


def displaying_groups(database_local):
    if len(database_local) == 0:
        print("\nСистеме не удалось найти ни одной группы. Создайте первую группу.\n")
    elif len(database_local) > 0:
        print("Группы которые уже существуют:")
        for groups in database_local.keys():
            print(groups)


def displaying_students_in_group(database_local, group_number):
    if len(database_local[group_number]) == 0:
        print("\nВ этой группе нет ни одного студента. Добавьте студентов.\n")
    elif len(database_local[group_number]) > 0:
        print(f"Все студенты в группе {group_number}:")
        for students in database_local[group_number].keys():
            formatted_name = students.replace('_', ' ').title()
            print(formatted_name)


def displaying_student_marks(database_local, group_number):
    if len(database_local) == 0 or len(database_local[group_number]) == 0:
        print('\nВ базе данных отсутствуют введенные данные (группа или студент)\n')
    elif len(database_local) > 0 and len(database_local[group_number]) == 0:
        for group, students in database_local.items():
            for student, marks in students.items():
                if len(database_local[group_number][student]) == 0:
                    print('\nУ указанного студента нет ни одной отметки. Добавьте отметки студенту.\n')
                elif len(database_local[group_number][student]) > 0:
                    print(f"Студент: {student}")
                    for mark in marks:
                        print(mark)


def group_creation_space(database_main):
    # Group_creation_space пространство для создания группы. Функция хранит в себе другие функции для взаимодействия
    # с данными которые приходят из локальной переменной database_main. После чего возвращает измененный словарь с
    # данными.

    def checking_and_creating_group(database_local):
        displaying_groups(database_local)
        enter_group_name = str(input("Создайте номер группы: "))
        if enter_group_name.strip() == '':
            print("\nИмя группы не может быть пустым!\n")

        elif enter_group_name in database_local:
            print(
                "\nЭта группа уже есть в базе данных. Создайте новую или редактируйте уже существующую в разделе "
                "\"Редактирования базы данных учебного заведения\" в главном меню\n")

        elif enter_group_name not in database_local:
            print("\nГруппа", enter_group_name, "верифицирована\n")
            database_local[enter_group_name] = {}
            # отображения состояния словаря (для разработчиков)
            print(database_dict)
        return database_local

    valid_group_number = checking_and_creating_group(database_main)
    return valid_group_number


def data_management_space(database_main):
    # Пространство которые управляет данными (добавляет студента и его отметки, или добавляет отметки уже
    # существующему студенту)
    while True:
        if len(database_main) == 0:
            print('\nСистема не обнаружила ни одной группы. Создайте первую группу для работы с данными.\n')
            break

        def checking_data(database_local):
            while True:
                displaying_groups(database_main)
                finding_group = input("Введите в какую группу вы хотите внести данные или обновить её: ")
                if finding_group in database_local:
                    return finding_group
                elif finding_group.strip() == '':
                    print("\nИмя группы не может быть пустым! Повторите попытку.\n")
                    continue
                elif finding_group not in database_local:
                    print("\nГруппа", finding_group,
                          "не была найдена системой. Пожалуйста, проверьте правильность введенных данных.\n")
                    continue

        valid_group_number = checking_data(database_main)

        # Блок добавления студентов и их отметок
        def adding_marks(database_local, group_number):
            while True:

                action = input("Для добавления данных нажмите ENTER, "
                               "или введите \"R\" для перехода в главное меню: ").lower()
                if action == "r":
                    break
                elif action.strip() == '':
                    pass
                else:
                    print('\nВы ввели неверные данные. Повторите попытку.\n')
                    continue

                def creating_student_id():
                    displaying_students_in_group(database_local, group_number)
                    while True:
                        if len(database_local[group_number]) == 0:
                            enter_new_student_name = input("Введите имя для нового студента: ").upper()
                            enter_new_student_surname = input("Введите фамилию для нового студента: ").upper()
                            if enter_new_student_name.strip() == '' or enter_new_student_surname.strip() == '':
                                print("\nПоле не может быть пустым. Пожалуйста, введите значение заново.\n")
                                continue
                            else:
                                return enter_new_student_name + '_' + enter_new_student_surname

                        enter_student_name = input("Введите имя ученика: ").upper()
                        enter_student_surname = input("Введите фамилию ученика: ").upper()

                        if enter_student_name.strip() == '' or enter_student_surname.strip() == '':
                            print("\nПоле не может быть пустым. Пожалуйста, введите значение заново.\n")
                            continue
                        else:
                            return enter_student_name + "_" + enter_student_surname

                # Создаю ID студента из полученного результата функции в которой я привожу ID в определенный формат.
                student_id = creating_student_id()

                # создаю formatted_name для дальнейшего отображения имени в более удобной форме.
                formatted_name = student_id.replace('_', ' ').title()
                if student_id not in database_local[group_number]:
                    database_local[group_number][student_id] = {}

                print("Вводите отметки для ученика", formatted_name, "в строке ввода. По завершению введите E")
                while True:
                    displaying_student_marks(database_main, group_number)
                    # отображения состояния словаря (для разработчиков)
                    print(database_local)
                    try:
                        enter_marks = input("Ввод отметок: ").lower()

                        if enter_marks == "e":
                            break
                        else:
                            enter_marks = int(enter_marks)

                        if enter_marks <= 0 or enter_marks > 10:
                            print("\nМинимальная оценка 1, максимальная 10\n")
                            continue

                        else:
                            if len(database_local[group_number][student_id]) == 0:
                                database_local[group_number][student_id] = []
                            database_local[group_number][student_id].append(enter_marks)
                            # отображения состояния словаря (для разработчиков)
                            print(database_local)
                            continue
                    except ValueError:
                        print(
                            '\nВведены неверные данные. Проверьте ввод повторите попытку. Или введите (E)'
                            ' для выхода.\n')
            return database_local

        # присваиваю главной переменной database_main словарь с измененными данными
        database_main = adding_marks(database_main, valid_group_number)
        # если цик достиг данной строки, то он прерывается для выхода в главное меню
        break
    # используя return отдаю главной функции data_management_space измененный словарь database_main с данными.
    return database_main


# 0214
def editing_space(database_main):
    while True:
        if len(database_main) == 0:
            print('\nСистема не обнаружила ни одной группы. Создайте первую группу для работы с данными.\n')
            break

        def displaying_group_and_student_quantity(database_local):
            print("Найдены следующие группы:")
            for group, students in database_local.items():
                print(f'Группа: {group} Кол-во студентов: {len(students)}')

        def checking_group(database_local):
            while True:
                displaying_group_and_student_quantity(database_local)
                enter_group_number = input("Введите номер группы: ")
                if enter_group_number.strip() == '':
                    print("\nИмя группы не может быть пустым!\n")
                    continue
                elif enter_group_number not in database_local:
                    print("\nСистеме не удалось найти группу", enter_group_number, "в базе данных.\n")
                    break
                elif enter_group_number in database_local:
                    return enter_group_number

        valid_group_number = checking_group(database_main)
        if valid_group_number is None:
            continue

        def checking_user_action(group_number):
            while True:
                print("Введите \"1\" для редактирования группы или \"2\" ДЛЯ редактирования студентов группы",
                      group_number)
                try:
                    enter_action = int(input("Выберите действие: "))

                    if enter_action == 1 or enter_action == 2:
                        return enter_action
                    else:
                        print('\nВы ввели неподдерживаемые значения. Повторите попытку\n')
                        continue
                except ValueError:
                    print('\nВы ввели неверные данные повторите ввод.\n')

        selected_action = checking_user_action(valid_group_number)

        if selected_action == 1:
            def deleting_renaming_group(database_local, group_number):
                def checking_entered_action():
                    # Функция берет переменную database_local из функции deleting_renaming_group
                    while True:
                        print("Для удаления группы в строке ввода введите \"D\", для переименования группы \"R\" ")
                        choice_action = input("Ввод: ").lower()
                        if choice_action.strip() == '':
                            print('\nПоле не может быть пустым! Повторите попытку.\n')
                            continue
                        elif choice_action == 'r' or choice_action == 'd':
                            break
                        else:
                            print('\nВы ввели символ который не соответствует правилам ввода. Повторите попытку '
                                  'или нажмите \'E\' для выхода.\n')
                            continue
                    return choice_action

                del_rename_choice = checking_entered_action()

                if del_rename_choice == "d":
                    def deleting_group_number():
                        # переменная group_number берется из функции deleting_renaming_group
                        del database_local[group_number]
                        print(f"\nГруппа {group_number} была удалена\n")
                        return database_local

                    # переопределяю переменную database_local с измененными данными
                    database_local = deleting_group_number()
                    # с помощью return отдаю измененные данные словаре если пользователь выбрал 'd'
                    return database_local

                elif del_rename_choice == "r":
                    def renaming_group_number():
                        # переменные database_local и group_number берутся из функции deleting_renaming_group
                        while True:
                            print("Для переименования группы", group_number, "введите новый номер группы")
                            enter_new_group_number = input("Ввод нового номера группы: ")
                            if enter_new_group_number.strip() == '':
                                print('\nНазвание группы не может быть пустым! Повторите попытку.\n')
                                continue
                            elif enter_new_group_number in database_local:
                                print("\nИзменить номер группы невозможно т.к. она уже существует\n")
                                continue
                            elif enter_new_group_number not in database_local:
                                database_local[enter_new_group_number] = database_local.pop(group_number)
                                print("\nНазвание группы успешно изменено на", enter_new_group_number, '\n')
                                # отображения состояния словаря (для разработчиков)
                                print(database_local)
                                break

                            else:
                                print('\nВы ввели неверные данные. Если хотите продолжить введите ДА.'
                                      ' Если хотите выйти введите НЕТ.\n')
                                continue
                                # continue_or_exit = input('ДА или НЕТ: ').upper()
                                # if continue_or_exit == 'ДА':
                                #     continue
                                # elif continue_or_exit == 'НЕТ':
                                #     break
                        # отдаю функции обновленные данные
                        return database_local

                    # переопределяю database_local для обновления данных
                    database_local = renaming_group_number()
                return database_local

            # переопределяю database_main для того чтобы в будущем работать с уже измененными данными
            database_main = deleting_renaming_group(database_main, valid_group_number)

        if selected_action == 2 and len(database_main[valid_group_number]) > 0:

            def checking_entered_student_id(database_local, group_number):
                # Здесь проверка осуществляется иначе. Она идентична с проверкой от 74 по 86 строку.
                # Ожидается комментарий преподавателя по поводу лучших способов.
                while True:
                    displaying_students_in_group(database_local, group_number)
                    enter_student_name = input("Введите имя студента: ").upper()
                    enter_student_surname = input("Введите фамилию студента: ").upper()
                    if enter_student_name.strip() == '' or enter_student_surname.strip() == '':
                        print("\nПоле не может быть пустым. Пожалуйста, введите значение заново.\n")
                        continue
                    check_id = enter_student_name + "_" + enter_student_surname
                    if check_id not in database_local[group_number]:
                        # formatted_name используется для пользователя, чтобы он видел имя и фамилию без регистра.
                        formatted_name = check_id.replace("_", " ").title()
                        print("\nПроверьте правильность данных. Система не распознала "
                              "студента", formatted_name, "в группе\n",
                              group_number)
                        continue
                    elif check_id in database_local[group_number]:
                        return check_id
                    break

            valid_student_id = checking_entered_student_id(database_main, valid_group_number)

            def checking_data_and_choice_v1():
                # formatted_name используется для пользователя, чтобы он видел имя и фамилию без регистра.
                formatted_name = valid_student_id.replace("_", " ").title()
                # переменные из функции checking_user_choice используются из области видимости функции editing_space
                while True:
                    print("Выберите действие:")
                    print("Введите \"1\" для переименования студента в группе", valid_group_number)
                    print("Введите \"2\" для удаления или замены оценок ученика", formatted_name)
                    try:
                        enter_user_choice = int(input("Введите номер нужного вам действия: "))
                        if enter_user_choice == '':
                            print('\nЭто поле не может быть пустым!\n')
                            continue
                        if enter_user_choice == 1 or enter_user_choice == 2:
                            break
                    except ValueError:
                        print('\nВы ввели неверные данные. Повторите попытку.\n')
                    else:
                        print('\nВы ввели данные которые не соответствуют правилам ввода. Повторите попытку\n')
                        continue
                return enter_user_choice

            selected_choice = checking_data_and_choice_v1()

            if selected_choice == 1:
                def rename_student_id(database_local, old_student_id, group_number):
                    formatted_name = old_student_id.replace("_", " ").title()
                    print("Теперь введите новое имя и фамилию для студента", formatted_name)
                    while True:
                        enter_new_student_name = input("Новое имя студента: ").upper()
                        enter_new_student_surname = input("Новая фамилия студента: ").upper()
                        if enter_new_student_name.strip() == '' or enter_new_student_surname.strip() == '':
                            print("\nДанные студента не могут быть пустыми. Пожалуйста, введите данные заново.\n")
                            continue
                        new_student_id = enter_new_student_name + "_" + enter_new_student_surname
                        if new_student_id in database_dict[group_number]:
                            print("\nТакой студент уже существует. Повторите попытку.\n")
                            continue
                        elif new_student_id not in database_local[group_number]:
                            database_local[group_number][new_student_id] = database_dict[group_number].pop(
                                old_student_id)
                            print("Данные ученика успешно изменены!")
                            # отображения состояния словаря (для разработчиков)
                            print(database_local)
                            break
                    return database_local

                # переопределяю database_main для возврата всего словаря с измененными данными
                database_main = rename_student_id(database_main, valid_student_id, valid_group_number)

            elif selected_choice == 2:
                def replacing_deleting_marks(database_local, group_number, student_id_local):
                    formatted_name = student_id_local.replace("_", " ").title()

                    def replacing_deleting_marks_choice():
                        while True:
                            print("Введите \"S\" для замены оценок или \"R\" для удаления отметок студента",
                                  formatted_name)
                            enter_user_action = input("Ввод: ").upper()
                            if enter_user_action.strip() == '':
                                print('Поле не может быть пустым. Повторите попытку')
                                continue
                            elif enter_user_action == "S":
                                return 'S'
                            elif enter_user_action == 'R':
                                return 'R'
                            else:
                                print('\nВы ввели данные которые не соответствуют правилам ввода. Повторите попытку\n')
                                continue

                    user_choice = replacing_deleting_marks_choice()

                    def replacing_marks(status):
                        while status == 'S':
                            try:
                                enter_delete_mark = int(input("Введите оценку которую хотите удалить: "))
                                index_for_replace = database_local[group_number][student_id_local].index(
                                    enter_delete_mark)

                                if len(database_local[group_number][student_id_local]) == 0:
                                    print("\nУ студента нету ни одной отметки. Замена невозможна. "
                                          "Для начала добавьте студенту отметки.\n")

                                elif enter_delete_mark in database_local[group_number][student_id_local]:
                                    enter_new_mark = int(input("Введите новую отметку: "))
                                    database_local[group_number][student_id_local].remove(enter_delete_mark)
                                    database_local[group_number][student_id_local].insert(index_for_replace,
                                                                                          enter_new_mark)
                                    print("Для ученика", formatted_name, "были применена следующие изменения:")
                                    print("Оценка", enter_delete_mark, "была успешно заменена на новую отметку",
                                          enter_new_mark)
                                    print(database_dict)
                                    break
                            except ValueError:
                                print('\nВведенной отметки не существует у указанного студента.\n')
                                continue
                        return database_local

                    database_local = replacing_marks(user_choice)

                    def deleting_marks(status):
                        while status == "R":
                            print(database_local[group_number][student_id_local])
                            try:
                                enter_delete_mark = int(input("Введите оценку которую хотите удалить: "))
                                if len(database_local[group_number][student_id_local]) == 0:
                                    print("\nУ студента нет ни одной отметки. Удаление невозможно. "
                                          "Для начала добавьте студенту отметки.\n")
                                    print(database_dict)
                                    continue

                                elif enter_delete_mark not in database_local[group_number][student_id_local]:
                                    print('\nУказанная отметка отсутствует у ученика', formatted_name, '\n')
                                    continue

                                elif enter_delete_mark in database_local[group_number][student_id_local]:
                                    database_dict[group_number][student_id_local].remove(enter_delete_mark)
                                    print("Для ученика", formatted_name, "были применена следующие изменения:")
                                    print("Оценка", enter_delete_mark, "была успешно удалена")
                                    print(database_dict)
                                    break
                            except ValueError:
                                print('\nВы ввели неверные данные. Повторите попытку.\n')
                                continue
                        return database_local

                    database_local = deleting_marks(user_choice)
                    # 0214
                    return database_local

                database_main = replacing_deleting_marks(database_main, valid_group_number, valid_student_id)

        # Сообщения об ошибках.

        # Срабатывает если условие selected_action равно 2 и в базе данных отсутствуют студенты.
        elif selected_action == 2 and len(database_main[valid_group_number]) <= 0:
            print('\nВ указанной группе нет ни одного студента. '
                  'Для изменения данных студентов сначала добавьте первого студента.\n')

        break
    return database_main


def displaying_information(database_main):
    while True:
        if len(database_main) == 0:
            displaying_groups(database_main)
            break
        else:
            displaying_groups(database_main)

        enter_group_number = str(input('Введите номер группы, с которой хотите взаимодействовать: '))
        if enter_group_number.strip() == '':
            print('\nВвод не может быть пустым. Повторите попытку.\n')
            continue
        elif enter_group_number not in database_main:
            print('\nГруппа которую вы указали отсутствует в базе данных. Повторите попытку.\n')
            continue

        def checking_entered_user_data():

            while True:

                print("Для просмотра всех групп в базе данных нажмите \"1\" ")
                print("Для просмотра студентов в одной группе введите \"2\" ")
                print("Для просмотра оценок студентов введите \"3\" ")
                print('Для просмотра лучших студентов (60+ баллов) введите \"4\" ')

                try:
                    enter_search_choice = int(input("Выберите действие: "))

                    if enter_search_choice == 1 or enter_search_choice == 2 or enter_search_choice == 3 or \
                            enter_search_choice == 4:
                        break
                    else:
                        print('Вы ввели значения, которые не соответствуют правилам ввода. Повторите попытку')
                        continue
                except ValueError:
                    print('Вы ввели неверные данные. Повторите попытку.')

            return enter_search_choice

        user_choice = checking_entered_user_data()

        def list_best_students(database_local, group_number):
            if len(database_local[group_number]) == 0:
                displaying_students_in_group(database_local, group_number)

            for students in database_local[group_number]:
                len_marks = len(database_local[group_number][students])
                # sum_marks = reduce(lambda x, y: x + y, database_local[enter_group_number][students])
                sum_marks = sum(database_local[enter_group_number][students])
                average_score = sum_marks / len_marks
                if average_score > 6:
                    print(f'\nСтудент {students} | Средний балл: {average_score:.1f}\n')
                else:
                    print('\nВ группе ещё нет студентов со средним баллом выше 6\n')

        if user_choice == 1:
            displaying_groups(database_main)

        elif user_choice == 2:
            displaying_students_in_group(database_main, enter_group_number)

        elif user_choice == 3:
            displaying_student_marks(database_main, enter_group_number)

        elif user_choice == 4:
            list_best_students(database_main, enter_group_number)

        else:
            print('\nВвод неверных данных. Проверьте ввод и повторите попытку.\n')
            continue

        break


while True:

    while True:

        with open('database.json', 'w') as file:
            json.dump(database_dict, file)

        print("Введите (1) для создания новой группы. ")
        print("Введите (2) для перехода в раздел \"Управление данными\". Здесь вы сможете добавить студента"
              " в группу или добавить/обновить отметки.")
        print("Введите (3) для редактирования базы данных учебного заведения ")
        print("Введите (4) для просмотра нужной вам информации")
        print("Введите (5) для выхода из программы")

        try:
            enter_choice = int(input("Введите нужное вам действие: "))
        except ValueError:
            print('\nВведены неверные данные. Проверьте вводи повторите попытку.\n')
            continue

        if enter_choice == 1:
            database_dict = group_creation_space(database_dict)

        elif enter_choice == 2:
            database_dict = data_management_space(database_dict)

        elif enter_choice == 3:
            database_dict = editing_space(database_dict)

        elif enter_choice == 4:
            displaying_information(database_dict)

        elif enter_choice == 5:
            break
        else:
            print('\nВведены неверные данные. Проверьте данные которые вы ввели и повторите попытку.\n')
    break
    # update

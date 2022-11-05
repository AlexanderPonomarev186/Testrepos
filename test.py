import csv
import re
import prettytable
import os
def create_table(outprint_list, head):
    myTable = prettytable.PrettyTable()
    myTable.hrules = 1
    myTable.align = "l"
    myTable.field_names = head
    for item in head:
        myTable._max_width[item] = 20
    for i in range(len(outprint_list)):
        myTable.add_row(outprint_list[i])
    return myTable
def parse_into_list(dict):
    result_list = list()
    for i in range(len(dict)):
        temp_list = list()
        for key, item in dict[i].items():
            temp_list.append(item)
        result_list.append(temp_list)
    return numerating_lists(result_list)
def set_strings_size(lst):
    for i in range(len(lst)):
        for g in range(len(lst[i])):
            if len(lst[i][g]) > 100:
                lst[i][g] = lst[i][g][:100] + "..."
    return lst
def numerating_lists(lst):
    for i in range(len(lst)):
        lst[i].reverse()
        lst[i].append(str(i+1))
        lst[i].reverse()
    return lst



def clear(x):
    return ' '.join(re.sub(r"<[^>]+>", '', x).split())
def count(x):
    if (x%10 == 1) or (x-10 == x%10) or (x/10 >= 5):
        return "раз"
    else: return "раза"
def rubels(x):
    if (x%10 == 1):
        return "рубль"
    if (2 <= x%10 <= 4):
        return "рубля"
    else: return "рублей"
def vacancies(x):
    if (x%10 == 1) and (x != 11):
        return "вакансия"
    if (2 <= x%10 <= 4):
        return "вакансии"
    if (11 >= x >= 19): return "вакансий"
    else: return "вакансий"
def boolean(x):
    if x == "False":
        return "Нет"
    if x == "True":
        return "Да"
def tax_parser(x):
    if x == "Нет":
        return "С вычетом налогов"
    if x == "Да":
        return "Без вычета налогов"
def number_parser(x):
    temp_num = str(x)[-3:]
    temp_num2 = int(x/1000)
    if temp_num2 > 0:
        return str(temp_num2) + " "+ str(temp_num)
    else: return str(temp_num)
def format_date(x):
    x = x[:10].split("-")
    x.reverse()
    x = '.'.join(x)
    return x



def csv_reader(file_name):
    with open(file_name, encoding='utf-8-sig') as fp:
        reader = csv.reader(fp)
        head = next(reader)
        data_lines = []
        for row in reader:
            flag = True
            if (len(row) < len(head)):
                continue
            for i in row:
                if (i == ""):
                    flag = False
            if (flag):
                data_lines.append(row)
        return data_lines
def csv_filer(reader,list_naming):
    output_dict = list()
    for line in reader:
        data_dict = dict()
        for i in range(len(list_naming)):
            temp_line = line[i]
            temp_line = temp_line.split('\n')
            if (len(temp_line) == 1):
                data_dict[list_naming[i]] = clear(temp_line[0])
            else:
                for g in range(len(temp_line)):
                    temp_mass = temp_line[g].split()
                    temp_line[g] = ' '.join(temp_mass)
                data_dict[list_naming[i]] = ', '.join(temp_line)
        output_dict.append(data_dict)
    return output_dict
def formatter(row):
    experience = {"noExperience": "Нет опыта",
                  "between1And3": "От 1 года до 3 лет",
                  "between3And6": "От 3 до 6 лет",
                  "moreThan6": "Более 6 лет"}
    valutes = {"AZN": "Манаты",
               "BYR": "Белорусские рубли",
               "EUR": "Евро",
               "GEL": "Грузинский лари",
               "KGS": "Киргизский сом",
               "KZT": "Тенге",
               "RUR": "Рубли",
               "UAH": "Гривны",
               "USD": "Доллары",
               "UZS": "Узбекский сум"}
    for i in range(len(row)):
        for key, item in row[i].items():
            if key == "experience_id":
                row[i][key] = experience[item]
            if item == "False" or item == "True":
                row[i][key] = boolean(item)
            if key == "salary_currency":
                row[i][key] = valutes[item]
            if key == "published_at":
                row[i][key] = format_date(item)
        row[i]["salary_from"] = "{0} - {1} ({2}) ({3})".format(number_parser(int(float(row[i]["salary_from"]))),
                                                               number_parser(int(float(row[i]["salary_to"]))),
                                                               row[i]["salary_currency"],
                                                               tax_parser(row[i]["salary_gross"]))
        del row[i]["salary_to"], row[i]["salary_currency"],row[i]["salary_gross"]
        row[i]["key_skills"] = row[i]["key_skills"].replace(", ", "\n")
    return row
def filtring(lst, filter, head,reverse_head):
    result_lst = lst
    if len(filter) == 1 and not filter[0]:
        return lst
    if len(filter) == 1 and isinstance(filter[0], str):
        print("Формат ввода некорректен таблицу не печатать")
        return
    if reverse_head[filter[0]] not in head.keys():
        print("Параметр поиска некорректен таблицу не печатать")
        return
    if filter[0] != "Навыки" and filter[0] != "Идентификатор валюты оклада" and filter[0] != "Оклад":
        result_lst = [i for i in result_lst if i[reverse_head[filter[0]]] == filter[1]]
    else:
        for i in range(len(lst)):
            if filter[0] == "Навыки":
                temp_skills = filter[1].split(", ")
                temp_item_list = lst[i][reverse_head[filter[0]]].split("\n")
                flag = True
                for item in temp_skills:
                    if item not in temp_item_list:
                        flag = False
                if not flag:
                    lst[i][reverse_head[filter[0]]] = "Null"
            if filter[0] == "Идентификатор валюты оклада":
                if filter[1] not in lst[i][reverse_head[filter[0]]]:
                    lst[i][reverse_head[filter[0]]] = "Null"
            if filter[0] == "Оклад":
                temp_num = int(filter[1])
                temp_item_list = ''.join(lst[i][reverse_head[filter[0]]].split())
                temp_item_list = re.split(r'\W+', temp_item_list)
                if not(int(temp_item_list[0]) <= temp_num <= int(temp_item_list[1])):
                    lst[i][reverse_head[filter[0]]] = "Null"
        result_lst = [i for i in result_lst if i[reverse_head[filter[0]]] != "Null"]
    if len(result_lst) == 0:
        print("Ничего не найдено таблицу не печатать")
    else: return result_lst
def print_vacancies(data_vacancies, dic_naming):
    data_vacancies = formatter(data_vacancies)
    for i in range(len(data_vacancies)):
        for key, item in data_vacancies[i].items():
            print(dic_naming[key] + ": " + item)
        if (i < len(output_dict) - 1): print()
def print_table(table,count_of_rows,names_of_columns):
    def adding_num_to_columns(lst):
        lst.reverse()
        lst.append("№")
        lst.reverse()
        return lst
    if len(count_of_rows) == 1 and not str.isdecimal(count_of_rows[0]):
        if len(names_of_columns) == 1 and not names_of_columns[0]:
            return table.get_string()
        else: return table.get_string(fields = adding_num_to_columns(names_of_columns))
    if len(count_of_rows) == 1:
        return table.get_string(start=int(count_of_rows[0]) - 1, fields=adding_num_to_columns(names_of_columns))
    if len(names_of_columns) == 1 and not names_of_columns[0]:
        return table.get_string(start=int(count_of_rows[0]) - 1, end=int(count_of_rows[1]) - 1)
    return table.get_string(start=int(count_of_rows[0]) - 1, end=int(count_of_rows[1]) - 1, fields=adding_num_to_columns(names_of_columns))



head_first = ["name","description","key_skills","experience_id","premium","employer_name"
    ,"salary_from","salary_to","salary_gross","salary_currency","area_name","published_at"]
head = {"name":"Название", "description": "Описание","key_skills": "Навыки",
        "experience_id": "Опыт работы","premium": "Премиум-вакансия",
        "employer_name": "Компания","salary_from": "Оклад",
        "salary_to": "Верхняя граница вилки оклада","salary_gross": "Оклад указан до вычета налогов",
        "salary_currency": "Идентификатор валюты оклада","area_name": "Название региона",
        "published_at":"Дата публикации вакансии"}
reverse_head = {"Название":"name","Описание": "description","Навыки":"key_skills",
        "Опыт работы":"experience_id","Премиум-вакансия":"premium",
        "Компания":"employer_name","Оклад":"salary_from",
        "Верхняя граница вилки оклада":"salary_to","Оклад указан до вычета налогов":"salary_gross",
        "Идентификатор валюты оклада":"salary_currency" ,"Название региона":"area_name",
        "Дата публикации вакансии":"published_at"}
head_list = ["№", "Название", "Описание","Навыки",
        "Опыт работы","Премиум-вакансия",
        "Компания","Оклад","Название региона",
        "Дата публикации вакансии"]
file_name = input()
if os.stat(file_name).st_size == 0:
    print("Пустой файл")
else:
    data_lines = csv_reader(file_name)
    if len(data_lines) == 0:
        print("Нет данных")
    else:
        names_of_filter = input().split(': ')
        count_of_rows = input().split(' ')
        names_of_columns = input().split(', ')
        output_dict = formatter(csv_filer(data_lines,head_first))
        output_dict = filtring(output_dict,names_of_filter,head,reverse_head)
        if (output_dict != None):
            lst = parse_into_list(output_dict)
            table = create_table(set_strings_size(lst),head_list)
            print(print_table(table,count_of_rows,names_of_columns))

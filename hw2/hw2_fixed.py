import csv
from collections import defaultdict
PRINT_HIERARCHY = 1
MAKE_REPORT = 2
MAKE_CSVREPORT = 3


def read_input() -> int:
    """Function prints the options and reads the number"""
    print('Добро пожаловать в разбор csv файла!')
    print('Чтобы увидеть иерархию команд, введите 1')
    print('Чтобы увидеть сводный отчет, введите 2')
    print('Чтобы сохранить сводный отчет в csv файл, введите 3')
    val = ''
    options = [PRINT_HIERARCHY, MAKE_REPORT, MAKE_CSVREPORT]
    while val not in options:
        print('Введите корректное число: ')
        val = int(input())
    return val


def dict_opener() -> dict:
    """Function opens csv file and forms a dictionary with values from
        header as keys
        {'ФИО':['ФИО1','ФИО2',...],'Департамент':['Депт1',...],...}"""
    file_dict = defaultdict(list)
    with open('Corp_Summary.csv', newline='', encoding='UTF8') as csvfile:
        file = csv.DictReader(csvfile, delimiter=';')
        for row in file:
            for key, val in row.items():
                file_dict[key].append(val)
    return file_dict


def depts_selection(file_dict: dict) -> list:
    """Function picks out departments and forms them into a list"""
    depts = file_dict['Департамент']
    depts = list(set(depts))
    depts.sort()
    return depts


def teams_selection(file_dict: dict) -> dict:
    """Function assigns team to its department and forms a dictionary
        {'Dept1':['Team1', 'Team2',...], 'Dept2': [],...}"""
    depts = depts_selection(file_dict)
    dept_teams = {i: [] for i in depts}
    for i in range(0, len(file_dict['Департамент'])):
        dept = file_dict['Департамент'][i]
        team = file_dict['Отдел'][i]
        if team not in dept_teams[dept]:
            dept_teams[dept].append(team)
    return dept_teams


def report_maker(file_dict: dict) -> dict:
    """Function counts number of employees and their payments for each
        department and forms a dictionary {'Dept1':[num, min, avg, max]
        ,'Dept2': [],...}"""
    depts = depts_selection(file_dict)
    report = {i: [0, float('inf'), 0, 0] for i in depts}
    for i in range(0, len(file_dict['Департамент'])):
        dept = file_dict['Департамент'][i]
        report[dept][0] += 1
        pay = int(file_dict['Оклад'][i])
        if pay < report[dept][1]:
            report[dept][1] = pay
        elif pay > report[dept][3]:
            report[dept][3] = pay
        report[dept][2] += pay
    for dept in report:
        report[dept][2] = report[dept][2] // report[dept][0]
    return report


def option_1(file_dict: dict):
    """Function lists out departments and their teams"""
    hierarchy = teams_selection(file_dict)
    for dept in hierarchy:
        print(dept, end=': ')
        i = 0
        for i in range(0, len(hierarchy[dept]) - 1):
            print(hierarchy[dept][i], end=', ')
        print(hierarchy[dept][i + 1])
    return


def option_2(file_dict: dict):
    """Function makes report dictionary into a table"""
    report = report_maker(file_dict)
    print("{:^15} {:^15} {:^10} {:^10}"
          " {:^10}".format('Департамент', 'Численность', 'Минимум',
                           'Средняя', 'Максимум'))
    for dept in report:
        print("{:^15} {:^15} {:^10}"
              " {:^10} {:^10}".format(dept, report[dept][0], report[dept][1],
                                      report[dept][2], report[dept][3]))
    return


def option_3(file_dict: dict):
    """Function creates csv file from a dictionary"""
    report = report_maker(file_dict)
    header = ['Департамент', 'Численность', 'Минимум',
              'Средняя', 'Максимум']
    data = []
    for dept in report:
        report[dept].insert(0, dept)
        data.append(report[dept])
    with open('Report.csv', 'w+', encoding='UTF8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(header)
        writer.writerows(data)
    return


def choice(inp_num: int):
    """Function gets input value and
        runs 1 of 3 functions above depending on the input"""
    file_dict = dict_opener()
    if inp_num == PRINT_HIERARCHY:
        option_1(file_dict)
    elif inp_num == MAKE_REPORT:
        option_2(file_dict)
    else:
        option_3(file_dict)
    return


if __name__ == '__main__':
    choice(read_input())

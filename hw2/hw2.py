import csv


def read_input() -> int:
    """Function prints the options and reads the number"""
    print('Добро пожаловать в разбор csv файла!')
    print('Чтобы увидеть иерархию команд, введите 1')
    print('Чтобы увидеть сводный отчет, введите 2')
    print('Чтобы сохранить сводный отчет в csv файл, введите 3')
    val = ''
    options = [1, 2, 3]
    while val not in options:
        print('Введите корректное число: ')
        val = int(input())
    return val


def opener() -> iter:
    """Function opens initial csv file"""
    csvfile = open('Corp_Summary.csv', newline='', encoding='UTF8')
    file = csv.reader(csvfile, delimiter=';')
    return file


def depts_selection(file: iter) -> list:
    """Function picks out departments and forms them into a list"""
    depts = []
    next(file)
    for row in file:
        if row[1] not in depts:
            depts.append(row[1])
    return depts


def teams_selection(file: iter) -> dict:
    """Function assigns team to its department and forms a dictionary
        {'Dept1':['Team1', 'Team2',...], 'Dept2': [],...}"""
    depts = depts_selection(opener())
    next(file)
    dept_teams = {i: [] for i in depts}
    for row in file:
        if row[2] not in dept_teams[row[1]]:
            dept_teams[row[1]].append(row[2])
    return dept_teams


def report_maker(file: iter) -> dict:
    """Function counts number of employees and their payments for each
        department and forms a dictionary {'Dept1':[num, min, avg, max]
        ,'Dept2': [],...}"""
    depts = depts_selection(opener())
    next(file)
    report = {i: [0, float('inf'), 0, 0] for i in depts}
    for row in file:
        report[row[1]][0] += 1
        pay = int(row[5])
        if pay < report[row[1]][1]:
            report[row[1]][1] = pay
        elif pay > report[row[1]][3]:
            report[row[1]][3] = pay
        report[row[1]][2] += pay
    for dept in report:
        report[dept][2] = int(report[dept][2] / report[dept][0])
    return report


def option_1():
    """Function lists out departments and their teams"""
    hierarchy = teams_selection(opener())
    for dept in hierarchy:
        print(f'Департамент: {dept}')
        print('Команды:')
        for i in range(0, len(hierarchy[dept])):
            print(f'        {hierarchy[dept][i]}')
    return


def option_2():
    """Function makes report dictionary into a table"""
    report = report_maker(opener())
    print("{:^15} {:^15} {:^10} {:^10}"
          " {:^10}".format('Департамент', 'Численность', 'Минимум',
                           'Средняя', 'Максимум'))
    for dept in report:
        print("{:^15} {:^15} {:^10}"
              " {:^10} {:^10}".format(dept, report[dept][0], report[dept][1],
                                      report[dept][2], report[dept][3]))
    return


def option_3():
    """Function creates csv file from a dictionary"""
    report = report_maker(opener())
    header = ['Департамент', 'Численность', 'Минимум',
              'Средняя', 'Максимум']
    data = []
    for dept in report:
        report[dept].insert(0, dept)
        data.append(report[dept])
    file = open('Report.csv', 'w+', encoding='UTF8', newline='')
    writer = csv.writer(file, delimiter=';')
    writer.writerow(header)
    writer.writerows(data)
    return


def choice(inp_num: int):
    """Function runs 1 of 3 functions above depending on the input"""
    if inp_num == 1:
        option_1()
    elif inp_num == 2:
        option_2()
    else:
        option_3()
    return


if __name__ == '__main__':
    choice(read_input())

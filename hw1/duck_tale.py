def step1():
    print(
        'Утка-маляр 🦆 решила выпить зайти в бар. '
        'Взять ей зонтик? ☂️'
    )
    option = ''
    options = {'да': True, 'нет': False}
    while option not in options:
        print('Выберите: {}/{}'.format(*options))
        option = input()

    if options[option]:
        return step2_umbrella()
    return step2_no_umbrella()


def step2_umbrella():
    print('У утки есть зонты нескольких размеров. '
          'Нужно определиться, какой подойдет в этот раз?')
    size = ''
    sizes = ['маленький', 'средний', 'большой']
    while size not in sizes:
        print('Выберите: {}/{}/{}'.format(*sizes))
        size = input()
    print('А также они есть в разных цветах. Какой предпочтительнее?')
    color = ''
    colors = ['желтый', 'черный', 'белый', 'красный']
    while color not in colors:
        print('Выберите: {}/{}/{}/{}'.format(*colors))
        color = input()
    choice = ' '.join([size, color])
    print(f'{choice} зонтик, отличный выбор!')
    return step3_positive()


def step2_no_umbrella():
    print('Не брать зонтик - большой риск. '
          'Может быть, стоит хотя бы взять дождевик?')
    option = ''
    options = {'да': True, 'нет': False}
    while option not in options:
        print('Выберите: {}/{}'.format(*options))
        option = input()

    if options[option]:
        return step3_positive()
    return step3_negative()


def step3_positive():
    print('Благодаря Вашим решениям Утка-маляр добралась до бара 🍻')
    return


def step3_negative():
    print('К сожалению, дождь оказался настолько сильным, что '
          'утке-маляру пришлось вернуться домой и пить в одиночестве 😞')
    return


if __name__ == '__main__':
    step1()

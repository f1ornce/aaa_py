class Pokemon:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return f'{self.name}/{self.type}'


if __name__ == '__main__':
    bulbasaur = Pokemon(name='Bulbasaur', type='grass')
    print(bulbasaur)

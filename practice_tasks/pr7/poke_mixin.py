class BasePokemon:
    def __init__(self, name, category):
        self.name = name
        self.category = category

    def __str__(self):
        return f'{self.name}/{self.category}'


class EmojiMixin:
    icons = {
        'grass': '🌿',
        'electric': '⚡',
        'fire': '🔥',
        'water': '🌊'
    }

    def __str__(self):
        text = super().__str__()
        for desc, emoji in self.icons.items():
            replaced = text.replace(desc, emoji)
            if replaced != text:
                return replaced
        return text


class Pokemon(EmojiMixin, BasePokemon):
    pass


if __name__ == '__main__':
    pikachu = Pokemon(name='Pikachu', category='electric')
    print(pikachu)

END = '\033[0'
START = '\033[1;38;2'
MOD = 'm'


class Color:
    def __init__(self, red_level, green_level, blue_level):
        self.red_level = red_level
        self.green_level = green_level
        self.blue_level = blue_level

    def __str__(self):
        return f'{START};{self.red_level};{self.green_level};' \
               f'{self.blue_level}{MOD}●{END}{MOD}'

    def __eq__(self, other):
        s = (self.red_level, self.green_level, self.blue_level)
        o = (other.red_level, other.green_level, other.blue_level)
        return s == o

    def __add__(self, other):
        sum_red = min(self.red_level + other.red_level, 255)
        sum_green = min(self.green_level + other.green_level, 255)
        sum_blue = min(self.blue_level + other.blue_level, 255)
        return Color(sum_red, sum_green, sum_blue)

    def __mul__(self, c):
        cl = -256 * (1 - c)
        f = (259 * (cl + 255)) / (255 * (259 - cl))
        l_red = int(f * (self.red_level - 128) + 128)
        l_green = int(f * (self.green_level - 128) + 128)
        l_blue = int(f * (self.blue_level - 128) + 128)
        return Color(l_red, l_green, l_blue)

    def __rmul__(self, c):
        return self * c

    def __hash__(self):
        s = (self.red_level, self.green_level, self.blue_level)
        return hash(s)


if __name__ == '__main__':
    red = Color(255, 0, 0)
    print(0.5 * red)

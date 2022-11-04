import json
import os.path
import keyword
from typing import Dict, Union


class JsonParser:
    @staticmethod
    def parse(value: Union[Dict, str]):
        if isinstance(value, dict):
            return JsonParser.from_dict(value)
        elif isinstance(value, str):
            if os.path.isfile(value):
                return JsonParser.from_file(value)
            else:
                return JsonParser.from_string(value)
        else:
            raise TypeError(f"unknown input value type: {type(value)}")

    @staticmethod
    def from_file(filepath: str, encoding='utf-8') -> dict:
        with open(filepath, 'r', encoding=encoding) as f:
            data_dict = json.load(f)
        return data_dict

    @staticmethod
    def from_string(s: str) -> dict:
        return json.loads(s)

    @staticmethod
    def from_dict(d: Dict) -> dict:
        return d


class DefaultAttributer:
    def __getattribute__(self, attr):
        try:
            value = super().__getattribute__(attr)
        except AttributeError:
            value = None
        return value

    def __setattr__(self, attr, value):
        if keyword.iskeyword(attr):
            attr = f"{attr}_"
        __dict__ = super().__getattribute__("__dict__")
        __dict__[attr] = value


class DefaultStructure(DefaultAttributer):
    def __init__(self, data_dict=None):
        if data_dict:
            for key, value in data_dict.items():
                if isinstance(value, dict):
                    self.__setattr__(key, DefaultStructure(value))
                else:
                    self.__setattr__(key, value)


class AdvertStructure(DefaultStructure):
    def __init__(self, data_feed):
        data_dict = JsonParser().parse(data_feed)
        print(data_dict)
        super().__init__(data_dict)
        if self.title is None:
            raise AttributeError("'title' was not provided")

    def __getattribute__(self, attr):
        value = super().__getattribute__(attr)
        if attr == "price":
            return self._check_price(value, mode='get')
        return value

    def __setattr__(self, attr, value):
        if attr == "price":
            value = self._check_price(value, mode='set')
        super().__setattr__(attr, value)

    @staticmethod
    def _check_price(price, mode='get'):
        price = price or 0
        if mode == 'set':
            if price < 0:
                raise ValueError(f"price must be >= 0")
        return price

    def __repr__(self):
        return f'{self.title} | {self.price} ₽'


class ColorizeMixin:
    repr_color_code = 33

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        return f'\033[1;{self.repr_color_code};2m{super().__repr__()}'


class Advert(ColorizeMixin, AdvertStructure):
    def __init__(self, data_feed):
        super().__init__(data_feed)


JSON_FILEPATH = "./ads1.json"
DATA_DICT = {
    "title": "Вельш-корги",
    "price": 1000,
    "class": "dogs",
    "location": {
        "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
        }
    }
DATA_STR = '''{
    "title": "Вельш-корги",
    "price": 1000,
    "class": "dogs",
    "location": {
        "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
        }
    }'''

if __name__ == '__main__':
    a = Advert(JSON_FILEPATH)
    print(a.title)
    print(a.price)
    print(a.location.address)
    print(a.location.metro_stations)
    print(a.class_)
    print(a)

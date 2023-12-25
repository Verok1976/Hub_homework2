from datetime import datetime
import json
from item import Item, item_object_hook
import utils


# ---------------------------------------------------
# function of transformation Hub from json data
# ---------------------------------------------------
def transform_hub_json_data(json_data):
    hub_res = Hub()
    hub_res.clear()
    print(json_data)
    for i in json_data.get('_items'):
        hub_res.add_item(item_object_hook(i))
    hub_res.date = datetime.fromisoformat(json_data.get('_date'))
    return hub_res


# ---------------------------------------------------
# singleton, class object Hub
# ---------------------------------------------------
class Hub:
    _instance = None

    def __new__(cls, dt: datetime = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, dt: datetime = None):
        self._items = []
        self._date = dt

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError("Index should be integer")

        if 0 <= item < len(self._items):
            return self._items[item]
        else:
            raise IndexError("Incorrect index")

    # ---------------------------------------------------
    # method, which add new Item to items list
    # ---------------------------------------------------
    def add_item(self, item: Item):
        if self._items is None:
            self._items = []
        self._items.append(item)

    # ---------------------------------------------------
    # list of Items, property
    # ---------------------------------------------------
    @property
    def items(self):
        # print("Getting value...")
        return self._items

    # ---------------------------------------------------
    # date, property
    # ---------------------------------------------------
    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    # ---------------------------------------------------
    # метод, который возвращает (pos, item) предмета с id если он есть в Hib, и (-1, None) если его нет.
    # ---------------------------------------------------
    def find_by_id(self, id):

        if not isinstance(id, int):
            raise TypeError("Id should be integer")

        for value in self.items:
            if value.id == id:
                return (self._items.index(value), value)
        return (-1, None)

    # ---------------------------------------------------
    # метод, который возвращает контейнер, который содержит все предметы из items
    # у который есть ВСЕ теги из tags
    # ---------------------------------------------------
    def find_by_tags(self, tag):
        lst: list[Item] = []
        for value in self._items:
            if value.is_tagged(tag):
                lst.append(value)
        return lst

    # ---------------------------------------------------
    # метод, который возвращает лист предметов, соответствующих дате/периоду дат
    # ---------------------------------------------------
    def find_by_date(self, *dates):
        try:
            lst: list[Item] = []
            date_to = None
            date_from = None
            if 2 < len(dates) < 1:
                raise ValueError("Count of arguments should be 1 or 2")
            for i in range(len(dates)):
                if i == 0:
                    date_from = dates[i]
                else:
                    date_to = dates[i]

            for value in self._items:
                dt = value.dispatch_time

                if (utils.diff_days(dt, date_from) <= 0 and date_to is None) or (
                        date_to is not None and utils.diff_days(dt, date_to) <= 0 <= utils.diff_days(dt, date_from)):
                    lst.append(value)

            return lst
        except Exception as err:
            print(f"Error {err=}, {type(err)=}")
            raise

    # ---------------------------------------------------
    # метод, возвращает первые amount самых дорогих предметов на складе.
    # Если предметов на складе меньше чем amount - возвращает их все
    # ---------------------------------------------------
    def find_most_valuable(self, amount):
        try:
            lst = sorted(self.items, reverse=True)
            return lst[0:amount]
        except Exception as err:
            print(f"Error {err=}, {type(err)=}")
            raise

    # ---------------------------------------------------
    # метод, удаляет или item или Item по индексу
    # ---------------------------------------------------
    def rm_item(self, i):
        try:
            if isinstance(i, Item):
                self._items.remove(i)
            else:
                for item in self._items:
                    if item.id == i:
                        self._items.remove(i)
        except ValueError:
            print("Item is not defined")

    # ---------------------------------------------------
    # метод, удаляет items из переданного списка
    # ---------------------------------------------------
    def drop_items(self, items):
        try:
            for i in self._items:
                if i in items:
                    self._items.remove(i)
        except ValueError:
            print("Item is not found!")

    def __repr__(self):
        res = self.__class__.__name__
        a = self._items
        for value in list(a)[:3]:
            res += ("\n" if res else "") + str(value)
        return res

    def __str__(self):
        return f'Hub({self._date},{self._items})'

    def __len__(self):
        return len(self._items)

    def clear(self):
        self._items.clear()

    # ---------------------------------------------------
    # метод, dumps to json
    # ---------------------------------------------------
    def to_json(self):
        return json.dumps(self, default=utils.json_default, ensure_ascii=False)

    # ---------------------------------------------------
    # метод, save to json
    # ---------------------------------------------------
    def save_as_json(self):
        try:
            with open("hub.json", "w", encoding="utf-8") as write_file:
                json.dump(self.to_json(), write_file)
        except Exception as err:
            print(f"Error {err=}, {type(err)=}")
            raise


    @staticmethod
    def read_from_json(json_path):
        try:
            with open(json_path, "r") as jsonfile:
                json_str = json.load(jsonfile)
                json_data = json.loads(json_str)
                return transform_hub_json_data(json_data)
        except OSError as err:
            print("OS error:", err)
        except ValueError as err:
            print("Incorrect data: ", err)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise


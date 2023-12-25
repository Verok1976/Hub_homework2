import json
from datetime import datetime
from typing import List, Any

from utils import json_default


def generate():
    x = 0
    while True:
        x = x + 1
        yield x


# ---------------------------------------------------
# метод, конвертация json в объект Item
# ---------------------------------------------------
def item_object_hook(json_data):
    try:
        item_res = Item(
            json_data.get('_name'),
            json_data.get('_description'),
            datetime.fromisoformat(json_data.get('_dispatch_time')),
            json_data.get('_cost'),
            json_data.get('_tags'),
        )
        item_res.id = json_data.get('_id')
        return item_res
    except Exception as err:
        print(f"Error {err=}, {type(err)=}")
        raise


# ---------------------------------------------------
# метод, create from json
# ---------------------------------------------------
def create_from_json(json_path):
    try:
        with open(json_path, "r") as jsonfile:
            json_str = json.load(jsonfile)
            json_data = json.loads(json_str, object_hook=item_object_hook)
            return json_data
    except Exception as err:
        print(f"Error {err=}, {type(err)=}")
        raise


class Item:
    g = generate()

    _items: list[Any] = []

    def __init__(self, name, description, dispatch_time, cost=0, tags: list = None):
        self._tags = tags
        if self._tags is None:
            self._tags = []
        self._id = next(self.g)  # id(self)
        self._name = name
        self._description = description
        self._dispatch_time = dispatch_time
        self._cost = cost
        while len(self._items) < self._id:
            self._items.append(None)
            self._items.insert(self._id, self)

    def __repr__(self):
        try:
            res = self.__class__.__name__ + f'Item({self._id}) tags: '
            a = self._tags
            for value in list(a)[:3]:
                res += ("\n" if res else "") + str(value)
            return res
        except Exception as err:
            print(f"Error {err=}, {type(err)=}")
            raise

    def __str__(self):
        return f'Item({self._id},{self._name},{self._description},{self._dispatch_time},{self._cost},{self._tags})'

    def __getitem__(self, tag):
        if not isinstance(tag, int):
            raise TypeError("Index should be integer")

        if 0 <= tag < len(self._tags):
            return self._tags[tag]
        else:
            raise IndexError("Incorrect index")

    @property
    def tags(self) -> list:
        return self._tags

    @tags.setter
    def tags(self, value: list):
        self._tags = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def dispatch_time(self):
        return self._dispatch_time

    @dispatch_time.setter
    def dispatch_time(self, value):
        self._dispatch_time = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        self._cost = value

    # ---------------------------------------------------
    # метод, добавляем tag в список
    # ---------------------------------------------------
    def add_tags(self, tag):
        try:
            if type(tag) is list:
                lst = tag
            else:
                lst = [tag]
            self._tags = self._tags + lst
        except Exception as err:
            print(f"Error {err=}, {type(err)=}")
            raise

    # ---------------------------------------------------
    # метод, удаляем tag из списка
    # ---------------------------------------------------
    def rm_tag(self, tag):
        try:
            if type(tag) is list:
                lst = tag
            else:
                lst = [tag]
            for i in self._tags:
                if i in lst:
                    self._tags.remove(i)
        except Exception as err:
            print(f"Error {err=}, {type(err)=}")
            raise

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def __len__(self):
        if self._tags is None:
            return 0
        return len(list(set(self._tags)))

    def __hash__(self):
        return hash((self.id))

    # ---------------------------------------------------
    # метод, определяем, есть ли tag из параметров в списке tags
    # ---------------------------------------------------
    def is_tagged(self, tag):
        try:
            if type(tag) is list:
                lst = tag
            else:
                lst = [tag]
            lst = list(filter(lambda x: x not in self._tags, lst))
            return 0 == len(lst)
        except Exception as err:
            print(f"Error {err=}, {type(err)=}")
            raise

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        if isinstance(other, Item):
            return (self.name == other.name and other.tags == self.tags
                    and (self.dispatch_time - other.dispatch_time).seconds == 0
                    and self._description == other._description
                    and self.cost == other.cost)
        return False

    def copy(self):
        return type(self)(self._name, self._description, self._dispatch_time, self._cost, self._tags)

    # ---------------------------------------------------
    # метод, save to json
    # ---------------------------------------------------
    def to_json(self):
        try:
            return json.dumps(self, default=json_default, ensure_ascii=False)
        except Exception as err:
            print(f"Error {err=}, {type(err)=}")
            raise

    def save_as_json(self):
        try:
            with open("item.json", "w", encoding="utf-8") as write_file:
                json.dump(self.to_json(), write_file)
        except Exception as err:
            print(f"Error {err=}, {type(err)=}")
            raise

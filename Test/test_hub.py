import unittest
from datetime import datetime, timedelta
from random import random
from random import choice

from hub import Hub
from item import Item


# ---------------------------------------------------
# метод, для генерации Item
# ---------------------------------------------------
def generate_item():
    i = 0
    tag = ['tg_test']
    letter_list = ['A','a','b','B','c','C', 'd', 'D']
    while True:
        tag.append('tag' + str(i))
        if i % 2 == 0:
            dt = datetime.now() - timedelta(i * 3)
        else:
            dt = datetime.now() + timedelta(i * 3)
        s = choice(letter_list)
        item = Item(s + 'Ручка' + str(i), 'поступила ' + dt.strftime("%d/%m/%Y"), dt, round(random() * 1000, 2), tag.copy())
        item.add_tags(['id_tag' + str(item.id)])
        # print(item)
        i = i + 1
        yield item


class TestHub(unittest.TestCase):
    h = Hub()
    gi = generate_item()

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.count_items = 15

    def setUp(self):
        h = Hub()
        h.clear()
        count_items = 15
        h.date = datetime.now()
        i=0
        for i in range(count_items):
            self.h.add_item(next(self.gi))

    def tearDown(self):
        self.h.clear()

    # 'Проверка того что hub - синглтон'
    def test_hub_singleton(self):
        self.assertTrue(Hub() is Hub())

    # 'Проверка того что hub - синглтон'
    def test_hub_json(self):
        s: str = str(self.h)
        self.h.save_as_json()
        self.h.read_from_json("hub.json")
        s1: str = str(self.h)
        self.assertEqual(s, s1)

    # 'Проверка того что при добавлении предметов меняется значение len(item)'
    def test_len(self):
        self.assertEqual(len(self.h), self.count_items)

    # 'Проверка того что при поиске возвращается нужный объект'
    def test_find_by_id(self):

        self.assertEqual(self.h.find_by_id(self.h.items[0].id), (0, self.h.items[0]))
        self.assertEqual(self.h.find_by_id(250), (-1, None))

    # 'Проверка метода, который возвращает заданное количество самых дорогих товаров'
    def test_find_most_valuable(self):
        lst = []
        lst = sorted(self.h.items, reverse=True)
        self.assertEqual(self.h.find_most_valuable(5), lst[0:5])

    # 'Проверка того что при поиске по tag возвращается нужный объект'
    def test_find_by_tag(self):
        tag0 = ['tg_test']
        self.assertEqual(self.h.find_by_tags(tag0), self.h.items)
        self.assertEqual(self.h.find_by_tags(['id_tag' + str(self.h.items[len(self.h) - 1].id)]),
                         [self.h.items[len(self.h) - 1]])

    # Проверка того, что корректно работает поиск по датам
    def test_find_by_date(self, *args):
        self.assertEqual(self.h.find_by_date(datetime.now() - timedelta(3), datetime.now() + timedelta(1)),
                         [self.h.items[0]])
        dt = datetime.now() + timedelta(self.count_items * 3)
        self.assertEqual(self.h.find_by_date(dt),
                         self.h.items)

    if __name__ == '__main__':
        unittest.main(argv=['first-arg-is-ignored'], exit=False)

from datetime import datetime
from random import random
from random import choice
from item import Item, create_from_json

import unittest


class TestItem(unittest.TestCase):
    tags = []
    tags1 = []
    tags2 = []
    item1 = None
    item2 = None
    tags3 = []

    def setUp(self):
        tags_templates = ['новый', 'хороший', 'последний', 'высокий', 'русский', 'общий', 'главный', 'государственный',
                          'маленький',
                          'любой', 'полный', 'молодой', 'советский', 'разный', 'настоящий', 'всякий', 'военный', 'иной',
                          'нужный',
                          'нормальный', 'боевой', 'прямой', 'конкретный', 'любимый', 'уверенный', 'худой', 'пустой',
                          'очередной',
                          'городской', 'зеленый', 'западный', 'быстрый', 'дальнейший', 'золотой', 'знаменитый', 'тихий',
                          'иностранный',
                          'открытый', 'частый', 'родной', 'точный', 'центральный', 'немецкий', 'соответствующий',
                          'значительный',
                          'левый', 'информационный', 'холодный', 'слабый', 'тонкий', 'мелкий', 'немой', 'счастливый',
                          'европейский',
                          'частный', 'будущий', 'отечественный', 'физический', 'профессиональный', 'крайний',
                          'естественный',
                          'духовный',
                          'популярный', 'независимый', 'случайный', 'видный', 'аналогичный', 'честный', 'уникальный',
                          'муниципальный',
                          'одинаковый', 'меньший', 'бюджетный', 'телефонный', 'четкий', 'надежный', 'непонятный',
                          'японский',
                          'церковный', 'стратегический', 'мирный', 'тайный', 'верховный', 'очевидный', 'нежный',
                          'химический',
                          'чеченский', 'скромный', 'отличный', 'еврейский', 'демократический', 'раненый', 'законный',
                          'талантливый',
                          'рыночный', 'направленный', 'ядерный', 'густой', 'громкий', 'максимальный', 'действующий',
                          'самостоятельный',
                          'бесконечный', 'хозяйственный', 'прозрачный', 'ужасный', 'старинный', 'зимний', 'рыжий',
                          'текущий',
                          'вынужденный', 'неприятный', 'рекламный', 'статистический', 'экологический', 'пожилой',
                          'особенный',
                          'ответственный', 'закрытый', 'заметный', 'заинтересованный', 'нервный', 'незнакомый',
                          'противоположный',
                          'нравственный', 'одинокий', 'электрический', 'интеллектуальный', 'президентский', 'уважаемый',
                          'абсолютный']
        number = 0
        count = round(random() * 10, 0) + 2
        while number < count:
            number += 1
            self.tags.append(choice(tags_templates))

        number = 0
        count = round(random() * 10) + 2
        while number < count:
            number += 1
            self.tags1.append(choice(tags_templates))

        number = 0
        count = len(self.tags2) - 1
        while number < count:
            number += 1
            self.tags2.append(random.choice(self.tags1))

        self.tags3 = ['test3', 'test4']

        self.item1 = Item('Ручка1', 'поступила 23.08', datetime.now(), 5, self.tags.copy())
        self.item2 = Item('Ручка2', 'поступила 23.08', datetime.now(), 15, self.tags1.copy())

    def tearDown(self):
        self.tags = []
        self.tags1 = []
        self.tags2 = []
        self.item1 = None
        self.item2 = None
        self.tags3 = []

    # 'Проверка того что у разных self.items разные id'
    def test_item_id(self):
        self.assertNotEqual(self.item1.id, self.item2.id, 'item не создаёт разные id')

        # 'Проверка того что у разных self.items разные id'

    def test_item_json(self):

        self.item1.save_as_json()
        item_res1 = create_from_json("item.json")
        self.assertEqual(self.item1, item_res1, 'items is not equals')

    # 'Проверка того что при добавлении тэгов меняется значение len(self.item)'
    def test_len(self):
        len1 = len(self.item1)
        self.item1.add_tags('Test')
        len2 = len(self.item1)
        self.assertNotEqual(len1, len2, 'Длина листа не изменилась. Было ' + str(len1) + ', стало ' + str(len2))

    def test_add_tags(self):
        ln = len(self.item1.tags)
        self.item1.add_tags('add_tag_1')
        self.assertNotEqual(ln, len(self.item1.tags), 'Тэг не был добавлен')
        ln = len(self.item1.tags)
        self.item1.add_tags(['add_tag_2', 'add_tag_3'])
        self.assertNotEqual(ln, len(self.item1.tags), 'Тэги не были добавлены')

    def test_items(self):
        self.assertEqual(Item._items[1].id, 1)
        self.assertEqual(Item._items[3].id, 3)

    # 'Проверка того что если к предмету добавить два идентичных тега - их колчество будет один'
    def test_equal_tags(self):
        len1 = len(self.item1)
        self.item1.add_tags(self.item1.tags[1])
        len2 = len(self.item1)
        self.assertEqual(len1, len2, 'Длина листа изменилась. Было ' + str(len1) + ', стало ' + str(len2))

    # 'Проверка на наличие тегов из списка или просто в self.item'
    def test_isTagged(self):
        tag = choice(self.item2.tags)
        self.assertEqual(self.item2.is_tagged(self.tags2), True, 'Тэги не найдены!')
        self.assertEqual(self.item2.is_tagged(self.tags3), False, 'Тэги найдены! ')
        self.assertEqual(self.item2.is_tagged(tag), True, 'Тэги не найдены!')

    def test_Copy(self):
        item_c = self.item1.copy()
        self.assertEqual(item_c, self.item1)


# Проверим работоспособность
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

# This is a sample Python script.
import unittest
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from datetime import datetime

from Test.test_hub import generate_item
from hub import Hub


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    h = Hub(dt=datetime.now())
    g = generate_item()
    h.clear()
    a_list = []
    outdated_list = []
    most_valuable_list = []
    other_list = []
    count_items = 50
    i = 0
    for i in range(count_items):
        h.add_item(next(g))

    i = 0
    for i in range(count_items):
        if h.items[i].name.upper().find('A') == 0:
            a_list.append(h.items[i])

    outdated_list = h.find_by_date(h.date)
    most_valuable_list = h.find_most_valuable(10)
    lst = a_list + outdated_list + most_valuable_list
    other_list = list(filter(lambda x: x not in lst, h.items))

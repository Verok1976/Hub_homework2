import json
from datetime import datetime
from enum import Enum


# class syntax
class DatePart(Enum):
    DAY = 1
    MINUTE = 2
    SECOND = 3


def json_default(value):
    if isinstance(value, datetime):
        return value.isoformat()
    else:
        return value.__dict__


def diff_days(date1: datetime, date2: datetime, part: DatePart = DatePart.DAY) -> int:
    if part == DatePart.DAY:
        return (date1 - date2).days
    elif part == DatePart.MINUTE:
        return (date1 - date2).seconds * 60
    elif part == DatePart.SECOND:
        return (date1 - date2).seconds
    else:
        raise ValueError("Incorrect argument")

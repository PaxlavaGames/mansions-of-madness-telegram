import random
import json
import time
from django.db import models


sides = [
    'Empty',
    'Empty',
    'Empty',
    'Success',
    'Success',
    'Success',
    'Evidence',
    'Evidence',
]


def drop_cube():
    return random.choice(sides)


def drop_cubes(count):
    return [drop_cube() for _ in range(count)]


class Drop(models.Model):
    results = models.JSONField()
    create = models.DateTimeField(auto_now_add=True)


def save_statistic(results):
    json_results = json.dumps(results)
    Drop.objects.create(results=json_results)


def frequency():
    drops = Drop.objects.all()
    result = {}
    for drop in drops:
        results_list = drop.results
        cubes_count = len(results_list)
        if cubes_count in result:
            result[cubes_count] += 1
        else:
            result[cubes_count] = 1
    return result


def to_pictures(results, drop_format='one by one'):
    mapper = {
        'Success': '❤️',
        'Evidence': '🔍',
        'Empty': '👿',
    }
    mapped_list = [mapper[result] for result in results]
    if drop_format == 'one by one':
        return mapped_list

    def sort_function(result):
        sort_table = {
            '❤️': 1,
            '🔍': 2,
            '👿': 3,
        }
        return sort_table[result]
    mapped_list = sorted(mapped_list, key=sort_function)
    return [''.join(mapped_list)]



def make_delay():
    delay = random.uniform(0.2, 1.5)
    time.sleep(delay)


class Delay(models.Model):
    enabled = models.BooleanField(default=True)
    user_id = models.CharField(max_length=128)


def save_delay(enabled, user_id):
    Delay.objects.create(enabled=enabled, user_id=user_id)


def is_delay_enabled(user_id):
    delay = Delay.objects.filter(user_id=user_id).last()
    return delay.enabled if delay else True


class DropFormat(models.Model):
    # one by one, raw
    name = models.CharField(max_length=10)
    user_id = models.CharField(max_length=128)


def save_drop_format(name, user_id):
    DropFormat.objects.create(name=name, user_id=user_id)


def get_drop_format(user_id):
    drop_format = DropFormat.objects.filter(user_id=user_id).last()
    return drop_format.name if drop_format else 'one by one'


VARIANTY = {
    'Success': 3/8,
    'Evidence': 2/8,
    'Empty': 3/8,
}


def one_equity(results, name):
    total = len(results)
    count = results.count(name)
    expected = total * VARIANTY[name]
    difference = count - expected  # > 0 удача, < 0 неудача
    return expected, count, difference


def all_equity(results):
    drop_names = [
        'Success', 'Evidence', 'Empty'
    ]
    result = {}
    for name in drop_names:
        expected, count, difference = one_equity(results, name)
        result[name] = {
            'expected': expected,
            'count': count,
            'difference': difference,
        }
    return result


def date_equity(date):
    drops = Drop.objects.filter(
        create__day=date.day,
        create__month=date.month,
        create__year=date.year
    )
    results = []
    for drop in drops:
        results += drop.results
    equity = all_equity(results)
    return equity


def equity_to_str(equity):
    order_list = [
        'Success',
        'Evidence',
        'Empty',
    ]
    mapper = {
        'Success': '❤️',
        'Evidence': '🔍',
        'Empty': '👿',
    }
    result_rows = []
    for order_item in order_list:
        data = equity[order_item]
        row_str = (f'{mapper[order_item]}: '
                   f'факт - {data["count"]}, '
                   f'ожидание - {data["expected"]}, '
                   f'разница - {data["difference"]}')
        result_rows.append(row_str)
    result = '\n'.join(result_rows)
    return result

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

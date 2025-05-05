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


def to_pictures(results):
    mapper = {
        #'Success': '✅',
        'Success': '❤️',
        'Evidence': '🔍',
        # 'Empty': '💀',
        'Empty': '👿',
    }
    return [mapper[result] for result in results]


def make_delay():
    delay = random.uniform(0, 1)
    time.sleep(delay)

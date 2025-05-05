import random
import json
from django.test import TestCase, SimpleTestCase
from mainapp import models


class TestDropCube(SimpleTestCase):

    def setUp(self):
        self.expected = [
            'Empty',
            'Success',
            'Evidence',
        ]

    def test_drop_cube_variants(self):
        self.assertIn(models.drop_cube(), self.expected)

    def test_drop_cubes(self):
        count = random.randint(1, 10)
        results = models.drop_cubes(count)
        self.assertEqual(len(results), count)
        for result in results:
            self.assertIn(result, self.expected)


class TestSaveStatistic(TestCase):

    def test_save_statistic(self):
        drops_exists = models.Drop.objects.all().exists()
        self.assertFalse(drops_exists)
        results = [
            'Empty',
            'Evidence',
            'Evidence',
        ]
        models.save_statistic(results)
        drops_exists = models.Drop.objects.all().exists()
        self.assertTrue(drops_exists)
        last_result = models.Drop.objects.all().first()
        self.assertEqual(json.loads(last_result.results), results)

    def test_frequency(self):
        results = [
            [
                'Empty',
                'Evidence',
                'Evidence',
            ],
            [
                'Success',
            ],
            [
                'Empty',
            ]
        ]
        drops = []
        for result in results:
            drops.append(
                models.Drop(
                    results = result
                )
            )
        models.Drop.objects.bulk_create(drops)
        self.assertEqual(3, models.Drop.objects.count())

        expected_result = {
            1: 2,  # 1 кубик бросали 1 раз
            3: 1,  # 3 кубика бросали 1 раз
        }

        result = models.frequency()
        self.assertEqual(expected_result, result)

from datetime import date
import random
import json

from django.test import TestCase, SimpleTestCase
from mainapp import models
from mainapp.tests.data import EXPECTED_IDEAL


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


class TestUserSettings(TestCase):

    def test_save_delay(self):
        self.assertFalse(models.Delay.objects.all().exists())
        models.save_delay(False, 123)
        self.assertTrue(models.Delay.objects.all().exists())
        models.save_delay(True, 123)
        self.assertEqual(2, models.Delay.objects.count())

    def test_get_delay(self):
        self.assertTrue(models.is_delay_enabled(123))
        models.save_delay(False, 123)
        self.assertFalse(models.is_delay_enabled(123))
        models.save_delay(True, 123)
        self.assertTrue(models.is_delay_enabled(123))

    def test_save_drop_format(self):
        self.assertFalse(models.DropFormat.objects.all().exists())
        models.save_drop_format('raw', 123)
        self.assertTrue(models.DropFormat.objects.all().exists())
        models.save_drop_format('one by one', 123)
        self.assertEqual(2, models.DropFormat.objects.count())

    def test_get_drop_format(self):
        self.assertEqual('one by one', models.get_drop_format(123))
        models.save_drop_format('raw', 123)
        self.assertEqual('raw', models.get_drop_format(123))
        models.save_drop_format('one by one', 123)
        self.assertEqual('one by one', models.get_drop_format(123))


class TestEquity(TestCase):

    def setUp(self):
        self.some_date = date(
            year=2024,
            month=12,
            day=1,
        )
        self.expected_empty = {
            'Success': {
                'expected': 0.,
                'count': 0,
                'difference': 0.,
            },
            'Evidence': {
                'expected': 0.,
                'count': 0,
                'difference': 0.,
            },
            'Empty': {
                'expected': 0.,
                'count': 0,
                'difference': 0.,
            },
        }
        self.expected_ideal = EXPECTED_IDEAL
        self.ideal = [
            'Success',
            'Success',
            'Success',
            'Empty',
            'Empty',
            'Empty',
            'Evidence',
            'Evidence',
        ]

    def test_equity_empty(self):
        equity = models.all_equity([])
        self.assertEqual(self.expected_empty, equity)

    def test_all_equity_ideal(self):
        equity = models.all_equity(self.ideal)
        self.assertEqual(self.expected_ideal, equity)

    def test_date_equity_empty(self):
        equity = models.date_equity(self.some_date)
        self.assertEqual(self.expected_empty, equity)

    def test_date_equity_ideal(self):
        drop = models.Drop.objects.create(results=self.ideal)
        drop.create = self.some_date
        drop.save()
        equity = models.date_equity(self.some_date)
        self.assertEqual(self.expected_ideal, equity)

    def test_show_equity(self):
        expected_output = ('❤️: факт - 3, ожидание - 3.0, разница - 0.0\n'
                           '🔍: факт - 2, ожидание - 2.0, разница - 0.0\n'
                           '👿: факт - 3, ожидание - 3.0, разница - 0.0')
        self.assertEqual(expected_output, models.equity_to_str(self.expected_ideal))

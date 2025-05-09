from django import test
from mainapp import filters


class TestFilters(test.SimpleTestCase):

    def test_is_date(self):

        class Message:

            def __init__(self, text):
                self.text = text

        self.assertTrue(filters.is_date(Message('22.01.2024')))
        self.assertFalse(filters.is_date(Message('not date')))

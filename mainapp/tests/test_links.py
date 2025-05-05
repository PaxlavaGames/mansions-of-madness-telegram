from telegram_framework.test import TestCase
from mainapp import models


class TestCommands(TestCase):


    def test_introduction(self):
        """
        Test /start: success
        """
        chat = self.assertCommandWasHandled('/start', self.chat)
        self.assertChatLastMessageTextEqual(chat, '<b>Mansions of Madness</b> 👋')
        keyboard = self.assertChatKeyboardName(chat, 'menu_numbers')
        self.assertEqual(5, len(keyboard))


    def test_drop_cubes_action(self):
        """
        Test any text message (positive number): success
        """
        cubes_count = 2
        chat = self.assertTextMessageWasHandled(str(cubes_count), self.chat)
        self.assertChatMessagesCount(chat, cubes_count+1)
        # statistic
        self.assertEqual(1, models.Drop.objects.count())

    def test_drop_cubes_invalid_input(self):
        """
        Test any text message (invalid number): success
        """
        inputs = [
            'not number',
            '-1',
            '0',
            '100',
            '150',
        ]
        for text in inputs:
            with self.subTest(input):
                chat = self.assertTextMessageWasHandled(text, self.chat)
                self.assertChatLastMessageTextEqual(chat, 'Нужно ввести положительное число < 100')


    def test_statistics_action(self):
        """
        Test /statistics: success
        """
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
        chat = self.assertCommandWasHandled('/statistics', self.chat)
        expected_response = '1 - 2\n3 - 1'
        self.assertChatLastMessageTextEqual(chat, expected_response)

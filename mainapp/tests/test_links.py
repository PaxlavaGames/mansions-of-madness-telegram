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

    def test_drop_cubes_action_no_delay(self):
        """
        Test any text message (positive number): success, not delay
        """
        models.save_delay(False, self.client.id)
        cubes_count = 2
        chat = self.assertTextMessageWasHandled(str(cubes_count), self.chat)
        self.assertChatMessagesCount(chat, cubes_count+1)
        # statistic
        self.assertEqual(1, models.Drop.objects.count())

    def test_drop_cubes_raw(self):
        """
            Test any text message (positive number): success, not delay, raw
            """
        user_id = self.client.id
        models.save_delay(False, user_id)
        models.save_drop_format('raw', user_id)
        cubes_count = 2
        chat = self.assertTextMessageWasHandled(str(cubes_count), self.chat)
        self.assertChatMessagesCount(chat, 2)
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
            '50',  # ограничение
            '150',
        ]
        for text in inputs:
            with self.subTest(input):
                chat = self.assertTextMessageWasHandled(text, self.chat)
                self.assertChatLastMessageTextEqual(chat, 'Нужно ввести положительное число < 50')


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


    def test_enable_delay(self):
        user_id = self.client.id
        models.save_delay(False, user_id)
        self.assertFalse(models.is_delay_enabled(user_id))
        chat = self.assertCommandWasHandled('/enable_delay', self.chat)
        self.assertChatLastMessageTextEqual(chat, 'Задержка перед броском включена')
        self.assertTrue(models.is_delay_enabled(user_id))


    def test_disable_delay(self):
        user_id = self.client.id
        models.save_delay(True, user_id)
        self.assertTrue(models.is_delay_enabled(user_id))
        chat = self.assertCommandWasHandled('/disable_delay', self.chat)
        self.assertChatLastMessageTextEqual(chat, 'Задержка перед броском отключена')
        self.assertFalse(models.is_delay_enabled(user_id))


    def test_set_raw_format(self):
        user_id = self.client.id
        models.save_drop_format('one to one', user_id)
        self.assertEqual('one to one', models.get_drop_format(user_id))
        chat = self.assertCommandWasHandled('/set_raw_format', self.chat)
        self.assertChatLastMessageTextEqual(chat, 'Включен вывод в строчку')
        self.assertEqual('raw', models.get_drop_format(user_id))


    def test_set_one_by_one_format(self):
        user_id = self.client.id
        models.save_drop_format('raw', user_id)
        self.assertEqual('raw', models.get_drop_format(user_id))
        chat = self.assertCommandWasHandled('/set_one_by_one_format', self.chat)
        self.assertChatLastMessageTextEqual(chat, 'Включен вывод по очереди')
        self.assertEqual('one by one', models.get_drop_format(user_id))

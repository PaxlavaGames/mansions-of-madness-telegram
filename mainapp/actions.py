from datetime import datetime
from telegram_framework import messages, actions
from .keyboards import menu_numbers_keyboard
from . import models


def introduction(bot, message):
    intro_message = messages.create_template_message(
        bot,
        'mainapp/bot/intro.html'
    )
    intro_message = messages.add_keyboard(intro_message, menu_numbers_keyboard)
    return actions.send_message(message.chat, intro_message)


def invalid_input_action(bot, message):
    invalid_message = messages.create_message(
        'Нужно ввести положительное число < 50',
        bot,
    )
    return actions.send_message(message.chat, invalid_message)


def drop_cubes_action(bot, message):
    chat = message.chat

    count = int(message.text)
    results = models.drop_cubes(count)
    drop_format = models.get_drop_format(message.sender.id)
    pictures = models.to_pictures(results, drop_format)
    for result in pictures:
        result_message = messages.create_message(
            result,
            bot,
        )
        if models.is_delay_enabled(message.sender.id):
            models.make_delay()
        chat = actions.send_message(chat, result_message)

    models.Drop.objects.create(results=results)
    return chat


def statistics_action(bot, message):
    frequency_dict = models.frequency()
    frequency_ordered_list = sorted(frequency_dict.items(), key=lambda pair: pair[0])
    raws = []
    for count, freq in frequency_ordered_list:
        raws.append(f'{count} - {freq}')
    result_message = messages.create_message(
        '\n'.join(raws),
        bot,
    )
    return actions.send_message(message.chat, result_message)


def save_delay(bot, message, delay, text):
    models.save_delay(delay, message.sender.id)
    response_message = messages.create_message(
        f'Задержка перед броском {text}',
        bot,
    )
    return actions.send_message(message.chat, response_message)


def enable_delay(bot, message):
    return save_delay(bot, message, True, 'включена')


def disable_delay(bot, message):
    return save_delay(bot, message, False, 'отключена')


def save_drop_format(bot, message, name, text):
    models.save_drop_format(name, message.sender.id)
    response_message = messages.create_message(
        f'Включен вывод {text}',
        bot,
    )
    return actions.send_message(message.chat, response_message)


def set_raw_format(bot, message):
    return save_drop_format(bot, message, 'raw', 'в строчку')


def set_one_by_one_format(bot, message):
    return save_drop_format(bot, message, 'one by one', 'по очереди')


def get_date_equity(bot, message):
    date = datetime.strptime(message.text, '%d.%m.%Y')
    equity = models.date_equity(date)
    response_text = models.equity_to_str(equity)
    response_message = messages.create_message(
        response_text,
        bot,
    )
    return actions.send_message(message.chat, response_message)

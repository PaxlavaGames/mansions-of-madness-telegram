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
        'Нужно ввести положительное число < 100',
        bot,
    )
    return actions.send_message(message.chat, invalid_message)


def drop_cubes_action(bot, message):
    chat = message.chat

    count = int(message.text)
    results = models.drop_cubes(count)
    pictures = models.to_pictures(results)
    for result in pictures:
        result_message = messages.create_message(
            result,
            bot,
        )
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

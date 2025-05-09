from telegram_framework import links, commands
from . import actions, filters


bot_links = [
    links.on_command(actions.set_raw_format, 'set_raw_format', 'Включить вывод в строчку'),
    links.on_command(
        actions.set_one_by_one_format,
        'set_one_by_one_format',
        'Включить вывод по очереди'
    ),
    links.on_command(actions.disable_delay, 'disable_delay', 'Отключить задержку перед броском'),
    links.on_command(actions.enable_delay, 'enable_delay', 'Включить задержку перед броском'),
    links.on_command(commands.user_commands, 'commands', 'Доступные команды'),
    links.on_command(actions.introduction, 'start', 'Запуск бота'),
    links.on_command(actions.statistics_action, 'statistics', 'Статистика'),
    links.on_command(commands.bot_father_commands, 'bot_father_commands'),
    links.on_message(actions.drop_cubes_action, filters.is_valid),
    links.on_message(actions.invalid_input_action),
]

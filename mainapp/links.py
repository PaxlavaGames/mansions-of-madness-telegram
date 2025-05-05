from telegram_framework import links
from . import actions, filters


bot_links = [
    links.on_command(actions.introduction, 'start', 'run bot'),
    links.on_command(actions.statistics_action, 'statistics'),
    links.on_message(actions.drop_cubes_action, filters.is_valid),
    links.on_message(actions.invalid_input_action),
]

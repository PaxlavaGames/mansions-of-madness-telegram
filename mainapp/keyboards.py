from telegram_framework import keyboards


menu_numbers_keyboard = keyboards.reply.Keyboard(
    name = 'menu_numbers',
    buttons=[
        keyboards.reply.Button(str(number))
        for number in range(1,6)
    ]
)

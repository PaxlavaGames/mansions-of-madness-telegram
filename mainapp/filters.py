from datetime import datetime

def is_valid(message):
    text = message.text
    if not text.isdigit():
        return False
    number = int(text)
    return 0 < number < 50


def is_date(message):
    try:
        datetime.strptime(message.text, '%d.%m.%Y')
        return True
    except ValueError:
        return False

def is_valid(message):
    text = message.text
    if not text.isdigit():
        return False
    number = int(text)
    return 0 < number < 50

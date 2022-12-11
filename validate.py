from datetime import datetime
import re


phone_pattern = "\s\+?[-\s]?(?:\d{2,3})?[-\s]?(?:\([-\s]?\d{2,3}[-\s]?\)|\d{2,3})?[-\s]?\d{2,3}[-\s]?\d{2,3}[-\s]?\d{2,3}\s"
mail_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def convert_to_date(birthday: str = None):
    birthday_date = None
    try:
        birthday_date = datetime.strptime(birthday, '%Y-%m-%d')
    except ValueError:
        pass
    try:
        birthday_date = datetime.strptime(birthday, '%m.%d.%Y')
    except ValueError:
        pass
    try:
        birthday_date = datetime.strptime(birthday, '%m.%d')
        birthday_date = birthday_date.replace(year=2)
    except ValueError:
        pass
    try:
        birthday = birthday.replace("29", "28", 1)
        birthday_date = datetime.strptime(birthday, '%m.%d.%Y')
    except:
        pass
    return birthday_date


def validate_date(data: str) -> bool:
    return False if convert_to_date(data) else False


def valid_phone_number(text: str):
    template = re.compile(phone_pattern)
    text = text.lower().strip()
    phone = template.findall(" " + text + " ")
    if phone and phone[0]:
        phone = phone[0].strip()
        return phone
    return None


def valid_email(text: str):
    template = re.compile(mail_pattern)
    text = text.lower().strip()
    mail = template.findall(" " + text + " ")
    if mail and mail[0]:
        mail = mail[0].strip()
        return mail
    return None

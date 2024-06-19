import os
from django.core import validators
from django.core.exceptions import ValidationError

class username_validator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = (
        "Введите действительное имя пользователя. Это значение может содержать только буквы, "
        "цифры и символы @/./+/-/_."
    )
    flags = 0
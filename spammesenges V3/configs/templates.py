# -*- coding: utf-8 -*-
"""
Шаблоны (пресеты) для spammesenges V3.
Применяются из settings.py через меню [M].
"""

TEMPLATES = {

    "simple": {
        "name": "Просто спам (без рандома)",
        "desc": "Отправляет одно и то же сообщение без изменений.",
        "settings": {
            "avoid_repeats": False,
            "translit_mode": "off",
            "translit_chance": 0.0,
            "replace_spaces_with_digits": False,
            "insert_between_letters": False,
            "emoji_mode": "off",
            "emoji_chance": 0.0,
            "randomize_case": False,
            "absolute_random": False,
            "absolute_tail": False,
        },
    },

    "digits": {
        "name": "Рандом цифрами",
        "desc": "Пробелы заменяются на случайные цифры.",
        "settings": {
            "avoid_repeats": True,
            "translit_mode": "off",
            "replace_spaces_with_digits": True,
            "digits_min": 1,
            "digits_max": 3,
            "insert_between_letters": False,
            "emoji_mode": "off",
            "randomize_case": False,
            "absolute_random": False,
            "absolute_tail": False,
        },
    },

    "digits_symbols": {
        "name": "Рандом цифрами + символами",
        "desc": "Цифры вместо пробелов + символы между буквами.",
        "settings": {
            "avoid_repeats": True,
            "translit_mode": "off",
            "replace_spaces_with_digits": True,
            "digits_min": 1,
            "digits_max": 3,
            "insert_between_letters": True,
            "emoji_mode": "off",
            "insert_chance": 0.3,
            "symbols_min": 1,
            "symbols_max": 2,
            "randomize_case": False,
            "absolute_random": False,
            "absolute_tail": False,
        },
    },

    "digits_symbols_emoji": {
        "name": "Цифры + символы + эмодзи",
        "desc": "Полный микс: цифры, обычные символы и эмодзи.",
        "settings": {
            "avoid_repeats": True,
            "translit_mode": "off",
            "replace_spaces_with_digits": True,
            "digits_min": 1,
            "digits_max": 3,
            "insert_between_letters": True,
            "emoji_mode": "mixed",
            "emoji_chance": 0.5,
            "insert_chance": 0.4,
            "symbols_min": 1,
            "symbols_max": 2,
            "randomize_case": False,
            "absolute_random": False,
            "absolute_tail": False,
        },
    },

    "digits_emoji": {
        "name": "Цифры + эмодзи",
        "desc": "Цифры вместо пробелов + эмодзи между буквами.",
        "settings": {
            "avoid_repeats": True,
            "translit_mode": "off",
            "replace_spaces_with_digits": True,
            "digits_min": 1,
            "digits_max": 3,
            "insert_between_letters": True,
            "emoji_mode": "emoji",
            "emoji_chance": 1.0,
            "insert_chance": 0.3,
            "randomize_case": False,
            "absolute_random": False,
            "absolute_tail": False,
        },
    },

    "emoji": {
        "name": "Только эмодзи",
        "desc": "Без цифр и символов — только эмодзи между буквами.",
        "settings": {
            "avoid_repeats": True,
            "translit_mode": "off",
            "replace_spaces_with_digits": False,
            "insert_between_letters": True,
            "emoji_mode": "emoji",
            "emoji_chance": 1.0,
            "insert_chance": 0.4,
            "randomize_case": False,
            "absolute_random": False,
            "absolute_tail": False,
        },
    },

    # 7. АБСОЛЮТНАЯ РАНДОМИЗАЦИЯ с генерацией хвоста
    "absolute": {
        "name": "АБСОЛЮТНАЯ РАНДОМИЗАЦИЯ",
        "desc": "Сообщение = только защищённые слова, хвост генерируется сам.",
        "settings": {
            # Сообщение — только защищённое слово, весь текст будет генерироваться
            "message": "/cc",
            "avoid_repeats": True,
            "history_size": 500,
            "max_generation_attempts": 100,
            "translit_mode": "mix",
            "translit_chance": 0.7,
            "replace_spaces_with_digits": True,
            "digits_min": 1,
            "digits_max": 3,
            "insert_between_letters": True,
            "emoji_mode": "mixed",
            "emoji_chance": 0.3,
            "insert_chance": 0.5,
            "symbols_min": 1,
            "symbols_max": 3,
            "randomize_case": True,
            "absolute_random": True,
            "absolute_tail": True,       # генерировать хвост после защищённого
            "absolute_tail_min": 8,      # мин. длина хвоста в символах
            "absolute_tail_max": 20,     # макс. длина хвоста
        },
    },
}


def get_template_names():
    order = [
        "simple",
        "digits",
        "digits_symbols",
        "digits_symbols_emoji",
        "digits_emoji",
        "emoji",
        "absolute",
    ]
    return [k for k in order if k in TEMPLATES]


def get_template(key):
    return TEMPLATES.get(key)
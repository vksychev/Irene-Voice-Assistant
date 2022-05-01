# Приветствие (и демо-плагин)
# author: Vladislav Janvarev (inspired by EnjiRouz)

import random

from utils.functions import choose_by_rarity
from vacore import VACore

ANSWERS = {
    "common": ["Рада тебя видеть!"],
    "uncommon": ["Иди нахуй"],
    "rare": [],
    "mythic": [],
    "legendary": []
}


# функция на старте
def start(core: VACore):
    manifest = {  # возвращаем настройки плагина - словарь
        "name": "Привет",  # имя
        "version": "1.0",  # версия
        "require_online": False,  # требует ли онлайн?

        "commands": {  # набор скиллов. Фразы скилла разделены | . Если найдены - вызывается функция
            "привет|доброе утро": play_greetings,
        }
    }
    return manifest


def play_greetings(core: VACore, phrase: str):  # в phrase находится остаток фразы после названия скилла,
    # если юзер сказал больше
    # в этом плагине не используется
    # Проигрывание случайной приветственной речи
    answer = choose_by_rarity(ANSWERS)
    core.play_voice_assistant_speech(answer)

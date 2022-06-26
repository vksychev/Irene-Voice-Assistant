# функция на старте
from utils.functions import choose_by_rarity
from utils.home_assistant_hook import HomeAssistantHook, run_service
from vacore import VACore

ANSWERS_ERROR = {
    "common": ["Какая-то ошибка"],
    "uncommon": [],
    "rare": [],
    "mythic": [],
    "legendary": []
}
ANSWERS = {
    "common": ["Будет сделано", "Опять работать"],
    "uncommon": ["Оооо, ща ебану"],
    "rare": [],
    "mythic": [],
    "legendary": []
}

ROOMS = {
    "kitchen": ["кухня", "кухне", "кухню", "жральне"]
}


def start(core: VACore):
    manifest = {  # возвращаем настройки плагина - словарь
        "name": "Чайник",  # имя
        "version": "1.0",  # версия
        "require_online": False,  # требует ли онлайн?

        "commands": {  # набор скиллов. Фразы скилла разделены | . Если найдены - вызывается функция
            "выключи": {
                "свет": turn_off_light
            },
            "включи": {
                "свет": turn_on_light
            }
        },

    }
    return manifest


def turn_off_light(core: VACore, phrase: str):
    collector = {}
    for room in ROOMS:
        for synonym in ROOMS[room]:
            if phrase.find(synonym) > -1:
                collector[synonym] = turn_off(room)
    codes = collector.values()
    result = 200
    for code in codes:
        if code >= 300:
            result = code
    process_code(result, core)


def turn_on_light(core: VACore, phrase: str):
    collector = {}
    for room in ROOMS:
        for synonym in ROOMS[room]:
            if phrase.find(synonym) > -1:
                collector[synonym] = turn_on(room)
    codes = collector.values()
    result = 200
    for code in codes:
        if code >= 300:
            result = code
    process_code(result, core)


def turn_on(room):
    return run_service("light.turn_on", room)


def turn_off(room):
    return run_service("light.turn_off", room)


def process_code(code, core):
    if code != 200:
        core.play_voice_assistant_speech(choose_by_rarity(ANSWERS_ERROR))
    else:
        core.play_voice_assistant_speech(choose_by_rarity(ANSWERS))

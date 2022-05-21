# функция на старте
from utils.functions import choose_by_rarity
from utils.home_assistant_hook import HomeAssistantHook
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


def start(core: VACore):
    manifest = {  # возвращаем настройки плагина - словарь
        "name": "Чайник",  # имя
        "version": "1.0",  # версия
        "require_online": False,  # требует ли онлайн?

        "commands": {  # набор скиллов. Фразы скилла разделены | . Если найдены - вызывается функция
            "чай": turn_on_kettle,
        },

    }
    return manifest


SETTINGS = {
    "service": "water_heater.turn_on",
    "entity": "water_heater.skykettle"
}


def turn_on_kettle(core: VACore, phrase: str):
    hook = HomeAssistantHook()
    hook.trigger_service(
        service=SETTINGS["service"],
        entity=SETTINGS["entity"]
    )


def process_code(code, core):
    if code != 200:
        core.play_voice_assistant_speech(choose_by_rarity(ANSWERS_ERROR))
    else:
        core.play_voice_assistant_speech(choose_by_rarity(ANSWERS))

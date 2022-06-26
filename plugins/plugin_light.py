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
            "выключи": {
                "свет | свет везде": turn_off_light
            },
            "включи": {
                "свет": {
                    "на кухне": turn_on_light
                }
            }
        },

    }
    return manifest


def turn_off_light(core: VACore, phrase: str):
    settings = {
        "service": "light.turn_off",
        "entity": "light.all"
    }
    hook = HomeAssistantHook()
    code = hook.trigger_service(
        service=settings["service"],
        entity=settings["entity"]
    )
    process_code(code, core)


def turn_on_light(core: VACore, phrase: str):
    settings = {
        "service": "light.turn_off",
        "entity": "light.kitchen"
    }
    hook = HomeAssistantHook()
    code = hook.trigger_service(
        service=settings["service"],
        entity=settings["entity"]
    )
    process_code(code, core)


def process_code(code, core):
    if code != 200:
        core.play_voice_assistant_speech(choose_by_rarity(ANSWERS_ERROR))
    else:
        core.play_voice_assistant_speech(choose_by_rarity(ANSWERS))

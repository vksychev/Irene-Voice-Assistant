# функция на старте
from utils.home_assistant_hook import HomeAssistantHook
from vacore import VACore


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
    "service": "water_heater",
    "method": "turn_on",
    "entity": "skykettle"
}


def turn_on_kettle(core: VACore, phrase: str):
    hook = HomeAssistantHook()
    code = hook.kettle_turn_on(
        service=SETTINGS["service"],
        method=SETTINGS["method"],
        name=SETTINGS["entity"]
    )
    if code != 200:
        core.play_voice_assistant_speech("Какая-то ошибка")
    else:
        core.play_voice_assistant_speech("Ооо чайку. Ща поставлю")


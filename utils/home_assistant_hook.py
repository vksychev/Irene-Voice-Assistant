from requests import get, post
import os

BEARER_TOKEN = os.getenv('HOME_ASSISTANT_TOKEN')
HOST = "192.168.1.220"
PORT = "8123"


class HomeAssistantHook:
    manifest = {
        "token": BEARER_TOKEN,
        "host": HOST,
        "port": PORT
    }

    def __init__(
            self,
            bearer_token=None,
            host=None,
            port=None,
    ):
        self._token = bearer_token if bearer_token is not None else self.manifest['token']
        self._host = host if host is not None else self.manifest['host']
        self._port = port if port is not None else self.manifest['port']

    def trigger_service(self, service: str, entity=None, data_extra=None):
        if data_extra:
            data = data_extra
        else:
            data = {
                "entity_id": f"{entity}"
            }
        return self._send_request(service, data)

    def _send_request(self, service: str, data: dict):
        path = service.replace('.', '/')
        url = f"http://{self._host}:{self._port}/api/services/{path}"
        headers = self.make_headers()
        response = post(url, headers=headers, json=data)
        print(response)
        return response.status_code

    def make_headers(self):
        auth = f"Bearer {self._token}"
        return {
            "Authorization": auth,
            "content-type": "application/json",
        }


if __name__ == '__main__':
    SETTINGS = {
        "service": "water_heater.turn_on",
        "entity": "water_heater.skykettle"
    }
    hook = HomeAssistantHook()
    hook.trigger_service(
        service=SETTINGS["service"],
        entity=SETTINGS["entity"]
    )

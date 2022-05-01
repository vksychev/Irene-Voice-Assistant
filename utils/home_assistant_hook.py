from requests import get, post
import os

# BEARER_TOKEN = os.environ['HOME_ASSISTANT_TOKEN']
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

    def kettle_turn_on(self, service: str, method: str, name: str):
        data = {
            "entity_id": f"{service}.{name}"
        }
        return self._send_request(service, method, data)

    def _send_request(self, service: str, method: str, data: dict):
        url = f"http://{self._host}:{self._port}/api/services/{service}/{method}"
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
        "service": "water_heater",
        "method": "turn_on",
        "entity": "skykettle"
    }
    hook = HomeAssistantHook()
    hook.kettle_turn_on(
        service=SETTINGS["service"],
        method=SETTINGS["method"],
        name=SETTINGS["entity"]
    )

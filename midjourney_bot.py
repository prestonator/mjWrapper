from urllib3.util.retry import Retry
import json
import time
import requests
from requests.adapters import HTTPAdapter
from dotenv import load_dotenv
import os

load_dotenv()

API_BASE_URL = "https://discord.com/api/v9"
API_VERSION = "1077969938624553050"
APP_ID = "936929561302675456"
SESSION_ID = "45bc04dd4da37141a5f73dfbfaf5bdcf"


class MidjourneyBot:
    def __init__(self):
        self._user_token = os.getenv("USER_TOKEN")
        self._server_id = os.getenv("SERVER_ID")
        self._channel_id = os.getenv("CHANNEL_ID")
        self._proxy = None
        self._proxies = None
        if self._proxy:
            self._proxies = {
                "http": self._proxy,
                "https": self._proxy,
            }

        self._header = {"authorization": self._user_token}
        self._session = requests.Session()

        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    def wait(self, seconds=2):
        time.sleep(seconds)

    def content(self, message):
        return message["content"]

    def message_id(self, message):
        return message["id"]

    def message_hash(self, message):
        return self.get_image_url(message).split("_")[-1].split(".")[0]

    def get_image_url(self, message):
        time.sleep(2)
        return message["attachments"][0]["url"]

    def validate_image_url(self, message):
        if message["attachments"]:
            image_url = self.get_image_url(message)
            response = self._session.get(
                url=image_url,
                headers=self._header,
                proxies=self._proxies,
                timeout=120,
            )
            return response.status_code == 200
        return False

    def ask(self, prompt):
        payload = {
            "type": 2,
            "application_id": APP_ID,
            "guild_id": self._server_id,
            "channel_id": self._channel_id,
            "session_id": "2fb980f65e5c9a77c96ca01f2c242cf6",
            "data": {
                "version": API_VERSION,
                "id": "938956540159881230",
                "name": "imagine",
                "type": 1,
                "options": [{"type": 3, "name": "prompt", "value": prompt}],
                "application_command": {
                    "id": "938956540159881230",
                    "application_id": APP_ID,
                    "version": API_VERSION,
                    "default_permission": True,
                    "default_member_permissions": None,
                    "type": 1,
                    "nsfw": False,
                    "name": "imagine",
                    "description": "Create images with Midjourney",
                    "dm_permission": True,
                    "options": [
                        {
                            "type": 3,
                            "name": "prompt",
                            "description": "The prompt to imagine",
                            "required": True,
                        }
                    ],
                },
                "attachments": [],
            },
        }

        url = f"{API_BASE_URL}/interactions"
        response = self._session.post(
            url=url,
            json=payload,
            headers=self._header,
            proxies=self._proxies,
            timeout=120,
        )
        return response.status_code

    def up_scale(self, index, message):
        message_id = self.message_id(message)
        payload = {
            "type": 3,
            "guild_id": self._server_id,
            "channel_id": self._channel_id,
            "message_flags": 0,
            "message_id": self.message_id(message),
            "application_id": APP_ID,
            "session_id": SESSION_ID,
            "data": {
                "component_type": 2,
                "custom_id": f"MJ::JOB::upsample::{index}::{self.message_hash(message)}",
            },
        }
        url = f"{API_BASE_URL}/interactions"
        response = self._session.post(
            url=url,
            json=payload,
            headers=self._header,
            proxies=self._proxies,
            timeout=120,
        )
        if response.status_code != 200:
            print("Error in up_scale:", response.status_code, response.text)
        return response.status_code

    def messages(self, limit=1):
        url = f"{API_BASE_URL}/channels/{self._channel_id}/messages?limit={limit}"
        response = self._session.get(
            url=url,
            headers=self._header,
            proxies=self._proxies,
            timeout=120,
        )
        return json.loads(response.text)

    def save_image(
        self,
        image_url,
        external_url=None,
        headers=None,
        additional_data=None,
    ):
        if external_url:
            payload = {
                "image_url": image_url,
            }

            if additional_data:
                payload.update(additional_data)

            self._session.post(external_url, headers=headers, data=payload)

        # Add this line to return the payload
        return payload

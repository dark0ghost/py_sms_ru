from logging import getLogger
from typing import List, Optional, Tuple, Dict, Union
from enum import Enum

import aiohttp

try:
    import ujson as json
except ImportError:
    import json

logger = getLogger(__name__)



class CheckCallEnum(Enum):
    WAIT_ACCEPT_PHONE = 400
    PHONE_ACCEPT = 401
    NOT_VALID_PHONE = 202
    NO_ACCEPT_PHONE = 402



class CheckCallException(Exception):
    pass



class CheckCall:
    session: aiohttp.ClientSession
    response_code: Dict[int, str]

    def __init__(self, api_key: str, session: Optional[aiohttp.ClientSession] = None) -> None:
        self.api_key = api_key
        if session is None:
            self.session = aiohttp.ClientSession(json_serialize=json.dumps)
        else:
            self.session = session

    async def check_status_call(self, check_id: str) -> CheckCallEnum:
        """
        check status call
        """
        params = [('api_id', self.api_key), ('check_id', check_id), ("json", 1)]
        async with self.session.get(
                url=f"https://sms.ru/callcheck/status?", params=params) as response:
            js_resp = await response.json()
            if response.status == 200:
                try:
                    return CheckCallEnum(js_resp["check_status"])
                except ValueError:
                    logger.error("request not valid")
                    return CheckCallEnum.NOT_VALID_PHONE

            logger.error(f"servis have status {response.status}")
            raise CheckCallException

    async def send_phone(self, phone: str) -> Optional[Tuple[str, str, str]]:
        """
        send phone on server and return phone tuple  on neeed call
        use 0 element for standart phone or 1 element for html
        and 2 element - check_id
        """
        params = [('api_id', self.api_key), ('phone', phone), ("json", 1)]
        async with self.session.get(
                url=f"https://sms.ru/callcheck/add?", params=params) as response:
            if response.status == 200:
                js_response = await response.json()
                if js_response["status"] == "OK":
                    re_list = (js_response["call_phone"], js_response["call_phone_html"], js_response["check_id"])
                    return re_list
                return None
            logger.error(f"servis have status {response.status}")
            raise 

# py_sms_ru
__a library that allows you to check the phone by sending SMS to the telophone and then entering it into the service.__
[service](sms.ru)


# how use
```python
from sms_ru import SmsApi
import aiohttp
async def main():
 session = aiohttp.ClientSession()
 sms_api = SmsApi(session=session,api_key="")
 print(await sms_api.sen_phone(" (+420) ***-***-**"))
 # ((+420) ***-***-***, <html>(+420) ***-***-**</html>,check_id)
 print(await sms_api.check_status_call(chek_id))
 #  CheckCallEnum.WAIT_ACCEPT_PHONE or CheckCallEnum.PHONE_ACCEPT or CheckCallEnum.NOT_VALID_PHONE or  CheckCallEnum.NO_ACCEPT_PHONE
```
__file path:"./staticfile/cat.jpg"__

aiohttp>=3
python>=3.7

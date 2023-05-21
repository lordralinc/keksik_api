# Keksik API wrapper

Обвертка над API [keksik.io](https://keksik.io/api)

<p align="center">
  <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/keksik-api">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/keksik-api?color=green&label=PyPI">
</p>

# Использование:
```python
import os
from keksik_api import KeksikAPI, KeksikAPIException

GROUP_ID = int(os.environ.get('GROUP_ID'))
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')


api = KeksikAPI(GROUP_ID, ACCESS_TOKEN)

last_donates = await api.donates.get_last()
for item in last_donates.items:
    print(item.id)

# Передача токена динамически
await api.donates.answer(1, "Спасибо :3", group=GROUP_ID, token=ACCESS_TOKEN)

# Ошибочки
try:
    await api.donates.answer(-666, '')
except KeksikAPIException as exc:
    print("Произошла ошибка: ", exc.error_code, exc.message)

# Кастомные запросы
await api.request("{method}", dict(data='...'), raise_errors=False)

# Callback
import uvicorn
from fastapi import FastAPI

from keksik_api.callback import Callback, Router
from keksik_api import schemas

SECRET_KEY = os.environ.get('SECRET_KEY')
CONFIRMATION_CODE = os.environ.get('CONFIRMATION_CODE')


router = Router()

@router.on_new_donate()
async def on_new_donate_handler(event: schemas.DonateEvent):
    print("New donate", event.donate.id)

callback = Callback(
    KeksikAPI(GROUP_ID, ACCESS_TOKEN),
    SECRET_KEY,
    CONFIRMATION_CODE,
    router=router
)


app = FastAPI()

@app.post("/")
async def app_route(params: dict):
    return await callback.route_web_request(params)


if __name__ == "__main__":
    uvicorn.run(app)
```
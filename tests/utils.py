import aiohttp
from aiohttp import web


def wait_response(expected_response: str):
    async def request_handler(request: web.Request):
        return web.Response(
            text=expected_response,
            headers={'Content-Type': 'application/json'}
        )

    return request_handler


async def make_session(client_maker, url: str, message: str) -> aiohttp.ClientSession:
    app = web.Application()
    app.router.add_post(url, wait_response(message))
    return await client_maker(app)


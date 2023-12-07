import asyncio
from io import BytesIO

import aiohttp


LIMIT_ASYNC_CONNECT = 10
ASYNC_SIZE_CHUNK_B = 1024


async def get_data(sess, url):
    data = None
    async with sess.get(url, ssl=False) as resp:
        status = resp.status
        if resp.status == 200:
            data = BytesIO()
            async for chunk in resp.content.iter_chunked(ASYNC_SIZE_CHUNK_B):
                data.write(chunk)
            data.seek(0)
        return {"url": url, "status": status, "data": data}


async def get_text(sess, url):
    data = None
    async with sess.get(url, ssl=False) as resp:
        status = resp.status
        if status == 200:
            data = (await resp.read()).decode()
        return {"url": url, "status": status, "data": data}


async def fetch_all(args, data):
    tasks = []
    my_connector = aiohttp.TCPConnector(limit=LIMIT_ASYNC_CONNECT)
    async with aiohttp.ClientSession(connector=my_connector) as session:
        for arg in args:
            async_f = get_data if data else get_text
            tasks.append(asyncio.create_task(async_f(session, arg)))

        responses = await asyncio.gather(*tasks)

    return responses


def async_get(arg, data=False):
    result = asyncio.run(fetch_all(arg, data))
    return result

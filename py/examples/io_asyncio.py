#!/usr/bin/env python3
import asyncio
import time
import aiohttp

counter = 0
data = 0


async def download_site(session, url):
    global counter
    global data
    async with session.get(url) as response:
        counter += 1
        data += response.content_length


async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(download_site(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 40
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    duration = time.time() - start_time
    print(
        f"Multitask (asyncio):\n\tDownloaded {counter} sites ({data} bytes) in {duration} seconds")

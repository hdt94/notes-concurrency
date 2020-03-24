#!/usr/bin/env python3
import requests
import time

counter = 0
data = 0


def download_site(url, session):
    global counter
    global data
    with session.get(url) as response:
        counter += 1
        data += len(response.content)


def download_all_sites(sites):
    with requests.Session() as session:
        for url in sites:
            download_site(url, session)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 40
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(
        f"Non-concurrent:\n\tDownloaded {counter} sites ({data} bytes) in {duration} seconds")

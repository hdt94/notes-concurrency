#!/usr/bin/env python3
import requests
import multiprocessing
import time

counter = None
data = None
session = None


def initializer():
    # global counter
    # global data
    global session
    if not session:
        session = requests.Session()
        counter = 0
        data = 0


def download_site(url):

    with session.get(url) as response:
        pass
        # name = multiprocessing.current_process().name
        # print(f"{name}:Read {len(response.content)} from {url}")
        # counter += 1
        # data += len(response.content)


def download_all_sites(sites):
    with multiprocessing.Pool(initializer=initializer) as pool:
        pool.map(download_site, sites)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(
        f"Multiprocesing:\n\tDownloaded {counter} sites ({data} bytes) in {duration} seconds")

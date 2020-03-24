#!/usr/bin/env python3
import concurrent.futures
import requests
import threading
import time


counter = 0
data = 0
lock = threading.Lock()
thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    global counter
    global data

    session = get_session()
    with session.get(url) as response:
        lock.acquire()
        counter += 1
        data += len(response.content)
        lock.release()


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 40
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(
        f"Multithreading:\n\tDownloaded {counter} sites ({data} bytes) in {duration} seconds")

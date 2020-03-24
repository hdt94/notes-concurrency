#!/usr/bin/env bash
source venv/bin/activate
python examples/io_non_concurrent.py
python examples/io_threading.py
python examples/io_asyncio.py
python concurrency-overview/io_mp.py
#!/usr/bin/env bash
source venv/bin/activate
pip3 freeze
python examples/cpu_non_concurrent.py
python examples/cpu_threading.py
python examples/cpu_mp.py
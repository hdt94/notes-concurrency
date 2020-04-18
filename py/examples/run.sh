#!/usr/bin/env bash

set -e


###### FUNCTIONS ######

function activate_env() {
case $OSTYPE in
  "linux-gnu" | "darwin"*)
    source venv/bin/activate;;
  "msys" | "cygwin")
    source venv/Scripts/activate;;
  *)
    echo "Unknown platform; activate virtual environment manually" >&2
    exit 1;;
esac
}

function setup_env() {
echo CREATING VIRTUAL ENVIRONMENT
case $OSTYPE in
  "linux-gnu" | "darwin"*)
    python3 -m venv venv;;
  "msys" | "cygwin")
    python -m venv venv;;
  *)
    echo "Unknown platform; setup virtual environment manually" >&2
    exit 1;;
esac

activate_env
echo INSTALLING DEPENDENCIES
pip install -r requirements.txt
}

function run_cpu() {
echo RUNNING CPU-BOUND EXAMPLES
FILES="cpu_non_concurrent.py cpu_threading.py cpu_mp.py"
for file in $FILES
do
  python $file
done
}

function run_io() {
echo RUNNING IO-BOUND EXAMPLES
FILES="io_non_concurrent.py io_threading.py io_asyncio.py io_mp.py"
for file in $FILES
do
  python $file
done
}


###### EXECUTION ######

if [ -d venv ]; then
  activate_env
else
  setup_env
fi

if [[ -z $1 ]]; then
  run_cpu
  echo $'\n'
  run_io
elif [[ $1 == "--cpu" ]]; then
  run_cpu
elif [[ $1 == "--io" ]]; then
  run_io
else
  echo "Unknown option; please use --cpu or --io"
  exit 1
fi
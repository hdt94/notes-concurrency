# Concurrency with Python

Python offers multiple modules within its standard library to do concurrency:

- `asyncio`: cooperative multitasking.
- `concurrent.futures`: common interface for multithreading and multiprocessing.
- `threading`: multithreading.
- `multiprocessing`: multiprocessing.

## What is a _future_ object?

A _future_ is an object that encapsulates the result of an asynchronous execution or operation. The interface of _future_ objects varies whether using `asyncio` or `concurrent.futures`. These objects usually are not directly handled in `asyncio` but in `concurrent.futures`.

_More on `asyncio.Future` in: [https://docs.python.org/3/library/asyncio-future.html#future-object](https://docs.python.org/3/library/asyncio-future.html#future-object)_

_More on `concurrent.futures.Future` in: [https://docs.python.org/3/library/concurrent.futures.html#future-objects](https://docs.python.org/3/library/concurrent.futures.html#future-objects)_

## `asyncio`

`asyncio` is a module for asynchronous programming that's part of the standard Python library since version 3.4+ and it's based on an event-loop model, pausing and resuming the execution of tasks through coroutines. The tasks in `asyncio` are wrappers of coroutine objects (objects returned by calling coroutines).

The definition of coroutines and the execution control is done through `async/await` syntax (Python 3.5+):

- Define coroutines by prefixing functions and context managers with `async` keyword.
- Await the execution of an awaitable (e.g. task, coroutine, or future) by prefixing it with `await` keyword.

```py
import asyncio

async def my_sleep_coroutine(time, string):
	coro = asyncio.sleep(time) # asyncio.sleep() is a coroutine for sleeping
	await coro
	print(string)
```

_More on awaitables in:_

_[https://docs.python.org/3/library/asyncio-task.html#awaitables](https://docs.python.org/3/library/asyncio-task.html#awaitables)_

_[https://docs.python.org/3/glossary.html#term-awaitable](https://docs.python.org/3/glossary.html#term-awaitable)_

You must explicitly create and run an event loop with an entry point coroutine or task. As async programming has been an evolving feature in Python, it can be done through several means:

```py
# Python 3.7+
coro = my_sleep_coroutine(2, "Printed after 2 seconds")
asyncio.run(coro)

# Python < 3.7
coro = my_sleep_coroutine(2, "Printed after 2 seconds")
task = asyncio.ensure_future(coro)
loop = asyncio.get_event_loop()
loop.run_until_complete(task)
loop.close()
```

The complete snippet would be:

```py
import asyncio

async def my_sleep_coroutine(time, string):
  coro = asyncio.sleep(time)
  await coro
  print(string)

coro = my_sleep_coroutine(2, "Printed after 2 seconds")
asyncio.run(coro)
```

### Tasks

A _task_ in `asyncio` is a future-like object that wraps the execution of a coroutine.

The work of a _task_ is scheduling the execution in the event loop and storing the result when the execution is over.

You can create a _task_ through `asyncio.create_task()` or `async.ensure_future()`:

```py
# Python 3.7+
task = asyncio.create_task(coro)

# Python < 3.7
task = asyncio.ensure_future(coro)
```

A _task_ can be awaited to let the event loop orchestrate the computing of the queue of tasks and return control when execution of task is over:

```py
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    coro = say_after(1, 'hello')
    task = asyncio.create_task(coro)

    await task

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
```

Under the hood, awaiting a coroutine or future, is awaiting an internally created _task_ wrapping the object. However, directly awaiting coroutines can be inefficient:

```py
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    # These should take around 3 seconds
    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
```

Awaiting coroutines one after another implies that the scheduling of subsequent coroutines is done once the execution of current coroutine is over, so then, the execution of subsequent coroutine can be started, resulting in a sequential programming.

Remember: **creating a task schedules the coroutine immediately**

```py
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))

    # These should take around 2 seconds (1 second less than previous snippet)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
```

Because of the immediate scheduling, awaiting current task allows to start execution of subsequent task, so the waiting times are overlapped and the remaining time of awaiting subsequent tasks is shorter.

_More on tasks in: [https://docs.python.org/3/library/asyncio-task.html#asyncio.Task](https://docs.python.org/3/library/asyncio-task.html#asyncio.Task)_

You can start multiple coroutines with `async.gather()`.

### Working with modules based on `asyncio`

You should work with async versions of libraries for compatibility e.g. usage of `requests` module as HTTP client is replaced by `aiohttp` module (HTTP client based on `asyncio`).

You can find a complete list of modules and frameworks based on `asyncio` in: [https://github.com/timofurrer/awesome-asyncio](https://github.com/timofurrer/awesome-asyncio)

### Working with modules NOT based on `asyncio`

`async.ensure_future()`

## `concurrent.futures`

`concurrent.futures` is a library with high-level interfaces to facilitate implementation of concurrency in Python and it's part of standard library since version 3.2+.

It allows to do multithreading and multiprocessing through `ThreadPoolExecutor` class and `ProcessPoolExecutor` class; both of these return an `Executor` class object handling a pool of threads or processes, to submit and execute tasks.

Pool of threads:

```py
import concurrent.futures

with concurrent.futures.ThreadPoolExecutor() as executor:
    # multithreading
```

Pool of processes:

```py
import concurrent.futures

with concurrent.futures.ProcessPoolExecutor() as executor:
    # multiprocessing
```

A _task_ in `concurrent.futures` is a call to a _callable_ object which is anything that can be called such as a function or class method, and more general, any instance of a class with a `__call__` method.

You can submit a _task_ to later be run through `Executor.submit()` method which returns a future object:

```py
def return_after(message):
    time.sleep(2)
    return message

with concurrent.futures.ThreadPoolExecutor() as executor:
    future = executor.submit(return_after, ("hello"))
```

The complete example would be:

```py
import concurrent.futures
import time

start = time.perf_counter()


def return_after(message):
    time.sleep(2)
    return message


with concurrent.futures.ThreadPoolExecutor() as executor:
    future1 = executor.submit(return_after, ("hello"))
    future2 = executor.submit(return_after, ("world"))

    print(future1.result(), future2.result())

end = time.perf_counter()
print(f'Total time in seconds: {end - start}')
```

You can submit and run multiple _tasks_ at once through several means with an iterable of futures as argument:

- `Executor.map()`: map-like operation over each future returning a generator of future results.

  ```py
  import concurrent.futures
  import math

  PRIMES = [
      112272535095293,
      112582705942171,
      112272535095293,
      115280095190773,
      115797848077099,
      1099726899285419]

  def is_prime(n):
      if n < 2:
          return False
      if n == 2:
          return True
      if n % 2 == 0:
          return False

      sqrt_n = int(math.floor(math.sqrt(n)))
      for i in range(3, sqrt_n + 1, 2):
          if n % i == 0:
              return False
      return True

  def main():
      with concurrent.futures.ProcessPoolExecutor() as executor:
          results_generator = executor.map(is_prime, PRIMES)
          for number, prime in zip(PRIMES, results_generator):
              print('%d is prime: %s' % (number, prime))

  if __name__ == '__main__':
      main()
  ```

- `concurrent.futures.as_completed()`: returns an iterator that returns futures as they're completed not matter initial order in iterable argument.

  ```py
  import concurrent.futures
  import time

  start = time.perf_counter()

  def return_after(id, seconds):
      time.sleep(seconds)
      return f"Return of ID: {id}"

  with concurrent.futures.ThreadPoolExecutor() as executor:
      seconds = [5, 4, 3, 2, 1]
      futures = [executor.submit(return_after, *args)
                for args in enumerate(seconds)]
      for future in concurrent.futures.as_completed(futures):
          print(future.result())

  end = time.perf_counter()
  print(f'Total time in seconds: {end - start}')
  ```

  _More on `concurrent.futures.as_completed()` in: [https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.as_completed](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.as_completed)_

- `concurrent.futures.wait()`: execute and wait for tasks with optional conditionals of returning.

  ```py
  import concurrent.futures
  from time import sleep
  from random import randint

  def return_after(task_id):
      sleep(randint(1, 5))
      return f"Return of ID: {task_id}"

  with concurrent.futures.ThreadPoolExecutor() as executor:
      futures = [executor.submit(return_after, x) for x in range(4)]
      done, not_done = concurrent.futures.wait(
          futures, return_when='FIRST_COMPLETED')

      print(f'Done:\n\t{done}')
      print(f'Not done:\n\t{not_done}')

      future_done = done.pop()
      print(future_done.result())
  ```

  _More on `concurrent.futures.wait()` in: [https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.wait](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.wait)_

Remember: **using a context manager with either `ThreadPoolExecutor`/`ProcessPoolExecutor` automatically joins threads/processes** (i.e. `join()` method is called on each thread/process):

```py
import concurrent.futures
import time

start = time.perf_counter()


def wait_for(seconds):
    time.sleep(seconds)


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit(wait_for, 3)

    # Elapsed time is around 0 seconds
    timestamp = time.perf_counter()
    print(f'Elapsed time in seconds: {timestamp - start}')

    # Threads are automatically joined so it waits before continuing execution

# Total time is around 3 seconds
end = time.perf_counter()
print(f'Total time in seconds: {end - start}')

```

### `ThreadPoolExecutor`

`ThreadPoolExecutor` class uses `threading` module to handle a pool of threads that are subjected to all regards of multithreading such as the Global Interpreter Lock (read further).

### `ProcessPoolExecutor`

`ProcessPoolExecutor` class uses `multiprocessing` module to handle a pool of processes that are subjected to all regards of multiprocessing such as returning pickable objects (read further).

### Some adds

One recommendation is to use as many threads or processes, as the number of logical cores on your CPU.

## `threading`

```py
import concurrent.futures
import threading
```

thread-safe, bugs related to it

number of threads

### GIL: Global Interpreter Lock

The Python Global Interpreter Lock (GIL) is a global mutex (or lock) that protects access to data from multiple threads at a time (i.e. prevents race conditions and deadlocks). The inconvenient it brings up is that only one thread can be executed at a time, even in multithreaded architectures, so cpu-bound programs using multiple threads are indeed single-threaded, resulting in slower execution because of the overhead of working with threads in comparison to a non-concurrent execution.

The most common path taken in Python to address cpu-bound issues is to use `multiprocessing` module instead.

### Local data

You can have local data for each thread through `threading.local()`:

```py
import concurrent.futures
import threading
import uuid
from time import sleep
from random import randint


thread_local = threading.local()


def return_after(id):
    if (not hasattr(thread_local, 'id')):
        thread_local.id = uuid.uuid4()

    sleep(randint(1, 5))
    print(f'Task ID: {id}\nThread ID: {thread_local.id}\n')

    return f"Return of {id}"


with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    # It will print only two unique thread IDs
    executor.map(return_after, [n for n in range(6)])
```

## `multiprocessing`

Processes in Python can be thought as instances of a Python interpreter that run independently from each other.

### Pickable data

The arguments passed to a multi-processing process and the values returned by them must be serializable by using `pickle` module.

_More on `pickle` module in: [https://docs.python.org/3/library/pickle.html](https://docs.python.org/3/library/pickle.html)_

## Other alternatives for concurrency

If you require to use older versions of Python < 3.4, you can look at `gevent` and `tornado` libraries.

## References

- `asyncio`: [https://docs.python.org/3/library/asyncio.html](https://docs.python.org/3/library/asyncio.html)

- `concurrent.futures`: [https://docs.python.org/3/library/concurrent.futures.html](https://docs.python.org/3/library/concurrent.futures.html)

- PYTHON: GENERATORS, COROUTINES, NATIVE COROUTINES AND ASYNC/AWAIT: [http://masnun.com/2015/11/13/python-generators-coroutines-native-coroutines-and-async-await.html](http://masnun.com/2015/11/13/python-generators-coroutines-native-coroutines-and-async-await.html)

- A simple introduction to Python's asyncio:

  Publication: [https://hackernoon.com/a-simple-introduction-to-pythons-asyncio-595d9c9ecf8c](https://hackernoon.com/a-simple-introduction-to-pythons-asyncio-595d9c9ecf8c)

  Snippet 1: [https://gist.githubusercontent.com/apoorv007/4d1b431043ded551c2c387d02cee5a61/raw/8e346d4dd84654edcaff6c8d832a490b5c7be4b9/coroutine_example.py](https://gist.githubusercontent.com/apoorv007/4d1b431043ded551c2c387d02cee5a61/raw/8e346d4dd84654edcaff6c8d832a490b5c7be4b9/coroutine_example.py)

  Snippet 2: [https://gist.githubusercontent.com/apoorv007/323b20a9f08c9bd26bd36c2cdd6c6337/raw/92cc003837bcf72d2032337dabc8e51620ddef3c/asyncio_example.py](https://gist.githubusercontent.com/apoorv007/323b20a9f08c9bd26bd36c2cdd6c6337/raw/92cc003837bcf72d2032337dabc8e51620ddef3c/asyncio_example.py)

- AsyncIO for the Working Python Developer:

  Publication: [https://yeray.dev/python/asyncio/asyncio-for-the-working-python-developer](https://yeray.dev/python/asyncio/asyncio-for-the-working-python-developer)

  Code: [https://github.com/yeraydiazdiaz/asyncio-ftwpd](https://github.com/yeraydiazdiaz/asyncio-ftwpd)

- Async Through the Looking Glass: [https://hackernoon.com/async-through-the-looking-glass-d69a0a88b661](https://hackernoon.com/async-through-the-looking-glass-d69a0a88b661)

- Asynchronous Python:

  Publication: [https://hackernoon.com/asynchronous-python-45df84b82434](https://hackernoon.com/asynchronous-python-45df84b82434)

  Snippet `gevent`: [https://gist.githubusercontent.com/nhumrich/b53cc1e0482411e4b53d74bd12a485c1/raw/dfaabdd310eb4ce24817e591133540a949881342/gevent_example.py](https://gist.githubusercontent.com/nhumrich/b53cc1e0482411e4b53d74bd12a485c1/raw/dfaabdd310eb4ce24817e591133540a949881342/gevent_example.py)

  Snippet `tornado`: [https://gist.githubusercontent.com/nhumrich/c0ee81ddc3127fce21b674bfa996b2aa/raw/deafc7211c1c0fe484a1f78d15f48ec0edecf60d/tornado_example.py](https://gist.githubusercontent.com/nhumrich/c0ee81ddc3127fce21b674bfa996b2aa/raw/deafc7211c1c0fe484a1f78d15f48ec0edecf60d/tornado_example.py)

  Snippet `asyncio` (decorators): [https://gist.githubusercontent.com/nhumrich/e269a1364739b5965172fdde9321785d/raw/140ced31493dd9108eb41b95c97041eb009c407a/asyncio_example.py](https://gist.githubusercontent.com/nhumrich/e269a1364739b5965172fdde9321785d/raw/140ced31493dd9108eb41b95c97041eb009c407a/asyncio_example.py)

  Snippet `asyncio` (async/await): [https://gist.githubusercontent.com/nhumrich/933445f9de156b02950f3dacdd3ba9bb/raw/2ce52550369a20973c87b5b402d3182c316ce6ca/asyncio_await_example.py](https://gist.githubusercontent.com/nhumrich/933445f9de156b02950f3dacdd3ba9bb/raw/2ce52550369a20973c87b5b402d3182c316ce6ca/asyncio_await_example.py)

- PYTHON: A QUICK INTRODUCTION TO THE CONCURRENT.FUTURES MODULE: [http://masnun.com/2016/03/29/python-a-quick-introduction-to-the-concurrent-futures-module.html](http://masnun.com/2016/03/29/python-a-quick-introduction-to-the-concurrent-futures-module.html)

- Python Threading Tutorial: Run Code Concurrently Using the Threading Module:

  Video: [https://www.youtube.com/watch?v=IEEhzQoKtQU](https://www.youtube.com/watch?v=IEEhzQoKtQU)

  Code: [https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Threading](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Threading)

- What is the Python Global Interpreter Lock (GIL)?: [https://realpython.com/python-gil/](https://realpython.com/python-gil/)

- Python Multiprocessing Tutorial: Run Code in Parallel Using the Multiprocessing Module:

  Publication: [https://www.youtube.com/watch?v=fKl2JW_qrso](https://www.youtube.com/watch?v=fKl2JW_qrso)

  Code: [https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/MultiProcessing](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/MultiProcessing)

- Speed Up Your Python Program With Concurrency:

  Publication: [https://realpython.com/python-concurrency](https://realpython.com/python-concurrency)

  Code: [https://github.com/realpython/materials/tree/master/concurrency-overview](https://github.com/realpython/materials/tree/master/concurrency-overview)

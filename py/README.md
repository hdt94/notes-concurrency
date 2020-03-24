# Concurrency with python

## Up and running with examples

Set up examples
```
chmod +x run-examples-cpu.sh run-examples-io.sh setup-examples.sh
./setup-examples.sh
```

Run examples
```
./run-examples-cpu.sh
./run-examples-io.sh
```

## Notes


### Multithreading with `threading`

```py
import concurrent.futures
import threading
```

thread-safe, bugs related to it

number of threads

### Cooperative multitasking with `asyncio`

```py
import asyncio

```

tasks never give up control without intentionally doing so. They never get interrupted in the middle of an operation. This allows us to share resources a bit more easily in asyncio than in threading. You don’t have to worry about making your code thread-safe.

You can share the session across all tasks, so the session is created here as a context manager. The tasks can share the session because they are all running on the same thread. There is no way one task could interrupt another while the session is in a bad state.

One of the cool advantages of asyncio is that it scales far better than threading. Each task takes far fewer resources and less time to create than a thread, so creating and running more of them works well. This example just creates a separate task for each site to download, which works out quite well.

The scaling issue also looms large here. Running the threading example above with a thread for each site is noticeably slower than running it with a handful of threads. Running the asyncio example with hundreds of tasks didn’t slow it down at all.

Problems with asyncio

There are a couple of issues with asyncio at this point. You need special async versions of libraries to gain the full advantage of asycio. Had you just used requests for downloading the sites, it would have been much slower because requests is not designed to notify the event loop that it’s blocked. This issue is getting smaller and smaller as time goes on and more libraries embrace asyncio.

Another, more subtle, issue is that all of the advantages of cooperative multitasking get thrown away if one of the tasks doesn’t cooperate. A minor mistake in code can cause a task to run off and hold the processor for a long time, starving other tasks that need running. There is no way for the event loop to break in if a task does not hand control back to it.

### Multiprocesing with `multiprocessing` module

Processes in Python can be thought as instances of a Python interpreter.

The `multiprocessing` in the standard library was designed to break down that barrier and run your code across multiple CPUs. At a high level, it does this by creating a new instance of the Python interpreter to run on each CPU and then farming out part of your program to run on it.

As you can imagine, bringing up a separate Python interpreter is not as fast as starting a new thread in the current Python interpreter. It’s a heavyweight operation and comes with some restrictions and difficulties, but for the correct problem, it can make a huge difference.

The communication between the main process and the other processes is handled by the multiprocessing module for you.

As mentioned above, the processes optional parameter to the multiprocessing.Pool() constructor deserves some attention. You can specify how many Process objects you want created and managed in the Pool. By default, it will determine how many CPUs are in your machine and create a process for each one. While this works great for our simple example, you might want to have a little more control in a production environment.

If you have a CPU-bound program and you’re going to use the multiprocessing library, what’s a good number of processes to create?

One process for each CPU

I/O bound problem
For this problem, increasing the number of processes did not make things faster. It actually slowed things down because the cost for setting up and tearing down all those processes was larger than the benefit of doing the I/O requests in parallel.

Next we have the initializer=set_global_session part of that call. Remember that each process in our Pool has its own memory space. That means that they cannot share things like a Session object. You don’t want to create a new Session each time the function is called, you want to create one for each process.

The initializer function parameter is built for just this case. There is not a way to pass a return value back from the initializer to the function called by the process download_site(), but you can initialize a global session variable to hold the single session for each process. Because each process has its own memory space, the global for each one will be different.

The initializer function parameter is built for just this case. There is not a way to pass a return value back from the initializer to the function called by the process download_site(), but you can initialize a global session variable to hold the single session for each process. Because each process has its own memory space, the global for each one will be different.

## References

[Speed Up Your Python Program With Concurrency](https://realpython.com/python-concurrency)
[https://github.com/realpython/materials/tree/master/concurrency-overview](https://github.com/realpython/materials/tree/master/concurrency-overview)







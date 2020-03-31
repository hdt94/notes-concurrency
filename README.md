# Concurrency

Concurrency is the simultaneous computing of multiple programming sequences (i.e. instructions), implemented through processes, threads, or tasks.

Parallelism is the computing of programming sequences in several CPU cores (physical or logical) under a concurrent model.

Asynchronous programming is a high-level branch of concurrent programming to implement cooperative multitasking (read further).

Concurrent programming is made to address two main problems that slow down programs:

- **I/O-bound**: input/output operations I/O (e.g. file system calls, network connections) make programs to wait responses:

![](https://files.realpython.com/media/IOBound.4810a888b457.png)

- **CPU-bound**: calculations reach computing limit of CPU:

![](https://files.realpython.com/media/CPUBound.d2d32cb2626c.png)

Concurrency follows several approaches according to the problem to be addressed, the CPU architecture and the execution wrapper (e.g. operating system OS, interpreter/runtime):

- **Preemptive multitasking:** wrapper preempts the execution of programs at any arbitrary time. **This is only for I/O-bound**. It can be inefficient if misused. Multithreading is an example of preemptive multitasking in which all threads use only one CPU core and can be randomly interrupted by wrapper.

- **Cooperative multitasking:** wrapper waits to be gave with control of execution by programs through coroutines (cooperative routines) pausing and resuming execution its own execution. **This is only for I/O-bound**. The nature of cooperative multitasking is using one CPU core that executes the tasks. The models and interfaces of cooperative multitasking (e.g. async/await) constitute what is known as asynchronous programming. One popular implementation is the event-loop model which execute tasks based on states and queues, this is used in interpreted languages and libraries such as JavaScript and `asyncio` module in Python.

- **Multiprocessing:** wrapper executes programs through self-contained processes in many CPU cores. **This is only for CPU-bound**.

Usually multithreading addresses issues with race conditions bugs, i.e. bugs related to simultaneous writing of data -leading to data inconsistency-, that makes neccessary to protect data accesses to prevent threads from interfering with each other. In multiprocessing, processes are supossed to not share data because of its self-contained model, but there could be cases forcing some degree of sharing allowable by some wrappers (e.g. `multiprocessing` module in Python) leading to same issues and preventions as in multithreading.

## Addressing I/O-bound

Ideally you address I/O-bound through cooperative multitasking over multithreading to overcome problems such as race conditions and performance issues due to the overhead of creating threads.

![](https://files.realpython.com/media/Threading.3eef48da829e.png)

![](https://files.realpython.com/media/Asyncio.31182d3731cf.png)

In I/O operations both multithreading and cooperative multitasking are efficient in using one single CPU core while multiprocesing use multiple cores that spend most of its time waiting for responses, resulting in inneficcient usage.

## Addressing CPU-bound

Multiprocessing is the only way to correctly address CPU-bound by splitting up the program into multiple processes.

Because of the nature of multithreading and cooperative multitasking regarding one single core of computing, they slow down programs with CPU-bound because of the overhead of setting up threads and processing tasks.

## Is concurrent programming a must?

You should worry about concurrency until you have a known performance issue: _“Premature optimization is the root of all evil in programming.”_

Consider adding concurrency to your program will not always speed it up.

## References

Some of the following references come along with language-specific examples but have relevant content regarding concurrency in general:

- **Multitasking vs Multithreading vs Multiprocessing** [https://www.youtube.com/watch?v=Tn0u-IIBmtc](https://www.youtube.com/watch?v=Tn0u-IIBmtc)

- **Speed Up Your Python Program With Concurrency** [https://realpython.com/python-concurrency](https://realpython.com/python-concurrency)

- **A simple introduction to Python's asyncio** [https://hackernoon.com/a-simple-introduction-to-pythons-asyncio-595d9c9ecf8c](https://hackernoon.com/a-simple-introduction-to-pythons-asyncio-595d9c9ecf8c)

- **Concurrency model and the event loop** [https://developer.mozilla.org/en-US/docs/Web/JavaScript/EventLoop](https://developer.mozilla.org/en-US/docs/Web/JavaScript/EventLoop)

- **Async Through the Looking Glass** [https://hackernoon.com/async-through-the-looking-glass-d69a0a88b661](https://hackernoon.com/async-through-the-looking-glass-d69a0a88b661)

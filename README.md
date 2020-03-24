# Concurrency

Concurrency is the simultaneous computing of multiple programming sequences (i.e. instructions), implemented through processes, threads, or tasks.

Parallelism is the computing of programming sequences in several CPU cores (physical or logical) under a concurrent model.

Concurrent programming is made to address two main problems that slow down programs:

- **I/O bound**: input/output operations I/O (e.g. file system, network connections) make programs to wait responses:

![](https://files.realpython.com/media/IOBound.4810a888b457.png)

- **CPU bound**: calculations reach computing limit of CPU:

![](https://files.realpython.com/media/CPUBound.d2d32cb2626c.png)

Concurrency follows several approaches according to the problem to be addressed, the CPU architecture and the execution wrapper (e.g. operating system OS, interpreter/runtime):

- **Preemptive multitasking:** wrapper preempts the execution of programs at any arbitrary time. This is only for I/O bound. It can be inefficient if misused. Multithreading is an example of preemptive multitasking.

- **Cooperative multitasking:** wrapper waits to be gave with control of execution by programs. This is only for I/O bound.

- **Multiprocessing:** wrapper executes programs through self-contained processes in many cores. This is only for CPU bound.

Usually multithreading and multiprocessing address issues with race conditions bugs, i.e. bugs related to simultaneous writing of data that makes neccessary to protect data accesses to prevent threads/processes from interfering with each other.

## Addressing I/O bound

Ideally you address I/O bound through cooperative multitasking over multithreading to overcome problems such as race conditions and performance issues due to the overhead of creating threads.

![](https://files.realpython.com/media/Threading.3eef48da829e.png)

![](https://files.realpython.com/media/Asyncio.31182d3731cf.png)

## Addressing CPU bound
Multiprocessing is the only way to address CPU bound by splitting up the program into multiple processes.

## Is concurrent programming a must?

You should worry about concurrency until you have a known performance issue: _“Premature optimization is the root of all evil in programming.”_

Consider adding concurrency to your program will not always speed it up.

## References

[Speed Up Your Python Program With Concurrency](https://realpython.com/python-concurrency)

# Python Concurrency Exploration

This project explores various concurrency models in Python, focusing on different combinations of task types (I/O-bound and CPU-bound) and execution modes (single-thread, multi-thread, multi-process, single coroutine, and multi coroutine). It allows you to evaluate the best execution model based on the nature of the task being executed.

## Task Types and Execution Modes

### TaskType.IO
- **Suitable for**: I/O-bound tasks such as file operations, network requests, or database queries. These tasks spend most of the time waiting for external resources.
- **Recommended Execution Modes**:
  - **SINGLE_THREAD**: Not recommended for I/O-bound tasks; inefficient due to waiting.
  - **MULTI_THREAD**: Effective for I/O-bound tasks since threads can switch during I/O wait times.
  - **SINGLE_COROUTINE**: Useful when tasks are simple and don't require full multi-threading.
  - **MULTI_COROUTINE**: Excellent for handling many I/O-bound tasks concurrently with minimal resource usage.

### TaskType.CPU
- **Suitable for**: CPU-bound tasks that involve heavy computations like mathematical calculations, image processing, or data analysis.
- **Recommended Execution Modes**:
  - **SINGLE_THREAD**: Poor performance for CPU-bound tasks, as only one core is used.
  - **MULTI_THREAD**: Limited effectiveness for CPU-bound tasks due to Python's Global Interpreter Lock (GIL).
  - **MULTI_PROCESS**: Best for CPU-bound tasks, as it leverages multiple CPU cores to run tasks in parallel.

## Understanding the Global Interpreter Lock (GIL)

The Global Interpreter Lock (GIL) is a mechanism in CPython (the most common Python interpreter) that allows only one thread to execute Python bytecode at a time. This lock is necessary because Python's memory management is not thread-safe.

- **Effect on multi-threading**: The GIL limits the ability of Python to execute CPU-bound tasks in parallel using threads. Even if you use multiple threads, only one thread can execute Python code at any given time, which makes multi-threading less effective for CPU-bound tasks.
  
- **Workaround**: For CPU-bound tasks, using **multi-processing** is recommended because each process has its own GIL, allowing true parallelism across multiple CPU cores.

## Execution Modes Overview
1. **SINGLE_THREAD**: Sequentially executes tasks in a single thread. Useful for simple operations but inefficient for both I/O-bound and CPU-bound tasks.
   
2. **MULTI_THREAD**: Runs tasks in parallel using threads, ideal for I/O-bound tasks but constrained by the GIL for CPU-bound operations.

3. **MULTI_PROCESS**: Runs tasks in parallel across multiple processes. Highly recommended for CPU-bound tasks, as each process runs in its own memory space, bypassing the GIL.

4. **SINGLE_COROUTINE**: Executes asynchronous tasks in a non-blocking manner, one at a time. Suitable for I/O-bound tasks, but limited to single-threaded execution.

5. **MULTI_COROUTINE**: Runs multiple asynchronous tasks concurrently. Well-suited for handling large numbers of I/O-bound tasks efficiently with minimal overhead.

## Running the Project

To execute the code and observe the performance of different combinations of `TaskType` and execution modes:

```bash
python main.py
```

You can modify the `task_type` and `run_mode` variables in `main.py` to test different combinations.

### Example
To run a multi-process test for CPU-bound tasks, set:
```python
task_type = TaskType.CPU
run_mode = RunMode.MULTI_PROCESS
```

## Running Unit Tests

This project includes unit tests that mock time-consuming operations like `time.sleep` and `asyncio.sleep` to allow for fast test execution. To run the tests:

```bash
python -m unittest test_main.py
```
import time
import asyncio
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool

# Task type: can be either IO-bound or CPU-bound
class TaskType:
    IO = "io"
    CPU = "cpu"

# Run mode: defines how tasks are executed (single thread, multi-thread, multi-process, coroutines)
class RunMode:
    SINGLE_THREAD = "single_thread"
    MULTI_THREAD = "multi_thread"
    MULTI_PROCESS = "multi_process"
    SINGLE_COROUTINE = "single_coroutine"
    MULTI_COROUTINE = "multi_coroutine"

# Determine the number of times to run based on task type
def get_run_times(task_type):
    if task_type == TaskType.IO:
        return 10  # Less iterations for I/O-bound tasks
    elif task_type == TaskType.CPU:
        return 1000000  # More iterations for CPU-bound tasks

# Define I/O-bound task (simulates I/O operation with a sleep)
def io_square(n: int):
    time.sleep(1)  # Simulate I/O operation
    return n**2

# Define async version of I/O-bound task (simulates I/O operation with asyncio sleep)
async def io_square_async(n: int):
    await asyncio.sleep(1)  # Simulate I/O operation
    return n**2

# Define CPU-bound task (performs a heavy computation)
def cpu_square(n):
    return n**100

# Define async version of CPU-bound task (uses asyncio to allow resource yielding)
async def cpu_square_async(n: int):
    await asyncio.sleep(0)  # Yield control to allow other tasks to run
    return cpu_square(n)

# Synchronous task executor (chooses task type based on input)
def task(n, task_type):
    if task_type == TaskType.IO:
        return io_square(n)
    else:
        return cpu_square(n)

# Asynchronous task executor (chooses task type based on input)
async def task_async(n: int, task_type):
    if task_type == TaskType.IO:
        return await io_square_async(n)
    else:
        return await cpu_square_async(n)

# Single-threaded execution
def run_single_thread(task_type, run_times):
    numbers = list(range(1, run_times))  # List of tasks to run
    start_time = time.time()  # Start time for performance measurement
    results = [task(n, task_type) for n in numbers]  # Execute each task sequentially
    print(f"Single-threaded time: {time.time() - start_time} seconds")  # Print total time
    return results

# Multi-threaded execution
def run_multi_thread(task_type, run_times):
    numbers = list(range(1, run_times))  # List of tasks to run
    start_time = time.time()  # Start time for performance measurement
    with ThreadPool(8) as pool:  # Create a thread pool, adjust based on CPU cores
        results = pool.map(lambda n: task(n, task_type), numbers)  # Execute tasks in parallel using threads
    print(f"Multi-threaded time: {time.time() - start_time} seconds")  # Print total time
    return results

# Define a serializable function to replace the lambda
def task_for_multiprocessing(n_task_type):
    n, task_type = n_task_type
    return task(n, task_type)

# Multi-process execution
def run_multi_process(task_type, run_times):
    numbers = list(range(1, run_times))  # List of tasks to be executed
    start_time = time.time()  # Record the start time for performance measurement
    with Pool(4) as pool:  # Create a process pool, adjust the number based on available CPU cores
        # Use a serializable function to replace the lambda expression
        results = pool.map(task_for_multiprocessing, [(n, task_type) for n in numbers])  
    print(f"Multi-process time: {time.time() - start_time} seconds")  # Print the total execution time
    return results


# Single coroutine execution
async def run_single_coroutine(task_type, run_times):
    numbers = list(range(1, run_times))  # List of tasks to run
    start_time = time.time()  # Start time for performance measurement
    results = [await task_async(n, task_type) for n in numbers]  # Execute each task sequentially in an async manner
    print(f"Single coroutine time: {time.time() - start_time} seconds")  # Print total time
    return results

# Multi coroutine execution
async def run_multi_coroutine(task_type, run_times):
    numbers = list(range(1, run_times))  # List of tasks to run
    start_time = time.time()  # Start time for performance measurement
    tasks = [task_async(n, task_type) for n in numbers]  # Gather all tasks to run asynchronously
    results = await asyncio.gather(*tasks)  # Run tasks concurrently
    print(f"Multi coroutine time: {time.time() - start_time} seconds")  # Print total time
    return results

# Main control function: decides the execution method based on run mode and task type
def run(task_type, run_mode):
    run_times = get_run_times(task_type)  # Get number of times to run based on task type
    
    if run_mode == RunMode.SINGLE_THREAD:
        return run_single_thread(task_type, run_times)  # Execute in single-thread mode
    elif run_mode == RunMode.MULTI_THREAD:
        return run_multi_thread(task_type, run_times)  # Execute in multi-thread mode
    elif run_mode == RunMode.MULTI_PROCESS:
        return run_multi_process(task_type, run_times)  # Execute in multi-process mode
    elif run_mode == RunMode.SINGLE_COROUTINE:
        asyncio.run(run_single_coroutine(task_type, run_times))  # Execute in single coroutine mode
    elif run_mode == RunMode.MULTI_COROUTINE:
        asyncio.run(run_multi_coroutine(task_type, run_times))  # Execute in multi coroutine mode
    else:
        raise ValueError(f"Unknown run mode: {run_mode}")  # Raise error for invalid run mode

if __name__ == "__main__":
    task_type = TaskType.CPU  # Choose between TaskType.IO or TaskType.CPU
    run_mode = RunMode.MULTI_PROCESS  # Choose different run modes: SINGLE_THREAD, MULTI_THREAD, MULTI_PROCESS, SINGLE_COROUTINE, MULTI_COROUTINE
    run(task_type, run_mode)  # Run the selected mode

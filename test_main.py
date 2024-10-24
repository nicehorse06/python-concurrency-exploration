import unittest
import asyncio
from unittest.mock import patch
from main import (
    TaskType,
    get_run_times,
    io_square,
    cpu_square,
    run_single_thread,
    run_multi_thread,
    run_multi_process,
    run_single_coroutine,
    run_multi_coroutine,
)

class TestConcurrencyModule(unittest.TestCase):
    def test_get_run_times_io(self):
        self.assertEqual(get_run_times(TaskType.IO), 10)

    def test_get_run_times_cpu(self):
        self.assertEqual(get_run_times(TaskType.CPU), 1000000)

    @patch('main.time.sleep', return_value=None)  # Mock sleep to speed up the test
    def test_io_square(self, mock_sleep):
        self.assertEqual(io_square(2), 4)

    def test_cpu_square(self):
        self.assertEqual(cpu_square(2), 2 ** 100)

    @patch('main.time.sleep', return_value=None)  # Mock sleep to speed up the test
    def test_run_single_thread(self, mock_sleep):
        result = run_single_thread(TaskType.IO, 5)
        self.assertEqual(result, [1, 4, 9, 16])

    @patch('main.time.sleep', return_value=None)  # Mock sleep to speed up the test
    def test_run_multi_thread(self, mock_sleep):
        result = run_multi_thread(TaskType.IO, 5)
        self.assertEqual(result, [1, 4, 9, 16])

    @patch('main.time.sleep', return_value=None)  # Mock sleep to speed up the test
    def test_run_multi_process(self, mock_sleep):
        result = run_multi_process(TaskType.IO, 5)
        self.assertEqual(result, [1, 4, 9, 16])

    @patch('main.asyncio.sleep', return_value=None)  # Mock asyncio.sleep to speed up the test
    @patch('main.io_square_async', side_effect=lambda n: n ** 2)  # Mock async io_square
    def test_run_single_coroutine(self, mock_sleep, mock_io_square):
        result = asyncio.run(run_single_coroutine(TaskType.IO, 5))
        self.assertEqual(result, [1, 4, 9, 16])

    @patch('main.asyncio.sleep', return_value=None)  # Mock asyncio.sleep to speed up the test
    @patch('main.io_square_async', side_effect=lambda n: n ** 2)  # Mock async io_square
    def test_run_multi_coroutine(self, mock_sleep, mock_io_square):
        result = asyncio.run(run_multi_coroutine(TaskType.IO, 5))
        self.assertEqual(result, [1, 4, 9, 16])

if __name__ == "__main__":
    unittest.main()

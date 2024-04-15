import os
import time
import threading
from logger import Logger

def test_logger():
    log_dir = 'logs'  # Specify the directory for log files
    os.makedirs(log_dir, exist_ok=True)  # Create the directory if it doesn't exist

    logger = Logger(log_file=os.path.join(log_dir, 'test_log.txt'), log_level='DEBUG')
    logger.rotation_threshold = 10000  # 10 KB

    # Log messages with different log levels
    logger.log("This is a debug message", level='DEBUG')
    logger.log("This is an info message", level='INFO')
    logger.log("This is an error message", level='ERROR')

    # Test logging from multiple threads
    def log_messages():
        for i in range(10):
            logger.log(f"Thread-{threading.get_ident()} Message {i}")

    threads = []
    for _ in range(5):
        thread = threading.Thread(target=log_messages)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Check if log file exists
    assert os.path.exists(os.path.join(log_dir, 'test_log.txt'))

    # Check if log file has content
    with open(os.path.join(log_dir, 'test_log.txt'), 'r') as f:
        content = f.read()
        assert content != ''

    # Test edge cases
    logger.log("")  # Log empty message
    logger.log("A")  # Log message with a single character

    # Log a message exceeding the rotation threshold by a small margin
    logger.log(f"{'X' * (logger.rotation_threshold + 100)}")

    # Test error handling
    try:
        # Intentionally passing invalid log level
        logger.log("Invalid log level message", level='INVALID_LEVEL')
    except ValueError:
        pass  # Expected ValueError, ignore it
    else:
        assert False, "Expected ValueError but no exception was raised"

    # Test performance
    start_time = time.time()
    for i in range(1000):
        logger.log(f"Performance test message {i}")
    end_time = time.time()
    print(f"Time taken to log 1000 messages: {end_time - start_time} seconds")

    # Clean up
    os.remove(os.path.join(log_dir, 'test_log.txt'))

test_logger()

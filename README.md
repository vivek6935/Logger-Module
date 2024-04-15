Logger Module:
    Overview:
        The Logger module provides a flexible and easy-to-use logging mechanism for seamlessly integrating into any Python codebase. It allows logging messages to a file with customizable log levels, log file rotation, and thread safety features. This module is designed to handle logging in multithreaded environments efficiently.



Features:
1. Flexible Configuration: Configure log file location and log level according to your requirements.
2. Customizable Log Levels: Supports log levels such as DEBUG, INFO, and ERROR.
3. Automatic Log Rotation: Rotates log files based on size, ensuring optimal storage usage.
4. Thread Safety: Utilizes threading locks to ensure safe logging in multithreaded environments.
5. Informative Log Format: Logs include timestamp, log level, source file, function name, thread ID, and the log message itself.

Installation -> 
To use the Logger module, simply include the logger.py file in your project directory.

Usage: 
1. Initialization: Create an instance of the Logger class with optional parameters for log file location and log level.
    <!-- from logger import Logger
    logger = Logger(log_file='log.txt', log_level='INFO') -->
2. Logging: Use the log() method to log messages with the desired log level.
    <!-- logger.log("This is an info message", level='INFO')
    logger.log("This is a debug message", level='DEBUG')
    logger.log("This is an error message", level='ERROR') -->
3. Log Rotation: Log files are automatically rotated after reaching a specified size limit.

Example: 
    <!-- Refer to test.py for an example usage and test cases demonstrating the functionality of the Logger module. --


How to Test:
    To run the test cases, execute the test_logger() function in test.py. Ensure that the necessary permissions are granted for file operations.
    <!-- Python Test.py -->
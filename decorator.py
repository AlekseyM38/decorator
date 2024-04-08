import os
from datetime import datetime

def logger(path):
    def decorator(old_function):
        def new_function(*args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            function_name = old_function.__name__
            arguments = ", ".join([repr(arg) for arg in args] + [f"{key}={value!r}" for key, value in kwargs.items()])
            result = old_function(*args, **kwargs)

            with open(path, 'a') as log_file:
                log_file.write(f"{timestamp} - {function_name}({arguments}) -> {result}\n")

            return result
        return new_function
    return decorator

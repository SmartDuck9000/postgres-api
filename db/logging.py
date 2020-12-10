import threading

mutex = threading.Lock()

def logging(func):
    def wrapper(*args, **kwargs):
        with mutex:
            with open('.log', 'w') as log:
                pass
    return wrapper


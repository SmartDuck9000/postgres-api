import threading
import datetime
from termcolor import colored

mutex = threading.Lock()

def logging(func):
    def wrapper(self, *args, **kwargs):
        res = func(self, *args, **kwargs)

        query = kwargs['query']
        cur_time = '[' + str(datetime.datetime.now()) + '] '
        log_str = self.host + ':' + self.port + ' ' + self.user + ' ' + cur_time + query + '\n'

        with mutex:
            with open(self.log_file, 'a') as log:
                log.write(log_str)
        print(colored(query, color='blue'))

        return res

    return wrapper

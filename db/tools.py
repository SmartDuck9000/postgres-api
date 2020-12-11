import threading
import datetime
from termcolor import colored

mutex = threading.Lock()

def logging(func):
    def wrapper(self, *args, **kwargs):
        res = func(self, *args, **kwargs)

        query = '\"' + kwargs['query'] + '\"'
        cur_time = '[' + str(datetime.datetime.now()) + ']'
        url = self.host + ':' + self.port
        log_str = url + ' ' + self.user + ' ' + cur_time + ' ' + query + '\n'

        with mutex:
            with open(self.log_file, 'a') as log:
                log.write(log_str)
        print(colored(url, color='yellow'),
              colored(self.user, color='yellow'),
              colored(cur_time, color='blue'),
              colored(query, color='green'))

        return res

    return wrapper

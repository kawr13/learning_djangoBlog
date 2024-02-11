import threading
import time
from queue import Queue


print_lock = threading.Lock()


class CustomThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, Verbose=None, flag=None, timers=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
        self._is_killed = False
        self.start_time = None
        self.flag = flag
        self.timers = timers

    def kill(self):
        self._is_killed = True

    def run(self):
        if self._is_killed:
            return
        if self._target is not None:
            if self.flag:
                self.start_time = time.perf_counter()
                self._return = self._target(*self._args, **self._kwargs)
                while True:
                    if self._is_killed or time.perf_counter() - self.start_time >= self.timers:
                        self.kill()
                        break
            else:
                self._return = self._target(*self._args, **self._kwargs)

    def join(self, timeout=None):
        threading.Thread.join(self, timeout=timeout)
        return self._return


def multipool(func):
    def wrapper(*args, **kwargs):
        my_thread = CustomThread(target=func, args=args, kwargs=kwargs)
        my_thread.daemon = True
        my_thread.start()
        return my_thread
    return wrapper


from multiprocessing import Manager, Process
import time


def multipliproc(func):
    def wrapper(*args, **kwargs):
        manager = Manager()
        result_queue = manager.Queue()

        def worker():
            result = func(*args, **kwargs)
            result_queue.put(result)

        p = Process(target=worker)
        p.start()
        result = result_queue.get()
        p.join()
        return result

    return wrapper
import time
import threading
from functools import wraps
from collections import defaultdict
from exceptions import RateGuardException


class RateGuard(object):

    def __init__(self, rate_number=5, rate_time=60):
        self.rate_number = rate_number
        self.rate_time = rate_time
        self.clock = time.time

        self.last_reset = time.time()
        self.num_calls = 0
        self.arguments_called = defaultdict(int)

        self.lock = threading.RLock()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kargs):
            with self.lock:
                time_remain = self._time_remain()
                if time_remain <= 0:
                    self.num_calls = 0
                    self.last_reset = self.clock()

                self.arguments_called[(kargs["account_id"], kargs["user_name"])] += 1

                if self.arguments_called[(kargs["account_id"], kargs["user_name"])] > self.rate_number:
                    raise RateGuardException('call limit exceeded')

            return func(*args, **kargs)

        return wrapper

    def _time_remain(self):
        elapsed = self.clock() - self.last_reset
        return self.rate_time - elapsed


@RateGuard(rate_number=10, rate_time=4)
def get_users(account_id, user_name):
    print(account_id, user_name)


for i in range(100):
    account_id = f'omer{i}'
    get_users(account_id=account_id, user_name="raviv")

for i in range(100):
    get_users(account_id="omer", user_name="raviv")
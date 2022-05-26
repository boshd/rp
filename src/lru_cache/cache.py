import time
from collections import OrderedDict

class LRUCache():
    '''
    Least Recently Used (LRU) Cache implementation.
    '''

    def __init__(self, cache_capacity, record_expiry_duration):
        self.cache_capacity = int(cache_capacity)
        self.record_expiry_duration = int(record_expiry_duration)
        self.dict = OrderedDict()

    def get(self, k):
        if not k in self.dict:
            return -1

        if self.dict[k][1] < time.time():
            print(f'record w/ key {k} has expired; evicting.')
            self.dict.pop(k)
            return -1

        self.dict.move_to_end(k)
        return self.dict[k]

    def put(self, k, v):
        # key -> (value, expiry time = current + duration)
        self.dict[k] = (v, time.time() + self.record_expiry_duration)
        self.dict.move_to_end(k)
        if len(self.dict) > self.cache_capacity:
            poped_item = self.dict.popitem(last=False)
            print(f'cache capacity reached, evicting key {poped_item[0]}.')



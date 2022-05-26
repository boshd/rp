import time, pytest
from cache import LRUCache

@pytest.fixture(autouse=True)
def slow_down_tests():
    print('\n**************** LRU Cache test ****************\n')
    yield
    time.sleep(2)

class TestLRUCache(object):

    def test_simple_get_key(self):
        print('\n**************** Testing simple get operation ****************')
        capacity, expiry = 5, 10
        cache = LRUCache(capacity, expiry)
        print(f'Initializing cache w/ capacity: {capacity} and record expiry duration: {expiry}')
        cache.put(1, 1)
        print(f'-> Inserting (1, 1) into cache...')
        print(f'-> Getting key 1 from cache...')
        assert cache.get(1)[0] == 1

    def test_simple_put(self):
        print('\n**************** Testing simple put operation ****************')
        k, v = 2, 2
        capacity, expiry = 5, 10
        cache = LRUCache(capacity, expiry)
        print(f'Initializing cache w/ capacity: {capacity} and record expiry duration: {expiry}')
        cache.put(k, v)
        assert len(cache.dict) == 1

    def test_get_key_not_in_cache(self):
        print('\n**************** Testing get item not in cache ****************')
        capacity, expiry = 5, 10
        cache = LRUCache(capacity, expiry)
        print(f'Initializing cache w/ capacity: {capacity} and record expiry duration: {expiry}')
        print('-> Inserting (1, 1) into cache...')
        cache.put(1, 1)
        v = cache.get(2)
        print(f'-> Getting key 2 from cache. Result: {v}')
        assert v == -1

    def test_get_expired_key(self):
        print('\n**************** Testing if record is retreived after expiring ****************')
        capacity, expiry = 5, 5
        cache = LRUCache(capacity, expiry)
        print(f'Initializing cache w/ capacity: {capacity} and record expiry duration: {expiry}')
        cache.put(1, 1)
        print('-> Sleeping for 6 seconds ')
        for i in range(6):
            print('.', end=' ', flush=True)
            time.sleep(1)
        print()

        assert cache.get(1) == -1

    def test_put_key_into_full_cache(self):
        print('\n**************** Testing if cache size is larger than max capacity ****************')
        capacity, expiry = 5, 5
        cache = LRUCache(capacity, expiry)
        print(f'Initializing cache w/ capacity: {capacity} and record expiry duration: {expiry}')
        for i in range(1, 6):
            print(f'-> adding key {i} and value {i*100} to cache')
            cache.put(i, i*100)
            time.sleep(1)

        print(f'-> inserting 1 more record w/ key 6 and value 600')
        time.sleep(2)
        cache.put(6, 600)

        print(f'cache size = {len(cache.dict)}')
        assert len(cache.dict) == 5
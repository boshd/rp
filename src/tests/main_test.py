import requests, os, pytest, time
from redis import Redis

BASE_URL = 'http://localhost:8080'

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)

redis = Redis(redis_host, redis_port)

@pytest.fixture(autouse=True)
def slow_down_tests():
    redis.flushdb()
    print('\n**************** End-to-end test ****************\n')
    yield
    redis.flushdb()
    time.sleep(1)

class TestMain():

    # get
    def test_get_item(self):
        redis.set('hello', 'world')
        response = requests.get(BASE_URL + '/get/hello')
        assert response.json()['value'] == 'world'
        assert response.json()['source'] == 'redis'

    # non-existence
    def test_get_non_existent_item(self):
        response = requests.get(BASE_URL + '/get/rubbish')
        assert response.text == 'key was not found'

    # eviction
    def test_item_eviction(self):
        redis.set('one', 1)
        redis.set('two', 2)
        redis.set('three', 3)
        redis.set('four', 4)
        redis.set('five', 5)
        _ = requests.get(BASE_URL + '/get/three')
        redis.set('six', 6)
        response = requests.get(BASE_URL + '/get/one')
        assert response.json()['value'] == '1'
        assert response.json()['source'] == 'redis'

    # expiry
    def test_item_expiry(self):
        redis.set('two', 2)
        response = requests.get(BASE_URL + '/get/two')
        assert response.json()['value'] == '2'
        assert response.json()['source'] == 'redis'

        response = requests.get(BASE_URL + '/get/two')
        assert response.json()['value'] == '2'
        assert response.json()['source'] == 'cache'
        print('-> Sleeping for 11 seconds ')
        for i in range(11):
            print('.', end=' ', flush=True)
            time.sleep(1)
        print()
        response = requests.get(BASE_URL + '/get/two')
        assert response.json()['value'] == '2'
        assert response.json()['source'] == 'redis'

    # caching
    def test_item_caching(self):
        redis.set('some_key', 500)
        response = requests.get(BASE_URL + '/get/some_key')
        assert response.json()['value'] == '500'
        assert response.json()['source'] == 'redis'

        response = requests.get(BASE_URL + '/get/some_key')
        assert response.json()['value'] == '500'
        assert response.json()['source'] == 'cache'

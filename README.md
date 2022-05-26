# redis proxy

A simple HTTP Redis Proxy Server w/ a local Least Recently Used (LRU) Cache.

## High-level architecture overview

There are three major components to the system: Redis backing instance, LRU Cache and HTTP Server.

- Redis
The Redis instance serves as a key-value data store. In our case, it is used to retrieve data if the data is not available in our LRU cache.

- LRU Cache
This is a local cache built using the Least Recently Used (LRU) algorithm. The cache has a pair of configurable env. vars: capacity and expiry duration:
    - Capacity: Maximum number of items that can be held by the local cache.
    - Expiry duration: Maximum amount of time an item can stay in the cache before it expires. This happens whenever a get operation is invoked, otherwise it stays unexpired.

- HTTP Server
This is a simple HTTP Server using the Base HTTPServer `class Server(ThreadingMixIn, HTTPServer)` class: . It has two request handlers: `do_GET` and `do_POST`.

  - `do_GET`: Handles requests from the following paths:
    - `GET /` -- returns if server is up.
    - `GET /get/{key}` -- returns value for key if it exists or an 'key not found' message if it doesn't.
    - `GET /randompath` -- returns 'Resource not found' when an invalid path is entered.

  - **Multithreading**
    The server is built with the ability to handle requests in seperate threads. This is done through the use of the `ThreadingMixIn` mix-in class which allows the server to undertake parallel processing of `GET` requests.

## What the code does

The code is split up into five major components: **lru_cache**, **proxy**, **redis_client**, **main** and **tests**. The following breakdown intuitively follows the directory tree structure:

- **lru_cache**
  - **cache.py**
    - This is where the LRU Cache implementation lives. It uses a dictionary and an OrderedDict as a base of storing data and maintaining key access recency, respectively. OrderedDict objects are built on top of Doubly Linked-List data structures, which offers a significant time complexity boost over arrays (more on this in the Algorithmic Complexity section below).

  - **cache_test.py**
    - This is a test class for the LRU Cache. It tests out: get, put, existence, expiry and capacity.

- **proxy**
  - proxy.py
    - This class glues together the local LRU Cache and Redis client. It also handles the retrieval of data from the cache (if available) or from the Redis backing instance.

- **redis_client**
  - redis_client.py
    - This is a simple Redis client class that connects to the Redis backing instance using a pre-installed redis client library. It safely accesses the **set** and **get** methods.

  - redis_test.py:
    - Runs basic get, put and existence tests on the redis backing instance.

- **main.py**
  - Creates and starts a new server instance which includes a proxy instance inside it. This class glues together all the components and runs them in unison (minus redis instance, which is run separately using the docker scripts).

- **tests**
  - main_test.py
    - This runs the end-to-end tests using the python requests library to communicate with the proxy.

## Algorithmic complexity

#### Proxy
A `GET /get/{key}` operation is *O(1)* for both the local lru cache and Redis instances. Therefore, the overall complexity for a `GET` operation within the proxy is *O(1)*.

#### LRU Cache
- **Time complexity**
  - Get the least recent item: *O(1)*
  - Access item: *O(1)*
- **Space complexity**: *O(n)*

## Usage

```
$ git clone ...
$ cd rp

# builds redis a proxy server (ps) containers.
$ make build

# runs redis a proxy server (ps) containers.
$ make run

# stops redis a proxy server (ps) containers.
$ make stop

# runs make stop, make build and make run.
$ make restart

# runs make build -> make start -> ./run-ps-tests.sh -> make stop
$ make test
```

## Testing

The current tests run on the env. vars shown below, otherwise they would break. This is a point of improvement for the future.

## Configuration

There are a number of configurable parameters in this system, controlled by the following Environment Variables stored in the .env file in the root directory:

```
HOST_NAME="0.0.0.0"
SEVER_PORT=8080
RECORD_CAPACITY=5
RECORD_EXPIRY=10
REDIS_HOST="redis"
REDIS_PORT=6379
REDIS_DB=0
```

## Time spent on each component

- LRU Cache: **2 hrs**
- Redis Client: **30 mins**
- HTTP Server: **2 hrs**
- Proxy: **1 hr**
- Tests: **2 hrs**
- Containerization + config: **2 hrs**
- Total: **9.5 hrs**

## Not implemented
- Configurable concurrent client limit
- Redis client protocol




#!/bin/sh

python3 -m pytest ./src/lru_cache/
python3 -m pytest ./src/redis_client/
python3 -m pytest ./src/tests/
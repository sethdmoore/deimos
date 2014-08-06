#!/usr/bin/env python
import redis
import sys
import os


def main():
    """
    Simple CLI utility to dump the upstream host redis keys to terminal.
    Start with 'clear' arg to wipe all the redis keys
    """
    clear = False
    redis_host = os.environ.get("UPSTREAM_REDIS_HOST")
    if redis_host:
        r = redis.StrictRedis(host=redis_host)
    else:
        print "Must set UPSTREAM_REDIS_HOST"
        sys.exit(2)

    if len(sys.argv) > 1:
        if sys.argv[1] == 'clear':
            clear = True

    for key in r.keys():
        if 'use' in key:
            if clear:
                r.delete(key)
            else:
                print key
                print r.lrange(key, 0, -1)


if __name__ == '__main__':
    main()


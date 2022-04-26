# analog-assesment
(NOTE: I developed and tested this on Ubuntu running in WSL. Although I can't imagine anything in the repo that would break if ran on a different environment, I have not actually been able to test it.)
## Getting Started/Running
 1. Ensure Redis is [installed](https://redis.io/docs/getting-started/) and 'redis-server' is accessible from the path. Verify that the default redis port 6379 is not being used by another program.
 2. Ensure that python3 and pipenv are [installed](https://docs.python-guide.org/dev/virtualenvs/#installing-pipenv) on the system.
 3. Start redis if it is not already with `redis-server`
 4. Clone the repo and and cd into the root directory
 5. Run `pipenv install`  to install dependencies and  `pipenv shell` to activate the virtual environment
 6. You can now execute the `demo.sh` shell script, which will run the tests as well as start one producer, one monitor , and three senders.
 7. Note that if you plan on running the program manually and not via `demo.sh` you should run `redis-cli FLUSHALL` to clear the redis state between runs

## Limitations


1. The program relies on the most basic, unsecured local redis instance possible. This is a natural sideffect of this being just a demo
2. There are no integration tests, just a demo.
3. No real logging, error catching, etc. again just a demo
4. Unit test coverage could be improved some, but much of uncovered code is library code, which should not be explicitly unit tested
5. The monitor has to be killed manually via CTRL+C, which is annoying but fine for a demo.
6. Configuration is done in the laziest way (cli args) both due to again, the fact it's a demo, as well as to demonstrate competency in a variety of libraries instead of simply relying on either redis or a config file for all of the config.
# gridappsd-python
Python library for developing applications and services against the gridappsd api

## Requirements

The gridappsd-python library requires a  python version >= 3.6 and < 4 in order to work properly (Note no testing
has been done with python 4 to date).

## Installation

The recommended installation of `gridappsd-python` is in a separate virtual environment.  Executing the following
will create an environment called `griddapps-env`.

```shell
python3 -m venv gridappsd-env
```

Upgrade pip to the latest (some packages require 19.0+ version of pip).

```shell
python -m pip --upgrade pip
```

Install the latest `gridappsd-python` and its dependencies in the virtual environment.

```shell
pip install gridappsd-python
```

### Verifying things are working properly

The following code snippet assumes you have created a gridappsd instance using the steps in
https://github.com/GRIDAPPSD/gridappsd-docker.

Create a test script (tester.py) with the following content.

```python

from gridappsd import GridAPPSD

def on_message_callback(header, message):
    print(f"header: {header} message: {message}")

# Note these should be changed on the server in a cyber secure environment!
username = "app_user"
password = "1234App"

# Note: there are other parameters for connecting to
# systems other than localhost
gapps = GridAPPSD(username=username, password=password)

assert gapps.connected

gapps.send('send.topic', {"foo": "bar"})

# Note we are sending the function not executing the function in the second parameter
gapps.subscribe('subscribe.topic', on_message_callback)

gapps.send('subcribe.topic', 'A message about subscription')

time.sleep(5)

gapps.close()

```


Start up the gridappsd-docker enabled platform.  Then run the following to execute the tester.py script

```shell
python tester.py
```




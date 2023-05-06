---
layout: post
title: "Understanding the why and how of Python logging"
slug: python-logging
date:   2023-05-5 10:00:00 +0100
categories: [programming-tips]
tags: [python, observability, logging]
---

Let’s face it - any Python developer would have used the `print()` statement more than once in their lifetime to debug code. I still do from time to time, because it’s convenient for quick and dirty development. When implementing some observability to production code, though, you’ll need an organised and scalable logging solution in your application, which makes the  `print()` statement inadequate, for the following reasons:

1. It does not provide the ability to set severity levels nor timestamps of logs, which makes it difficult for a debugger to filter through a whole stack of logs - for example, to look for a particular error within thousands of logs within a time range. One would need to implement these repetitively by hand within the `print()` statement itself, which could easily become a tedious task as your code base grows.
2. It only prints to the standard console output, which means that you’d need to make a separate routing implementation to a file or to an external system.

.. and probably more reasons. Python’s built-in `logging` module is a straightforward answer to those pains, plus it has added benefits to production code. The module provides functions to intuitively separate logs by severity, as well as configuration options to handle and format your application logs. But before we get to the code, let’s first dive into three important concepts surrounding a log:

1. Logging Level - this represents the type of log being created. In Python, there are five logging levels, in order of increasing severity: DEBUG, INFO, WARNING, ERROR, CRITICAL.
2. Handler - this represents a set of actions to filter the log by a specified level or any other condition, and then route it to a particular output.
3. Formatter - this transforms the log into a specified pattern when the handler outputs the log.

When you create a logger through the logging module, its default handler is the standard output - the log is just printed out with default formatting into your terminal. A logger can have multiple handlers to handle routing to different systems (like to a file). Each handler can take in logs within a specified minimum logging level - for example, setting a handler’s logging level to WARNING means that it will process logs only of levels WARNING, ERROR, and CRITICAL.

These three concepts can be summarised by the illustration below:
![Pyhton logging concepts]({{site.baseurl}}/assets/images/logging-drawings/logging-module.png){: width="620" loading="lazy" style="margin-bottom: 1em"}

The logger has three handlers - each handler is associated to a minimum log level, which means that it will only process logs that are at or above that log level. For example, the first handler from the top is set to DEBUG level, so it will process all logs above or at the DEBUG level. The second handler is set to WARNING level, so it will process logs at WARNING, ERROR, and CRITICAL. The third handler, meanwhile, is set to the highest level, CRITICAL, which means it will only process logs at that level since it’s the highest level in that hierarchy. Each handler has one formatter and one output destination.

This logging model allows us to create loggers that can handle different levels of logs and output to different destinations. In a typical productionised solution, one might print out debug logs into a file like `debug.log`, print out logs from info level into the console, and even send critical level logs through email.

## Default logging configuration
The `logging` module provides a function for logging on each of the logging levels.

```python
import logging

logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is warning!')
logging.error('This is an error!')
logging.critical('This is a critical message!')
```

Running the code above prints out the following into your console:
```
WARNING:root:This is a warning!
ERROR:root:This is an error!
CRITICAL:root:This is a critical message!
```

There are two things to note about the output: (1) only the logs from warning level have been printed out; and (2) the log string is formatted to show the log level, the log name (“root”), and the message. The reason for these is because we haven’t set any custom configuration, so logging resorts to its default behaviour, which is to log only starting from WARNING level, and with a default format.

To override the default behaviour, we can use the `basicConfig()` function to set the logging level and the format, like this:

```python
import logging

logging.basicConfig(level=logging.DEBUG,
			           format='%(name)s - %(levelname)s - %(message)s')
logging.debug('Log this')
```

This will output
```
root - DEBUG - Log this
```

`basicConfig()` has other optional paramters to customise your logger, which you can find in [Python’s logging documentation](https://docs.python.org/3/library/logging.html#logging.basicConfig). Also note that you can only call `basicConfig()` once to set your logging configuration, so to reset it, you’ll need to start a new terminal session.

## Creating multiple loggers
So far, we’ve only created a logger with basic configuration through the `basicConfig()` function, which configures what is known as the **root** logger, or the default logger. In practice, it’s a good idea to create a logger for each of your code’s modules for easier debugging - each logger has a unique name to help you identify which part of the code is being logged.

To create a custom logger, use the `getLogger()` function and pass it with a name of your choosing:
```python
logger = logging.getLogger('logger')
```

Alternatively, you can use python’s `__name__` keyword to name your logger with the name of the module in which the logger is created.
```python
logger = logging.getLogger(__name__)
logger.warning('This is a log!')
```

If you had created the logger within the main module of your application, the resulting log would look like this:
```
WARNING:__main__:This is a log!
```

You can create a new logger within another module in your application, for example, within a module named `io` , and the same code above using `__name__` would result to the following log:
```
WARNING:io:This is a log!
```

**Note:** The output format of the logs follow the format that you’ve specified when calling the `basicConfig()`  function. If you don’t call `basicConfig()` before creating your custom loggers, only the message will be printed by default:

```
This is a log!
```

## Creating multiple handlers
Each logger can have multiple handlers. Recall that a handler implements how a log of a certain level is processed. Let’s take a look at an example where we create a new logger named `logger` with two handlers - one for printing logs to the console and one for saving error and critical logs to a file.

```python
import logging

logger = logging.getLogger('logger')

# Handler 1: print logs to the console
handler1 = logging.StreamHandler()
handler1.setLevel(logging.DEBUG)
logger.addHandler(handler1)

# Handler 2: save error and critical logs to a file
handler2 = logging.FileHandler('errors.log')
handler2.setLevel(logging.ERROR)
logger.addHandler(handler2)
```

The `logging` module provides classes for different types of handlers. The more common ones are `StreamHandler` and `FileHandler`. A `StreamHandler` is used to output logs into the standard output console, while a `FileHandler` is to output logs into a file.

The first handler `handler1` created in the code above was a `StreamHandler`, which was set to level `DEBUG` so that it handles logs from that level and output them to the standard output console. The second handler `handler2` is configured to output logs from level `ERROR` to a file named `errors.logs`. Each handler is added into the logger using the `addHandler()` function.

If we then create these logs:
```python
logger.warning('This is a warning')
logger.error('This is an error')
```

The following logs will be printed into the console:
```
This is a warning
This is an error
```

Meanwhile, `errors.log` will only contain:
```
This is an error
```

When `This is a warning` was received by the logger, `handler1` caught the log and processed it accordingly. When `This is an error` was received by the logger, `handler1` ignored the log because it was above the expected level, but `handler2` was able to catch it because it was able to handle logs of level `ERROR`. 

## Creating custom formatters
We’ve been using default formatting for the loggers we’ve created so far. To customise log formats, we use the logging module’s `Formatter` class. A `Formatter` can only be added to a handler, and not to a custom logger.

Going back to the example of the two handlers above, let’s say we want to have each handler output the logs in a particular format. `handler1` will output the log name, log level, timestamp, and log message; while `handler2` will output just the log name, timestamp, and message.

```python
# Handler 1 formatter
formatter1 = logging.Formatter('%(name)s: %(levelname)s: %(asctime)s - %(message)s')
handler1.setFormatter(formatter1)

# Handler 2 formatter
formatter2 = logging.Formatter('%(name)s: %(asctime)s - %(message)s')
handler2.setFormatter(formatter2)
```

Then creating the following logs:
```python
logger.warning('This is a warning')
logger.error('This is an error')
```

The following will be printed into the console:
```
logger: WARNING: 2023-05-02 19:59:41,803 - This is a warning
logger: ERROR: 2023-05-02 19:59:41,804 - This is an error
```

Meanwhile, only the following will be printed inside the `errors.log` file:
```
logger: 2023-05-02 19:59:41,804 - This is an error
```

In the above example, `handler1`  was able to process both the warning and error logs because it was configured at `DEBUG` level. It then formats each log through its attached formatter upon printing the output to the console. `handler2`, on the other hand, only processed the error log and formatted that log through its attached formatter upon printing the output to the file.

---

In this article, we’ve explored some fundamental concepts around logging in Python - log levels, handlers, and formatters. By leveraging these three concepts in production code, we can smoothly enforce some standard logging for debugging and other observability checks.

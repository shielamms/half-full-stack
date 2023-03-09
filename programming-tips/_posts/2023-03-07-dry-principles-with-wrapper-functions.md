---
layout: post
title: Observing DRY principles with wrapper functions
slug: dry-principles-with-wrapper-functions
date:   2023-03-06 13:00:00 +0100
categories: [programming-tips]
tags: [python, logging]
---

_Write once and minimise repetitive code with wrappers._

---

Say you have a bunch of functions in your codebase and you want to print out logs whenever a function is run. If you only have a couple of functions, it probably wouldn't hurt to do something like this:

```python
import logging

def function_1():
    logging.info('Starting function_1...')
    print('foo')
    logging.info('function_1 executed successfully!')

def function_2():
    logging.info('Starting function_2...')
    print('bar')
    logging.info('function_2 executed successfully!')

```

But as your codebase grows and you keep adding more functions, you'll start to realise just how repetitive your code becomes (i.e., printing out the same kind of logs in each function). For this, you can leverage the power of **wrapper functions**, which are a way to extend what your functions can do without having to modify their implementation. Let's take the logging example above to illustrate how wrapper functions can help clean up your repetitive code.

```python
def log_me(fn):
    def log_fn():
        logging.info(f'Starting {fn.__name__}...')
        result = fn()
        logging.info(f'{fn.__name__} successfully executed.')
        return result
    return log_fn

```

A wrapper function consists of an outer function and an inner function. In the example above, `log_me()` is the outer function that takes another function as a parameter. `log_fn()` is the inner function that contains the implementation to extend the functionality of `fn` that was passed as a parameter. The `log_me()` function can be used to "wrap around" any other function in your code where you want to implement the extension done by its inner `log_fn()` function.

To use `log_me()` to "wrap around" another function, we use the python decorator syntax just right before the function definition:

```python
@log_me
def function_1():
    print('foo')

@log_me
def function_2():
    print('bar')
```

Running `function_1()` will result to the following:
```
Starting function_1...
foo
function_1 successfully executed.
```

Similarly, running `function_2()` will result to the following:
```
Starting function_2...
bar
function_2 successfully executed.
```

Notice that we only needed to implement logging once through the wrapper function. Then we just decorated the functions that we wanted to add logging to, without having to modify the functions themselves. Wrappers allow functions that contain our main business logic to remain as they are while we extend their implementation for other things we may want to do to several functions. They also allow us to define a single implementation for extending functionality, i.e., making a change to the wrapper function changes its implementation on all the functions that it wraps around - no need to repetitively modify several functions!

## Another use case: timing your functions

As you have already seen, wrapper functions are a great way to avoid repetitive code. They come in handy whenever I need to do some checks on how my functions are performing. The example below demonstrates the use of a wrapper function to measure the execution time of another function that it wraps around.

```python
import time

def time_me(fn):
    def get_elapsed_time():
        start = time.time() # or use time.perf_counter()
        fn()
        end = time.time()
        print(f'Elapsed time: {end - start}')
    return get_elapsed_time()

@time_me
def waste_time():
    # some arbitrary operation
    for i in range(1000000):
        i**2
```

The fun thing here is that once I've written `time_me()`, I can just copy-paste this function anywhere and use it on any project where I want to time functions.

## Bonus: Implement unit tests using wrapper functions

Not that I want to reinvent the wheel of what `pytest` or `unittest` does for unit testing, but if you don't want to use third-party libraries to write your unit tests for some reason, you can use a wrapper function to execute multiple test cases.

Let's say you have a function that returns the square of a number `n`:

```python
def square(n):
    return n**2
```

You'd probably have a test function that looks like this:

```python
def test_square(n, expected):
    return expected == square(n)
```

But then if you wanted to run your function on several test cases, you'd write multiple calls to the `test_square()` function, like this:

```python
test_square(1,1)
test_square(2,4)
test_square(3,10) # let's assume 3**2==10 is mathematically correct :D
# ... and so on
```

What if you could just write all your test cases in a list and just execute the test function once? Well, you can do that with a wrapper function!

```python
def test(test_cases):
    def test_function(fn):
        print(f'Running test cases on {fn.__name__}')
        for tc in test_cases:
            # tc[0] is the test input value, tc[1] is the expected value
            res = fn(tc[0], tc[1])
            if res:
                print(tc, 'PASSED')
            else:
                print(tc, 'FAILED')
    return test_function

```

In the example above, the outer function receives a parameter called `test_cases`, which is a the list of test cases that you would like to test on. The inner function `test_function()` loops through each test case, where each test case is a pair of test input and expected result value. It then prints out a "PASS" or "FAIL" depending on the result returned by the function `fn` that you want to test.

To use this wrapper function, just put it as a decorator to the function that you want to test:

```python
@test([(1,1), (2,4), (3,10)])
def test_square(n, expected):
    return expected == square(n)
```

Observe that the `@test` decorator has a parameter which is a list. This list contains your test cases. In the example above, the original test function `test_square()` receives two parameters: `n` and `expected`, so each test case is a tuple pair of input n and expected result. For example `(2,4)` means that the test case input value is 2, and the expected value returned from the `square()` function is 4.

Running this test produces the following:

```
Running test cases on test_square
(1, 1) PASSED
(2, 4) PASSED
(3, 10) FAILED
```

---

Wrapper functions are powerful. They can look a bit intimidating at first (a function within a function can be hard to wrap your head around..pun intended), but as your codebase grows bigger, wrapper functions can be a scalable way of implementing observability checks like logging and performance measures. They also help your project look tidier by removing the mud of repetitive lines of code.

Happy coding!

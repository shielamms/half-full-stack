---
layout: post
title: Organise your Python Environment Setup
slug: organise-python-environment-setup
date:   2023-03-06 13:00:00 +0100
categories: [python-tips]
tags: [python]
---

Ok, so you probably have a new development machine. And you also probably want to set up a Python environment so you can start coding right away. Chances are that you already have a bunch of python projects in some repository somewhere and want to check them out and run them on your new machine. For that, you'll need to setup your python tools correctly from the start so you can just easily switch between your projects without much repetition. I often use a two-step setup consisting of a python version manager and a virtual environment manager - and that's pretty much all I need to get started. This is how I would normally start my python setup in a new local machine. I tend to install more lightweight software than all-in-one packages just so I have a feeling of control over the resources I use and I could understand the basic steps better.

## 1. Install a python version manager

If you think that you'll be working on several python projects with different requirements, installing a python version manager from the get-go is a must for productivity. This way, you don't need to worry about keeping track of which python versions you have installed in your system and where to find their respective binaries. In addition, you'll be able to spin up new environments with different python versions much more quickly.

A lot of people use Anaconda since it's so convenient to set up and it already includes a package manager and a virtual environment manager. But Anaconda takes quite a lot of space in my disk for things I won't normally use anyway. And I found `conda` commands are not very intuitive for me, so I always go for `pyenv` instead.

```
brew install pyenv
```

Pyenv is a simple and lightweight python version manager that can help you easily switch between different python versions either globally throughout your system or locally in a single project folder. For instance, you could set python 3.10 as your global version (or default), but you can also install and set python 3.6 in one of your projects, or python 2 in another project.

### Installing a python version

To check all the python versions that are available through pyenv, type:

```
pyenv install -l
```

Once you've determined what python version you need, you can install it by running the following command (Note: This will not set your global or local version yet.)

```
pyenv install 3.10.10
```

After this finishes installing, you can check the new installed version in your pyenv versions:

```
pyenv versions
```

### Set the global python version

To set the version that you just installed above as your global python version, run the following:
```
pyenv global 3.10.10
```

Note that you need to have the version installed first before you can set it as your global version.

To verify that you have set the correct global version, just type:
```
python -V
```

### Set a local python version

You can specify a python version to use in a particular project or directory. For exmaple, if you want to use python 3.6 in a folder named `my-new-project`, first install the version:

```
pyenv install 3.6.0
```

Then set up the version inside the folder:
```
mkdir my-new-project
cd my-new-project
pyenv local 3.6.0
```

Whenever your current working directory the `my-new-project` folder, your terminal will refer to the locally set python version in that folder. In other words, doing `python -V` inside the `my-new-project` folder will print out python 3.6.0 instead of 3.10.10.

You can repeat this process of setting up local versions in any new project in your system. It's a quick and convenient way to switch between your python projects without worrying about version problems whenever you do so.


## 2. Install a python virtual environment manager

Python virtual environments are much like local pyenv environments, with the main difference being that virtual environments are symbolic links to your python path. This means that you can have multiple virtual environments running the same version of python but different library dependencies. This is especially handy for single-repository projects that contain multiple projects - all projects may be running on the same python base version, but each has its own set of library requirements for setup.

`virtualenv` is a python virtual environment manager that allows you to spin up a virtual environment on top of your local or system installation of python. To install `virtualenv` on MacOS:

```
brew install virtualenv
```

Then to create a virtual environment:

```
virtualenv venv
```
where `venv` is an arbitrary environment name. For simplicity in practice, developers just use the name "venv".

You then need to activate the virtual environment:

```
source venv/bin/activate
```

The above command takes you inside the virtual environment in your terminal. You can proceed to installing your project's dependencies, perhaps with something like:

```
pip install -r requirements.txt
```

---

Hope this two-step process would be useful for you whenever you're working in a new machine! It certainly has been for me!

Happy coding!

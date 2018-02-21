# lab-flask-tdd

[![Build Status](https://travis-ci.org/rofrano/lab-flask-tdd.svg?branch=master)](https://travis-ci.org/rofrano/lab-flask-tdd)
[![Codecov](https://img.shields.io/codecov/c/github/rofrano/lab-flask-tdd.svg)]()

NYU DevOps lab on Test Driven Development

## Introduction

One of my favorite quotes is:

_“If it's worth building, it's worth testing.
If it's not worth testing, why are you wasting your time working on it?”_

As Software Engineers we need to have the discipline to ensure that our code works as expected and continues to do so regardless of any changes, refactoring, or the introduction of new functionality.

This lab introduces Test Driven Development using `PyUnit` and `nose` (a.k.a. `nosetests`). It also demonstrates how to create a simple RESTful service using Python Flask and SQLite.
The resource model is persistences using SQLAlchemy to keep the application simple. It's purpose is to show the correct API calls and return codes that should be used for a REST API.

**Note:** The base service code is contained in `server.py` while the business logic for manipulating Pets is in the `models.py` file. This follows the popular Model View Controller (MVC) separation of duities by keeping the model separate from the controller. As such, we have two tests suites: one for the model (`test_pets.py`) and one for the serveice itself (`test_server.py`)

## Prerequisite Installation using Vagrant

The easiest way to use this lab is with Vagrant and VirtualBox. if you don't have this software the first step is down download and install it.

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)

Then all you have to do is clone this repo and invoke vagrant:

    git clone https://github.com/nyu-devops/lab-flask-tdd.git
    cd lab-flask-tdd
    vagrant up
    vagrant ssh
    cd /vagrant

You can now run `nosetests` to run the tests. As developers we always want to run the tests before we change any code so that we know if we brike the code or perhaps someone before us did? Always run the test cases first!

## Manually running the Tests

Run the tests using `nose`

    $ nosetests

Nose is configured via the included `setup.cfg` file to automatically include the flags `--with-spec --spec-color` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

Nose is also configured to automatically run the `coverage` tool and you should see a percentage of coverage report at the end of your tests. If you want to see what lines of code were not tested use:

    $ coverage report -m

This is particularly useful because it reports the line numbers for the code that is not covered so that you can write more test cases to get higher code coverage.

You can also run the Code Coverage tool manually without `nosetests` to see how well your test cases exercise your code:

    $ coverage run test_server.py
    $ coverage report -m --include=server.py

You can also manually run `nosetests` with `coverage` (but `setup.cfg` does this already)

    $ nosetests --with-coverage --cover-package=server

Try and get as close to 100% coverage as you can.

It's also a good idea to make sure that your Python code follows the PEP8 standard. `flake8` has been included in the `requirements.txt` file so that you can check if your code is compliant like this:

    $ flake8 --count --max-complexity=10 --statistics model,server

I've also include `pylint` in the requirements. If you use a programmer's editor like Atom.io you can install plug-ins that will use `pylint` while you are editing. This catches a lot of errors while you code that would normally be caught at runtime. It's a good idea to always code with pylint active.

When you are done, you can exit and shut down the vm with:

    $ exit
    $ vagrant halt

If the VM is no longer needed you can remove it with:

    $ vagrant destroy


## What's featured in the project?

    * server.py -- the main Service using Python Flask
    * models.py -- the data model using SQLAlchemy
    * tests/test_server.py -- test cases against the service
    * tests/test_pets.py -- test cases against the Pet model

This repo is part of the CSCI-GA.3033-013: **DevOps** course at NYU created by John Rofrano.

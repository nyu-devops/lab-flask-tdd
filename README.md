# lab-flask-tdd

[![Build Status](https://travis-ci.org/nyu-devops/lab-flask-tdd.svg?branch=master)](https://travis-ci.org/nyu-devops/lab-flask-tdd)
[![Codecov](https://codecov.io/gh/nyu-devops/lab-flask-tdd/branch/master/graph/badge.svg)](https://codecov.io/gh/nyu-devops/lab-flask-tdd/branch/master/graph/badge.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

NYU DevOps lab on Test Driven Development

## Introduction

One of my favorite quotes is:

_“If it's worth building, it's worth testing.
If it's not worth testing, why are you wasting your time working on it?”_

As Software Engineers we need to have the discipline to ensure that our code works as expected and continues to do so regardless of any changes, refactoring, or the introduction of new functionality.

This lab introduces **Test Driven Development** using `PyUnit` and `nose` (a.k.a. `nosetests`). It also demonstrates how to create a simple RESTful service using Python Flask and PostgreSQL. The resource model is persistences using SQLAlchemy to keep the application simple. It's purpose is to show the correct API calls and return codes that should be used for a REST API.

**Note:** The base service code is contained in `routes.py` while the business logic for manipulating Pets is in the `models.py` file. This follows the popular Model View Controller (MVC) separation of duities by keeping the model separate from the controller. As such, we have two test suites: one for the model (`test_pets.py`) and one for the service itself (`test_service.py`)

## Prerequisite Installation using Vagrant

The easiest way to use this lab is with Vagrant and VirtualBox. If you don't have this software the first step is to download and install it. If you have an 2020 or newer Apple Mac with the M1 chip, you should download Docker Desktop instead of VirtualBox. Here is what you need:

Download: [Vagrant](https://www.vagrantup.com/)

Intel Download: [VirtualBox](https://www.virtualbox.org/)

Apple M1 Download: [Apple M1 Tech Preview](https://docs.docker.com/docker-for-mac/apple-m1/)

Install each of those. Then all you have to do is clone this repo and invoke vagrant:

### Using Vagrant and VirtualBox

```shell
git clone https://github.com/nyu-devops/lab-flask-tdd.git
cd lab-flask-tdd
vagrant up
```

### Using Vagrant and Docker Desktop

You can also use Docker as a provider instead of VirtualBox. This is useful for owners of Apple M1 Silicon Macs which cannot run VirtualBox because they have an ARM-based CPU  architecture instead of x86 (Intel).

Just add `--provider docker` to the `vagrant up` command like this:

```sh
git clone https://github.com/nyu-devops/lab-flask-tdd.git
cd lab-flask-tdd
vagrant up --provider docker
```

This will use a Docker container instead of a Virtual Machine (VM). Everything else should be the same.

## Running the tests

You can now `ssh` into the virtual machine and run the service and the test suite:

```sh
vagrant ssh
cd /vagrant
```

You will now be inside the Linux virtual machine so all commands will be Linux commands.

## Running the service

The project uses *honcho* which gets it's commands from the `Procfile`. To start the service simply use:

```shell
$ honcho start
```

You should be able to reach the service at: http://localhost:5000

## Manually running the Tests

As developers we always want to run the tests before we change any code. That way we know if we broke the code or if someone before us did. Always run the test cases first!

Run the tests using `nosetests`

```shell
$ nosetests
```

Nose is configured via the included `setup.cfg` file to automatically include the flags `--with-spec --spec-color` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

Nose is also configured to automatically run the `coverage` tool and you should see a percentage-of-coverage report at the end of your tests. If you want to see what lines of code were not tested use:

```shell
$ coverage report -m
```

This is particularly useful because it reports the line numbers for the code that have not been covered so you know which lines you want to target with new test cases to get higher code coverage.

You can also manually run `nosetests` with `coverage` (but `setup.cfg` does this already)

```shell
$ nosetests --with-coverage --cover-package=service
```

Try and get as close to 100% coverage as you can.

It's also a good idea to make sure that your Python code follows the PEP8 standard. `flake8` has been included in the `requirements.txt` file so that you can check if your code is compliant like this:

```shell
$ flake8 --count --max-complexity=10 --statistics model,service
```

I've also included `pylint` in the requirements. If you use a programmer's editor like Atom.io you can install plug-ins that will use `pylint` while you are editing. This catches a lot of errors while you code that would normally be caught at runtime. It's a good idea to always code with pylint active.

When you are done, you can exit and shut down the vm with:

```shell
$ exit
$ vagrant halt
```

If the VM is no longer needed you can remove it with:

```shell
$ vagrant destroy
```

## What's featured in the project?

    * app/routes.py -- the main Service routes using Python Flask
    * app/models.py -- the data model using SQLAlchemy
    * tests/test_service.py -- test cases against the Pet service
    * tests/test_pets.py -- test cases against the Pet model

This repo is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created by John Rofrano.

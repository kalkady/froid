.. _install:

### Installation

#### Installation via pip

The recommended way to install **froid** is via `pip`.

```shell
$ pip install froid
```

For instructions on installing python and pip see “The Hitchhiker’s Guide to Python” 
[Installation Guides](https://docs.python-guide.org/starting/installation/).

#### Building from source

`froid` is actively developed on [https://github.com](https://github.com/achillesrasquinha/froid)
and is always avaliable.

You can clone the base repository with git as follows:

```shell
$ git clone https://github.com/achillesrasquinha/froid
```

Optionally, you could download the tarball or zipball as follows:

##### For Linux Users

```shell
$ curl -OL https://github.com/achillesrasquinha/tarball/froid
```

##### For Windows Users

```shell
$ curl -OL https://github.com/achillesrasquinha/zipball/froid
```

Install necessary dependencies

```shell
$ cd froid
$ pip install -r requirements.txt
```

Then, go ahead and install froid in your site-packages as follows:

```shell
$ python setup.py install
```

Check to see if you’ve installed froid correctly.

```shell
$ froid --help
```
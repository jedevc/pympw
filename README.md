# pympw

**WARNING**: This branch is in development and is unstable. Do not use it for
anything important.

pympw is a master password generation tool based on
[Master Password](https://github.com/Lyndir/MasterPassword). I loved the idea,
and I wanted to try writing my own (unofficial) version of it.

## Installation

Setting up pympw is simple.

	$ git clone https://github.com/jedevc/pympw.git
	$ cd pympw
	$ python setup.py install

Done!

## Usage

Running pympw is simple. Provide the commandline arguments that you need, and
then enter your master password when prompted. Here are a few examples:

	$ mpw -p 'James Smith' github.com  # generate a password
	Master Password:
	Site Password: "XamiJeqaDiku5["

	$ mpw -p 'James Smith' github.com -c 3  # generate a password with an explicit site counter
	Master Password:
	Site Password: "CeyhCosaYoru7@"

	$ mpw -p 'James Smith' github.com -t maximum  # generate a maximum security password
	Master Password:
	Site Password: "n5:@PVWg&g9ACZz8fdCh"

pympw comes with its own built in help. To access it, simply execute the following:

	$ mpw --help

For more information on Master Password, see [here](http://masterpasswordapp.com/).

## Goals

- Master key caching
- Storage of site data

## Development

To setup pympw for development, simply follow the steps below. Note that
there's no requirement to use virtualenv, I just tend to find it a lot simpler
to manage multiple projects that way.

	# clone repo
	$ git clone https://github.com/jedevc/pympw.git
	$ cd pympw

	# setup virtualenv (optional)
	$ virtualenv venv
	$ source venv/bin/activate

	# install dependencies
	$ pip install -r requirements.txt

To run pympw, simply run ```python main.py``` with appropriate arguments.

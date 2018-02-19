# pympw

pympw is a master password generation tool based on
[Master Password](https://github.com/Lyndir/MasterPassword). I loved the idea,
and I wanted to try writing my own (unofficial) version of it.

## Installation

Currently there are no neat installation instructions :(

However, you can setup pympw by running the development instructions below.

## Usage

Running pympw is simple. Provide the commandline arguments that you need, and
then enter your master password when prompted. Here are a few examples:

	$ python main.py 'James Smith' github.com  # generate a password
	Master Password:
	Site Password: XamiJeqaDiku5[

	$ python main.py 'James Smith' github.com -c 3  # generate a password with an explicit site counter
	Master Password:
	Site Password: CeyhCosaYoru7@

	$ python main.py 'James Smith' github.com -t maximum  # generate a maximum security password
	Master Password:
	Site Password: n5:@PVWg&g9ACZz8fdCh

For more usage of Master Password, see [here](http://masterpasswordapp.com/).

## Features

- [x] Generate passwords
- [x] Command line interface
- [x] Increase counter
- [ ] Multiple versions of algorithm
- [ ] Storage of sites and passwords

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

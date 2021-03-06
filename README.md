# pympw

pympw is a master password generation tool that relies on the [Master
Password](https://github.com/Lyndir/MasterPassword) algorithm.

## Installation

Setting up pympw is pretty straightforward.

	$ git clone https://github.com/jedevc/pympw.git
	$ cd pympw
	$ pip install .

To install a desktop launcher, simply copy one of the .desktop files from
`data/applications/' to a location that your desktop environment will read.

	$ cp data/applications/mpw.desktop ~/.local/share/applications/

## Usage

Running pympw is simple. Provide the commandline arguments that you need, and
then enter your master password when prompted. Here are a few examples using
the password `hunter2`.

	$ mpw gen 'James Smith' github.com -p # generate a password
	Master Password:
	Site Password: "PiloCiwm9.Qupa"

	$ mpw gen 'James Smith' github.com -p -c3  # generate a password with an explicit site counter
	Master Password:
	Site Password: "YipyMibf7'Yiwo"

	$ mpw gen 'James Smith' github.com -p -t maximum  # generate a maximum security password
	Master Password:
	Site Password: "cKnotHyu3)h04qiPZh1%"

If that's too much work for you, pympw can also create a prompt for you.

	$ mpw prompt
	Name: James Smith
	Version (3):
	Master Password:
	----------------------------------------
	Site: github.com
	Template (long):
	Counter (1):
	Site Password: "PiloCiwm9.Qupa"

	$ mpw dprompt
	--> presents a dialog interface

pympw comes with its own built in help. To access it, simply execute the
following:

	$ mpw --help

For more information on Master Password, see [here](http://masterpasswordapp.com/).

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

To run pympw, execute ```python -m mpw``` with appropriate arguments.
To run the tests, execute ```python -m unittest```.

## Goals

- Key expiry for prompts
- Storage of site data

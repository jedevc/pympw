# =============================================================================
#
#  Copyright (c) 2017, Justin Chadwell.
#
#  This program is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You can find a copy of the GNU General Public License in the LICENSE file.
#  Alternatively, see <http://www.gnu.org/licenses/>.
#
# =============================================================================

import argparse

from . import algorithm
from . import cmd

def main():
    parser = argparse.ArgumentParser(description='A password manager using the MasterPassword algorithm.')
    subparsers = parser.add_subparsers(title='subcommands')

    generate = subparsers.add_parser('generate', aliases=['gen'],
            help='Generate a password')
    generate.set_defaults(func=cmd.generate)
    generate.add_argument('name', help='Your full name')
    generate.add_argument('site', help='The site name')
    generate.add_argument('-t', '--template', default='long',
            choices=algorithm.TEMPLATE_TYPES.keys(),
            help='The password type template')
    generate.add_argument('-c', '--counter', type=int, default=1,
            help="The site's password counter")
    generate.add_argument('-v', '--version', type=int, default=3,
            choices=[0, 1, 2, 3], help='MasterPassword algorithm version')
    generate.add_argument('-p', '--print', action='store_true',
            help="Print the password to stdout")
    generate.add_argument('-x', '--cut', action='store_true',
            help='Paste the password to the system clipboard')

    prompt = subparsers.add_parser('prompt',
            help='Generate a password with the help of a prompt')
    prompt.set_defaults(func=cmd.prompt)
    prompt.add_argument('-n', '--name', help='Your full name')
    prompt.add_argument('-s', '--site', help='The site name')
    prompt.add_argument('-t', '--template',
            choices=algorithm.TEMPLATE_TYPES.keys(),
            help='The password type template')
    prompt.add_argument('-c', '--counter', type=int,
            help="The site's password counter")
    prompt.add_argument('-v', '--version', type=int, default=3,
            choices=[0, 1, 2, 3], help='MasterPassword algorithm version')
    prompt.add_argument('-p', '--print', action='store_true',
            help="Print the password to stdout")
    prompt.add_argument('-x', '--cut', action='store_true',
            help='Paste the password to the system clipboard')

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

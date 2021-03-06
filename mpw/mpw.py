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

import sys
import argparse

from . import algorithm
from . import cmd

def main(*arglist):
    # mpw
    parser = argparse.ArgumentParser(description='Manage your passwords using the MasterPassword algorithm')
    subparsers = parser.add_subparsers(title='subcommands')

    # mpw generate
    generate = subparsers.add_parser('generate', aliases=['gen'],
            help='Generate a password')
    generate.set_defaults(func=cmd.generate)
    generate.add_argument('name', help='Your full name')
    generate.add_argument('-v', '--version', type=int, default=3,
            choices=[0, 1, 2, 3], help='MasterPassword algorithm version')
    generate.add_argument('site', help='The site name')
    generate.add_argument('-t', '--template', default='long',
            choices=algorithm.TEMPLATE_TYPES,
            help='The password type template')
    generate.add_argument('-c', '--counter', type=int, default=1,
            help="The site's password counter")
    generate.add_argument('-p', '--stdout', '--print', action='store_true',
            help='Print the password to stdout')
    generate.add_argument('-x', '--clipboard', '--copy', action='store_true',
            help='Copy the password to the system clipboard')

    # mpw prompt
    prompt = subparsers.add_parser('prompt',
            help='Generate a password with the help of a prompt')
    prompt.set_defaults(func=cmd.prompt)
    prompt.add_argument('-n', '--name', help='Your full name')
    prompt.add_argument('-v', '--version', type=int, default=3,
            choices=[0, 1, 2, 3], help='MasterPassword algorithm version')
    prompt.add_argument('-s', '--site', help='The site name')
    prompt.add_argument('-t', '--template', default='long',
            choices=algorithm.TEMPLATE_TYPES,
            help='The password type template')
    prompt.add_argument('-c', '--counter', type=int, default=1,
            help="The site's password counter")
    prompt.add_argument('-p', '--stdout', action='store_true',
            help='Print the password to stdout')
    prompt.add_argument('-x', '--clipboard', action='store_true',
            help='Copy the password to the system clipboard')
    prompt.add_argument('-l', '--loop', action='store_true',
            help='Read site details in a loop')

    # mpw dialog-prompt
    dialog = subparsers.add_parser('dialog-prompt', aliases=['dialog', 'dprompt'],
            help='Generate a password with the help of a dialog')
    dialog.set_defaults(func=cmd.dprompt)
    dialog.add_argument('-n', '--name', default='', help='Your full name')
    dialog.add_argument('-v', '--version', type=int, default=3,
            choices=[0, 1, 2, 3], help='MasterPassword algorithm version')
    dialog.add_argument('-s', '--site', default='', help='The site name')
    dialog.add_argument('-t', '--template', default='long',
            choices=algorithm.TEMPLATE_TYPES,
            help='The password type template')
    dialog.add_argument('-c', '--counter', type=int, default=1,
            help="The site's password counter")
    dialog.add_argument('-p', '--stdout', action='store_true',
            help='Print the password to stdout')
    dialog.add_argument('-x', '--clipboard', action='store_true',
            help='Copy the password to the system clipboard')
    dialog.add_argument('-l', '--loop', action='store_true',
            help='Read site details in a loop')

    if arglist:
        args = parser.parse_args(arglist)
    else:
        args = parser.parse_args()

    if hasattr(args, 'func'):
        try:
            args = vars(args)
            func = args.pop('func')
            return func(**args)
        except EOFError:  # keyboard exit code (Ctrl+d)
            print()
    else:
        parser.print_help()

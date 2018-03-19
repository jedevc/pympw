# =============================================================================
#
#  Copyright (c) 2011-2017, Justin Chadwell (@jedevc).
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
# 
#  This is a python implementation of the Master Password algorithm, found at
#  <https://github.com/Lyndir/MasterPassword>.
#
#  All credit for the algorithm goes to Maarten Billemont.
#

import argparse
import subprocess
from getpass import getpass

from . import algorithm
from .algorithm import Algorithm

def main():
    parser = argparse.ArgumentParser(description = 'Generate a password using the MasterPassword algorithm.')

    # input options
    parser.add_argument('name', help = 'Your full name')
    parser.add_argument('site', help = 'The site name')
    parser.add_argument('-t', '--template', default = 'long',
            choices = algorithm.TEMPLATE_TYPES.keys(),
            help = 'The password type template')
    parser.add_argument('-c', '--counter', type = int, default = 1,
            help = "The site's password counter")
    parser.add_argument('-v', '--version', type = int, default = 3,
            choices = [0, 1, 2, 3],
            help = 'MasterPassword algorithm version')

    # output options
    parser.add_argument('-p', '--print', action = 'store_true',
            help = "Print the password to stdout")
    parser.add_argument('-x', '--cut', action = 'store_true',
            help = 'Paste the password to the system clipboard')

    args = parser.parse_args()

    # get master password
    password = getpass('Master Password: ')

    # generate site password
    gen = Algorithm(args.version)
    key = gen.master_key(password, args.name)
    site_seed = gen.site_seed(key, args.site, args.counter)
    site_password = gen.site_password(site_seed, args.template)

    # output site password
    if args.print:
        print('Site Password: "{}"'.format(site_password))
    if args.cut:
        clipboard_copy(site_password)

def clipboard_copy(data):
    '''
    Utility function to copy a string to the system clipboard.

    Args:
        data: The data to copy to the clipboard.
    '''

    proc = subprocess.run(['xsel', '-bi'], input = data.encode('utf8'))
    proc.check_returncode()

if __name__ == "__main__":
    main()

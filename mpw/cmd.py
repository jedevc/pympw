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

import subprocess
from getpass import getpass
from shutil import get_terminal_size

from . import algorithm

def generate(args):
    password = getpass('Master Password: ')

    gen = algorithm.Algorithm(args.version)
    key = gen.master_key(password, args.name)
    site_seed = gen.site_seed(key, args.site, args.counter)
    site_password = gen.site_password(site_seed, args.template)

    if args.print:
        print('Site Password: "{}"'.format(site_password))
    if args.cut:
        clipboard_copy(site_password)

def prompt(args):
    name = args.name or input('Name: ')
    if not name: raise ValueError('empty string')

    password = getpass('Master Password: ')

    version = int(args.version or input('Version (3): ') or 3)
    if not 0 <= version <= 3:
        raise ValueError('invalid version number')

    while True:  # do while loop
        cols = get_terminal_size()[0]
        print('-' * cols)

        site = args.site or input('Site: ')
        if not site: raise ValueError('empty string')

        template = args.template or input('Template (long): ') or 'long'
        if template not in algorithm.TEMPLATE_TYPES.keys():
            raise KeyError('invalid template type')

        counter = int(args.counter or input('Counter (1): ') or 1)

        gen = algorithm.Algorithm(version)
        key = gen.master_key(password, name)
        site_seed = gen.site_seed(key, site, counter)
        site_password = gen.site_password(site_seed, template)

        if args.print:
            print('Site Password: "{}"'.format(site_password))
        if args.cut:
            clipboard_copy(site_password)

        if not args.loop: break

def clipboard_copy(data):
    '''
    Utility function to copy a string to the system clipboard.

    Args:
        data: The data to copy to the clipboard.
    '''

    proc = subprocess.run(['xsel', '-bi'], input=data.encode('utf8'))
    proc.check_returncode()

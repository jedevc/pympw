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
    if not args.name:
        args.name = input('Name: ')
        if not args.name: raise ValueError('empty string')
    if not args.site:
        args.site = input('Site: ')
        if not args.site: raise ValueError('empty string')
    if not args.template:
        args.template = input('Template (long): ') or 'long'
        if args.template not in algorithm.TEMPLATE_TYPES.keys(): 
            raise KeyError('invalid template type')
    if not args.counter:
        args.counter = int(input('Counter (1): ') or 1)
    if not args.version:
        args.version = int(input('Version (3): ') or 3)
        if 0 <= args.version <= 3:
            raise ValueError('invalid version number')

    password = getpass('Master Password: ')

    gen = algorithm.Algorithm(args.version)
    key = gen.master_key(password, args.name)
    site_seed = gen.site_seed(key, args.site, args.counter)
    site_password = gen.site_password(site_seed, args.template)

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

    proc = subprocess.run(['xsel', '-bi'], input=data.encode('utf8'))
    proc.check_returncode()
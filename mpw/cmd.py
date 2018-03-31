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

import dialog

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
    # details prompt
    name = args.name or input('Name: ')
    if not name: raise ValueError('empty string')

    version = int(args.version or input('Version (3): ') or 3)
    if not 0 <= version <= 3:
        raise ValueError('invalid version number')

    # password prompt
    while True:
        password = getpass('Master Password: ')
        if len(password) == 0:
            raise ValueError('zero length password')
        else:
            break

    # setup master password
    gen = algorithm.Algorithm(version)
    key = gen.master_key(password, name)

    while True:  # do while loop
        cols = get_terminal_size()[0]
        print('-' * cols)

        # site prompt
        site = args.site or input('Site: ')
        if not site: raise ValueError('empty string')

        template = args.template or input('Template (long): ') or 'long'
        if template not in algorithm.TEMPLATE_TYPES.keys():
            raise ValueError('invalid template type')

        counter = int(args.counter or input('Counter (1): ') or 1)

        site_seed = gen.site_seed(key, site, counter)
        site_password = gen.site_password(site_seed, template)

        # output
        if args.print:
            print('Site Password: "{}"'.format(site_password))
        if args.cut:
            clipboard_copy(site_password)

        if not args.loop: break

def dialog_prompt(args):
    d = dialog.Dialog()

    offset = 10

    # details dialog
    name = args.name
    version = args.version
    while True:
        status, elements = d.form('Enter your login details.', [
            ('Name', 1, 0, name, 1, offset, 128, 0),
            ('Version', 2, 0, str(version), 2, offset, 4, 0)
        ])
        if status != d.OK: return

        # parse entries
        name = elements[0]
        try:
            version = int(elements[1])
        except ValueError:
            version = None

        # error messages
        if len(name) == 0:
            d.msgbox('Must input a name.')
        elif not version or not 0 <= version <= 3:
            d.msgbox('Must input a valid version number (0, 1, 2, 3).')
            version = args.version
        else:
            break

    # password dialog
    while True:
        status, password = d.passwordbox('Enter your master password.', insecure=True)
        if status != d.OK: return

        if len(password) == 0:
            d.msgbox('Must input a master password.')
        else:
            break

    # setup master password
    gen = algorithm.Algorithm(version)
    key = gen.master_key(password, name)

    while True:  # do while loop
        # site dialog
        site = args.site
        template = args.template
        counter = args.counter
        while True:
            status, elements = d.form('Enter the site details.', [
                ('Site', 1, 0, site, 1, offset, 128, 0),
                ('Template', 2, 0, template, 2, offset, 128, 0),
                ('Counter', 3, 0, str(counter), 3, offset, 128, 0)
            ])
            if status != d.OK: return

            # parse entries
            site = elements[0]
            template = elements[1]
            try:
                counter = int(elements[2])
            except ValueError:
                counter = None

            # error messages
            if len(site) == 0:
                d.msgbox('Must input a sitename.')
            elif template not in algorithm.TEMPLATE_TYPES.keys():
                d.msgbox('Must input a valid template type.')
            elif counter is None:
                d.msgbox('Must input a counter value.')
                counter = args.counter
            else:
                site_seed = gen.site_seed(key, site, counter)
                site_password = gen.site_password(site_seed, template)

                # output
                if args.print:
                    d.msgbox('Site Password: "{}"'.format(site_password))
                if args.cut:
                    clipboard_copy(site_password)

                break

        if not args.loop: break

def clipboard_copy(data):
    '''
    Utility function to copy a string to the system clipboard.

    Args:
        data: The data to copy to the clipboard.
    '''

    proc = subprocess.run(['xsel', '-bi'], input=data.encode('utf8'))
    proc.check_returncode()

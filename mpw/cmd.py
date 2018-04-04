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

from getpass import getpass
from shutil import get_terminal_size

from . import algorithm

def generate(name, version, site, template, counter, stdout, clipboard):
    password = getpass('Master Password: ')

    gen = algorithm.Algorithm(version)
    key = gen.master_key(password, name)
    site_seed = gen.site_seed(key, site, counter)
    site_password = gen.site_password(site_seed, template)

    if stdout:
        print('Site Password: "{}"'.format(site_password))
    if clipboard:
        print('Copied to clipboard.')
        clipboard_copy(site_password)

    return site_password

def prompt(name, version, site, template, counter, stdout, clipboard, loop):
    # input helper function
    def input_conditional(prompt, condition, default = None, type = str):
        while True:
            if default:
                value = input('{} ({}): '.format(prompt, default)) or default
            else:
                value = input('{}: '.format(prompt))

            try:
                value = type(value)
            except ValueError:
                continue

            if condition(value): return value

    # details prompt
    name = input_conditional('Name', lambda x: len(x) != 0, name)
    version = input_conditional('Version', lambda x: 0 <= x <= 3, version, int)

    # password prompt
    while True:
        password = getpass('Master Password: ')
        if len(password) != 0: break

    # setup master password
    gen = algorithm.Algorithm(version)
    key = gen.master_key(password, name)

    while True:
        cols = get_terminal_size()[0]
        print('-' * cols)

        # site prompt
        site = input_conditional('Site', lambda x: len(x) != 0, site)
        template = input_conditional('Template',
                lambda x: x in algorithm.TEMPLATE_TYPES.keys(), template)
        counter = input_conditional('Counter', lambda x: True, 1, int)

        site_seed = gen.site_seed(key, site, counter)
        site_password = gen.site_password(site_seed, template)

        # output
        if stdout:
            print('Site Password: "{}"'.format(site_password))
        if clipboard:
            print('Copied to clipboard.')
            clipboard_copy(site_password)

        if not loop: break

def dprompt(name, version, site, template, counter, stdout, clipboard, loop):
    import dialog

    d = dialog.Dialog()

    offset = 10

    # details dialog
    old_name = name
    old_version = version
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
        errors = []
        if len(name) == 0:
            errors.append('Must input a name.')
            name = old_name
        if not version or not 0 <= version <= 3:
            errors.append('Must input a valid version number (0, 1, 2, 3).')
            version = old_version

        if errors:
            d.msgbox('\n'.join(errors))
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

    old_site = site
    old_template = template
    old_counter = counter
    while True:
        # site dialog
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
            errors = []
            if len(site) == 0:
                errors.append('Must input a sitename.')
                site = old_site
            if template not in algorithm.TEMPLATE_TYPES.keys():
                errors.append('Must input a valid template type.')
                template = old_template
            if counter is None:
                errors.append('Must input a counter value.')
                counter = old_counter

            if errors:
                d.msgbox('\n'.join(errors))
            else:
                site_seed = gen.site_seed(key, site, counter)
                site_password = gen.site_password(site_seed, template)

                # output
                messages = []
                if stdout:
                    msg = 'Site Password: "{}"'.format(site_password)
                    messages.append(msg)
                if clipboard:
                    messages.append('Copied to clipboard.')
                    clipboard_copy(site_password)
                if messages: d.msgbox('\n'.join(messages))

                site = old_site
                template = old_template
                counter = old_counter

                break

        if not loop: break

def clipboard_copy(data):
    '''
    Utility function to copy a string to the system clipboard.

    Args:
        data: The data to copy to the clipboard.
    '''

    import pyperclip

    pyperclip.copy(data)

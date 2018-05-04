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
    key = gen.generate_key(password, name)
    site_password = gen.generate_password(key, site, counter, template)

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
    key = gen.generate_key(password, name)

    while True:
        cols = get_terminal_size()[0]
        print('-' * cols)

        # site prompt
        site = input_conditional('Site', lambda x: len(x) != 0, site)
        template = input_conditional('Template',
                lambda x: x in algorithm.TEMPLATE_TYPES, template)
        counter = input_conditional('Counter', lambda x: True, 1, int)

        site_password = gen.generate_password(key, site, counter, template)

        # output
        if stdout:
            print('Site Password: "{}"'.format(site_password))
        if clipboard:
            print('Copied to clipboard.')
            clipboard_copy(site_password)

        if not loop: break

class DialogPrompt:
    def __init__(self, name, version, site, template, counter, stdout, clipboard, loop):
        self.name = self.default_name = name
        self.version = self.default_version = version
        self.site = self.default_site = site
        self.template = self.default_template = template
        self.counter = self.default_counter = counter

        self.stdout = stdout
        self.clipboard = clipboard
        self.loop = loop

        self.generator = None
        self.key = None

        import dialog
        self.dialog = dialog.Dialog()
        self.offset = 10

    def run(self):
        self.login()
        self.password()

        while True:
            self.generate()
            if not self.loop: break

    def login(self):
        self.name = self.default_name
        self.version = self.default_version

        while True:
            # get entries
            status, elements = self.dialog.form('Enter your login details.', [
                ('Name', 1, 0, self.name, 1, self.offset, 128, 0),
                ('Version', 2, 0, str(self.version), 2, self.offset, 4, 0)
            ])
            if status != self.dialog.OK: return

            # parse entries
            self.name = elements[0]
            try:
                self.version = int(elements[1])
            except ValueError:
                self.version = None

            # error messages
            errors = []
            if len(self.name) == 0:
                errors.append('Must input a name.')
                self.name = self.default_name
            if self.version is None or not 0 <= self.version <= 3:
                errors.append('Must input a valid version number (0, 1, 2, 3).')
                self.version = self.default_version

            if errors:
                self.dialog.msgbox('\n'.join(errors))
            else:
                break

    def password(self):
        while True:
            status, password = self.dialog.passwordbox('Enter your master password.', insecure=True)
            if status != self.dialog.OK: return

            if len(password) == 0:
                self.dialog.msgbox('Must input a master password.')
            else:
                break

        self.generator = algorithm.Algorithm(self.version)
        self.key = self.generator.generate_key(password, self.name)

    def generate(self):
        self.site = self.default_site
        self.template = self.default_template
        self.counter = self.default_counter
        
        while True:
            status, elements = self.dialog.form('Enter the site details.', [
                ('Site', 1, 0, self.site, 1, self.offset, 128, 0),
                ('Template', 2, 0, self.template, 2, self.offset, 128, 0),
                ('Counter', 3, 0, str(self.counter), 3, self.offset, 128, 0)
            ])
            if status != self.dialog.OK: return

            # parse entries
            self.site = elements[0]
            self.template = elements[1]
            try:
                self.counter = int(elements[2])
            except ValueError:
                self.counter = None

            # error messages
            errors = []
            if len(self.site) == 0:
                errors.append('Must input a sitename.')
                self.site = self.default_site
            if self.template not in algorithm.TEMPLATE_TYPES:
                valid = ', '.join(algorithm.TEMPLATE_TYPES.keys())
                errors.append('Must input a valid template type ({}).'.format(valid))
                self.template = self.default_template
            if self.counter is None:
                errors.append('Must input a counter value.')
                self.counter = self.default_counter

            if errors:
                self.dialog.msgbox('\n'.join(errors))
            else:
                site_password = self.generator.generate_password(self.key, self.site, self.counter, self.template)

                # output
                messages = []
                if self.stdout:
                    msg = 'Site Password: "{}"'.format(site_password)
                    messages.append(msg)
                if self.clipboard:
                    messages.append('Copied to clipboard.')
                    clipboard_copy(site_password)
                if messages: self.dialog.msgbox('\n'.join(messages))

                break

def dprompt(*args, **kwargs):
    dp = DialogPrompt(*args, **kwargs)
    dp.run()

def clipboard_copy(data):
    '''
    Utility function to copy a string to the system clipboard.

    Args:
        data: The data to copy to the clipboard.
    '''

    import pyperclip

    pyperclip.copy(data)

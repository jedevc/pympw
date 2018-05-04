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

class Prompt:
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

    def run(self):
        self.login()
        self.password()

        while True:
            cols = get_terminal_size()[0]
            print('-' * cols)

            self.generate()

            if not self.loop: break

    def login(self):
        self.name = self._input_conditional('Name', lambda x: len(x) != 0, self.default_name)
        self.version = self._input_conditional('Version', lambda x: 0 <= x <= 3, self.default_version, int)

    def password(self):
        while True:
            password = getpass('Master Password: ')
            if len(password) != 0: break

        self.generator = algorithm.Algorithm(self.version)
        self.key = self.generator.generate_key(password, self.name)

    def generate(self):
        self.site = self._input_conditional('Site', lambda x: len(x) != 0,
                self.default_site)
        self.template = self._input_conditional('Template',
                lambda x: x in algorithm.TEMPLATE_TYPES, self.default_template)
        self.counter = self._input_conditional('Counter', lambda x: True, self.default_counter, int)

        site_password = self.generator.generate_password(self.key, self.site, self.counter, self.template)

        # output
        if self.stdout:
            print('Site Password: "{}"'.format(site_password))
        if self.clipboard:
            print('Copied to clipboard.')
            clipboard_copy(site_password)

    def _input_conditional(self, prompt, condition, default = None, type = str):
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

def prompt(*args, **kwargs):
    p = Prompt(*args, **kwargs)
    p.run()

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
        '''
        Display the dialog, allowing some basic back-and-forward navigation.
        '''

        while True:
            if not self.login(): return
            if not self.password(): continue

            while True:
                if not self.generate(): break
                if not self.loop: return

    def login(self):
        '''
        Get and store the login details.

        Returns:
            True on a success.
            False on a cancellation.
        '''

        # set defaults
        self.name = self.default_name
        self.version = self.default_version

        while True:
            # get entries
            status, elements = self.dialog.form('Enter your login details.', [
                ('Name', 1, 0, self.name, 1, self.offset, 128, 0),
                ('Version', 2, 0, str(self.version), 2, self.offset, 4, 0)
            ])
            if status != self.dialog.OK: return False

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

        return True

    def password(self):
        '''
        Get and store the master password.

        Returns:
            True on a success.
            False on a cancellation.
        '''

        while True:
            # input password
            status, password = self.dialog.passwordbox('Enter your master password.', insecure=True)
            if status != self.dialog.OK: return False

            # error message
            if len(password) == 0:
                self.dialog.msgbox('Must input a master password.')
            else:
                break

        # calculate master key
        self.generator = algorithm.Algorithm(self.version)
        self.key = self.generator.generate_key(password, self.name)

        return True

    def generate(self):
        '''
        Get the site details and display the site password.

        Returns:
            True on a success.
            False on a cancellation.
        '''

        # set defaults
        self.site = self.default_site
        self.template = self.default_template
        self.counter = self.default_counter
        
        while True:
            # input entries
            status, elements = self.dialog.form('Enter the site details.', [
                ('Site', 1, 0, self.site, 1, self.offset, 128, 0),
                ('Template', 2, 0, self.template, 2, self.offset, 128, 0),
                ('Counter', 3, 0, str(self.counter), 3, self.offset, 128, 0)
            ])
            if status != self.dialog.OK: return False

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
                # calculate site password
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

        return True

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

# ==============================================================================
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
# ==============================================================================
# 
#  This is a python implementation of the Master Password algorithm, found at
#  <https://github.com/Lyndir/MasterPassword>.
#
#  All credit for the algorithm goes to Maarten Billemont.
#

import argparse
import subprocess
from getpass import getpass

from Crypto.Hash import HMAC, SHA256
import scrypt

def main():
    '''
    Wrap master_password_app function by providing a neat argparse interface.
    '''

    parser = argparse.ArgumentParser(description = 'Generate a password according to the MasterPasswordApp algorithm.')

    # input options
    parser.add_argument('-n', '--name', help = 'Your name (used as a salt)')
    parser.add_argument('-s', '--site', help = 'The name of the website')
    parser.add_argument('-t', '--template', choices = TEMPLATE_TYPES.keys(),
            default = 'long', help = 'The type of password to generate')
    parser.add_argument('-c', '--counter', type = int, default = 1,
            help = "The site's password counter")

    # output options
    parser.add_argument('-p', '--print', action = 'store_true',
            help = "Print the password to stdout")
    parser.add_argument('-x', '--cut', action = 'store_true',
            help = 'Paste the password to the system clipboard')

    args = parser.parse_args()

    name = args.name or input('Name: ')
    site = args.site or input('Site: ')

    # get master password
    password = getpass('Master Password: ')

    # generate site password
    key = generate_master_key(password, name)
    site_password = generate_password(key, site, args.counter, args.template)

    # output site password
    if args.print:
        print('Site Password: "{}"'.format(site_password))
    if args.cut:
        clipboard_copy(site_password)

def generate_master_key(master_password, salt_string):
    '''
    Generate the master key using the scrypt algorithm.

    The master key is the result of hashing the master password along with the
    provided salt.
    '''

    salt = utf8(PACKAGE_NAME) + uint_32(len(salt_string)) + utf8(salt_string)
    key = scrypt.hash(utf8(master_password), salt, 32768, 8, 2, 64)

    return key

def generate_password(key, site, counter, template_type):
    '''
    Generate a site password using the seed and the template type.

    The template is iterated through, using the seed to generate characters
    within a range determined by the template.
    '''

    # generate the seed
    msg = utf8(PACKAGE_NAME) + uint_32(len(site)) + utf8(site) + uint_32(counter)
    seed = HMAC.new(key, msg, SHA256).digest()

    # select template
    templates = TEMPLATE_TYPES[template_type]
    template = templates[seed[0] % len(templates)]

    # generate password from template
    site_password = []
    for i, tchar in enumerate(template):
        if tchar == ' ':
            site_password.append(tchar)
        else:
            pchars = CHARACTER_GROUPS[tchar]
            pchar = pchars[seed[i + 1] % len(pchars)]
            site_password.append(pchar)

    return ''.join(site_password)

def clipboard_copy(data):
    '''
    Utility function to copy a string to the system clipboard.
    '''

    proc = subprocess.run(['xsel', '-bi'], input=utf8(data))
    proc.check_returncode()

def uint_32(i):
    '''
    Utility function to convert unsigned integer to bytes
    '''

    return i.to_bytes(4, 'big')

def utf8(s):
    '''
    Utility function to convert string to utf-8 encoded bytes
    '''

    return s.encode('UTF-8')

# the following constants are taken directly from
# http://masterpasswordapp.com/algorithm.html
PACKAGE_NAME = 'com.lyndir.masterpassword'
TEMPLATE_TYPES = {
    'maximum': [
        'anoxxxxxxxxxxxxxxxxx',
        'axxxxxxxxxxxxxxxxxno'
    ],
    'long': [
        'CvcvnoCvcvCvcv',
        'CvcvCvcvnoCvcv',
        'CvcvCvcvCvcvno',
        'CvccnoCvcvCvcv',
        'CvccCvcvnoCvcv',
        'CvccCvcvCvcvno',
        'CvcvnoCvccCvcv',
        'CvcvCvccnoCvcv',
        'CvcvCvccCvcvno',
        'CvcvnoCvcvCvcc',
        'CvcvCvcvnoCvcc',
        'CvcvCvcvCvccno',
        'CvccnoCvccCvcv',
        'CvccCvccnoCvcv',
        'CvccCvccCvcvno',
        'CvcvnoCvccCvcc',
        'CvcvCvccnoCvcc',
        'CvcvCvccCvccno',
        'CvccnoCvcvCvcc',
        'CvccCvcvnoCvcc',
        'CvccCvcvCvccno'
    ],
    'medium': [
        'CvcnoCvc',
        'CvcCvcno'
    ],
    'short': [
        'Cvcn'
    ],
    'basic': [
        'aaanaaan',
        'aannaaan',
        'aaannaaa'
    ],
    'pin': [
        'nnnn'
    ],
    'name': [
        'cvccvcvcv'
    ],
    'phrase': [
        'cvcc cvc cvccvcv cvc',
        'cvc cvccvcvcv cvcv',
        'cv cvccv cvc cvcvccv'
    ]
}
CHARACTER_GROUPS = {
    'V': 'AEIOU',
    'C': 'BCDFGHJKLMNPQRSTVWXYZ',
    'v': 'aeiou',
    'c': 'bcdfghjklmnpqrstvwxyz',
    'A': 'AEIOUBCDFGHJKLMNPQRSTVWXYZ',
    'a': 'AEIOUaeiouBCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz',
    'n': '0123456789',
    'o': "@&%?,=[]_:-+*$#!'^~;()/.",
    'x': "AEIOUaeiouBCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz0123456789!@#$%^&*()"
}

if __name__ == "__main__":
    main()

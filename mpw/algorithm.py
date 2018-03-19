# =============================================================================
#
#  Copyright (c) 2011-2017, Justin Chadwell.
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

from Crypto.Hash import HMAC, SHA256
import scrypt

def Algorithm(version):
    '''
    Create an algorithm object to do all the master password operations.

    Args:
        version: The algorithm version to create.

    Returns:
        An algorithm object.
    '''

    if version == 0:
        return AlgorithmV0
    elif version == 1:
        return AlgorithmV1
    elif version == 2:
        return AlgorithmV2
    elif version == 3:
        return AlgorithmV3
    else:
        raise ValueError('invalid version')

class AlgorithmBase:
    def master_key(master_password, salt_string):
        '''
        Generate the master key.

        Args:
            master_password: A secret string used to derive the key.
            salt_string: A string used to improve the key's security.

        Returns:
            The master key.
        '''

        pass

    def site_seed(key, site, counter):
        '''
        Generate a site password generation seed.

        Args:
            key: The master key.
            site: The site's name.
            counter: The password version to generate.
        '''

        pass

    def site_password(seed, template_type):
        '''
        Generate a site password.

        Args:
            seed: The password generation seed.
            template_type: The type of password to generate.
        '''

        pass

class AlgorithmV0(AlgorithmBase):
    def master_key(master_password, salt_string):
        salt = utf8(PACKAGE_NAME) + \
               uint_32(len(salt_string)) + \
               utf8(salt_string)
        key = scrypt.hash(utf8(master_password), salt, 32768, 8, 2, 64)
        return key

    def site_seed(key, site, counter):
        msg = utf8(PACKAGE_NAME) + \
              uint_32(len(site)) + \
              utf8(site) + \
              uint_32(counter)
        seed = HMAC.new(key, msg, SHA256).digest()
        return seed

    def site_password(seed, template_type):
        seed = list(seed)
        for i, v in enumerate(seed):
            # ported this operation from js to python
            # https://github.com/tmthrgd/mpw-js/blob/master/mpw.js#L219
            seed[i] = (0x00ff if v > 127 else 0x0000) | (v << 8)

        templates = TEMPLATE_TYPES[template_type]
        template = templates[seed[0] % len(templates)]

        password = []
        for i, tchar in enumerate(template):
            if tchar == ' ':
                password.append(tchar)
            else:
                pchars = CHARACTER_GROUPS[tchar]
                pchar = pchars[seed[i + 1] % len(pchars)]
                password.append(pchar)

        return ''.join(password)

class AlgorithmV1(AlgorithmV0):
    def site_password(seed, template_type):
        templates = TEMPLATE_TYPES[template_type]
        template = templates[seed[0] % len(templates)]

        password = []
        for i, tchar in enumerate(template):
            if tchar == ' ':
                password.append(tchar)
            else:
                pchars = CHARACTER_GROUPS[tchar]
                pchar = pchars[seed[i + 1] % len(pchars)]
                password.append(pchar)

        return ''.join(password)

class AlgorithmV2(AlgorithmV1):
    def site_seed(key, site, counter):
        msg = utf8(PACKAGE_NAME) + \
              uint_32(len(utf8(site))) + \
              utf8(site) + \
              uint_32(counter)
        seed = HMAC.new(key, msg, SHA256).digest()
        return seed

class AlgorithmV3(AlgorithmV2):
    def master_key(master_password, salt_string):
        salt = utf8(PACKAGE_NAME) + \
               uint_32(len(utf8(salt_string))) + \
               utf8(salt_string)
        key = scrypt.hash(utf8(master_password), salt, 32768, 8, 2, 64)
        return key

# the following constants are taken directly from
# https://github.com/Lyndir/MasterPassword/blob/master/core/c/mpw-types.c
PACKAGE_NAME = 'com.lyndir.masterpassword'
TEMPLATE_TYPES = {
    'maximum': [
        'anoxxxxxxxxxxxxxxxxx', 'axxxxxxxxxxxxxxxxxno'
    ],
    'long': [
        'CvcvnoCvcvCvcv', 'CvcvCvcvnoCvcv', 'CvcvCvcvCvcvno', 'CvccnoCvcvCvcv',
        'CvccCvcvnoCvcv', 'CvccCvcvCvcvno', 'CvcvnoCvccCvcv', 'CvcvCvccnoCvcv',
        'CvcvCvccCvcvno', 'CvcvnoCvcvCvcc', 'CvcvCvcvnoCvcc', 'CvcvCvcvCvccno',
        'CvccnoCvccCvcv', 'CvccCvccnoCvcv', 'CvccCvccCvcvno', 'CvcvnoCvccCvcc',
        'CvcvCvccnoCvcc', 'CvcvCvccCvccno', 'CvccnoCvcvCvcc', 'CvccCvcvnoCvcc',
        'CvccCvcvCvccno'
    ],
    'medium': [
        'CvcnoCvc', 'CvcCvcno'
    ],
    'short': [
        'Cvcn'
    ],
    'basic': [
        'aaanaaan', 'aannaaan', 'aaannaaa'
    ],
    'pin': [
        'nnnn'
    ],
    'name': [
        'cvccvcvcv'
    ],
    'phrase': [
        'cvcc cvc cvccvcv cvc', 'cvc cvccvcvcv cvcv', 'cv cvccv cvc cvcvccv'
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

def uint_32(i):
    return i.to_bytes(4, 'big')

def utf8(s):
    return s.encode('UTF-8')

from Crypto.Hash import HMAC, SHA256
import scrypt

def generate_master_key(master_password, salt_string):
    '''
    Generate the master key using the scrypt algorithm.

    Args:
        master_password: The secret string used to derive the key.
        salt_string: A less-secret string used to improve the key's security.

    Returns:
        The master key.
    '''

    salt = utf8(PACKAGE_NAME) + uint_32(len(salt_string)) + utf8(salt_string)
    key = scrypt.hash(utf8(master_password), salt, 32768, 8, 2, 64)

    return key

def generate_password(key, site, counter, template_type):
    '''
    Generate a site password using the master key and the site data.

    Args:
        key: The master key.
        site: The site's name.
        counter: The password version to generate.
        template_type: The type of password template to use.
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

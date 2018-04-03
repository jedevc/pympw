from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='pympw',
    version='0.1',
    description='Manage your passwords using the MasterPassword algorithm',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/jedevc/pympw',
    author='Justin Chadwell',
    license='GPL3',

    packages=['mpw'],
    python_requires='>=3',
    install_requires=['pycrypto', 'scrypt'],
    extras_require={
        'dialog': ['pythondialog']
    },

    entry_points={
        'console_scripts': [
            'mpw = mpw.mpw:main'
        ]
    }
)

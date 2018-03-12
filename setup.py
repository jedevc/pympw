from setuptools import setup

setup(
    name='pympw',
    version='0.1',
    description='A python implementation of the Master Password algorithm.',
    url='https://github.com/jedevc/pympw',
    author='Justin Chadwell',
    license='GPL3',

    packages=['mpw'],
    install_requires=['pycrypto', 'scrypt'],
    python_requires='>=3',
    
    entry_points={
        'console_scripts': [
            'mpw=mpw:main'
        ]
    }
)

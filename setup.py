try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Implementation of LSB Steganography to hide texts in images',
    'author': 'Krishna Ram Prakash R',
    'url': 'https://github.com/rkrp/maraithal',
    'download_url': 'https://github.com/rkrp/maraithal',
    'author_email': 'krp@gtux.in',
    'version': '0.4',
    'install_requires': ['pillow'],
    'packages': ['maraithal'],
    'scripts': [],
    'name': 'maraithal',
    'license' : 'GPLv3',
#    'classifiers' : {
#        'Development Status :: 4 - Beta',
#        'Topic :: Security',
#        'Topic :: Security :: Cryptography',
#        },
}

setup(**config)

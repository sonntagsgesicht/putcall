# -*- coding: utf-8 -*-

#  putcall
#  ------------
#  Collection of classical option pricing formulas.
#
#  Author:  pbrisk <pbrisk_at_github@icloud.com>
#  Copyright: 2016, 2017 Deutsche Postbank AG
#  Website: https://github.com/pbrisk/putcall
#  License: APACHE Version 2 License (see LICENSE file)


import codecs
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


setup(
    name='putcall',
    description='Collection of classical option pricing formulas.',
    version='0.1',
    author='Deutsche Postbank AG [pbrisk]',
    author_email='pbrisk_at_github@icloud.com',
    url='https://github.com/pbrisk/putcall',
    bugtrack_url='https://github.com/pbrisk/putcall/issues',
    license='Apache License 2.0',
    packages=find_packages(),
    install_requires=['mathtoolspy'],
    long_description=codecs.open('README.rst', encoding='utf-8').read(),
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Education',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Financial',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Utilities',
        'Topic :: Office/Business :: Scheduling',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Localization',
    ],
)

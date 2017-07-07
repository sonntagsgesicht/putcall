# -*- coding: utf-8 -*-

#  optionpricing
#  ------------
#  Collection of classical option pricing formulas.
#
#  Author:  pbrisk <pbrisk_at_github@icloud.com>
#  Copyright: 2016, 2017 Deutsche Postbank AG
#  Website: https://github.com/pbrisk/optionpricing
#  License: APACHE Version 2 License (see LICENSE file)


import codecs
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='optionpricing',
    description='Collection of classical option pricing formulas.',
    version='0.1',
    author='Deutsche Postbank AG [pbrisk]',
    author_email='pbrisk_at_github@icloud.com',
    url='https://github.com/pbrisk/optionpricing',
    bugtrack_url='https://github.com/pbrisk/optionpricing/issues',
    license='Apache License 2.0',
    packages=['optionpricing',
              'optionpricing.formulas',
              'optionpricing.formulas.plain_vanilla_options',
              'optionpricing.formulas.exotic_options',
              'optionpricing.formulas.interest_rate_options',
              'optionpricing.calibration'],
    install_requires=['mathtools'],
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

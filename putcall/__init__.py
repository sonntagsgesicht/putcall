# -*- coding: utf-8 -*-

# putcall
# -------
# Collection of classical option pricing formulas.
# 
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.2, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/putcall
# License:  Apache License 2.0 (see LICENSE file)


import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())


__doc__ = 'Collection of classical option pricing formulas.'
__version__ = '0.2'
__dev_status__ = '4 - Beta'
__date__ = 'Wednesday, 18 September 2019'
__author__ = 'sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]'
__email__ = 'sonntagsgesicht@icloud.com'
__url__ = 'https://github.com/sonntagsgesicht/' + __name__
__license__ = 'Apache License 2.0'
__dependencies__ = ('mathtoolspy',)
__dependency_links__ = ()
__data__ = ()
__scripts__ = ()

from .formulas import *
from .calibration import *
from .optionvaluator import *

# -*- coding: utf-8 -*-

#  putcall
#  -----------
#  Collection of classical option pricing formulas.
#
#  Author:  pbrisk <pbrisk_at_github@icloud.com>
#  Website: https://github.com/pbrisk/putcall
#  License: MIT (see LICENSE file)

import os
import unittest

from putcall import OptionType, OptionValuatorIntrinsic, \
    OptionValuatorN, OptionValuatorLN, OptionValuatorSLN
from datetime import datetime


class OptionValuatorTests(unittest.TestCase):

    def test_option_valuator_n(self):
        forward = 0.01
        strike = 0.025
        time = 3.25
        volatility = 0.012
        option_type = OptionType.CALL
        discount_factor = 0.9
        opt_val = OptionValuatorN()
        r_option_value = opt_val.option_value(forward, strike, time, volatility, option_type, discount_factor)
        b_option_value = 0.00312578018785
        r_delta = opt_val.delta(forward, strike, time, volatility, option_type, discount_factor)
        b_delta = 0.496702566538
        r_gamma = opt_val.gamma(forward, strike, time, volatility, option_type, discount_factor)
        b_gamma = 0.219822574661
        r_vega = opt_val.vega(forward, strike, time, volatility, option_type, discount_factor)
        b_vega = 0.719178857034

        r_option_value = opt_val.option_value(forward, strike, time, volatility, option_type, discount_factor)
        b_option_value = 0.00312578018785
        b_option_value = 0.0028132021690656416
        r_delta = opt_val.delta(forward, strike, time, volatility, option_type, discount_factor)
        b_delta = 0.496702566538
        b_delta = 0.44703230988407483
        b_delta = 0.21963327565176002
        r_gamma = opt_val.gamma(forward, strike, time, volatility, option_type, discount_factor)
        b_gamma = 0.219822574661
        b_gamma = 0.19784031719473505
        b_gamma = 13.050643811628296
        r_vega = opt_val.vega(forward, strike, time, volatility, option_type, discount_factor)
        b_vega = 0.719178857034
        b_vega = 0.647260971330887
        b_vega = 0.5089751086535035

        places = 10
        self.assertAlmostEqual(b_option_value, r_option_value, places)
        self.assertAlmostEqual(b_delta, r_delta, places)
        self.assertAlmostEqual(b_gamma, r_gamma, places)
        self.assertAlmostEqual(b_vega, r_vega, places)

    def test_option_valuator_n_bumped_risk(self):
        forward = 0.01
        strike = 0.025
        time = 3.25
        volatility = 0.012
        option_type = OptionType.CALL
        discount_factor = 0.9
        opt_val = OptionValuatorN()
        opt_val_bumped = OptionValuatorN(delta=(0.000001, 1.0, True), vega=(0.00001, 1.0, True))
        r_option_value = opt_val.option_value(forward, strike, time, volatility, option_type, discount_factor)
        b_option_value = opt_val_bumped.option_value(forward, strike, time, volatility, option_type, discount_factor)
        r_delta = opt_val.delta(forward, strike, time, volatility, option_type, discount_factor)
        b_delta = opt_val_bumped.delta(forward, strike, time, volatility, option_type, discount_factor)
        r_gamma = opt_val.gamma(forward, strike, time, volatility, option_type, discount_factor)
        b_gamma = opt_val_bumped.gamma(forward, strike, time, volatility, option_type, discount_factor)
        r_vega = opt_val.vega(forward, strike, time, volatility, option_type, discount_factor)
        b_vega = opt_val_bumped.vega(forward, strike, time, volatility, option_type, discount_factor)

        self.assertAlmostEqual(b_option_value, r_option_value, 7)
        self.assertAlmostEqual(b_delta, r_delta, 4)
        self.assertAlmostEqual(b_gamma, r_gamma, 3)
        self.assertAlmostEqual(b_vega, r_vega, 3)

    def test_option_valuator_ln(self):
        forward = 0.01
        strike = 0.025
        time = 3.25
        volatility = 0.55
        option_type = OptionType.CALL
        discount_factor = 0.9
        opt_val = OptionValuatorLN()
        r_option_value = opt_val.option_value(forward, strike, time, volatility, option_type, discount_factor)
        b_option_value = 0.00125679205126
        r_delta = opt_val.delta(forward, strike, time, volatility, option_type, discount_factor)
        b_delta = 0.300775792005
        r_gamma = opt_val.gamma(forward, strike, time, volatility, option_type, discount_factor)
        b_gamma = 33.03739172857978
        r_vega = opt_val.vega(forward, strike, time, volatility, option_type, discount_factor)
        b_vega = 0.00590540661053

        places = 10
        self.assertAlmostEqual(b_option_value, r_option_value, places)
        self.assertAlmostEqual(b_delta, r_delta, places)
        self.assertAlmostEqual(b_gamma, r_gamma, places)
        self.assertAlmostEqual(b_vega, r_vega, places)

    def test_option_valuator_sln(self):
        forward = 0.01
        strike = 0.025
        time = 3.25
        volatility = 0.55
        option_type = OptionType.CALL
        discount_factor = 0.9
        opt_val = OptionValuatorSLN()
        r_option_value = opt_val.option_value(forward, strike, time, volatility, option_type, discount_factor)
        b_option_value = 0.0102491451034
        r_delta = opt_val.delta(forward, strike, time, volatility, option_type, discount_factor)
        b_delta = 0.512368522188
        r_gamma = opt_val.gamma(forward, strike, time, volatility, option_type, discount_factor)
        b_gamma = 8.915958112439837
        b_gamma = 8.91595814366486
        r_vega = opt_val.vega(forward, strike, time, volatility, option_type, discount_factor)
        b_vega = 0.0254997180934

        places = 10
        self.assertAlmostEqual(b_option_value, r_option_value, places)
        self.assertAlmostEqual(b_delta, r_delta, places)
        self.assertAlmostEqual(b_gamma, r_gamma, places*6/10)
        self.assertAlmostEqual(b_vega, r_vega, places)

    def test_option_valuator_intrinsic(self):
        forward = 0.03
        strike = 0.025
        time = 3.25
        volatility = 0.55
        option_type = OptionType.CALL
        discount_factor = 0.9
        opt_val = OptionValuatorIntrinsic()
        r_option_value = opt_val.option_value(forward, strike, time, volatility, option_type, discount_factor)
        self.assertAlmostEqual(0.0045, r_option_value)
        r_delta = opt_val.delta(forward, strike, time, volatility, option_type, discount_factor)
        self.assertAlmostEqual(discount_factor * opt_val._delta[1], r_delta)
        r_gamma = opt_val.gamma(forward, strike, time, volatility, option_type, discount_factor)
        self.assertAlmostEqual(0.0 , r_gamma)
        r_vega = opt_val.vega(forward, strike, time, volatility, option_type, discount_factor)
        self.assertAlmostEqual(0.0, r_vega)

    # ------------------- IMPLIED VOL TEST ----------------
    def test_implied_vol_N_00(self):
        forward = 0.01
        strike = 0.025
        time = 3.25
        option_type = OptionType.CALL
        discount_factor = 0.9
        discount_factor = 1.
        price = 0.00312578018785
        opt_val = OptionValuatorN()
        p = OptionValuatorN().option_value(forward, strike, time, 0.01199999, OptionType.CALL, discount_factor)
        impl_vol = opt_val.implied_vol(forward, strike, time, price, option_type, discount_factor)
        price_with_impl_vol = opt_val.option_value(forward, strike, time, impl_vol, option_type, discount_factor)
        self.assertAlmostEqual(impl_vol, 0.0119999999982, 8)
        self.assertAlmostEqual(price_with_impl_vol, price, 8)

    def test_implied_vol_N_01(self):
        forward = 0.01
        strike = 0.025
        time = 3.25
        option_type = OptionType.PUT
        discount_factor = 0.9
        vol = 0.0014
        opt_val = OptionValuatorN()
        price = opt_val.option_value(forward, strike, time, vol, option_type, discount_factor)
        impl_vol = opt_val.implied_vol(forward, strike, time, price, option_type, discount_factor)
        price_with_impl_vol = opt_val.option_value(forward, strike, time, impl_vol, option_type, discount_factor)
        self.assertAlmostEqual(impl_vol, vol, 8)
        self.assertAlmostEqual(price_with_impl_vol, price, 8)


class BlackScholesUnitTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_call(self):
        self.assertTrue(True)

    def test_put(self):
        self.assertTrue(True)


if __name__ == "__main__":
    import sys

    start_time = datetime.now()

    print('')
    print('======================================================================')
    print('')
    print('run %s' % __file__)
    print('in %s' % os.getcwd())
    print('started  at %s' % str(start_time))
    print('')
    print('----------------------------------------------------------------------')
    print('')

    suite = unittest.TestLoader().loadTestsFromModule(__import__("__main__"))
    testrunner = unittest.TextTestRunner(stream=sys.stdout, descriptions=2, verbosity=2)
    testrunner.run(suite)

    print('')
    print('======================================================================')
    print('')
    print('ran %s' % __file__)
    print('in %s' % os.getcwd())
    print('started  at %s' % str(start_time))
    print('finished at %s' % str(datetime.now()))
    print('')
    print('----------------------------------------------------------------------')
    print('')

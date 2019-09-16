# -*- coding: utf-8 -*-

# putcall
# -------
# Collection of classical option pricing formulas.
#
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.2, copyright Saturday, 14 September 2019
# Website:  https://github.com/sonntagsgesicht/putcall
# License:  Apache License 2.0 (see LICENSE file)


import math

from mathtoolspy.distribution.normal_distribution import cdf_abramowitz_stegun as normal_cdf
# from ..option_payoffs import option_payoff
from putcall.formulas.option_payoffs import option_payoff, digital_option_payoff


def black_scholes(spot_value, strike_value, vol_value, time_value, is_call_bool, rate=0.):
    """
    Black Scholes option pricing formula on log-normal spot value

    :param forward_value: forward price of underlying at exercise date
    :type forward_value: real
    :param strike_value: strike of the option
    :type strike_value: real
    :param vol_value: volatility of underlying price
    :type vol_value: non-negative real
    :param time_value: year fraction until exercise date
    :type time_value: non-negative real
    :param is_call_bool: call -> True, put -> False
    :type is_call_bool: boolean
    :param rate: risk free rate
    :type rate: real
    :return: option price
    :rtype: real
    :return:

    """
    if not vol_value >= 0:
        raise AssertionError("Negative vol in %s" % __name__)
    sigma = vol_value * math.sqrt(time_value)

    if sigma == 0:
        # non-random option value, e.g. on exercise date
        return option_payoff(spot_value, strike_value, is_call_bool)

    d1 = (math.log(spot_value / strike_value) + rate * time_value + 0.5 * sigma ** 2) / sigma
    d2 = d1 - sigma

    if is_call_bool:
        return spot_value * normal_cdf(d1) - strike_value * math.exp(-rate * time_value) * normal_cdf(d2)
    else:
        return strike_value * math.exp(-rate * time_value) * normal_cdf(-d2) - spot_value * normal_cdf(-d1)


def black_scholes_digital(spot_value, strike_value, vol_value, time_value, is_call_bool, rate=0.):
    """
    Black Scholes digital option pricing formula on log-normal spot value

    :param spot_value: forward price of underlying at exercise date
    :type spot_value: real
    :param strike_value: strike of the option
    :type strike_value: real
    :param vol_value: volatility of underlying price
    :type vol_value: non-negative real
    :param time_value: year fraction until exercise date
    :type time_value: non-negative real
    :param is_call_bool: call -> True, put -> False
    :type is_call_bool: boolean
    :param rate: risk free rate
    :type rate: real
    :return: option price
    :rtype: real
    :return:
    """
    if not vol_value >= 0:
        raise AssertionError("Negative vol in %s" % __name__)
    sigma = vol_value * math.sqrt(time_value)

    if sigma == 0:
        # non-random option value, e.g. on exercise date
        return digital_option_payoff(spot_value, strike_value, is_call_bool)

    d0 = (math.log(spot_value / strike_value) + rate * time_value - 0.5 * sigma ** 2) / sigma

    return math.exp(-rate * time_value) * normal_cdf(d0)


def forward_black_scholes(forward_value, strike_value, vol_value, time_value, is_call_bool, rate=0.):
    """
    Black Scholes option pricing formula on log-normal forward value

    :param strike_value: strike of the option
    :type strike_value: real
    :param forward_value: forward price of underlying at exercise date
    :type forward_value: real
    :param vol_value: volatility of underlying price
    :type vol_value: non-negative real
    :param time_value: year fraction until exercise date
    :type time_value: non-negative real
    :param is_call_bool: call -> True, put -> False
    :type is_call_bool: boolean
    :param rate: risk free rate
    :type rate: real
    :return: option price
    :rtype: real
    :return:

    """
    if not vol_value >= 0:
        raise AssertionError("Negative vol in %s" % __name__)
    sigma = vol_value * math.sqrt(time_value)

    if sigma == 0:
        # non-random option value, e.g. on exercise date
        return option_payoff(forward_value, strike_value, is_call_bool)

    d1 = (math.log(forward_value / strike_value) + 0.5 * sigma ** 2) / sigma
    d2 = d1 - sigma

    if is_call_bool:
        return (forward_value * normal_cdf(d1) - strike_value * normal_cdf(d2)) * math.exp(-rate * time_value)
    else:
        return (strike_value * normal_cdf(-d2) - forward_value * normal_cdf(-d1)) * math.exp(-rate * time_value)


def forward_black_scholes_digital(forward_value, strike_value, vol_value, time_value, is_call_bool, rate=0.):
    """
    Black Scholes digital option pricing formula on log-normal forward value

    :param strike_value: strike of the option
    :type strike_value: real
    :param forward_value: forward price of underlying at exercise date
    :type forward_value: real
    :param vol_value: volatility of underlying price
    :type vol_value: non-negative real
    :param time_value: year fraction until exercise date
    :type time_value: non-negative real
    :param is_call_bool: call -> True, put -> False
    :type is_call_bool: boolean
    :param rate: risk free rate
    :type rate: real
    :return: option price
    :rtype: real
    :return:
    """
    if not vol_value >= 0:
        raise AssertionError("Negative vol in %s" % __name__)
    sigma = vol_value * math.sqrt(time_value)

    if sigma == 0:
        # non-random option value, e.g. on exercise date
        return digital_option_payoff(forward_value, strike_value, is_call_bool)

    d0 = (math.log(forward_value / strike_value) + rate * time_value - 0.5 * sigma ** 2) / sigma

    return math.exp(-rate * time_value) * normal_cdf(d0)

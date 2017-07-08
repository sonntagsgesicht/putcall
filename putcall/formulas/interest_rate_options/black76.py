# -*- coding: utf-8 -*-

#  putcall
#  ------------
#  Collection of classical option pricing formulas.
#
#  Author:  pbrisk <pbrisk_at_github@icloud.com>
#  Copyright: 2016, 2017 Deutsche Postbank AG
#  Website: https://github.com/pbrisk/putcall
#  License: APACHE Version 2 License (see LICENSE file)


from math import sqrt, log

from mathtoolspy import cdf_abramowitz_stegun as normal_cdf
from mathtoolspy import density_normal_dist as normal_density

#from ..option_payoffs import option_payoff, digital_option_payoff, straddle_payoff
from putcall.formulas.option_payoffs import option_payoff, digital_option_payoff, straddle_payoff


def _black_param(forward_value, strike_value,  implied_vol_value, time_value):
    sigma = implied_vol_value * sqrt(time_value)
    fms = forward_value - strike_value
    d0 = (log(forward_value / strike_value) - 0.5 * sigma ** 2) / sigma if sigma > 0.0 else 0.0
    d1 = d0 + sigma
    return sigma, fms, d0, d1


def black(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Standard Black-76 formula for log-normal underlying distribution.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d0, d1 = _black_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return option_payoff(forward_value, strike_value, is_call_bool)

    if is_call_bool:
        # call
        return forward_value * normal_cdf(d1) - strike_value * normal_cdf(d0)
    else:
        # put
        return strike_value * normal_cdf(-d0) - forward_value * normal_cdf(-d1)


def black_delta(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Black-76 delta sensitivity.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d0, d1 = _black_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        if is_call_bool:
            return 1.0 if fms > 0.0 else 0.0
        else:
            return -1.0 if fms < 0.0 else 0.0

    # call
    call_value = normal_cdf(d1)
    return call_value if is_call_bool else call_value - 1.0  # put


def black_gamma(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Black-76 gamma sensitivity.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d0, d1 = _black_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 0.0

    return None  # TODO Black76 gamma


def black_vega(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Black-76 vega sensitivity.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d0, d1 = _black_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 0.0

    return forward_value * sqrt(time_value) * normal_density(d1)


def black_digital(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Standard Black-76 formula for digital option on log-normal underlying distribution.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d0, d1 = _black_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return digital_option_payoff(forward_value, strike_value, is_call_bool)

    return normal_cdf(d0) if is_call_bool else normal_cdf(-d0)


def black_digital_delta(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Black-76 delta sensitivity for digital payoff.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d0, d1 = _black_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 0.0

    if is_call_bool:
        # call
        return normal_density(d1) / (sigma * forward_value)
    else:
        # put
        return -normal_density(-d1) / (sigma * forward_value)


def black_digital_gamma(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Black-76 gamma sensitivity for digital payoff.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d0, d1 = _black_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 0.0

    return None  # TODO Black76 gamma for digital payoff


def black_digital_vega(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Black-76 vega sensitivity for digital payoff.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d0, d1 = _black_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 0.0

    # call
    call_value = d1 * normal_density(d0) / implied_vol_value
    return call_value if is_call_bool else -call_value  # put


def black_straddle(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Standard Black-76 formula for straddle option on log-normal underlying distribution.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d0, d1 = _black_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return straddle_payoff(forward_value, strike_value, is_call_bool)

    nd1 = normal_cdf(d1)
    nd2 = normal_cdf(d0)
    mnd1 = normal_cdf(-d1)
    mnd2 = normal_cdf(-d0)

    return forward_value * nd1 - strike_value * nd2 + strike_value * mnd2 - forward_value * mnd1


def black_straddle_delta(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Black-76 delta sensitivity for straddle payoff.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d0, d1 = _black_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 1.0 if fms >= 0.0 else -1.0

    return 2.0 * normal_density(d1) - 1


def black_straddle_gamma(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Black-76 gamma sensitivity for straddle payoff.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d0, d1 = _black_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 0.0

    return None  # TODO Black76 gamma for straddle payoff


def black_straddle_vega(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Black-76 vega sensitivity for straddle payoff.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d0, d1 = _black_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 0.0

    return 2.0 * forward_value * sqrt(time_value) * normal_density(d1)

# -*- coding: utf-8 -*-

# putcall
# -------
# Collection of classical option pricing formulas.
# 
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.2, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/putcall
# License:  Apache License 2.0 (see LICENSE file)


from math import exp, sqrt, pi

from mathtoolspy import cdf_abramowitz_stegun as normal_cdf
from mathtoolspy import density_normal_dist as normal_density

from ..option_payoffs import option_payoff, digital_option_payoff, straddle_payoff


def _bachelier_param(forward_value, strike_value, implied_vol_value, time_value):
    sigma = implied_vol_value * sqrt(time_value)
    fms = forward_value - strike_value
    d = fms / sigma if sigma > 0.0 else 0.0
    return sigma, fms, d


def bachelier(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Bachelier formula (Black formula for normal underlying distribution).

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d = _bachelier_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return option_payoff(forward_value, strike_value, is_call_bool)

    # call
    # call_value = fms * normal_cdf(d) + exp(-d ** 2 / 2) * sigma / sqrt(2 * pi)  # intern version
    call_value = fms * normal_cdf(d) + sigma * normal_density(d)
    put_value = -fms * normal_cdf(-d) + sigma * normal_density(d)
    return call_value if is_call_bool else call_value - fms  # put


def bachelier_delta(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    delta sensitivity for Bachelier formula.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d = _bachelier_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 1.0 if fms > 0.0 else 0.0

    return normal_cdf(d) if is_call_bool else -normal_cdf(-d)


def bachelier_gamma(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    gamma sensitivity for Bachelier formula.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d = _bachelier_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 0.0

    return normal_density(d) / sigma


def bachelier_vega(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    vega sensitivity for Bachelier formula.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d = _bachelier_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 0.0

    return sqrt(time_value) * normal_density(d)


def bachelier_digital(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Bachelier formula for digital option (Black formula for normal underlying distribution).

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d = _bachelier_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return digital_option_payoff(forward_value, strike_value, is_call_bool)

    # call
    call_price = -1 * normal_cdf(d) + exp(-d ** 2 / 2) * sigma / sqrt(2 * pi)
    return call_price if is_call_bool else call_price + 1  # put


def bachelier_digital_delta(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    delta sensitivity for Bachelier formula for digital option.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d = _bachelier_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 0.0

    # call
    call_value = normal_density(d) / sigma
    return call_value if is_call_bool else -call_value  # put


def bachelier_digital_gamma(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    gamma sensitivity for Bachelier formula for digital option.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d = _bachelier_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 0.0

    return d * normal_density(d) / (implied_vol_value * implied_vol_value * time_value)


def bachelier_digital_vega(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    vega sensitivity for Bachelier formula for digital option.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d = _bachelier_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 0.0

    # call
    call_value = -d * normal_density(d) / implied_vol_value
    return call_value if is_call_bool else -call_value  # put


def bachelier_straddle(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Bachelier formula for straddle option on log-normal underlying distribution.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d = _bachelier_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return straddle_payoff(forward_value, strike_value, is_call_bool)

    return None  # TODO Bachelier for straddle payoff


def bachelier_straddle_delta(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Bachelier delta sensitivity for straddle payoff.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d = _bachelier_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 1.0 if fms >= 0.0 else -1.0

    return None  # TODO Bachelier delta for straddle payoff


def bachelier_straddle_gamma(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Bachelier gamma sensitivity for straddle payoff.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d = _bachelier_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 0.0

    return None  # TODO Bachelier gamma for straddle payoff


def bachelier_straddle_vega(forward_value, strike_value, implied_vol_value, time_value, is_call_bool):
    """
    Bachelier vega sensitivity for straddle payoff.

    :param float forward_value: forward price of underlying at exercise date
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of underlying price
    :param float time_value: year fraction until exercise date
    :param boolean is_call_bool: call -> True, put -> False
    :return: float

    """

    sigma, fms, d = _bachelier_param(forward_value, strike_value, implied_vol_value, time_value)

    if sigma == 0.0:
        return 0.0

    return None  # TODO Bachelier vega for straddle payoff

import math

from mathtoolspy.distribution.normal_distribution import cdf_abramowitz_stegun as normal_cdf
#from ..option_payoffs import option_payoff
from putcall.formulas.option_payoffs import option_payoff


def black_scholes(strike_value, forward_value, implied_vol_value, time_value, is_call_bool, rf):
    """
    Black Scholes option pricing formula

    :param strike_value: strike of the option
    :type strike_value: real
    :param forward_value: forward price of underlying at exercise date
    :type forward_value: real
    :param implied_vol_value: volatility of underlying price
    :type implied_vol_value: non-negative real
    :param time_value: year fraction until exercise date
    :type time_value: non-negative real
    :param is_call_bool: call -> True, put -> False
    :type is_call_bool: boolean
    :param rf: risk free rate
    :type rf: real
    :return: option price
    :rtype: real
    :return:

    """
    assert implied_vol_value >= 0
    sigma = implied_vol_value * math.sqrt(time_value)

    if sigma == 0:
        # non-random option value, e.g. on exercise date
        return option_payoff(forward_value, strike_value, is_call_bool)

    d0 = (math.log(forward_value / strike_value) + rf * time_value - 0.5 * sigma ** 2) / sigma
    d1 = d0 + sigma
    option_price = math.exp(rf * time_value) * forward_value * normal_cdf(d1) - strike_value * normal_cdf(d0)

    if is_call_bool:
        # call
        return option_price

    else:
        # put
        return option_price + strike_value - forward_value


def black_scholes_digital(strike_value, forward_value, implied_vol_value, time_value, is_call_bool, rf):
    """
    Black Scholes digital option pricing formula

    :param strike_value: strike of the option
    :type strike_value: real
    :param forward_value: forward price of underlying at exercise date
    :type forward_value: real
    :param implied_vol_value: volatility of underlying price
    :type implied_vol_value: non-negative real
    :param time_value: year fraction until exercise date
    :type time_value: non-negative real
    :param is_call_bool: call -> True, put -> False
    :type is_call_bool: boolean
    :param rf: risk free rate
    :type rf: real
    :return: option price
    :rtype: real
    :return:
    """
    assert implied_vol_value >= 0
    sigma = implied_vol_value * math.sqrt(time_value)

    if sigma == 0:
        # non-random option value, e.g. on exercise date
        return option_payoff(forward_value, strike_value, is_call_bool)

    d0 = (math.log(forward_value / strike_value) + rf * time_value - 0.5 * sigma ** 2) / sigma

    return math.exp(-rf * time_value) * normal_cdf(d0)

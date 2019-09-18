# -*- coding: utf-8 -*-

# putcall
# -------
# Collection of classical option pricing formulas.
# 
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.2, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/putcall
# License:  Apache License 2.0 (see LICENSE file)


import math

from mathtoolspy.distribution.normal_distribution import cdf_abramowitz_stegun as normal_cdf


def hw_discount_bond_option(forward_value, strike_value, implied_vol_value, time_value, is_call_bool,
                            time_to_bond_value, mean_reversion_value, maturity_discount_value):
    """
    discount bond option pricing formula in the Hull White  framework

    :param float forward_value: forward price of underlying (discount bond) at bond maturity (D(t,Tau,r))
    :param float strike_value: strike price
    :param float implied_vol_value: volatility of the spot rate
    :param float time_value: year fraction until exercise date (option maturity date)
    :param float bool is_call_bool: call -> True, put -> False
    :param float time_to_bond_value: year fraction between option's maturity and bond's maturity
    :param float maturity_discount_value: forward price of underlying (discount bond) at option maturity date (D(t,T,r))
    :param float mean_reversion_value: mean reversion / alpha
    :return: float

    discount bond option pricing formula in the Hull White framework
    as described in A. Pelsser, *Efficient Methods for Valuing Interest Rate Derivatives*, 2000, pp. 50

    """
    if time_value == 0:
        return 0.0
    else:
        strike = maturity_discount_value * strike_value
        A = forward_value / strike
        B = (1 - math.exp(-mean_reversion_value * (time_to_bond_value))) / mean_reversion_value
        var = ((implied_vol_value ** 2) / (2 * mean_reversion_value)) * \
              (1 - math.exp(-2 * mean_reversion_value * time_value))
        sigma = B * math.sqrt(var)
        h = (math.log(A) / sigma) + 0.5 * sigma
        if is_call_bool:
            # call
            option_bond_price = forward_value * normal_cdf(h) - strike * normal_cdf(h - sigma)
        else:
            # put
            option_bond_price = strike * normal_cdf(-h + sigma) - forward_value * normal_cdf(-h)
        return option_bond_price


def hw_cap_floor_let(forward_rate_value, strike_value, implied_vol_value, time_value, is_call_bool, year_fraction_value,
                     mean_reversion_value, discount_value):
    """
    pricing formula of a caplet/floorlet under the Hull White framework

    :param float forward_rate_value: forward rate (LIBOR,EURIBOR...)
    :param float discount_value: zero bond price between pricing time and start of the caplet (D(t,T,r))
    :param float mean_reversion_value: mean reversion in the Hull White model
    :param float strike_value: strike of the option
    :param float implied_vol_value: volatility of the spot rate
    :param float year_fraction_value: year fraction between start and maturity = tenor of the rate
    :param float time_value: year_fraction between pricing date (e.g. start of the Cap) and start of the caplet Y(t,T)
    :param bool is_call_bool: call(caplet) -> True, put(floorlet) -> False
    :return: float

    pricing formula of a caplet/floorlet under the Hull White framework
    as described in A. Pelsser, *Efficient Methods for Valuing Interest Rate Derivatives*, 2000, pp. 57

    """
    discount_forward_value = 1 / (1 + year_fraction_value * forward_rate_value)  # same as D(T,Tau,r)
    forward = discount_value * discount_forward_value
    strike = 1 / (1 + year_fraction_value * strike_value)
    vol = implied_vol_value
    t = time_value
    yf = year_fraction_value
    df = discount_value
    mr = mean_reversion_value
    hw_bond_opt = hw_discount_bond_option(forward, strike, vol, t, not is_call_bool, yf, mr, df)

    return (1 + year_fraction_value * strike_value) * hw_bond_opt

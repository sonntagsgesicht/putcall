# -*- coding: utf-8 -*-

# putcall
# -------
# Collection of classical option pricing formulas.
# 
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.2, copyright Saturday, 14 September 2019
# Website:  https://github.com/sonntagsgesicht/putcall
# License:  Apache License 2.0 (see LICENSE file)


def option_payoff(forward_value, strike_value, is_call_bool):
    """
    simple option payoff

    @param strike_value: strike price
    @param forward_value: forward price of underlying
    @param is_call_bool: call -> True, put -> False
    @return: option payoff value
    """

    if is_call_bool:
        # call
        return max(forward_value - strike_value, 0)
    else:
        # put
        return max(strike_value - forward_value, 0)


def digital_option_payoff(forward_value, strike_value, is_call_bool):
    """
    simple digital  option payoff

    @param strike_value: strike price
    @param forward_value: forward price of underlying
    @param is_call_bool: call -> True, put -> False
    @return: option payoff value
    """

    if is_call_bool:
        # call
        return 1.0 if forward_value >= strike_value else 0.0
    else:
        # put
        return 0.0 if forward_value >= strike_value else 1.0


def straddle_payoff(forward_value, strike_value, is_call_bool=True):
    """
    simple straddle option payoff

    @param strike_value: strike price
    @param forward_value: forward price of underlying
    @param is_call_bool: obsolete
    @return: option payoff value
    """
    return option_payoff(forward_value, strike_value, True) + option_payoff(forward_value, strike_value, False)

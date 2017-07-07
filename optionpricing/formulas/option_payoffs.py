# -*- coding: utf-8 -*-

#  optionpricing
#  ------------
#  Collection of classical option pricing formulas.
#
#  Author:  pbrisk <pbrisk_at_github@icloud.com>
#  Copyright: 2016, 2017 Deutsche Postbank AG
#  Website: https://github.com/pbrisk/optionpricing
#  License: APACHE Version 2 License (see LICENSE file)


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

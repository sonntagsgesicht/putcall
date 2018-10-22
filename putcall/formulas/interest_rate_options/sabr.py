# -*- coding: utf-8 -*-

#  putcall
#  ------------
#  Collection of classical option pricing formulas.
#
#  Author:  pbrisk <pbrisk_at_github@icloud.com>
#  Copyright: 2016, 2017 Deutsche Postbank AG
#  Website: https://github.com/pbrisk/putcall
#  License: APACHE Version 2 License (see LICENSE file)


import math
import logging

pace_log = logging.getLogger('pace')

# ----- sabr -----

EPS = 0.000000001


def sabr_black_vol(strike_value, forward_value, alpha_value, beta_value, nu_value, rho_value, time_value):
    '''
    :param strike_value:
    :type strike_value:
    :param forward_value:
    :type forward_value:
    :param alpha_value:
    :type alpha_value:
    :param beta_value:
    :type beta_value:
    :param nu_value:
    :type nu_value:
    :param rho_value:
    :type rho_value:
    :param time_value:
    :type time_value:
    :return:
    :rtype:
    '''
    return_value = 0.00
    # Compute the Black equivalent voltatility from SABR model
    forward_strike_value = forward_value * strike_value
    log_moneyness_value = math.log(forward_value / strike_value)
    one_minus_beta_value = 1 - beta_value
    factor = 0.00
    if abs(strike_value - forward_value) > EPS:
        Z = nu_value / alpha_value * forward_strike_value ** (one_minus_beta_value / 2) * log_moneyness_value
        xz = math.log((math.sqrt(1 - 2 * rho_value * Z + Z * Z) + Z - rho_value) / (1 - rho_value))
        denom_value = forward_strike_value ** (one_minus_beta_value / 2) * (
        1 + one_minus_beta_value ** 2 / 24 * log_moneyness_value ** 2 + one_minus_beta_value ** 4 / 1920 * log_moneyness_value ** 4)
        factor = one_minus_beta_value ** 2 / 24 * alpha_value ** 2 / (forward_strike_value ** one_minus_beta_value)
        factor = factor + 0.25 * rho_value * beta_value * alpha_value * nu_value / (
        forward_strike_value ** (one_minus_beta_value / 2))
        factor = factor + (2 - 3 * rho_value ** 2) * nu_value ** 2 / 24
        factor = 1 + factor * time_value
        # obloj correction
        # return_value = alpha_value / denom_value * Z / xz * factor
        return_value = alpha_value / denom_value * factor
    else:
        # factor = ( 1 +  ( one_minus_beta_value **2 / 24 * alpha_value ** 2 /  ( forward_value ** ( 2 * one_minus_beta_value ) ) + 0.25 * rho_value * beta_value * alpha_value * nu_value /  ( forward_value ** one_minus_beta_value )  +  ( 2 - 3 * rho_value * rho_value )  * nu_value * nu_value / 24 )  * time_value )
        factor = one_minus_beta_value ** 2 / 24 * alpha_value ** 2 / (forward_value ** (2 * one_minus_beta_value))
        factor = factor + 0.25 * rho_value * beta_value * alpha_value * nu_value / (
        forward_value ** one_minus_beta_value)
        factor = factor + (2 - 3 * rho_value ** 2) * nu_value ** 2 / 24
        factor = 1 + factor * time_value
        factor = (1 + (one_minus_beta_value ** 2 / 24 * alpha_value ** 2 / (
        forward_value ** (2 * one_minus_beta_value)) + 0.25 * rho_value * beta_value * alpha_value * nu_value / (
                       forward_value ** one_minus_beta_value) + (
                       2 - 3 * rho_value * rho_value) * nu_value * nu_value / 24) * time_value)
        return_value = alpha_value / forward_value ** one_minus_beta_value * factor
    return return_value


def sabr_atmadj_black_vol(strike_value, forward_value, atm_vol_value, beta_value, nu_value, rho_value, time_value):
    '''
    :param strike_value:
    :type strike_value:
    :param forward_value:
    :type forward_value:
    :param atm_vol_value:
    :type atm_vol_value:
    :param beta_value:
    :type beta_value:
    :param nu_value:
    :type nu_value:
    :param rho_value:
    :type rho_value:
    :param time_value:
    :type time_value:
    :return:
    :rtype:
    '''
    alpha_value = sabr_alpha_from_atm(forward_value, atm_vol_value, beta_value, nu_value, rho_value, time_value)
    pace_log.debug('sabr atm alpha: %f' % alpha_value)
    return sabr_black_vol(strike_value, forward_value, alpha_value, beta_value, nu_value, rho_value, time_value)


def sabr_alpha_from_atm(forward_value, atm_vol_value, beta_value, nu_value, rho_value, time_value):
    '''
    :param forward_value:
    :type forward_value:
    :param atm_vol_value:
    :type atm_vol_value:
    :param beta_value:
    :type beta_value:
    :param nu_value:
    :type nu_value:
    :param rho_value:
    :type rho_value:
    :param time_value:
    :type time_value:
    :return:
    :rtype:
    '''
    alpha_value = 0.0
    diff = sabr_black_vol(forward_value, forward_value, alpha_value, beta_value, nu_value, rho_value,
                          time_value) - atm_vol_value
    while diff < EPS:
        alpha_value += EPS
        diff = sabr_black_vol(forward_value, forward_value, alpha_value, beta_value, nu_value, rho_value,
                              time_value) - atm_vol_value
    return alpha_value

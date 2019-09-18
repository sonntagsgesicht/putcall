# -*- coding: utf-8 -*-

# putcall
# -------
# Collection of classical option pricing formulas.
# 
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.2, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/putcall
# License:  Apache License 2.0 (see LICENSE file)


from putcall.formulas import hw_cap_floor_let

EPS = 1e-12


def _frange(start, stop=None, step=None):
    if step is None:
        step = 1.0
    if stop is None:
        stop = start
        start = 0.0
    res = list()
    current = start
    if step > 0.0:
        while current < stop:
            res.append(current)
            current += step
    else:
        while stop < current:
            res.append(current)
            current += step
    return res


def _hw_price_dict(price_dict, mean_reversion, volatility, error_func=None):
    if error_func is None:
        error_func = (lambda x: x * x)
    error = 0.00
    for i in range(len(price_dict['strike'])):
        error += error_func(hw_cap_floor_let(price_dict['forward_values'][i], price_dict['strike'][i], volatility,
                                             price_dict['time_value'][i], price_dict['bool'][i],
                                             price_dict['year_fraction'][i], mean_reversion,
                                             price_dict['discfact'][i]) - price_dict['price'][i])
    return error


def binary_vol_hw_calibration_cap_floor(price_dict,
                                        mean_reversion_start=0.0,
                                        mean_reversion_stop=0.01,
                                        mean_reversion_step=0.0001,
                                        volatility_start=0.0001,
                                        volatility_stop=0.01,
                                        volatility_step=0.0001):
    """
    Binary search based calibration of the Hull White model using caps and floors

    :param price_dict: contains prices, time_values, year_fractions,forward values
    :type price_dict: dictionary
    :param mean_reversion_start: mean reversion error mean_reversion_start
    :type mean_reversion_start: real
    :param mean_reversion_stop: mean reversion error mean_reversion_stop
    :type mean_reversion_stop: real
    :param mean_reversion_step: step for the mean reversion optimisation loop
    :type mean_reversion_step: real
    :param volatility_start: volatility error mean_reversion_start
    :type volatility_start: real
    :param volatility_stop: volatility error mean_reversion_stop
    :type volatility_stop: real
    :param volatility_step: step for the volatility optimisation loop
    :type volatility_step: real
    :return: optimal mean reversion, optimal volatility, vector of errors
    :rtype: list(list())

    remarks:
        price_dict is a dictionary s.t.:
        price_dict['time_value'] contains the year fractions between start date and maturity
        price_dict['year_fraction'] contains the year fractions between start and maturity
        price_dict['forward_values'] contains the rate forward values
        price_dict['price'] price of the lets
        price_dict['strike'] list of strikes
        price_dict['bool'] list of booleans (True if call False if put)
        threshold_vol mean_reversion_stop on the vola
        mean_reversion_stop is the mean_reversion_stop on the mean revertion

    """
    if not 0.0 <= mean_reversion_start <= mean_reversion_stop and not mean_reversion_step > 0.0:
        raise AssertionError("Mean reversion either negative or greater expected or negative step.")
    if not 0.0 <= volatility_start <= volatility_stop and not volatility_step > 0.0:
        raise AssertionError("Volatility either negative or greater expected or negative step.")

    last = [None, None, None]
    for vol in _frange(volatility_start, volatility_stop + volatility_step, volatility_step):
        res = brute_hw_calibration_cap_floor(price_dict,
                                             mean_reversion_start, mean_reversion_stop, mean_reversion_step,
                                             vol, vol, volatility_step)
        if last[2] is None or last[2] > res[2]:
            last = res
        else:
            return last
    print('Mean reversion calibration of Hull White failed.')
    return last


def binary_mr_hw_calibration_cap_floor(price_dict,
                                       mean_reversion_start=0.0,
                                       mean_reversion_stop=0.01,
                                       mean_reversion_step=0.0001,
                                       volatility_start=0.0001,
                                       volatility_stop=0.01,
                                       volatility_step=0.0001):
    """
    Binary search based calibration of the Hull White model using caps and floors

    :param price_dict: contains prices, time_values, year_fractions,forward values
    :type price_dict: dictionary
    :param mean_reversion_start: mean reversion error mean_reversion_start
    :type mean_reversion_start: real
    :param mean_reversion_stop: mean reversion error mean_reversion_stop
    :type mean_reversion_stop: real
    :param mean_reversion_step: step for the mean reversion optimisation loop
    :type mean_reversion_step: real
    :param volatility_start: volatility error mean_reversion_start
    :type volatility_start: real
    :param volatility_stop: volatility error mean_reversion_stop
    :type volatility_stop: real
    :param volatility_step: step for the volatility optimisation loop
    :type volatility_step: real
    :return: optimal mean reversion, optimal volatility, vector of errors
    :rtype: list(list())

    remarks:
        price_dict is a dictionary s.t.:
        price_dict['time_value'] contains the year fractions between start date and maturity
        price_dict['year_fraction'] contains the year fractions between start and maturity
        price_dict['forward_values'] contains the rate forward values
        price_dict['price'] price of the lets
        price_dict['strike'] list of strikes
        price_dict['bool'] list of booleans (True if call False if put)
        threshold_vol mean_reversion_stop on the vola
        mean_reversion_stop is the mean_reversion_stop on the mean revertion

    """
    if not 0.0 <= mean_reversion_start <= mean_reversion_stop and not mean_reversion_step > 0.0:
        raise AssertionError("Mean reversion either negative or greater expected or negative step.")
    if not 0.0 <= volatility_start <= volatility_stop and not volatility_step > 0.0:
        raise AssertionError("Volatility either negative or greater expected or negative step.")

    last = [None, None, None]
    for mr in _frange(mean_reversion_start, mean_reversion_stop + mean_reversion_step, mean_reversion_step):
        res = binary_vol_hw_calibration_cap_floor(price_dict,
                                                  mr, mr, mean_reversion_step,
                                                  volatility_start, volatility_stop, volatility_step)
        if last[2] is None or last[2] > res[2]:
            last = res
        else:
            return last
    print('Mean reversion calibration of Hull White failed.')
    return last


def brute_hw_calibration_cap_floor(price_dict,
                                   mean_reversion_start=0.00,
                                   mean_reversion_stop=0.01,
                                   mean_reversion_step=0.0001,
                                   volatility_start=0.0001,
                                   volatility_stop=0.01,
                                   volatility_step=0.0001,
                                   error_func=None):
    """
    Brute force based calibration of the Hull White model using caps and floors

    :param price_dict: contains prices as a price_dict
    :type price_dict: dictionary
    :param mean_reversion_start: mean reversion starting point
    :type mean_reversion_start: float
    :param mean_reversion_stop: mean reversion threshold
    :type mean_reversion_stop: float
    :param mean_reversion_step: mean reversion step
    :type mean_reversion_step: float
    :param volatility_start: volatility starting point
    :type volatility_start: float
    :param volatility_stop: volatility reversion threshold
    :type volatility_stop: float
    :param volatility_step: volatility reversion step
    :type volatility_step: float
    :param error_func: function to aggregate errors
    :type error_func: function
    :return: optimal mean reversion, optimal volatility, corresponding error

    calculates the error for different choices of mean rev and volatility
    which will make it possible for the user to pick the values for which the error is minimal

    remarks:
        price_dict is a dictionary s.t.:
        price_dict['time_value'] contains the year fractions between start date and maturity
        price_dict['year_fraction'] contains the year fractions between start and maturity
        price_dict['forward_values'] contains the rate forward values
        price_dict['price'] price of the lets
        price_dict['strike'] list of strikes
        price_dict['bool'] list of booleans (True if call False if put)
        threshold_vol threshold on the vola
        threshold is the threshold on the mean reversion

    """
    if not 0.0 <= mean_reversion_start <= mean_reversion_stop and not mean_reversion_step > 0.0:
        raise AssertionError("Mean reversion either negative or greater expected or negative step.")
    if not 0.0 <= volatility_start <= volatility_stop and not volatility_step > 0.0:
        raise AssertionError("Volatility either negative or greater expected or negative step.")

    mean_reversion_opt = None
    volatility_opt = None
    error_opt = None
    for mr in _frange(mean_reversion_start, mean_reversion_stop + mean_reversion_step, mean_reversion_step):
        mr = EPS if mr == 0.00 else mr
        for vol in _frange(volatility_start, volatility_stop + volatility_step, volatility_step):
            vol = EPS if vol == 0.00 else vol
            err = _hw_price_dict(price_dict, mr, vol, error_func)
            if error_opt is None or error_opt > err:
                mean_reversion_opt = mr
                volatility_opt = vol
                error_opt = err
    return [mean_reversion_opt, volatility_opt, error_opt]

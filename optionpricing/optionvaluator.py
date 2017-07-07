# -*- coding: utf-8 -*-

#  optionpricing
#  ------------
#  Collection of classical option pricing formulas.
#
#  Author:  pbrisk <pbrisk_at_github@icloud.com>
#  Copyright: 2016, 2017 Deutsche Postbank AG
#  Website: https://github.com/pbrisk/optionpricing
#  License: APACHE Version 2 License (see LICENSE file)


from formulas import option_payoff, digital_option_payoff, straddle_payoff

from formulas import black, black_delta, black_gamma, black_vega
from formulas import black_digital, black_digital_delta, black_digital_gamma, black_digital_vega
from formulas import black_straddle, black_straddle_delta, black_straddle_gamma, black_straddle_vega

from formulas import bachelier, bachelier_delta, bachelier_gamma, bachelier_vega
from formulas import bachelier_digital, bachelier_digital_delta, bachelier_digital_gamma, bachelier_digital_vega
from formulas import bachelier_straddle, bachelier_straddle_delta, bachelier_straddle_gamma, bachelier_straddle_vega

from calibration import OptionValueByVolatility, ImpliedVolCalculator


class OptionType(object):
    CALL, PUT, DIGITAL_CALL, DIGITAL_PUT, STRADDLE = range(5)


class OptionValuator(object):
    def __init__(self, delta=None, vega=None):
        self._delta = self._parse(delta, (0.00001, 1.0, True))
        self._analytical_delta = delta is None
        self._vega = self._parse(vega, (0.0001, 1.0, True))
        self._analytical_vega = vega is None

    @staticmethod
    def _parse(arg, default=tuple()):
        # fill list entries by arg entries
        if arg is None:
            return default
        arg = [arg] if not isinstance(arg, (list, tuple)) else arg
        ret = list(default)
        for i in range(len(default)):
            ret[i] = arg[i] if i < len(arg) else default[i]
        return tuple(ret)

    # --- pricing ---
    def option_value(self, forward, strike, time, volatility, option_type, discount_factor=1.0):
        return discount_factor * self._option_value(forward, strike, time, volatility, option_type)

    def _option_value(self, forward, strike, time, volatility, option_type):
        raise NotImplementedError

    # --- solving ---
    def implied_vol(self, forward, strike, time, price, option_type, discount_factor=1.0):
        option_val = OptionValueByVolatility(self.option_value, forward, strike, time, option_type, discount_factor)
        implied_vol_calculator = ImpliedVolCalculator()
        impl_vol = implied_vol_calculator.implied_vol(price, option_val, 0.15, 0.03)
        return impl_vol

    # --- delta risk ---
    def delta(self, forward, strike, time, volatility, option_type, discount_factor=1.0):
        risk = None
        if self._analytical_delta:
            risk = self._analytic_delta(forward, strike, time, volatility, option_type)
        if risk is None:
            risk = self._bump_delta(forward, strike, time, volatility, option_type)
        return discount_factor * risk

    def _analytic_delta(self, forward, strike, time, volatility, option_type):
        return None

    def _bump_delta(self, forward, strike, time, volatility, option_type):
        f = (lambda x: self.option_value(x, strike, time, volatility, option_type))
        shift, quote, shift_abs = self._delta
        forward_shift = shift if shift_abs else forward * shift
        return quote * (f(forward + forward_shift) - f(forward)) / shift

    # --- gamma risk ---
    def gamma(self, forward, strike, time, volatility, option_type, discount_factor=1.0):
        risk = None
        if self._analytical_delta:
            risk = self._analytic_gamma(forward, strike, time, volatility, option_type)
        if risk is None:
            risk = self._bump_gamma(forward, strike, time, volatility, option_type)
        return discount_factor * risk

    def _analytic_gamma(self, forward, strike, time, volatility, option_type):
        return None

    def _bump_gamma(self, forward, strike, time, volatility, option_type):
        f = (lambda x: self._bump_delta(x, strike, time, volatility, option_type))
        shift, quote, shift_abs = self._delta
        forward_shift = shift if shift_abs else forward / shift
        return quote * (f(forward) - f(forward - forward_shift)) / shift

    # --- vega risk ---
    def vega(self, forward, strike, time, volatility, option_type, discount_factor=1.0):
        risk = None
        if self._analytical_vega:
            risk = self._analytic_vega(forward, strike, time, volatility, option_type)
        if risk is None:
            risk = self._bump_vega(forward, strike, time, volatility, option_type)
        return discount_factor * risk

    def _analytic_vega(self, forward, strike, time, volatility, option_type):
        return None

    def _bump_vega(self, forward, strike, time, volatility, option_type):
        f = (lambda x: self.option_value(forward, strike, time, x, option_type))
        shift, quote, shift_abs = self._vega
        volatility_shift = shift if shift_abs else volatility * shift
        return quote * (f(volatility + volatility_shift) - f(volatility)) / shift


class OptionValuatorIntrinsic(OptionValuator):
    def _option_value(self, forward, strike, time, volatility, option_type, discount_factor=1.0):
        if option_type == OptionType.CALL:
            result = option_payoff(forward, strike, True)
        elif option_type == OptionType.PUT:
            result = option_payoff(forward, strike, False)
        elif option_type == OptionType.DIGITAL_CALL:
            result = digital_option_payoff(forward, strike, True)
        elif option_type == OptionType.DIGITAL_CALL:
            result = digital_option_payoff(forward, strike, False)
        elif option_type == OptionType.STRADDLE:
            result = straddle_payoff(forward, strike)
        else:
            raise Exception('Unknown OptionType ' + str(option_type) + ' ' + __name__)
        return discount_factor * result

    def implied_vol(self, forward, strike, time, price, option_type, discount_factor=1.0):
        return 0.0


class OptionValuatorN(OptionValuator):
    def _option_value(self, forward, strike, time, volatility, option_type):
        if option_type == OptionType.CALL:
            return bachelier(forward, strike, volatility, time, True)
        if option_type == OptionType.PUT:
            return bachelier(forward, strike, volatility, time, False)
        if option_type == OptionType.DIGITAL_CALL:
            return bachelier_digital(forward, strike, volatility, time, True)
        if option_type == OptionType.DIGITAL_PUT:
            return bachelier_digital(forward, strike, volatility, time, False)
        if option_type == OptionType.STRADDLE:
            return bachelier_straddle(forward, strike, volatility, time, False)
        return None

    def _analytic_delta(self, forward, strike, time, volatility, option_type):
        if option_type == OptionType.CALL:
            return bachelier_delta(forward, strike, volatility, time, True)
        if option_type == OptionType.PUT:
            return bachelier_delta(forward, strike, volatility, time, False)
        if option_type == OptionType.DIGITAL_CALL:
            return bachelier_digital_delta(forward, strike, volatility, time, True)
        if option_type == OptionType.DIGITAL_PUT:
            return bachelier_digital_delta(forward, strike, volatility, time, False)
        if option_type == OptionType.STRADDLE:
            return bachelier_straddle_delta(forward, strike, volatility, time, False)
        return None

    def _analytic_gamma(self, forward, strike, time, volatility, option_type):
        if option_type == OptionType.CALL:
            return bachelier_gamma(forward, strike, volatility, time, True)
        if option_type == OptionType.PUT:
            return bachelier_gamma(forward, strike, volatility, time, False)
        if option_type == OptionType.DIGITAL_CALL:
            return bachelier_digital_gamma(forward, strike, volatility, time, True)
        if option_type == OptionType.DIGITAL_PUT:
            return bachelier_digital_gamma(forward, strike, volatility, time, False)
        if option_type == OptionType.STRADDLE:
            return bachelier_straddle_gamma(forward, strike, volatility, time, False)
        return None

    def _analytic_vega(self, forward, strike, time, volatility, option_type):
        if option_type == OptionType.CALL:
            return bachelier_vega(forward, strike, volatility, time, True)
        if option_type == OptionType.PUT:
            return bachelier_vega(forward, strike, volatility, time, False)
        if option_type == OptionType.DIGITAL_CALL:
            return bachelier_digital_vega(forward, strike, volatility, time, True)
        if option_type == OptionType.DIGITAL_PUT:
            return bachelier_digital_vega(forward, strike, volatility, time, False)
        if option_type == OptionType.STRADDLE:
            return bachelier_straddle_vega(forward, strike, volatility, time, False)
        return None


class OptionValuatorLN(OptionValuator):
    def _option_value(self, forward, strike, time, volatility, option_type, ):
        if option_type == OptionType.CALL:
            return black(forward, strike, volatility, time, True)
        if option_type == OptionType.PUT:
            return black(forward, strike, volatility, time, False)
        if option_type == OptionType.DIGITAL_CALL:
            return black_digital(forward, strike, volatility, time, True)
        if option_type == OptionType.DIGITAL_PUT:
            return black_digital(forward, strike, volatility, time, False)
        if option_type == OptionType.STRADDLE:
            return black_straddle(forward, strike, volatility, time, False)
        return None

    def _analytic_delta(self, forward, strike, time, volatility, option_type):
        if option_type == OptionType.CALL:
            return black_delta(forward, strike, volatility, time, True)
        if option_type == OptionType.PUT:
            return black_delta(forward, strike, volatility, time, False)
        if option_type == OptionType.DIGITAL_CALL:
            return black_digital_delta(forward, strike, volatility, time, True)
        if option_type == OptionType.DIGITAL_PUT:
            return black_digital_delta(forward, strike, volatility, time, False)
        if option_type == OptionType.STRADDLE:
            return black_straddle_delta(forward, strike, volatility, time, False)
        return None

    def _analytic_gamma(self, forward, strike, time, volatility, option_type):
        if option_type == OptionType.CALL:
            return black_gamma(forward, strike, volatility, time, True)
        if option_type == OptionType.PUT:
            return black_gamma(forward, strike, volatility, time, False)
        if option_type == OptionType.DIGITAL_CALL:
            return black_digital_gamma(forward, strike, volatility, time, True)
        if option_type == OptionType.DIGITAL_PUT:
            return black_digital_gamma(forward, strike, volatility, time, False)
        if option_type == OptionType.STRADDLE:
            return black_straddle_gamma(forward, strike, volatility, time, False)
        return None

    def _analytic_vega(self, forward, strike, time, volatility, option_type):
        if option_type == OptionType.CALL:
            return black_vega(forward, strike, volatility, time, True)
        if option_type == OptionType.PUT:
            return black_vega(forward, strike, volatility, time, False)
        if option_type == OptionType.DIGITAL_CALL:
            return black_digital_vega(forward, strike, volatility, time, True)
        if option_type == OptionType.DIGITAL_PUT:
            return black_digital_vega(forward, strike, volatility, time, False)
        if option_type == OptionType.STRADDLE:
            return black_straddle_vega(forward, strike, volatility, time, False)
        return None


class OptionValuatorSLN(OptionValuator):
    def __init__(self, displacement=0.03, delta=None, vega=None):
        super(OptionValuatorSLN, self).__init__(delta, vega)
        self.displacement = displacement
        self._option_valuatorLN = OptionValuatorLN()

    def _get_shifted_forward_and_strike(self, forward, strike):
        return forward + self.displacement, strike + self.displacement

    def _option_value(self, forward, strike, time, volatility, optionType):
        fwd, k = self._get_shifted_forward_and_strike(forward, strike)
        return self._option_valuatorLN._option_value(fwd, k, time, volatility, optionType)

    def implied_vol(self, forward, strike, time, price, optionType, discount_factor=1.0):
        fwd, k = self._get_shifted_forward_and_strike(forward, strike)
        return self._option_valuatorLN.implied_vol(fwd, k, time, price, optionType, discount_factor)

    def _analytic_vega(self, forward, strike, time, volatility, option_type):
        fwd, k = self._get_shifted_forward_and_strike(forward, strike)
        return self._option_valuatorLN._analytic_vega(fwd, k, time, volatility, option_type)

    def _analytic_gamma(self, forward, strike, time, volatility, option_type):
        fwd, k = self._get_shifted_forward_and_strike(forward, strike)
        return self._option_valuatorLN._analytic_gamma(fwd, k, time, volatility, option_type)

    def _analytic_delta(self, forward, strike, time, volatility, option_type):
        fwd, k = self._get_shifted_forward_and_strike(forward, strike)
        return self._option_valuatorLN._analytic_delta(fwd, k, time, volatility, option_type)

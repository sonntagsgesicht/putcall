# -*- coding: utf-8 -*-

# putcall
# -------
# Collection of classical option pricing formulas.
# 
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.2, copyright Saturday, 14 September 2019
# Website:  https://github.com/sonntagsgesicht/putcall
# License:  Apache License 2.0 (see LICENSE file)


from mathtoolspy import Optimizer1Dim, Constraint
from mathtoolspy.solver.minimize_algorithm_1dim_brent import minimize_algorithm_1dim_brent as brent


class OptionValueByVolatility:
    def __init__(self, option_value_function, forward, strike, time, option_type, discount_factor=1.0):
        self.option_value_function = option_value_function
        self.forward = forward
        self.strike = strike
        self.time = time
        self.option_type = option_type
        self.discount_factor = discount_factor

    def option_value(self, vol):
        return self.option_value_function(self.forward, self.strike, self.time, vol, self.option_type,
                                          self.discount_factor)

    def __call__(self, vol):
        return self.option_value(vol)


class ImpliedVolCalculator:
    VOL_CALIB_TOL = 1e-9
    MAX_VOL_FOR_IMPLIED_VOL = 10.0

    def implied_vol(self, price, option_value_function_by_volatility, upper_bound=1.0, initial_value=0.05):
        dev_fct = ImpliedVolCalculator.ImpliedVolErrorFunction(price, option_value_function_by_volatility)
        opt = Optimizer1Dim(minimize_algorithm=brent)
        MAXVOL = ImpliedVolCalculator.MAX_VOL_FOR_IMPLIED_VOL
        tol = ImpliedVolCalculator.VOL_CALIB_TOL
        max_vol = upper_bound if upper_bound < MAXVOL else MAXVOL
        while max_vol <= ImpliedVolCalculator.MAX_VOL_FOR_IMPLIED_VOL:
            constraint = Constraint(0.000001, max_vol)
            opt_result = opt.optimize(dev_fct, constraint, initial_value, tol)
            if opt_result.successful:
                impl_vol = opt_result.xmin * opt_result.xmin
                return impl_vol
            max_vol = 2.0 * max_vol
        raise Exception("Unable to find implied volatility for price " + str(price))

    class ImpliedVolErrorFunction:
        def __init__(self, price, option_value_function_by_volatility):
            self.price = price
            self.option_value = option_value_function_by_volatility

        def __call__(self, squared_root_of_vol):
            vol = squared_root_of_vol * squared_root_of_vol
            price = self.option_value(vol)
            diff = price - self.price
            return abs(diff)

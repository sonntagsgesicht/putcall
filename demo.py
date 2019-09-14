# -*- coding: utf-8 -*-

# putcall
# -------
# Collection of classical option pricing formulas.
# 
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.2, copyright Saturday, 14 September 2019
# Website:  https://github.com/sonntagsgesicht/putcall
# License:  Apache License 2.0 (see LICENSE file)


import numpy as np
from scipy.optimize import minimize

from putcall.formulas.interest_rate_options import sabr


def tprint(*args):
    # print(' '.join([str(x) for x in args]))  # print accepted for tutorials
    pass


tprint('')
tprint('first sabr test')
shift = 0.00
s, f, a, b, n, r, t = (0.005, 0.03, 0.001, 0.4, 0.01, 0.15, 5)
tprint(sabr.sabr_black_vol(s + shift, f + shift, a, b, n, r, t))
tprint(sabr.sabr_alpha_from_atm(f, 0.005, b, n, r, t))
tprint(sabr.sabr_atmadj_black_vol(s, f, 0.005, b, n, r, t))

if 0:
    x = [float(s) * 0.0001 for s in range(100, 1500, 1)]
    y = list()
    y = [sabr.sabr_black_vol(s + shift, f + shift, a, b, n, r, t) for s in x]
    x = [s + shift for s in x]
    g = [f + p for p in (-0.015, -0.01, -0.005, -0.0025, 0, 0.0025, 0.005, 0.01, 0.015)]
    q = [sabr.sabr_black_vol(s + shift, f + shift, a, b, n, r, t) for s in g]
    g = [p + shift for p in g]
    # import matplotlib.pyplot as plt
    # plt.plot(x, y, '-')
    # plt.plot(g, q, 'ro')
    # plt.show()

# --- sabr cali ---
def min_sabr(x):
    forward_value = 0.03
    beta_value = 0.1
    strike_list = [forward_value + p for p in (-0.015, -0.01, -0.005, -0.0025, 0, 0.0025, 0.005, 0.01, 0.015)]
    target_list = [0.2, 0.15, 0.11, 0.9, 0.8, 0.7, 0.8, 0.85, 0.9]
    ret = 0.00
    for i in range(len(strike_list)):
        s = strike_list[i]
        f = forward_value
        t = 5
        a = x[0]
        b = beta_value
        n = x[1]
        r = x[2]
        ret += (sabr.sabr_black_vol(s, f + shift, a, b, n, r, t) - target_list[i]) ** 2
    return ret


x0 = np.array([0.001, 0.01, 0.15])
# res = minimize(min_sabr, x0, method='nelder-mead', options={'xtol': 1e-8, 'disp': True})
res = minimize(min_sabr, x0)
tprint(res.x)

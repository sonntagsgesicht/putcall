# -*- coding: utf-8 -*-

# putcall
# -------
# Collection of classical option pricing formulas.
# 
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.2, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/putcall
# License:  Apache License 2.0 (see LICENSE file)


def convexity_option_replication(strike_value, forward_value, implied_vol_surface, time_value, is_call_bool,
                                 swap_maturity_value):
    """
        Hagan CMS option replication using swaptions

    @param strike_value:
    @param forward_value:
    @param implied_vol_surface:
    @param time_value:
    @param is_call_bool:
    @return:
    """
    pass

"""
def convexity_option_replication(isCall,strikePrice,payDelay,cfPeriods,nPeriods,volaInfo,resetDate,longestEndDate,
fwdRate,fixedTime,discountPayStart,payDate):

    # control integration
    eps             = 1e-12
    step            = 0.0005
    maxStrike       = 0.15
    minStrike       = -0.10

    # cast dates to ael.date
    if type(resetDate)==type(''):           resetDate       = ael.date_from_string(resetDate)
    if type(longestEndDate)==type(''):      longestEndDate  = ael.date_from_string(longestEndDate)

    # get vol type (log-normal or normal)
    volsStruc = volaInfo.VolatilityStructure()
    if volsStruc.Framework() == 'Black & Scholes':
        pricer          = BlackScholes
        minStrike       = eps
    elif volsStruc.Framework() == 'Black & Scholes - Normal':
        pricer          = NormalBlackScholes
    else:
        print 'vola %s of type %s not supported' %(volaInfo.Name(),volsStruc.Framework())
        raise
    #print 'use vola %s of type %s' %(volaInfo.Name(),volsStruc.Framework())

    # build strike grid
    s = strikePrice
    grid = []

    if isCall:
        while s < maxStrike:
            grid.append(s)
            s += step
    else:
        step *= -1
        while s > minStrike:
            grid.append(s)
            s += step
    #print 'grid', len(grid), min(grid), max(grid)

    # declare inital values
    i = 1
    price = 0
    weight = 0
    weightSum = 0
    weightSumSum = 0

    lastPayoffRatio = 0
    priceSG = 0
    weightSG = 0
    weightSGSum = 0

    # replicate with swaption portfolio
    for strikePrice in grid:
        # derive swaption weight
        repliPrice          = strikePrice + step
        payoffRatio         = (1 + repliPrice*payDelay) * getCashLevel(cfPeriods,nPeriods,repliPrice)
        weight              = i / payoffRatio - weightSum - weightSumSum
        #print 'weight ', weight, weightSum, weightSumSum

        # calculate swaption value
        vola                = volaInfo.Value(longestEndDate, resetDate,(strikePrice-fwdRate)*100, 0, 0)
        if volsStruc.Framework() == 'Black & Scholes - Normal':
            vola = vola/100
        swaptionPrice       = pricer(fwdRate,strikePrice,fixedTime,vola,isCall)
        #print 'swaption', fixedTime, strikePrice-fwdRate, vola, swaptionPrice

        # add swaption contribution to price
        price               = price + weight*swaptionPrice
        #print 'price   ', price, weight*swaptionPrice

        strikePrice += step
        weightSum += weight
        weightSumSum += weightSum

        # double check with soc gen implementation
        if 0:
            weightSG = i / payoffRatio - lastPayoffRatio - weightSGSum
            weightSGSum += weightSG
            priceSG = priceSG + weightSG*swaptionPrice

            lastPayoffRatio = i / payoffRatio


        # iterate
        i += 1

        # exit from loop when either contribution to price is negligible
        #if price and ( abs(weight*swaptionPrice/price) < eps ): break
        if price and ( abs(weight*swaptionPrice) < eps ): break

    #print 'payDate', payDate, 'i', i, 'strike ', repliPrice, 'contributions', weight*swaptionPrice,'price ', price

    # return replication price
    return price * getCashLevel(cfPeriods,nPeriods,fwdRate) / discountPayStart


def getCashLevel(cfPeriods,nPeriods,swapRate):
    return ( 1 - (1+swapRate*cfPeriods)**(-nPeriods) ) / swapRate


"""

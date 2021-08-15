# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 21:13:44 2021

@author: Danib
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import pandas as pd
import matplotlib
import numpy as np
import yfinance as yf 
from matplotlib import warnings
import backtrader.plot
matplotlib.use('QT5Agg')

# Import the backtrader platform
import backtrader as bt


# Create a Stratey
from datetime import datetime
import backtrader as bt

# Create a subclass of Strategy to define the indicators and logic

class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )
    
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        #print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
        # Keep a reference to the "close" line in the data[0] dataseries
       # self.dataclose = self.datas[0].close

    def next(self):
        # Simply log the closing price of the series from the reference
        #self.log('Close, %.2f' % self.dataclose[0])
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position


cerebro = bt.Cerebro()  # create a "Cerebro" engine instance


stock_prices = pd.read_csv('AAPL.csv', index_col=[0], parse_dates=[0])
# create data feed pandas df
feed = bt.feeds.PandasData(dataname=stock_prices)
# add feed
cerebro.adddata(feed)

cerebro.addstrategy(SmaCross)  # Add the trading strategy


print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()  # run it all
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot(iplot=False)

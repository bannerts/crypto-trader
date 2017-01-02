import datetime
import os, os.path
# import pandas as pd

from abc import ABCMeta, abstractmethod
from modules.event import MarketEvent


class DataHandler(object):
    """
    DataHandler is an abstract base class providing an interface for
    all subsequent (inherited) data handlers (both live and historic).

    The goal of a (derived) DataHandler object is to output a generated
    set of bars (OLHCVI) for each symbol requested. 

    This will replicate how a live strategy would function as current
    market data would be sent "down the pipe". Thus a historic and live
    system will be treated identically by the rest of the backtesting suite.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_latest_bars(self, symbol, N=1):
        """
        Returns the last N bars from the latest_symbol list,
        or fewer if less bars are available.
        """
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    def update_bars(self):
        """
        Pushes the latest bar to the latest symbol structure
        for all symbols in the symbol list.
        """
        raise NotImplementedError("Should implement update_bars()")


class HistoricCSVDataHandler(DataHandler):
    """
    HistoricCSVDataHandler is designed to read CSV files for
    each requested symbol from disk and provide an interface
    to obtain the "latest" bar in a manner identical to a live
    trading interface. 
    """

    def __init__(self, events, csv_dir, symbol_list):
        """
        Initialises the historic data handler by requesting
        the location of the CSV files and a list of symbols.

        It will be assumed that all files are of the form
        'symbol.csv', where symbol is a string in the list.

        Parameters:
        events - The Event Queue.
        csv_dir - Absolute directory path to the CSV files.
        symbol_list - A list of symbol strings.
        """
        self.events = events
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True       

        self._open_convert_csv_files()

    def _open_convert_csv_files(self):
        """
        Opens the CSV files from the data directory, converting
        them into a dictionary.
        CSV: 'datetime', 'open', 'low', 'high', 'close', 'volume', 'oi'

        """
        self.symbol_data = {}
        for s in self.symbol_list:
            # Load each CSV file
            file_name = os.path.join(self.csv_dir, '%s.csv' % s)
            f = open(self.csv_dir, 'r')
            i = 0
            X = {}
            names = []
            for line in f:
                if i = 0:
                    names = line.split(str=',')
                    for name in names:
                        X[name] = []
                else:
                    values = line.split(str=',')
                    for j in range(len(names)):
                        X[names[j]].append(values[j])
                i += 1
            self.symbol_data[s] = X

    def _get_new_bar(self, symbol):
        """
        Returns the latest bar from the data feed as a tuple of 
        (sybmbol, datetime, open, low, high, close, volume).
        """
        D = self.symbol_data[symbol]
        K = D.keys()
        i = 0
        for i in range(len(D[K[0]])):
            out = {}
            for key in K:
                out[key] = D[key][i]
            yield out

    def get_latest_bars(self, symbol, N=1):
        """
        Returns the last N bars from the latest_symbol list,
        or N-k if less available.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print "That symbol is not available in the historical data set."
        else:
            out = {}
            for key in bars_list.keys():
                out[key] = bars_list[key][-N:]
            return out        

   def update_bars(self):
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for s in self.symbol_list:
            try:
                bar = self._get_new_bar(s).next()
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    for key in bar.keys():
                        self.latest_symbol_data[s][key].append(bar[key])
        self.events.put(MarketEvent())

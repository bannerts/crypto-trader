# crypto-trader
Files related to the development of a crypt currency trading bot

# Install python 3.4 (or later)
    - comes with pip

## Major Components:

Event: 
fundamental class of event-driven system containing type (such as “MARKET”, “SIGNAL”, “ORDER”, “FILL”)

Event Queue: 
stores all of the Event objects generated by software in a queue for execution

DataHandler:
interface for handling both historical and live market data
generates a MarketEvent upon every heartbeat of the system

Strategy:
Interface for taking market data and generating corresponding SignalEvents related to a trading strategy

Portfolio:
interface handling order management associated with current and subsequent positions for a strategy
delegated to risk management in sophisticated implementation (using techniques such as Kelly Criterion)

ExecutionHandler:
interface to a brokerage (brokerage is simulated for backtesting)
handles OrderEvents from Queue by sending them with brokerage
fillEvents describe transactions after executed by brokerage

The Loop:
wraps all components in an event-loop
handles events by routing them to appropriate components

Reference: http://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-I

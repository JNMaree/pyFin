# Native Python modules
import datetime as dt
import enum
import imp

# External modules
import numpy as np

# Local modules


# Define the standard interest rate conversions
class IRConv(enum.Enum):
    NACC = 0
    NACA = 1
    NACS = 2
    NACQ = 4
    NACM = 12
    NACD = 365


# Define the Interest Rate Conventions
#   - default convention is NACC
class IR:
    def __init__(self, rate: float, irc: IRConv = IRConv.NACC) -> None:
        self.NACC = rate if irc == IRConv.NACC else self.to_continuousIR(rate, irc)
        self.NACA = rate if irc == IRConv.NACA else self.to_compoundIR(rate, irc, 1)
        self.NACS = rate if irc == IRConv.NACS else self.to_compoundIR(rate, irc, 2)
        self.NACQ = rate if irc == IRConv.NACQ else self.to_compoundIR(rate, irc, 4)
        self.NACM = rate if irc == IRConv.NACM else self.to_compoundIR(rate, irc, 12)
        self.NACD = rate if irc == IRConv.NACD else self.to_compoundIR(rate, irc, 365)
    def __str__(self) -> str:
        sret = f'{self.NACC * 100 :>12.8f}% NACC'
        return sret

    # Calculate the equivalent simple interest for the specified term duration
    def SIMPLE(self, term: int) -> float:
        return np.exp(-self.NACC) - 1
    
    # Convert Compound interest rate to Continuous
    def to_continuousIR(self, rate: float, irc: IRConv) -> float:
        return np.log((1 + rate/irc.value)**(float(irc.value)))

    # Convert Continous and Compound interest rates to Compound of a different period.
    def to_compoundIR(self, rate: float, irc: IRConv, cperiod: int) -> float:
        if irc == IRConv.NACC:     # Continuous to Compound
            return ((np.exp(rate))**(1/cperiod) - 1)*cperiod
        else:                       # Compound to Compound
            return ((1+rate/irc.value)**(irc.value/cperiod) - 1)*cperiod

    # Define the discount factor for two options for types of parameters:
    #   - Duration(int): Calculate the DF for the specified duration in days
    #   - Duration(float): Calculate the CF for the specified year fraction
    #   - Dates(list[dt.date_1, dt.date_2]): Calculate the DF to the specified date_2, from date_1
    def discount_to(self, d_day) -> float:
        if isinstance(d_day, (int)):        # If duration (in days) specified
            return np.exp(-(d_day/365) * self.NACC)
        elif isinstance(d_day, (float)):    # If duration (in fraction of a year) specified
            return np.exp(-d_day * self.NACC)
        elif isinstance(d_day, (list)):     # If day list is specified
            dt_d = dt.timedelta(d_day[1] - d_day[0]).days
            return np.exp(-(dt_d/365) * self.NACC)
        else:
            raise TypeError(f'discount function:\nType<{type(d_day)}> of {d_day} not accommodated.')
    
    # Define the capitilisation factor for two options for types of parameters:
    #   - Duration(int): Calculate the CF for the specified duration in days
    #   - Duration(float): Calculate the CF for the specified year fraction
    #   - Dates(list[dt.date_1, dt.date_2]): Calculate the CF to the specified date_2, from date_1
    def capitilise_to(self, d_day) -> float:
        if isinstance(d_day, (int)):        # If duration (in days) specified
            return np.exp((d_day/365) * self.NACC)
        elif isinstance(d_day, (float)):    # If duration (in fraction of a year) specified
            return np.exp((d_day/365) * self.NACC)
        elif isinstance(d_day, (list)):     # If day list specified
            dt_d = dt.timedelta(d_day[1] - d_day[0])
            return np.exp((dt_d/365) * self.NACC)
        else:
            raise TypeError(f'capitilise function:\nType<{type(d_day)}> of {d_day} not accommodated.')
# Native Python modules
import unittest
import enum
import datetime as dt

# External modules
import numpy as np
import holidays

# Local modules
import base.day

# Define all the Day Count Conventions (DCCs)
class DCC(enum.Enum):
    ACT_365 = 0
    ACT_360 = 1
    ACT_365_FIX = 2
    ACT_ACT = ACT_365
    B30_60 = 3
    BONDS_BASIS = B30_60
    B30_360E = 4

#   - Return TRUE if leap year
#   - Return FALSE if not leap year
def is_leap_year(year: int) -> bool:
    if year % 4 == 0:
        if year % 100 == 0:
            return True if year % 400 == 0 else False
        else:
            return True
    else:
        return False

# Compute the day count fraction per year for the specified two dates and convention.
#   - Default DCC is ACT 365
def day_count_factor(day_1: dt.date, day_2: dt.date, dcc: DCC = DCC.ACT_365) -> float:
    if dcc == DCC.ACT_365:                                                  # ACT 365
        df_d = (day_2 - day_1).days
        df_y = (day_2.year - day_1.year)    # number of years
        if df_y > 0:        # Dates fall in different years
            sum_day_fraction = dt.timedelta((dt.date(day_1.year,12,31)-day_1).days + 1).days/(366 if is_leap_year(day_1.year) else 365)
            for i in range(df_y - 1):
                sum_day_fraction += 1.0
            sum_day_fraction += (dt.timedelta((day_2 - dt.date(day_2.year, 1, 1)).days).days)/(366 if is_leap_year(day_2.year) else 365)
            return sum_day_fraction
        else:               # Dates fall into the same year
            return df_d/(366 if is_leap_year(day_1.year) else 365)
    elif dcc == DCC.ACT_360:                                                # ACT 360
        return (dt.timedelta((day_2 - day_1).days).days)/360
    elif dcc == DCC.ACT_365_FIX:                                            # ACT 365 FIX
        return (dt.timedelta((day_2 - day_1).days).days)/365
    elif dcc == DCC.B30_60 or dcc == DCC.B30_360E:                          # B30/60 + B30/60E                 
        df_y = day_2.year - day_1.year
        df_m = day_2.month - day_1.month
        d1 = day_1.day        
        d2 = day_2.day

        if dcc == DCC.B30_60:           # set the days for B30_60 
            d1 = min(d1, 30)
            if d1 > 29:
                d2 = min(d2, 30)
        else:                           # set the days for B30_60E
            d1 = 30 if d1 == 31 else d1
            d2 = 30 if d1 == 31 else d2
        df_d = d2 - d1
        return (360*df_y + 30*df_m + df_d)/360

    else:
        raise TypeError(f"{dcc} is of Unknown DCC Type.")


# Define all the Day Count Conventions (DCCs)
class DCC(enum.Enum):
    ACT_365 = 0
    ACT_360 = 1
    ACT_365_FIX = 2
    ACT_ACT = ACT_365
    B30_60 = 3
    BONDS_BASIS = B30_60
    B30_360E = 4


#   - Return TRUE if leap year
#   - Return FALSE if not leap year
def is_leap_year(year: int) -> bool:
    if year % 4 == 0:
        if year % 100 == 0:
            return True if year % 400 == 0 else False
        else:
            return True
    else:
        return False

# Compute the day count fraction per year for the specified two dates and convention.
#   - Default DCC is ACT 365
def day_count_factor(day_1: dt.date, day_2: dt.date, dcc: DCC = DCC.ACT_365) -> float:
    if dcc == DCC.ACT_365:                                                  # ACT 365
        df_d = (day_2 - day_1).days
        df_y = (day_2.year - day_1.year)    # number of years
        if df_y > 0:        # Dates fall in different years
            sum_day_fraction = dt.timedelta((dt.date(day_1.year,12,31)-day_1).days + 1).days/(366 if is_leap_year(day_1.year) else 365)
            for i in range(df_y - 1):
                sum_day_fraction += 1.0
            sum_day_fraction += (dt.timedelta((day_2 - dt.date(day_2.year, 1, 1)).days).days)/(366 if is_leap_year(day_2.year) else 365)
            return sum_day_fraction
        else:               # Dates fall into the same year
            return df_d/(366 if is_leap_year(day_1.year) else 365)
    elif dcc == DCC.ACT_360:                                                # ACT 360
        return (dt.timedelta((day_2 - day_1).days).days)/360
    elif dcc == DCC.ACT_365_FIX:                                            # ACT 365 FIX
        return (dt.timedelta((day_2 - day_1).days).days)/365
    elif dcc == DCC.B30_60 or dcc == DCC.B30_360E:                          # B30/60 + B30/60E                 
        df_y = day_2.year - day_1.year
        df_m = day_2.month - day_1.month
        d1 = day_1.day        
        d2 = day_2.day

        if dcc == DCC.B30_60:           # set the days for B30_60 
            d1 = min(d1, 30)
            if d1 > 29:
                d2 = min(d2, 30)
        else:                           # set the days for B30_60E
            d1 = 30 if d1 == 31 else d1
            d2 = 30 if d1 == 31 else d2
        df_d = d2 - d1
        return (360*df_y + 30*df_m + df_d)/360

    else:
        raise TypeError(f"{dcc} is of Unknown DCC Type.")
        
# Define all the valid business day (VBD) conventions
class BDC(enum.Enum):
    NO_ADJUSTMENT = -1
    FOLLOWING = 0
    PRECEDING = 1
    MOD_FOLLOWING = 2

# Get the day of the week (dow): int form:
#   - returns an integer representing the day of the week
#       0 = Mon
#       1 = Tues ...
#       6 = Sun
def dow_int(day_date: dt.date) -> int:
    return day_date.weekday()

# Get the day of the week (dow): str form:
#   - Returns string of name of day
def dow_str(day_date) -> str:
    return day_date.strftime("%A")

# Get the next valid business day based off the desired input day
def valid_business_day(d_day: dt.date, bdc: BDC) -> dt.date:
    dow = dow_int(d_day)
    hol = d_day in holidays.SouthAfrica(years=d_day.year)
    #print(f'{d_day} dow:{dow} hol:{hol}')
    if dow > 4 or hol:
        if bdc == BDC.NO_ADJUSTMENT:
            return d_day
        if bdc == BDC.FOLLOWING:
            return valid_business_day(d_day + dt.timedelta(days=1), bdc)
        elif bdc == BDC.PRECEDING:
            return valid_business_day(d_day - dt.timedelta(days=1), bdc)
        elif bdc == BDC.MOD_FOLLOWING:
            vbd_fol = valid_business_day(d_day + dt.timedelta(days=1), bdc)
            if vbd_fol.month != d_day.month:
                return valid_business_day(d_day - dt.timedelta(days=1), BDC.PRECEDING)
            else:
                return vbd_fol
    else:
        return d_day

# Generate a chronological cash-flow schedule for the specified:
#   - maturity date, 
#   - time period (years) 
#   - cash flow frequency(n payments per year)
def gen_cf_schedule(d_maturity: dt.date, t_period, cff: int) -> np.array:
    lret = np.array([])
    if isinstance(t_period, dt.timedelta):      # dt.TimeDelta specified
        n_pay = int ((t_period.days/365) * cff)
    elif isinstance(t_period, (int, float)):    # Years specified
        n_pay = int (t_period*cff)
    elif isinstance(t_period, dt.date):         # Settle date specified
        n_pay = int( (d_maturity - t_period).days / 365 )
    
    for c in range(n_pay):
        d_day = valid_business_day(d_maturity - dt.timedelta(days=c*365/cff), BDC.MOD_FOLLOWING)
        lret = np.append(lret, d_day)
    return lret[::-1]


# Implement native unit testing framework to execute test cases & verify results.
class TestDCC(unittest.TestCase):
    def test_day_count_factor(self):

        # Conventional Years:
        # Test single year day count fractions for all conventions
        self.assertEqual(day_count_factor(dt.date(2019, 2, 16), dt.date(2019, 2, 28), DCC.ACT_365), 12/365)
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2020, 2, 28), DCC.ACT_365), 12/366)
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2020, 2, 28), DCC.ACT_360), 12/360)
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2020, 2, 28), DCC.ACT_365_FIX), 12/365)
        self.assertEqual(day_count_factor(dt.date(2020, 3, 16), dt.date(2020, 4, 1), DCC.B30_60), 15/360)
        self.assertEqual(day_count_factor(dt.date(2020, 3, 16), dt.date(2020, 4, 1), DCC.B30_360E), 15/360)
        # Test multi-year day count fractions for all conventions
        self.assertEqual(day_count_factor(dt.date(2018, 2, 16), dt.date(2019, 2, 28), DCC.ACT_365), 319/365 + 58/365)
        self.assertEqual(day_count_factor(dt.date(2018, 2, 16), dt.date(2019, 1, 28), DCC.ACT_365), 319/365 + 27/365)
        self.assertEqual(day_count_factor(dt.date(2018, 2, 16), dt.date(2019, 2, 28), DCC.ACT_360), 319/360 + 58/360)
        self.assertEqual(day_count_factor(dt.date(2018, 2, 16), dt.date(2019, 1, 28), DCC.ACT_365_FIX), 319/365 + 27/365)
        self.assertEqual(day_count_factor(dt.date(2018, 3, 16), dt.date(2019, 4, 1), DCC.B30_60), 15/360 + 1)
        self.assertEqual(day_count_factor(dt.date(2018, 3, 16), dt.date(2019, 4, 1), DCC.B30_360E), 15/360 + 1)
        
        # Leap Years:
        # Test day count fractions in Feb during leap year
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2020, 3, 1), DCC.ACT_365), 14/366)
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2020, 3, 1), DCC.ACT_365), 14/366)
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2020, 3, 1), DCC.ACT_365), 14/366)
        # Test day count fractions across multiple years (normal and leap years)
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2022, 3, 1), DCC.ACT_365), 320/366 + 1 + 59/365)
        self.assertEqual(day_count_factor(dt.date(2019, 2, 16), dt.date(2020, 3, 1), DCC.ACT_365), 319/365 + 60/366)
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2022, 3, 1), DCC.ACT_365), 320/366 + 1 + 59/365)
        self.assertEqual(day_count_factor(dt.date(2023, 2, 16), dt.date(2025, 3, 1), DCC.ACT_365), 319/365 + 1 + 59/365)

unittest.main(TestDCC(), argv=[''], verbosity=2, exit=False)     # Call the unit test function

class TestVBD(unittest.TestCase):
    def test_valid_business_day(self):
        # Test Weekends as dates
        self.assertEqual(valid_business_day(dt.date(2022,1,17), BDC.FOLLOWING), dt.date(2022,1,17))         # Mon -ret Mon
        self.assertEqual(valid_business_day(dt.date(2022,1,17), BDC.PRECEDING), dt.date(2022,1,17))
        self.assertEqual(valid_business_day(dt.date(2022,1,17), BDC.MOD_FOLLOWING), dt.date(2022,1,17))

        self.assertEqual(valid_business_day(dt.date(2022,1,21), BDC.FOLLOWING), dt.date(2022,1,21))         # Fri -ret Fri
        self.assertEqual(valid_business_day(dt.date(2022,1,21), BDC.PRECEDING), dt.date(2022,1,21))
        self.assertEqual(valid_business_day(dt.date(2022,1,21), BDC.MOD_FOLLOWING), dt.date(2022,1,21))

        self.assertEqual(valid_business_day(dt.date(2022,1,22), BDC.FOLLOWING), dt.date(2022,1,24))         # Sat -ret Mon
        self.assertEqual(valid_business_day(dt.date(2022,1,22), BDC.MOD_FOLLOWING), dt.date(2022,1,24))
        self.assertEqual(valid_business_day(dt.date(2022,1,22), BDC.PRECEDING), dt.date(2022,1,21))         # Sat -ret Fri
        self.assertEqual(valid_business_day(dt.date(2022,1,23), BDC.FOLLOWING), dt.date(2022,1,24))         # Sun -ret Mon
        self.assertEqual(valid_business_day(dt.date(2022,1,23), BDC.MOD_FOLLOWING), dt.date(2022,1,24))
        self.assertEqual(valid_business_day(dt.date(2022,1,23), BDC.PRECEDING), dt.date(2022,1,21))         # Sun -ret Fri
        
        # Test end of month for MOD_FOLLOWING
        self.assertEqual(valid_business_day(dt.date(2022,4,30), BDC.FOLLOWING), dt.date(2022,5,3))          # Sat -ret Tue
        self.assertEqual(valid_business_day(dt.date(2022,4,30), BDC.MOD_FOLLOWING), dt.date(2022,4,29))     # Sat -ret Fri
        self.assertEqual(valid_business_day(dt.date(2022,7,31), BDC.FOLLOWING), dt.date(2022,8,1))          # Sun -ret Mon
        self.assertEqual(valid_business_day(dt.date(2022,7,31), BDC.MOD_FOLLOWING), dt.date(2022,7,29))     # Sun -ret Fri

        # Test Holidays as dates
        # 27 April 2022 (Wednesday) - Freedom Day
        self.assertEqual(valid_business_day(dt.date(2022,4,27), BDC.FOLLOWING), dt.date(2022,4,28))         # Wed -ret Thu
        self.assertEqual(valid_business_day(dt.date(2022,4,27), BDC.PRECEDING), dt.date(2022,4,26))         # Wed -ret Tue
        self.assertEqual(valid_business_day(dt.date(2022,4,27), BDC.MOD_FOLLOWING), dt.date(2022,4,28))     # Wed -ret Thu
        # 1 May 2022 (Falls on Sunday, Monday becomes holiday) - Workers Day
        self.assertEqual(valid_business_day(dt.date(2022,5,1), BDC.FOLLOWING), dt.date(2022,5,3))           # Sun -ret Tue
        self.assertEqual(valid_business_day(dt.date(2022,5,1), BDC.PRECEDING), dt.date(2022,4,29))          # Sun -ret Fri
        self.assertEqual(valid_business_day(dt.date(2022,5,1), BDC.MOD_FOLLOWING), dt.date(2022,5,3))       # Sun -ret Tue

unittest.main(TestVBD(), argv=[''], verbosity=2, exit=False)     # Call the unit test function

# Implement native unit testing framework to execute test cases & verify results.
class TestDCC(unittest.TestCase):
    def test_day_count_factor(self):

        # Conventional Years:
        # Test single year day count fractions for all conventions
        self.assertEqual(day_count_factor(dt.date(2019, 2, 16), dt.date(2019, 2, 28), DCC.ACT_365), 12/365)
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2020, 2, 28), DCC.ACT_365), 12/366)
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2020, 2, 28), DCC.ACT_360), 12/360)
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2020, 2, 28), DCC.ACT_365_FIX), 12/365)
        self.assertEqual(day_count_factor(dt.date(2020, 3, 16), dt.date(2020, 4, 1), DCC.B30_60), 15/360)
        self.assertEqual(day_count_factor(dt.date(2020, 3, 16), dt.date(2020, 4, 1), DCC.B30_360E), 15/360)
        # Test multi-year day count fractions for all conventions
        self.assertEqual(day_count_factor(dt.date(2018, 2, 16), dt.date(2019, 2, 28), DCC.ACT_365), 319/365 + 58/365)
        self.assertEqual(day_count_factor(dt.date(2018, 2, 16), dt.date(2019, 1, 28), DCC.ACT_365), 319/365 + 27/365)
        self.assertEqual(day_count_factor(dt.date(2018, 2, 16), dt.date(2019, 2, 28), DCC.ACT_360), 319/360 + 58/360)
        self.assertEqual(day_count_factor(dt.date(2018, 2, 16), dt.date(2019, 1, 28), DCC.ACT_365_FIX), 319/365 + 27/365)
        self.assertEqual(day_count_factor(dt.date(2018, 3, 16), dt.date(2019, 4, 1), DCC.B30_60), 15/360 + 1)
        self.assertEqual(day_count_factor(dt.date(2018, 3, 16), dt.date(2019, 4, 1), DCC.B30_360E), 15/360 + 1)
        
        # Leap Years:
        # Test day count fractions in Feb during leap year
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2020, 3, 1), DCC.ACT_365), 14/366)
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2020, 3, 1), DCC.ACT_365), 14/366)
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2020, 3, 1), DCC.ACT_365), 14/366)
        # Test day count fractions across multiple years (normal and leap years)
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2022, 3, 1), DCC.ACT_365), 320/366 + 1 + 59/365)
        self.assertEqual(day_count_factor(dt.date(2019, 2, 16), dt.date(2020, 3, 1), DCC.ACT_365), 319/365 + 60/366)
        self.assertEqual(day_count_factor(dt.date(2020, 2, 16), dt.date(2022, 3, 1), DCC.ACT_365), 320/366 + 1 + 59/365)
        self.assertEqual(day_count_factor(dt.date(2023, 2, 16), dt.date(2025, 3, 1), DCC.ACT_365), 319/365 + 1 + 59/365)

unittest.main(TestDCC(), argv=[''], verbosity=2, exit=False)     # Call the unit test function
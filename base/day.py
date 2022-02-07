import unittest

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
        
        
import unittest

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
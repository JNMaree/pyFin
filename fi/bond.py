# Define a bond as a class template
class Bond:
    def __init__(self, d_issue:dt.date, d_maturity:dt.date, redemption:float, coupon:float, price:float) -> None:
        if isinstance(d_issue, (dt.date)):                                      # Set issue date
            self.d_issue = d_issue
        elif isinstance(d_issue, (str)):
            sep = '/'
            self.d_issue = dt.datetime.strptime(d_issue, f'%Y{sep}%m{sep}%d').date()
        else:
            raise TypeError(f'Incompatible Type<{type(d_issue)}> for d_issue')
        if isinstance(d_maturity, (dt.date)):                                    # Set maturity date
            self.d_maturity = d_maturity
        elif isinstance(d_maturity, (str)):
            sep = '/'
            self.d_maturity = dt.datetime.strptime(d_maturity, f'%Y{sep}%m{sep}%d').date()
        else:
            raise TypeError(f'Incompatible Type<{type(d_maturity)}> for d_maturity')
        self.redemption = redemption
        self.coupon = coupon
        self.price = price
        # Generate a standard semi-annual payment schedule for a bond
        self.schedule = gen_cf_schedule(self.d_maturity, self.d_maturity - self.d_issue, 2)
        self.values = []    # Store the values at each spot in cashflow schedule

    def __str__(self) -> str:
        sret = f'date_Issue:\t{self.d_issue}\n'
        sret += f'date_Maturity:\t{self.d_maturity}\n'
        sret += f'redemption:\t{self.redemption}\n'
        sret += f'coupon:\t{self.coupon}\n'
        sret += f'price:\t{self.price}\n'
        sret += f'cash_flow_schedule:\n{self.schedule}'
        return sret

    # Define a function to value a bond to the specified IR terms as a curve
    def value(self, curve: Curve) -> list:
        pv_y = []
        for c in self.schedule[:-1]:
            pv_y.append(self.coupon * curve.rate_at_date(self.d_maturity).discount_to(self.d_issue) )
        pv_y.append((self.redemption + self.coupon) * curve.rate_at_date(self.d_maturity).discount_to(self.d_issue))
        self.values = pv_y
        return pv_y

    # Define a function to calculate the yield to maturity (YTM) for the bond at a specific date
    def yield_to_maturity(self, d_day: dt.date) -> float:
        pass
        
        
BOOKING = 10
PROUND = 3

# Evaluate a bond according to the BESA methodology
#   - at the specified settlement date (S)
#   - with the specified yield (Y)
# Returns a list of the following values:
#   0 - Rounded Accrued Interest
#   1 - Rounded Clean Price
#   2 - Rounded All-in Price
def BESA_valuate(bond: Bond, S: dt.date) -> list:
    lret = []
    LCD = bond.d_issue                          # Set the Last Coupon Date (LCD)
    c = 1
    while S > LCD:
        c += 1
        LCD = bond.schedule[c]
    LCD = bond.schedule[c-1]
    NCD = bond.schedule[c]                      # Set the Next Coupon Date (NCD)
    BCD = NCD - dt.timedelta(days=BOOKING)      # Set the Book Close Date (BCD)
    N = len(bond.schedule) - c                  # Set the amount of coupons remaining (N)

    CUMEX = 1                                   # Set cum/ex flag (CUMEX)
    DAYSACC = (S - LCD).days                    # Set days of accrued interest (DAYSACC)
    if S > BCD:
        CUMEX = 0
        DAYSACC = (S - NCD).days

    CPN = bond.coupon/2                         # Set the coupon amount (CPN)

    CPN_NCD = CPN * CUMEX                       # Set the coupon payable (CPN_NCD)

    Y = bond.yield_to_maturity(S)               # Calculate the YTM at the Settlement Date
    F = 1/(1 + Y/200)                           # Set the semi-annual discount factor (F)

    BP = (NCD - S).days/(NCD - LCD).days        # Set the Broken Period in half years (BP)
    BPF = F**(BP)                               # Set the Broken Period Discount Factor (BPF)
    if NCD == bond.d_maturity:
        BP = (NCD - S).days/(365/2)
        BPF = F/(F + BP*(1-F))
    
    ACCINT = DAYSACC*bond.coupon/365            # Set the unrounded, accrued interest(ACCINT)
    ACCINT_R = round(ACCINT, PROUND)
    lret.append(ACCINT_R)
    
    R = bond.redemption                         # Set the redemption amount (R)
    AIP = BPF*(CPN_NCD + CPN*(F*(1-F**N))/(1-F) + R*F**N)
    if F == 1:
        AIP = CPN_NCD + CPN*N + R               # Set the all-in-price (AIP)

    CP = AIP - ACCINT                           # Set the Clean Price (CP)
    CP_R = round(CP, PROUND)
    lret.append(CP_R)

    AIP_R = CP_R + ACCINT_R
    lret.append(AIP_R)
    return lret

class TestBESA(unittest.TestCase):
    def test_besa_valuation(self):
        for b in TestBond.BONDS:
            d_settle = dt.date(2020,1,3)
            BESA_valuate(b, d_settle)

unittest.main(TestBESA(), argv=[''], verbosity=2, exit=False)
        

class TestBond(unittest.TestCase):
    CURVE = []
    BONDS = []

    def test_lerp(self):                                        # Test Linear Interpolation with numbers
        self.assertEqual(lerp([0,4],[0,4],2),2)
        self.assertEqual(lerp([2,10],[2,10],6),6)
        self.assertEqual(lerp([0,2,6,12],[2,4,7,11],4),11/2)
        d1d = dt.date(2022,1,2)                                 # Test Linear Interpolation with dates
        d1v = 4
        d2d = dt.date(2022,1,7)
        d2v = 9
        d_d = dt.date(2022,1,6)
        self.assertEqual(lerp([d1d,d2d],[d1v,d2v],d_d),8)

    def test_curve_gen(self):                                   # Test JSON parsing & Curve Generation
        try:
            f = open('JSON/Nominal Govi Bond curve.json')
            curve_data = json.load(f)
            f.close()
        except:
            raise FileNotFoundError('test_curve JSON file not found!')
        spots = []
        for cd in curve_data:
            c = Spot(dt.datetime.strptime(cd['Tenor Date'], '%Y/%m/%d').date(), cd['Year Fraction'], cd['Instrument'], IR(cd['NACC Rate']/100))
            spots.append(c)
        self.CURVE = Curve(spots)
        #self.CURVE.plot()
        #print(self.CURVE)


    def test_bond_gen(self):                                    # Test JSON parsing & Bond Generation
        try:
            f = open('JSON/Bond details.json')
            bond_data = json.load(f)
            f.close()
        except:
            raise FileNotFoundError('test_bond_gen JSON file not found!')
        bonds = [Bond]
        for bd in bond_data:
            b = Bond(bd['Issue_Date'], bd['Maturity_Date'], bd['Bond_redemption'], bd['Annual_coupon'], bd['Bond_price'])
            bonds.append(b)
        self.BONDS = bonds

    def test_bond_valuation(self):                              # Test Bond Valuation for the JSON Curve
        bond_vals = []
        for b in self.BONDS:
            bond_vals.append(b.value(self.CURVE))
        #print(bond_vals)


unittest.main(TestBond(), argv=[''], verbosity=2, exit=False)
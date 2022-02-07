# Define a Forward Rate Agreement as an object template
class FRA:
    def __init__(self, notional: float, d_maturity: dt.date, d_settle: dt.date, rate: IR) -> None:
        self.notional = notional
        self.d_maturity = d_maturity
        self.d_settle = d_settle
        self.rate = rate
        self.period = (d_maturity - d_settle).days

    # Define a method to extract the mark-to-market (MtM) of a FRA
    #   - alpha=1 if long or alpha=-1 if short
    def value(self, curve: Curve, d_value: dt.date, alpha=1):
        val_period = (self.d_maturity - d_value).days
        r_val = curve.rate_at_date(d_value).discount_to(val_period)
        fwd = forward_rate(curve, d_value, self.d_settle, self.d_maturity)
        return alpha*self.notional*(fwd - self.rate)*self.period*r_val
    

class TestFRA(unittest.TestCase):
    def test_value_fra(self):
        try:
            f = open('JSON/Swap zero curve.json')
            curve_data = json.load(f)
            f.close()
        except:
            raise FileNotFoundError('test_zero_curve JSON file not found!')
        spots = []
        for cd in curve_data:
            c = Spot(dt.datetime.strptime(cd['Tenor Date'], '%Y/%m/%d').date(), cd['Year Fraction'], cd['Instrument'], IR(cd['NACC Rate']/100))
            spots.append(c)
        zcurve = Curve(spots)
        #zcurve.plot()
        #print(zcurve)

        fra = FRA(1e6, dt.date(2019,6,3), dt.date(2019,3,4), IR(0.111))        
        print(f'FRA_value Long:{fra.value(zcurve, dt.date(2019,2,4))}')
        print(f'FRA_value Shrt:{fra.value(zcurve, dt.date(2019,2,4),-1)}')
        
        
unittest.main(TestFR(), argv=[''], verbosity=2, exit=False)
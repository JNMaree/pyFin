# Define an Interest Rate swap as an object template
class IRS:
    def __init__(self, nom: float, schedule: list[dt.date], fix_rate: float) -> None:
        self.nom = nom
        self.cfs = schedule
        self.fixed_rate = fix_rate
        
    # Value an IRS by returning the calculated net cash flows and sum of net cash flows
    #   - if fix_float is -1, evaluate from perspective of floating buyer
    #   - fwd_fixing is initial fixing rate 
    def value(self, curve: Curve, fwd_fixing: float, fix_float=-1):
        dt = day_count_factor(self.cfs[0], self.cfs[1])
        t = float (dt)
        edf = [ curve.rate_at_date(self.cfs[0]).discount_to(t) ]
        fwd = fwd_fixing
        netcf = self.nom*(fix_float*(self.fixed_rate*dt) - fix_float*(fwd*dt))
        rcf = [netcf * edf[0]]

        for cf in range(1, len(self.cfs)):    # Loop through cf_schedule
            dt = day_count_factor(self.cfs[cf - 1], self.cfs[cf])
            t += dt
            edf.append( curve.rate_at_date(self.cfs[cf]).discount_to(t) )
            fwd = (edf[cf-1]/edf[cf] - 1)/dt
            # Calculate net cash flow
            netcf = fix_float * (self.nom*self.fixed_rate*dt)   # Fixed Cashflow
            netcf += -fix_float * (self.nom*fwd*dt)             # Floating Cashflow
            rcf.append(netcf * edf[cf])
        return rcf, sum(rcf)


class TestIRS(unittest.TestCase):

    def test_curve(self):
        dates = [dt.date(2007,9,20), dt.date(2009,8,21), dt.date(2010,12,20), dt.date(2012,12,19)]
        times = [0.0, 1.9233, 3.2548, 5.2548]
        rates = [0.095987, 0.098970, 0.096018, 0.093497]
        spots = []
        for d in range(len(dates)):
            spots.append(Spot(dates[d], times[d], 'test', rates[d]))
        curve = Curve(spots)
        print(curve)

    #def test_value_irs(self):
        d_mat = dt.date(2012,9,12)
        cfs = gen_cf_schedule(d_mat,5,4)
        #print(cfs)
        irs = IRS(250e6, cfs, 0.1015)
        irs_val, irs_npv = irs.value(curve, 0.1014)
        print(irs_val)
        print(irs_npv)


unittest.main(TestIRS(), argv=[''], verbosity=2, exit=False)
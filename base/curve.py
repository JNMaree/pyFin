# Define the spot rates at certain specified dates of a curve
class Spot:
    def __init__(self, d_tenor: dt.date, y_frac: float, inst: str, interest_rate: IR) -> None:
        self.d_tenor = d_tenor
        self.y_frac = y_frac
        self.instrument = inst
        self.rate = interest_rate
    def __str__(self) -> str:
        sret = f'{self.instrument :>20}:\t{self.d_tenor :%Y-%m-%d}\t{self.y_frac :>10.6f}\t{self.rate}'
        return sret

# Define a curve by specifying a list of Spots
class Curve:
    def __init__(self, spot_rates: list[Spot]) -> None:
        self.spots = spot_rates
        self.dates = []             # Define arrays of individual values for interpolation
        self.rates = []
        self.fracs = []
        for s in self.spots:
            self.dates.append(s.d_tenor)
            self.rates.append(s.rate.NACC)
            self.fracs.append(s.y_frac)
    def __str__(self) -> str:
        sret = f'Curve: {self.spots[0].d_tenor}   >>>   {self.spots[len(self.spots)-1].d_tenor}:\n'
        for s in self.spots:
            sret += f'{s}\n'
        return sret

    # Calculate the interest rate at the specified date on the curve by using linear interpolation
    def rate_at_date(self, date) -> IR:
        if isinstance(date, (dt.date)):
            return IR(lerp(self.dates, self.rates, date))
        elif isinstance(date, (float)):
            return IR(lerp(self.fracs, self.rates, date))
        else:
            raise TypeError(f'Incompatible Type<{type(date)}> specified for date!')

    # Plot a rate-vs-time representation of the curve
    def plot(self):
        xv, yv = [], []
        for s in self.spots:
            xv.append(s.y_frac)
            yv.append(s.rate.NACC * 100)
        
        plt.plot(xv,yv)
        plt.title('Curve')
        plt.xlabel('Time (years)')
        plt.ylabel('NACC rate (%)')
        plt.show()
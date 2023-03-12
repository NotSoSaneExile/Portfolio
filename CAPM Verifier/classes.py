class RiskFreeRate1Y():
    def __init__(self, WIBOR1Y : float):
        self.WIBOR1Y = WIBOR1Y
        
    def calculate_adjusted_rfr(self, days):
        adjusted_rfr = self.WIBOR1Y/days
        return adjusted_rfr
    

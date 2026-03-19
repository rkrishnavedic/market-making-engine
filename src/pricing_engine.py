import numpy as np
from math_utils import ASModel

class ASPricingEngine:
    def __init__(self, gamma, kappa):
        self._gamma = gamma
        self._kappa = kappa

    def set_gamma(self, new_gamma):
        self._gamma = new_gamma

    def set_kappa(self, new_kappa):
        self._kappa = new_kappa
    
    def get_quotes(self, s, q, keyl, variance, time_horizon):
        effective_kappa = self._kappa/(1+keyl)
        print("effect. kappa", effective_kappa)
        # r
        res_price = ASModel.reservation_price(s, q, self._gamma, variance, time_horizon) 
        
        # delta
        spread = ASModel.optimal_spread(self._gamma, variance, time_horizon, effective_kappa)
    
        # quotes
        bid = res_price - (spread / 2)
        ask = res_price + (spread / 2)
        
        return round(bid,2), round(ask,2)
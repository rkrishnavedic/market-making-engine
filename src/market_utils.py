import numpy as np

def optimal_spread(gamma, variance, time_horizon, kappa):
    # risk_term (charges for volatility) + liquidity_term ("minimal" addition to attract fill)
    return gamma*variance*time_horizon + (2*np.log(1+gamma/kappa))/gamma

def reservation_price(s, q, gamma, variance, time_horizon):
    return s - q*gamma*variance*time_horizon

def get_quotes(s, q, gamma, variance, time_horizon, kappa):
    # r
    res_price = reservation_price(s, q, gamma, variance, time_horizon) 
    
    # delta
    spread = optimal_spread(gamma, variance, time_horizon, kappa)

    # quotes
    bid = res_price - (spread / 2)
    ask = res_price + (spread / 2)
    
    return bid, ask
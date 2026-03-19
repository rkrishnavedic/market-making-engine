import numpy as np

class Signals:
    @staticmethod
    def calculate_volatility(prices):
        if len(prices) < 2: return 0
        # Log Returns: ln(Pt / Pt-1)
        returns = np.diff(np.log(prices))
        return np.std(returns)

    @staticmethod
    def keyle_lambda(price_change, net_order_flow):
        # net_order_flow = Vol_buy - Vol_sell
        # price_change = post_price - pre_price
        if not net_order_flow:
            return price_change/net_order_flow
        else:
            raise ValueError("Net Order Flow is Zero")

    @staticmethod
    def order_book_imbalance(bid_vol, ask_vol):
        return (bid_vol-ask_vol)/(bid_vol+ask_vol)

    @staticmethod
    def micro_price(bid, bid_vol, ask, ask_vol):
        return (bid*ask_vol+ask*bid_vol)/(bid_vol+ask_vol)

class ASModel:
    @staticmethod
    def optimal_spread(gamma, variance, time_horizon, kappa):
        # risk_term (charges for volatility) + liquidity_term ("minimal" addition to attract fill)
        return gamma*variance*time_horizon + (2*np.log(1+gamma/kappa))/gamma

    @staticmethod
    def reservation_price(s, q, gamma, variance, time_horizon):
        return s - q*gamma*variance*time_horizon
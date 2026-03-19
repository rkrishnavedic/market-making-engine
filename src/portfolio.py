import numpy as np

class Portfolio:
    def __init__(self, initial_cash=100000.0):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.inventory = 0
        self.realized_pnl = 0.0
        self.history = []

    def update_fill(self, side, price, size):
        """
        side: 'B' (Bot Buys from Market) or 'S' (Bot Sells to Market)
        """
        if side == 'B':
            self.cash -= (price * size)
            self.inventory += size
        elif side == 'S':
            self.cash += (price * size)
            self.inventory -= size
        
        # Log history
        self.history.append({
            'inventory': self.inventory,
            'cash': self.cash,
            'price': price
        })

    def get_metrics(self, current_mid):
        unrealized = self.inventory * current_mid
        total_pnl = (self.cash + unrealized) - self.initial_cash
        return {
            "inventory": self.inventory,
            "total_pnl": round(total_pnl, 2)
        }
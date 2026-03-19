class ExecutionEngine:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def process_market_event(self, market_side, market_price, market_size, my_bid, my_ask):
        """
        This mimics a 'Passive Fill'. 
        If a Market SELL comes in at 10.00 and our BID is 10.00, we get filled.
        
        Assumption here: ToB (Top-of-Book) If the market hits my price, I am filled.
        """
        fill_report = None
        
        # 1. Someone wants to SELL to us (hits our BID)
        if market_side == 'S' and market_price <= my_bid:
            self.portfolio.update_fill('B', my_bid, market_size)
            fill_report = f"FILLED BUY: {market_size} @ {my_bid}"
            
        # 2. Someone wants to BUY from us (hits our ASK)
        elif market_side == 'B' and market_price >= my_ask:
            self.portfolio.update_fill('S', my_ask, market_size)
            fill_report = f"FILLED SELL: {market_size} @ {my_ask}"
            
        return fill_report
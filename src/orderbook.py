from sortedcontainers import SortedDict
from math_utils import Signals

class OrderBook:
    def __init__(self):
        # Bids: -Price -> Volume (Negative keys keep highest price at index 0)
        self.bids = SortedDict() 
        # Asks: Price -> Volume (Positive keys keep lowest price at index 0)
        self.asks = SortedDict()

    def process_event(self, event):
        """
        Main entry point for events.
        event: (order_type, side, price, size)
        order_type: 'L' (Limit), 'X' (Cancel), 'M' (Market)
        """
        otype, side, price, size = event
        
        if otype == 'M':
            return self._handle_market_order(side, size)
        elif otype == 'L':
            return self._handle_limit_order(side, price, size)
        elif otype == 'X':
            self._handle_cancel(side, price, size)
            return None

    def get_micro_price(self):
        if len(self.bids) == 0 or len(self.asks) == 0:
            return None
        bid, bid_vol = self.bids.peekitem(0) #best
        ask, ask_vol = self.asks.peekitem(0) #best
        return Signals.micro_price(abs(bid), bid_vol, ask, ask_vol)

    def get_mid_price(self):
        if len(self.bids) == 0 or len(self.asks) == 0:
            return None
        bid = self.bids.iloc[0] #best
        ask = self.asks.iloc[0] #best
        return (abs(bid)+ask)/2.0

    def _handle_market_order(self, side, size):
        # Market orders just need to match against the opposing book
        remaining_size, fills = self._match(side, size, price=None)
        if remaining_size > 0:
            # In real worlds, this is 'Partial Fill' or 'Canceled'
            pass # Todo: implementation required based on requirement!
        return remaining_size, fills

    def _handle_limit_order(self, side, price, size):
        # 1. Try to match first (Handling "Crossing" Limit Orders)
        remaining_size, fills = self._match(side, size, price)
        
        # 2. If there's leftover size, add it to the book (The "Maker" part)
        if remaining_size > 0:
            book = self.bids if side == 'B' else self.asks
            # Use negative price for bids to maintain descending order
            key = -price if side == 'B' else price
            book[key] = book.get(key, 0) + remaining_size

        return remaining_size, fills

    def _handle_cancel(self, side, price, size):
        book = self.bids if side == 'B' else self.asks
        key = -price if side == 'B' else price
        
        if key in book:
            book[key] -= size
            if book[key] <= 0:
                book.pop(key)

    def _match(self, side, size, price=None):
        """
        Matches incoming volume against the opposing book.
        side: 'B' (Incoming Buyer) matches against Asks
        side: 'S' (Incoming Seller) matches against Bids
        """
        # Match against opposing book
        opposing_book = self.asks if side == 'B' else self.bids
        fills = []
        
        while size > 0 and opposing_book:
            best_key = opposing_book.iloc[0]
            # Convert key back to actual price for comparison
            best_price = abs(best_key) 
            
            # Price protection logic:
            # If I'm buying, I won't pay more than my limit 'price'
            if price is not None:
                if side == 'B' and best_price > price: break
                if side == 'S' and best_price < price: break
            
            available = opposing_book[best_key]
            if size >= available:
                size -= available
                opposing_book.pop(best_key)
                fills.append({'side': side, 'price': best_price, 'size': available})
            else:
                opposing_book[best_key] -= size
                size = 0
                fills.append({'side': side, 'price': best_price, 'size': size})
                
        return size, fills
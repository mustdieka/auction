from common.constants import Status


class LotBid(object):
    """Class used to store lot-bids combination"""

    def __init__(self, price, time):
        """Initializing instance after SELL command"""
        self.reserve_price = price
        self.close_time = time
        self.status = Status.UNSOLD
        self.total_bid_count = 0
        self.user_id = ''
        self.highest_bid = None
        self.second_highest_bid = None
        self.lowest_bid = None
        self.bids = {}

    def process_bid(self, time, user_id, bid):
        """Processing a new bid for lot"""

        # check that bid is valid
        if time > self.close_time or (user_id in self.bids and self.bids[user_id] >= bid):
            return

        self.total_bid_count += 1
        self.bids[user_id] = bid

        if not self.lowest_bid or bid < self.lowest_bid:
            self.lowest_bid = bid

        if not self.highest_bid:
            self.highest_bid = bid
            if bid >= self.reserve_price:
                self.user_id = user_id
                self.status = Status.SOLD
        elif bid >= self.highest_bid:
            if user_id != self.user_id:
                self.second_highest_bid = self.highest_bid
            if bid >= self.reserve_price and bid > self.highest_bid:
                self.user_id = user_id
                self.status = Status.SOLD
            self.highest_bid = bid
        elif not self.second_highest_bid or bid > self.second_highest_bid:
            self.second_highest_bid = bid

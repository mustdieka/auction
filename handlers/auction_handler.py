import logging
from os.path import exists
from models.lot_bid import LotBid
import common.constants as constants
from common.util import check_float, check_int


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='auction_house.log',
                    encoding='utf-8', level=logging.DEBUG)
log = logging.getLogger("auction_house")


class AuctionHandler(object):
    @staticmethod
    def process_file(name):
        if not exists(name):
            log.error("Input file {} does not exist on file system".format(name))
            return

        lots = {}

        # check all inputs types
        with open(name) as f:
            for line in f:
                row_data = line.strip().split('|')

                if len(row_data) not in (1, 5, 6):
                    # unknown command or incorrect number of parameters for command
                    log.error("Incorrect line in input data file: {}".format(line))
                    raise Exception("Incorrect input data")
                elif len(row_data) == 1:
                    # nothing to do when heartbeat
                    continue
                elif row_data[2] == constants.SELL_ACTION:
                    lot_name = row_data[3]

                    if lot_name in lots:
                        # assumption - item placed only once
                        log.error("Item with the same name {} already was placed on auction".format(lot_name))
                        raise Exception("Item with the same name already was placed on auction")

                    if check_int(row_data[5]):
                        end_time = int(row_data[5])
                    else:
                        log.error("Incorrect user id value found {}".format(row_data[5]))
                        raise Exception("Incorrect user id value")

                    if check_float(row_data[4]):
                        price = float(row_data[4])
                    else:
                        log.error("Incorrect bid value found {}".format(row_data[4]))
                        raise Exception("Incorrect bid value")

                    lots[lot_name] = LotBid(price, end_time)
                elif row_data[2] == constants.BID_ACTION:
                    lot_name = row_data[3]

                    if lot_name not in lots:
                        # bid for non-existent lot. It is OK to log warning here and continue execution
                        log.warning("Bid for non-existent lot found : {}".format(line))
                        continue

                    lot = lots[lot_name]

                    if check_int(row_data[0]):
                        new_time = int(row_data[0])
                    else:
                        log.error("Incorrect epoch value found {}".format(row_data[0]))
                        raise Exception("Incorrect epoch value")

                    if check_int(row_data[1]):
                        user_id = int(row_data[1])
                    else:
                        log.error("Incorrect user id value found {}".format(row_data[1]))
                        raise Exception("Incorrect user id value")

                    if check_float(row_data[4]):
                        bid = float(row_data[4])
                    else:
                        log.error("Incorrect bid value found {}".format(row_data[4]))
                        raise Exception("Incorrect bid value")

                    lot.process_bid(new_time, user_id, bid)
                else:
                    log.error("Incorrect action: {}".format(row_data[2]))
                    raise Exception("Incorrect input data")

        AuctionHandler.print_results(lots)

    @staticmethod
    def print_results(lots):
        for name, lot in lots.items():
            price_to_pay = lot.second_highest_bid if lot.second_highest_bid else lot.reserve_price
            price_paid = price_to_pay if lot.status == constants.Status.SOLD else constants.DEFAULT_PRICE_PAID
            status = constants.SOLD_LITERAL if lot.status == constants.Status.SOLD else constants.UNSOLD_LITERAL
            lowest_bid = '' if not lot.lowest_bid else '{:.2f}'.format(lot.lowest_bid)
            highest_bid = '' if not lot.highest_bid else '{:.2f}'.format(lot.highest_bid)
            print('{}|{}|{}|{}|{:.2f}|{}|{}|{}'.format(lot.close_time,
                                                       name,
                                                       lot.user_id,
                                                       status,
                                                       price_paid,
                                                       lot.total_bid_count,
                                                       highest_bid,
                                                       lowest_bid))

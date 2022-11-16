import unittest
from unittest.mock import patch
from io import StringIO
from handlers.auction_handler import AuctionHandler


class TestAuctionHouse(unittest.TestCase):

    def test_empty(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            AuctionHandler.process_file('examples/empty_input.txt')
            self.assertEqual(fake_out.getvalue().strip(), '')

    def test_bids_valid(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            AuctionHandler.process_file('examples/test_bids_valid.txt')
            self.assertEqual(fake_out.getvalue().strip(), '20|toaster_1|5|SOLD|11.50|4|12.50|5.00')

    def test_late_bids(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            AuctionHandler.process_file('examples/test_late_bids.txt')
            self.assertEqual(fake_out.getvalue().strip(), '11|toaster_1||UNSOLD|0.00|0||')

    def test_increasing_bids(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            AuctionHandler.process_file('examples/test_increasing_bids.txt')
            self.assertEqual(fake_out.getvalue().strip(), '20|toaster_1|1|SOLD|10.00|3|15.00|13.00')

    def test_bids_same_user_diff_lots(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            AuctionHandler.process_file('examples/test_bids_valid_diff_lots.txt')
            res = fake_out.getvalue().strip().splitlines()
            self.assertEqual(res[0], '20|toaster_1|8|SOLD|12.50|3|20.00|7.50')
            self.assertEqual(res[1], '20|toaster_2|5|SOLD|10.00|1|12.50|12.50')
            self.assertEqual(res[2], '20|tv_1||UNSOLD|0.00|2|200.00|150.00')

    def test_last_bids(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            AuctionHandler.process_file('examples/test_last_bids.txt')
            self.assertEqual(fake_out.getvalue().strip(), '12|toaster_1|3|SOLD|12.00|3|12.00|10.00')


if __name__ == '__main__':
    unittest.main()

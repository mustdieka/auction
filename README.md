Requirements:
Python.version >= 3.9 (due to logging)
Run:
python main.py examples/input.txt
Run tests:
python test_cases.py

Assumptions:
-From the description it seems that increasing bids from the same user are valid => should all be counted towards
total_bid_count albeit it is counterintuitive
-On the other hand it is stated that the 'winner will pay the price of the second highest bidder' which means that
the increasing bids from the same user should not be used for price_paid calculation (only bids from another users count)
-If second highest bid is less than reserve_price we still sell for this value (once again counterintuitive but it is
a part of description)
-Outputting decimal values for price_paid, highest_bid and lowest_bid rounded to 2 digits behind the decimal point
(not explicitly stated in description, but showed in the example)
-It is not stated whether the same user can put item on the sale and buy it so I allowed it (it seems intuitively
possible)
-File is a complete log of auction - when it is finished auction is finished


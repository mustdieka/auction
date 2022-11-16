import argparse
from handlers.auction_handler import AuctionHandler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)

    args = parser.parse_args()

    AuctionHandler.process_file(args.file)


if __name__ == '__main__':
    main()

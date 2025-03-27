import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)

from vnstock import Vnstock
from storage.minio_storage import MinioStorage



class Stock_Listing:
    def __init__(self):
        self.vnstock = Vnstock().stock()
    def get_stocks_listing_by_exchange(self):
        try:
            listing = self.vnstock.listing.symbols_by_exchange()

            storage = MinioStorage()
            storage.overwrite(listing,"bronze","listing_by_exchange")
            return True
        except:
            print("Error getting stocks listing by exchange")
            return False


if __name__ == "__main__":
    stock_listing = Stock_Listing()
    listing = stock_listing.get_stocks_listing_by_exchange()
    print(listing)

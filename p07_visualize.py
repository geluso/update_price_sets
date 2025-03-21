import sys
import matplotlib.pyplot as plt

from db import create_default_connection, count_rows_zip_zip_distance, count_rows_zip_zip_distances_from_zip_pick
from pricesheet import Pricesheet
from wa_zip_gps import WA_ZIP_CODE_GPS

base = [47.606267, -122.340369]
top_left = [47.848358, -122.482174]
top_right = [47.823696, -122.128760]
bot_left = [47.207655, -122.556328]
bot_right = [47.258837, -122.133549]

old_price_sheet = "./csv/2024_01_17.csv"
latest_price_sheet = "2025-03-20-15-01-prices.csv"

def main():
    prices = Pricesheet(old_price_sheet)

    min_price = 0
    max_price = 1200

    plt.figure(figsize=(10, 6))
    for zip_drop, latitude, longitude in WA_ZIP_CODE_GPS:
        base_to_drop = prices.get_zip_to_zip(98201, zip_drop)
        price = float(base_to_drop) if base_to_drop else 0
        brightness = (price - min_price) / (max_price - min_price)
        color = (1, 1 - brightness, 1 - brightness)  # Red color with varying brightness
        print(price, color)
        plt.scatter(longitude, latitude, label=str(zip_drop), color=[color])

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('2025 Prices from Base')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
    print('exit')
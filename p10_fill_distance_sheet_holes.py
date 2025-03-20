import requests

import csv
from datetime import datetime
import time
import os

from db import create_default_connection, get_all_zip_zip_distances, get_zip_zip_distance, \
    insert_zip_zip_distance
from smc_mapbox import ZipZipDistance
from wa_zip_gps import zip_to_longitude_latitude
from zip_codes import zone_to_zips, FORCE_REDO_ZONES

from dotenv import load_dotenv
load_dotenv()

IS_FETCHING = True
IS_FORCE_REDOING_ZONES = False

# row 243 (1 based)
# row 244 (0 based)
DOWNTOWN_INDEX = 244

BASE_PRICE = 10
PRICE_PER_MILE = 1.95

def distance_to_price(distance_base_to_pick, distance_pick_to_drop, price_fallback):
    if not distance_base_to_pick or not distance_pick_to_drop:
       return price_fallback
    total_distance = distance_base_to_pick + distance_pick_to_drop
    price = BASE_PRICE + PRICE_PER_MILE * float(total_distance)
    return price

def zips_to_average_longitude_latitude(zips):
    total_longitude = 0
    total_latitude = 0
    total = len(zips)
    for zip in zips:
        if not zip in zip_to_longitude_latitude:
            continue
        latitude, longitude = zip_to_longitude_latitude[zip]
        total_latitude += latitude
        total_longitude += longitude
    ave_latitude = total_latitude / total
    ave_longitude = total_longitude / total
    return [ave_latitude, ave_longitude]

def fetch_zip_zip_distance(zone_pick, zone_drop, zips_pick, zips_drop):
    pick_latitude, pick_longitude = zips_to_average_longitude_latitude(zips_pick)
    drop_latitude, drop_longitude = zips_to_average_longitude_latitude(zips_drop)

    try:
        locations = f"{pick_longitude},{pick_latitude};{drop_longitude},{drop_latitude}"
        token = os.getenv("MY_MAPBOX_TOKEN")
        url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{locations}?annotations=distance&exclude=ferry&access_token=" + token
        time.sleep(1)
        response = requests.get(url)
        jj = response.json()
        distance_meters = jj['routes'][0]['distance']
        print("DISTANCE", distance_meters, zone_pick, "to", zone_drop)
        return distance_meters
    except Exception as e:
        print("ERROR", e)
        return -1


def save_zip_zip_distances(conn, zips_pick, zips_drop, distance_meters):
    for zip_pick in zips_pick:
        for zip_drop in zips_drop:
            zzd = ZipZipDistance(zip_pick, zip_drop, distance_meters)
            was = get_zip_zip_distance(conn, zip_pick, zip_drop)
            insert_zip_zip_distance(conn, zzd)
            new_value = get_zip_zip_distance(conn, zip_pick, zip_drop)
            print("INSERT", zip_pick, zip_drop, distance_meters, "WAS", was, "NOW", new_value)

def is_either_zone_in_force_redo(zone_pick, zone_drop):
    for redo_zone_name, redo_zone_zips in FORCE_REDO_ZONES:
        if redo_zone_name == zone_pick or redo_zone_name == zone_drop:
            return True
    return False

def main():
    conn = create_default_connection()
    all = get_all_zip_zip_distances(conn)

    price_sheet_2024 = []
    with open('./csv/2024_01_17.csv', newline='') as csvfile:
        price_sets = csv.reader(csvfile)
        for row in price_sets:
            price_sheet_2024.append(row)

    original_sheet = []
    with open('./csv/2025-02-11.csv', newline='') as csvfile:
        price_sets = csv.reader(csvfile)
        for row in price_sets:
            original_sheet.append(row)

    distance_sheet = []
    distance_sheet.append(list(original_sheet[0]))

    hits = 0
    misses = 0
    total = 0

    rowi = 1
    while rowi < len(original_sheet):
        new_row = [''] * len(original_sheet[rowi])
        new_row[0] = original_sheet[rowi][0]

        coli = 1
        while coli < len(new_row):
            zone_pick = original_sheet[rowi][0]
            zone_drop = original_sheet[0][coli]

            zips_pick = zone_to_zips[zone_pick]
            zips_drop = zone_to_zips[zone_drop]

            total += 1
            if rowi == coli:
                new_row[coli] = 0
                hits += 1
            else:
                distances = []
                distance_total = 0
                for zip_pick in zips_pick:
                    for zip_drop in zips_drop:
                        distance1 = get_zip_zip_distance(conn, zip_pick, zip_drop)
                        distance2 = get_zip_zip_distance(conn, zip_drop, zip_pick)
                        if distance1 > 0:
                            distances.append(distance1)
                            distance_total += distance1
                        if distance2 > 0:
                            distances.append(distance2)
                            distance_total += distance2

                # if (not IS_FORCE_REDOING_ZONES and not is_either_zone_in_force_redo(zone_pick, zone_drop)) and len(distances) > 0:
                if len( distances) > 0:
                    ave_distance = distance_total / len(distances)
                    new_row[coli] = ave_distance
                    hits += 1
                else:
                    if IS_FETCHING:
                        distance_meters = fetch_zip_zip_distance(zone_pick, zone_drop, zips_pick, zips_drop)
                        if distance_meters > 0:
                            save_zip_zip_distances(conn, zips_pick, zips_drop, distance_meters)
                    print(misses, "MISSING", zone_pick, zone_drop)
                    misses += 1
            coli += 1
        rowi += 1
        distance_sheet.append(new_row)

    price_sheet = []
    price_sheet.append(list(original_sheet[0]))
    rowi = 1

    while rowi < len(original_sheet):
        new_row = [''] * len(original_sheet[rowi])
        new_row[0] = original_sheet[rowi][0]

        coli = 1
        while coli < len(new_row):
            zone_pick = original_sheet[0][coli]
            zone_drop = original_sheet[rowi][0]

            distance_base_to_pick = distance_sheet[DOWNTOWN_INDEX][coli]
            distance_base_to_drop = distance_sheet[DOWNTOWN_INDEX][rowi]
            distance_pick_to_drop = distance_sheet[rowi][coli]

            # use this price if we don't have either distance
            very_old_price = price_sheet_2024[rowi][coli]
            current_price = original_sheet[rowi][coli]
            price_fallback = current_price if current_price else very_old_price
            distance_based_price = distance_to_price(distance_base_to_pick, distance_pick_to_drop, price_fallback)

            new_price = distance_based_price
            if "SEATTLE:" in zone_pick and "SEATTLE:" in zone_drop and float(new_price) < float(price_fallback):
                new_price = max(float(very_old_price), float(current_price), float(new_price))
                print("SEATTLE SPECIAL", zone_pick, zone_drop, new_price)

            if zone_pick == "SEATTLE:DOWNTOWN" and zone_drop == "SEATTLE:" and float(new_price) < float(price_fallback):
                new_price = 10.75
            new_row[coli] = new_price
            coli += 1
        rowi += 1
        price_sheet.append(new_row)

    print(misses, "misses")
    print(str(hits / total * 100) + "% complete")

    now = datetime.now()
    distance_sheet_file = f'./csv/{now.year}-{now.month:02d}-{now.day:02d}-{now.hour:02d}-{now.minute:02d}-distances.csv'
    with open(distance_sheet_file, 'w', newline='') as csvfile:
        new_csv = csv.writer(csvfile)
        for row in distance_sheet:
            new_csv.writerow(row)

    price_sheet_file = f'./csv/{now.year}-{now.month:02d}-{now.day:02d}-{now.hour:02d}-{now.minute:02d}-prices.csv'
    with open(price_sheet_file, 'w', newline='') as csvfile:
        new_csv = csv.writer(csvfile)
        for row in price_sheet:
            new_csv.writerow(row)

if __name__ == "__main__":
    main()
    print('exit')
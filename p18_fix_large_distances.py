import csv
import math
from collections import defaultdict
from datetime import datetime
import time

from db import create_default_connection, count_rows_zip_zip_distance, get_zip_zip_distance, \
    insert_zip_zip_distance_pick_drop_distance_miles
from p10_fill_distance_sheet_holes import fetch_zip_zip_distance, save_zip_zip_distances, \
    zips_to_real_longitude_latitude
from wa_zip_gps import WA_ZIP_CODE_GPS, zip_to_longitude_latitude
from zip_codes import FORCE_REDO_ZONES, WA_ZIP_CODE_NAMES, zip_to_zone


def gps_distance(gps_pick, gps_drop):
    latitude_pick, longitude_pick = gps_pick
    latitude_drop, longitude_drop = gps_drop
    yy = (latitude_pick - latitude_drop) * 110.574
    xx = (longitude_pick - longitude_drop) * 111.320 * 0.68199836006
    distance_km = math.sqrt(yy * yy + xx * xx)
    miles = distance_km / 1.6
    return miles

def loadsheet():
    print("Reading distance sheet...")
    distance_sheet = []
    with open('./csv/2025-03-26-10-34-distances.csv', newline='') as csvfile:
        price_sets = csv.reader(csvfile)
        for row in price_sets:
            distance_sheet.append(row)
    return distance_sheet

def get_sheet_distance(sheet, zone_pick, zone_drop):
    pick_col = 0
    drop_row = 0

    pick_i = 0
    while pick_col < len(sheet[0]):
        if sheet[0][pick_i] == zone_pick:
            pick_col = pick_i
            break
        pick_i += 1

    drop_i = 0
    while drop_i < len(sheet):
        if sheet[0][drop_i] == zone_drop:
            drop_row = drop_i
            break
        drop_i += 1

    return float(sheet[drop_row][pick_i])

def main():
    conn = create_default_connection()
    with open("./notes/large_distances_5.txt") as large_distances:
        lines = list(large_distances.readlines())
        total = len(lines)
        count = 0
        for line in lines[2:]:
            count += 1
            print(count / total, count, "of", total)
            cells = line.split("|")
            zip_pick = cells[0].strip()
            zip_drop = cells[1].strip()

            is_continue = False
            if zip_pick not in zip_to_longitude_latitude:
                print("NO GPS", zip_pick)
                is_continue = True
            if zip_drop not in zip_to_longitude_latitude:
                print("NO GPS", zip_drop)
                is_continue = True
            if is_continue:
                continue

            original_distance_meters = cells[2].strip()
            original_distance_miles = cells[3].strip()

            zone_pick = zip_to_zone[zip_pick]
            zone_drop = zip_to_zone[zip_drop]

            distance = fetch_zip_zip_distance(zone_pick, zone_drop, [zip_pick], [zip_drop])
            if distance > 0:
                print("REDO", zip_pick, zip_drop, "was", original_distance_miles, "now", distance / 1600)
                save_zip_zip_distances(conn, [zip_pick], [zip_drop], distance)
                save_zip_zip_distances(conn, [zip_drop], [zip_pick], distance)
            else:
                print("MISS", zip_pick, zip_drop)
                pass

if __name__ == "__main__":
    main()
    print('exit')
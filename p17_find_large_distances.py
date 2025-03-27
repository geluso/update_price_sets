import csv
import math
from collections import defaultdict
from datetime import datetime
import time

from db import create_default_connection, count_rows_zip_zip_distance, get_zip_zip_distance, \
    insert_zip_zip_distance_pick_drop_distance_miles
from p10_fill_distance_sheet_holes import fetch_zip_zip_distance, save_zip_zip_distances, \
    zips_to_real_longitude_latitude
from wa_zip_gps import WA_ZIP_CODE_GPS
from zip_codes import FORCE_REDO_ZONES, WA_ZIP_CODE_NAMES

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
    threshold = 500

    distance_sheet = loadsheet()
    large_distances = 0
    distances = []
    for zone_pick, zips_pick in WA_ZIP_CODE_NAMES:
        for zone_drop, zips_drop in WA_ZIP_CODE_NAMES:
            sheet_distance = get_sheet_distance(distance_sheet, zone_pick, zone_drop)
            if sheet_distance > threshold:
                id = "%04d %s to %s" % (round(sheet_distance), zone_pick, zone_drop)
                large_distances += 1
                distances.append(id)
    distances.sort()
    for item in distances:
        print(item)
    print(len(distances))

if __name__ == "__main__":
    main()
    print('exit')
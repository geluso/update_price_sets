from collections import defaultdict
from datetime import datetime
import time

from db import create_default_connection, count_rows_zip_zip_distance, get_zip_zip_distance, \
    insert_zip_zip_distance_pick_drop_distance_miles
from p10_fill_distance_sheet_holes import fetch_zip_zip_distance, save_zip_zip_distances
from wa_zip_gps import WA_ZIP_CODE_GPS
from zip_codes import FORCE_REDO_ZONES, WA_ZIP_CODE_NAMES

def average_distance_zone_to_zone(conn, zone_pick, zips_pick, zone_drop, zips_drop):
    total_distance = 0
    count = 0
    for zip_pick in zips_pick:
        for zip_drop in zips_drop:
            distance = get_zip_zip_distance(conn, zip_pick, zip_drop)
            if distance > 0:
                total_distance += distance
                count += 1
    if count == 0:
        return -1
    return total_distance / count

KNOWN_IMPOSSIBLE = [
    "SAN JUAN ISLANDS:BLAKELY ISLAND, WA",
    "WEST PENINSULA:BEAVER, WA",
    "NORTH CENTRAL WA:Stehekin"
]

def main():
    conn = create_default_connection()
    count = 0
    total = pow(len(WA_ZIP_CODE_NAMES), 2)

    zone_misses = defaultdict(lambda: 0)

    now = datetime.now()
    filename = f'./out/{now.year}-{now.month:02d}-{now.day:02d}-{now.hour:02d}-{now.minute:02d}-missing_zones.txt'
    output = open(filename, "w")
    for zone_pick, zips_pick in WA_ZIP_CODE_NAMES:
        for zone_drop, zips_drop in WA_ZIP_CODE_NAMES:
            if zone_pick == zone_drop:
                continue
            if zone_pick in KNOWN_IMPOSSIBLE or zone_drop in KNOWN_IMPOSSIBLE:
                continue
            count += 1
            progress = round(100 * count / total)
            ave_distance = average_distance_zone_to_zone(conn, zone_pick, zips_pick, zone_drop, zips_drop)
            if ave_distance == -1:
                msg = f"FETCHING: {zone_pick} to {zone_drop}"
                print(progress, msg)
                output.write(msg + "\n")

                zone_misses[zone_pick] += 1
                zone_misses[zone_drop] += 1
                distance_meters = fetch_zip_zip_distance(zone_pick, zone_drop, zips_pick, zips_drop)
                if distance_meters > 0:
                    save_zip_zip_distances(conn, zips_pick, zips_drop, distance_meters)
                    print("REDO", zone_pick, zone_drop, distance_meters / 1600)
                else:
                    print("MISS", zone_pick, zone_drop, distance_meters / 1600)

    for key in zone_misses:
        msg = f"{zone_misses[key]} {key}"
        print(msg)
        output.write(msg + "\n")

if __name__ == "__main__":
    main()
    print('exit')
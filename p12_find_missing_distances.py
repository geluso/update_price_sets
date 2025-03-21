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

def main():
    conn = create_default_connection()
    count = 0
    total = pow(len(WA_ZIP_CODE_NAMES), 2)

    output = open("./out/missing_zone_distances.txt", "w")
    for zone_pick, zips_pick in WA_ZIP_CODE_NAMES:
        for zone_drop, zips_drop in WA_ZIP_CODE_NAMES:
            if zone_pick == zone_drop:
                continue
            count += 1
            progress = round(100 * count / total)
            ave_distance = average_distance_zone_to_zone(conn, zone_pick, zips_pick, zone_drop, zips_drop)
            if ave_distance == -1:
                msg = f"MISSING: {zone_pick} to {zone_drop}"
                print(progress, msg)
                output.write(msg + "\n")

if __name__ == "__main__":
    main()
    print('exit')
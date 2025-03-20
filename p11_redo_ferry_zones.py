import time

from db import create_default_connection, count_rows_zip_zip_distance, get_zip_zip_distance, \
    insert_zip_zip_distance_pick_drop_distance_miles
from p10_fill_distance_sheet_holes import fetch_zip_zip_distance, save_zip_zip_distances
from wa_zip_gps import WA_ZIP_CODE_GPS
from zip_codes import FORCE_REDO_ZONES, WA_ZIP_CODE_NAMES


def main():
    conn = create_default_connection()

    total = len(WA_ZIP_CODE_GPS) * len(WA_ZIP_CODE_GPS)
    count = 0
    missing = 0
    found = 0

    for zone_pick, zips_pick in FORCE_REDO_ZONES:
        for zone_drop, zips_drop in WA_ZIP_CODE_NAMES:
            fetch_zip_zip_distance(zone_pick, zone_drop, zips_pick, zips_drop)
            distance_meters = fetch_zip_zip_distance(zone_pick, zone_drop, zips_pick, zips_drop)
            if distance_meters > 0:
                save_zip_zip_distances(conn, zips_pick, zips_drop, distance_meters)
                print("REDO", zone_pick, zone_drop, distance_meters / 1600)
                time.sleep(1)
    print("MISSING", missing)
    print("FOUND", found)


if __name__ == "__main__":
    main()
    print('exit')
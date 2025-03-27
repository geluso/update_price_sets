from collections import defaultdict
from datetime import datetime
import time

from db import create_default_connection, count_rows_zip_zip_distance, get_zip_zip_distance, \
    insert_zip_zip_distance_pick_drop_distance_miles
from p10_fill_distance_sheet_holes import fetch_zip_zip_distance, save_zip_zip_distances
from wa_zip_gps import WA_ZIP_CODE_GPS
from zip_codes import FORCE_REDO_ZONES, WA_ZIP_CODE_NAMES

def main():
    misses = 0
    missed_zips = defaultdict(lambda: 0)
    conn = create_default_connection()
    for zone_pick, zips_pick in WA_ZIP_CODE_NAMES:
        for zone_drop, zips_drop in WA_ZIP_CODE_NAMES:
            for zip_pick in zips_pick:
                for zip_drop in zips_drop:
                    if zip_pick == zip_drop:
                        continue
                    distance1 = get_zip_zip_distance(conn, zip_pick, zip_drop)
                    distance2 = get_zip_zip_distance(conn, zip_drop, zip_pick)
                    if distance1 < 0 and distance2 < 0:
                        misses += 1
                        missed_zips[zip_pick] += 1
                        missed_zips[zip_drop] += 1
    for missed_zip in missed_zips:
        print(missed_zip, missed_zips[missed_zip])
    print("misses", misses)


if __name__ == "__main__":
    main()
    print('exit')
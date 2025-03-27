import time

from db import create_default_connection, count_rows_zip_zip_distance, get_zip_zip_distance, \
    insert_zip_zip_distance_pick_drop_distance_miles
from p10_fill_distance_sheet_holes import fetch_zip_zip_distance, save_zip_zip_distances
from wa_zip_gps import WA_ZIP_CODE_GPS
from zip_codes import FORCE_REDO_ZONES, WA_ZIP_CODE_NAMES, BOTCHED_GPS_ZONES


def main():
    conn = create_default_connection()

    downtown = ['SEATTLE:DOWNTOWN', [98101, 98104, 98121, 98154, 98174, 98164]]
    burton = ['VASHON: BURTON, WA', [98013]]
    vashon = ['VASHON', [98070]]
    southcenter = ['SOUTH I5 CORRIDOR:Southcenter', [98138]]
    clinton = ['WHIDBEY:CLINTON, WA', [98236]]
    bothel = ['NORTH I5 Corridor:BOTHELL, WA', [98011, 98041, 98021]]

    zone_pick, zips_pick = clinton
    zone_drop, zips_drop = bothel

    distance_meters = fetch_zip_zip_distance(zone_pick, zone_drop, zips_pick, zips_drop)
    distance_miles = distance_meters / 1600
    if distance_meters > 0:
        save_zip_zip_distances(conn, zips_pick, zips_drop, distance_meters)
        print("REDO", zone_pick, zone_drop, distance_meters / 1600)

if __name__ == "__main__":
    main()
    print('exit')
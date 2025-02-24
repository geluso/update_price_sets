from db import create_default_connection, count_rows_zip_zip_distance
from wa_zip_gps import WA_ZIP_CODE_GPS
from zip_codes import zip_to_zone

def main():
    conn = create_default_connection()

    total = len(WA_ZIP_CODE_GPS) * len(WA_ZIP_CODE_GPS)
    count = 0
    missing = 0

    missing_zone_to_zones = set()

    for pick_zip, lat, longg in WA_ZIP_CODE_GPS:
        print("progress", count / total)
        for drop_zip, lat, longg in WA_ZIP_CODE_GPS:
            count += 1
            rows = count_rows_zip_zip_distance(conn, pick_zip, drop_zip)
            rows_reversed = count_rows_zip_zip_distance(conn, drop_zip, pick_zip)
            if rows == 0 and rows_reversed == 0:
                missing += 1
                min_zip = min(pick_zip, drop_zip)
                max_zip = min(pick_zip, drop_zip)

                min_zone = zip_to_zone[min_zip]
                max_zone = zip_to_zone[max_zip]
                print(min_zip, max_zip, min_zone, max_zone)
                missing_zone_to_zones.add((min_zone, max_zone))
    for missing_route in missing_zone_to_zones:
        print(missing_route)
    print(len(missing))
    print("complete:", missing / count)

if __name__ == "__main__":
    main()
    print('exit')
from db import create_default_connection, count_rows_zip_zip_distance, get_zip_zip_distance, \
    insert_zip_zip_distance_pick_drop_distance_miles
from wa_zip_gps import WA_ZIP_CODE_GPS

def main():
    conn = create_default_connection()

    total = len(WA_ZIP_CODE_GPS) * len(WA_ZIP_CODE_GPS)
    count = 0
    missing = 0
    found = 0
    for pick_zip, lat, longg in WA_ZIP_CODE_GPS:
        for drop_zip, lat, longg in WA_ZIP_CODE_GPS:
            count += 1
            if count % 500 == 0:
                print("PROGRESS", count / total)
            distance = get_zip_zip_distance(conn, pick_zip, drop_zip)
            if distance == -1:
                missing += 1
                reversed_distance = get_zip_zip_distance(conn, drop_zip, pick_zip)
                if reversed_distance != -1:
                    found += 1
                    print("INSERT", drop_zip, pick_zip, reversed_distance)
                    insert_zip_zip_distance_pick_drop_distance_miles(conn, drop_zip, pick_zip, reversed_distance)
    print("MISSING", missing)
    print("FOUND", found)


if __name__ == "__main__":
    main()
    print('exit')
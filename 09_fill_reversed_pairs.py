from db import create_default_connection, count_rows_zip_zip_distance
from wa_zip_gps import WA_ZIP_CODE_GPS

def main():
    conn = create_default_connection()

    total = len(WA_ZIP_CODE_GPS) * len(WA_ZIP_CODE_GPS)
    count = 0
    missing = 0
    for pick_zip, lat, longg in WA_ZIP_CODE_GPS:
        for drop_zip, lat, longg in WA_ZIP_CODE_GPS:
            count += 1
            progress = count / total
            rows = count_rows_zip_zip_distance(conn, pick_zip, drop_zip)
            rows_reversed = count_rows_zip_zip_distance(conn, drop_zip, pick_zip)
            if rows == 0 and rows_reversed == 0:
                missing += 1
    print("complete:", missing / count)

if __name__ == "__main__":
    main()
    print('exit')
import csv

def main():
    original_sheet = []
    with open('./csv/2024_01_17.csv', newline='') as csvfile:
        price_sets = csv.reader(csvfile)
        for row in price_sets:
            original_sheet.append(row)

    new_sheet = []
    with open('./csv/today.csv', newline='') as csvfile:
        price_sets = csv.reader(csvfile)
        for row in price_sets:
            new_sheet.append(row)

    original_rowi = 0
    new_rowi = 0
    while original_rowi < len(original_sheet):
        original_row_label = original_sheet[0][original_rowi]
        new_row_label = new_sheet[0][new_rowi]
        if new_row_label != original_row_label:
            print(new_row_label)
            new_rowi += 1
        original_rowi += 1
        new_rowi += 1

if __name__ == "__main__":
    main()
    print('exit')
import csv
import os

from zip_codes import zip_to_zone

class Pricesheet:
  def __init__(self, csv_filepath):
    assert os.path.exists(csv_filepath), f"File {csv_filepath} does not exist"

    self.sheet = []
    with open(csv_filepath, newline='') as csvfile:
        sheet = list(csv.reader(csvfile))

        rowi = 0
        while rowi < len(sheet):
          row = []
          coli = 0
          while coli < len(sheet[rowi]):
              zone_pick = sheet[rowi][0]
              zone_drop = sheet[0][coli]
              cell = sheet[rowi][coli]
              row.append(cell)
              coli += 1
          self.sheet.append(row)
          rowi += 1

  def zone_to_index(self, zone):
    header_row = self.sheet[0]
    index = 0
    while index < len(header_row):
      if header_row[index] == zone:
        return index
      index += 1
    return -1

  def get_zip_to_zip(self, zip_pick, zip_drop):
    zone_pick = zip_to_zone[zip_pick]
    zone_drop = zip_to_zone[zip_drop]
    
    index_pick = self.zone_to_index(zone_pick)
    index_drop = self.zone_to_index(zone_drop)

    value = self.sheet[index_drop][index_pick]
    return value
    
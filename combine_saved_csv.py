import csv
from pathlib import Path
import sys

filename_origin = '090322_wireless_grass_test_device001_0811SSF5_8mm_black_sensor4_IR67700.csv'


num_of_file = 19
reader_list = [csv.reader(open(f'{filename_origin[:-4]}_{i}.csv', 'r')) for i in range(1, num_of_file + 1)]

new_file_name = f'{filename_origin[:-4]}_1_to_{num_of_file}.csv'

if Path(new_file_name).is_file():
    print('File already exists! Overwrite file? <y/[n]>')
    response = input()
    if response.lower() != 'y':
        print('Exiting program...\n')
        sys.exit()

writer = csv.writer(open(new_file_name, 'w', newline=''))
for i in range(1, num_of_file + 1):
        for row in reader_list[i-1]:
            writer.writerow(row)



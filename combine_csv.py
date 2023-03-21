import csv
from pathlib import Path
import sys

filename_origin = '081322_cont_stretch_0.000167mm_s_resistance1_0811SSF_film1_8mm_black_sensor1_just_Ag_large_black_IR93000_resistance2_same_film_8mm_wide_black_sensor3_just_Ag_large_black_IR47100.csv'

num_of_file = 185
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



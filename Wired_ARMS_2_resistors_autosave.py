import serial
import time
from pathlib import Path
import sys
import csv
import matplotlib.pyplot as plt

# Serial port settings
port = 'COM4'
timeout = 63.0 # time in seconds to wait for a response from Arduino
baudrate = 115200

# Open serial port to Arduino
print('Waiting for Arduino to initialize...\n')
ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
time.sleep(4) # wait 4 sec for Arduino to initialize

print('Enter filename to save data (e.g. resistance1.csv): ')
filename_origin = input()
if not filename_origin.endswith('.csv'):
    filename_origin += '.csv'

# check if file already exists
if Path(filename_origin).is_file():
    print('File already exists! Overwrite file? <y/[n]>')
    response = input()
    if response.lower() != 'y':
        print('Exiting program...\n')
        sys.exit()

num_of_file = int(input("Enter the number of files you want to save:"))
time_of_each_file = float(60 * 1000 * int(input("Enter the time of each file you want to save in minutes:")))
file_counter = 1
filename = f'{filename_origin[:-4]}_{file_counter}.csv'
start_experiment_time = time.time()
# open file and write data
while file_counter <= num_of_file:
        
        filename = f'{filename_origin[:-4]}_{file_counter}.csv'
        if Path(filename).is_file():
                filename = f'{filename[:-4]}_cont.csv'

        # open file and write data
        with open(filename, 'w', newline='') as csvfile:
            SavingFile = True
            # create writer object
            writer = csv.writer(csvfile)
            # get first data to determine number of columns and write column titles
            
            ser.read_all() # flush the read buffer
            data = ser.readline()
            data = data.decode('ascii').strip().replace(' ','').split(',') # bytes to string, strip whitespace, split into list using comma delimiter 
            print('The data is now being saved...')
            titles = ['Time']
            for i in range(len(data)-1):
                titles.append('Resistance' + str(i+1))
            
            if file_counter == 1:
                        writer.writerow(titles)

            
            # start writing data
            ser.read_all() # flush the read buffer
            x = []
            y = []
            z = []
            t = 0
            #target_value = 50000000
            while SavingFile:
                t += 1
                data = ser.readline()
                data = data.decode('ascii').strip().replace(' ','').split(',')             
                time_value = data[0]
                resistance_value = data[1]
                resistance_value_2 = data[2]
                x.append(int(time_value))
                y.append(float(resistance_value))
                z.append(float(resistance_value_2))
                writer.writerow(data)
                print(data)

                plt.cla()
                plt.plot(x, y)
                plt.plot(x, z)           
                plt.pause(0.05)
                if t%2000 == 0:
                    plt.tight_layout()
                    plt.show()
                
                if x[-1] - x[0] >= time_of_each_file:
                    SavingFile = False
                    file_counter += 1

reader_list = [csv.reader(open(f'{filename_origin[:-4]}_{i}.csv', 'r')) for i in range(1, num_of_file + 1)]
writer = csv.writer(open(filename_origin, 'w', newline=''))
for i in range(1, num_of_file + 1):
        for row in reader_list[i-1]:
                writer.writerow(row)


import serial
import time
from pathlib import Path
import sys
import csv

# Serial port settings
port = 'COM5'
timeout = 3.0 # time in seconds to wait for a response from Arduino
baudrate = 115200

# Open serial port to Arduino
print('Waiting for Arduino to initialize...\n')
ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
time.sleep(4) # wait 4 sec for Arduino to initialize

# Select file to save data to
print('Enter filename to save data (e.g. resistance1.csv): ')
filename = input()
if not filename.endswith('.csv'):
    filename += '.csv'

# check if file already exists
if Path(filename).is_file():
    print('File already exists! Overwrite file? <y/[n]>')
    response = input()
    if response.lower() != 'y':
        print('Exiting program...\n')
        sys.exit()


# open file and write data
with open(filename, 'w', newline='') as csvfile:
    # create writer object
    writer = csv.writer(csvfile)
    # get first data to determine number of columns and write column titles
    ser.read_all() # flush the read buffer
    data = ser.readline()
    data = data.decode('ascii').strip().replace(' ','').split(',') # bytes to string, strip whitespace, split into list using comma delimiter 

    titles = ['Time']
    for i in range(len(data)-1):
        titles.append('Resistance' + str(i+1))

    writer.writerow(titles)

    input('Press Enter to start saving data (Press Ctrl+C to exit at anytime) ')
    # start writing data
    ser.read_all() # flush the read buffer
    while True:
        data = ser.readline()
        data = data.decode('ascii').strip().replace(' ','').split(',') 
        writer.writerow(data)
        print(data)


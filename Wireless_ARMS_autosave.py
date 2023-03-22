# Read_screen_plot_autosave_7_two_sensor
# cv2.cvtColor takes a numpy ndarray as an argument
# calibrated from xlxs file 031422_compare_prostat_wireless_121421film sheet film 1-1 and 1-2
# Pin 1 2 3 calibrated with Read_screen_plot_save_6 (Stretching test with large resistance meter)
# Pin 4 5 6 calibrated with Read_screen_plot_save_4 (Resistor test, i.e. wireless resistance meter.xlxs) 
import numpy as nm
import math
import pytesseract
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# importing OpenCV
import cv2
import sys
import csv  
from pathlib import Path
from PIL import ImageGrab


def ReadScreen():
   
        # ImageGrab-To capture the screen image in a loop. 
        # Bbox used to capture a specific area.
        cap_1 = ImageGrab.grab(bbox =(160, 975, 500, 1000))
        cap_2 = ImageGrab.grab(bbox =(160, 985, 500, 1010))
        # Converted the image to monochrome for it to be easily 
        # read by the OCR and obtained the output String.
        tesstr_1 = pytesseract.image_to_string(
                cv2.cvtColor(nm.array(cap_1), cv2.COLOR_BGR2GRAY), 
                lang ='eng')
        #print("tesstr_1 is " + tesstr_1, str(len(tesstr_1)))
        tesstr_2 = pytesseract.image_to_string(
                cv2.cvtColor(nm.array(cap_2), cv2.COLOR_BGR2GRAY), 
                lang ='eng')
        #print("tesstr_2 is " + tesstr_2, str(len(tesstr_2)))

        if substring1 in tesstr_1 or substring2 in tesstr_1 or substring3 in tesstr_1 or substring4 in tesstr_1:
                tesstr = tesstr_1
        elif substring1 in tesstr_2 or substring2 in tesstr_2 or substring3 in tesstr_2 or substring4 in tesstr_2:
                tesstr = tesstr_2
        else:
                tesstr = tesstr_1
        print("\n-------------------------------------")
       
        if substring1 in tesstr and tesstr[-3] != " ":
                tesstr = tesstr[-len(tesstr):-2] + " " + tesstr[-2:-1] + " "
        elif substring2 in tesstr and tesstr[-3] != " ":
                tesstr = tesstr[-len(tesstr):-2] + " " + tesstr[-2:-1] + " "
        print("The screen reading result is: \n" + tesstr)
        return tesstr
def ConvertString(screen_reading_string):
        
        pin_value_str = screen_reading_string[-2:-1]
        adc_value_str = screen_reading_string[-8:-3]
                
        try:
        
                pin_value = int(pin_value_str)
                if pin_value in range(1,7):
                        pass
                else:
                        print("Invalid Pin number")
 
                adc_value = int(adc_value_str)
                strain_reading_list = [adc_value, pin_value]
                return strain_reading_list
        except:
                global Note
                Note = "Error when converting string"
                print(Note)

def CalculateResistance(adc_value, pin_value):
        global Note

        if pin_value == 1:
                resistance_value = 1711 * adc_value - 4619.5
        elif pin_value == 2:
                resistance_value = 5626.9 * adc_value - 23647
        elif pin_value == 3:
                resistance_value = 18197 * adc_value - 214154
        elif pin_value == 4:
                resistance_value = 30596 * adc_value + 52973
        elif pin_value == 5:
                resistance_value = 51266 * adc_value - 306532
        elif pin_value == 6:
                if adc_value <= 520:
                        resistance_value = math.exp(0.0058 * adc_value + 15.041)
                else:
                        resistance_value = math.exp(1.1706 * (adc_value/100)**3 - 18.802 * (adc_value/100)**2 + 101.69 * (adc_value/100) -166.86)
                        Note = "WARNING: Resistance out of range!"
                        print(Note)
        else:
                Note = "WARNING: Pin value out of range!"
                print(Note)
        datalist = [adc_value, pin_value, resistance_value]
        return datalist[2]
 


# Select file to save data to
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
time_of_each_file = float(60 * int(input("Enter the time of each file you want to save in minutes:")))
file_counter = 1
filename = f'{filename_origin[:-4]}_{file_counter}.csv'
start_experiment_time = time.time()
# open file and write data
while file_counter <= num_of_file:
        
        filename = f'{filename_origin[:-4]}_{file_counter}.csv'
        if Path(filename).is_file():
                filename = f'{filename[:-4]}_cont.csv'
                        
        with open(filename, 'w', newline='') as csvfile:
                SavingFile = True
                # create writer object
                writer = csv.writer(csvfile)
                if file_counter == 1:
                        titles = ['Device', 'Time', 'Resistance', '# of Measurement', 'Average ADC', 'Pin Number', 'Note']
                        writer.writerow(titles)

                print('Data is now being saved...')
                # start writing data
                global Note
                cycle = 0
                cycle_start_time = 0
                cycle_end_time = 0
                time_interval = 0
                sleep_time = 0
                tolerance = 1
               
                adc_reading_count_1 = 0
                average_adc_1 = 0
                time_variable_1 = []
                resistance_variable_1 = []
                measurement_variable_1 = []
                adc_variable_1 = []
                pin_variable_1 = []
                
                adc_reading_count_2 = 0
                average_adc_2 = 0
                time_variable_2 = []
                resistance_variable_2 = []
                measurement_variable_2 = []
                adc_variable_2 = []
                pin_variable_2 = []

                #start_time = time.time()
                substring1 = "The 001 strain reading"
                substring2 = "The 002 strain reading"
                substring3 = "Device 001 Sleeping"
                substring4 = "Device 002 Sleeping"
                # Path of tesseract executable
                pytesseract.pytesseract.tesseract_cmd ="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
                while SavingFile:
                        
                        cycle += 1
                        Note = ""
                        if cycle >= 2:
                                sleep_time = time_interval - (cycle_end_time - cycle_start_time)
                                if sleep_time > 0:
                                        time.sleep(sleep_time)
                                cycle_start_time = time.time()   
                                current_time = time.time() - start_experiment_time
                                try:
                                        screen_reading_string = ReadScreen()
                                        
                                        if substring1 in screen_reading_string:
                                                pin_value_1 = ConvertString(screen_reading_string)[1]
                                                adc_value_1 = ConvertString(screen_reading_string)[0]
                                                adc_reading_count_1 += 1
                                                average_adc_1 += adc_value_1
                                                print("The current time is " + str(current_time))
                                                print("The 001 strain reading of this single measurement is " + str(adc_value_1) + " " + str(pin_value_1))
                                        if substring2 in screen_reading_string:
                                                pin_value_2 = ConvertString(screen_reading_string)[1]
                                                adc_value_2 = ConvertString(screen_reading_string)[0]
                                                adc_reading_count_2 += 1
                                                average_adc_2 += adc_value_2
                                                print("The current time is " + str(current_time))
                                                print("The 002 strain reading of this single measurement is " + str(adc_value_2) + " " + str(pin_value_2))
                                        elif substring3 in screen_reading_string:
                                                if adc_reading_count_1 != 0:
                                                        average_adc_1 = average_adc_1 / adc_reading_count_1             
                                                        print("Device 001 finished this testing cycle. The current time is " + str(current_time))
                                                        average_resistance_1 = CalculateResistance(average_adc_1, pin_value_1)
                                                        print("The average strain reading of this testing cycle is " + str(average_adc_1) + " " + str(pin_value_1))
                                                        print("The average resistance value of this testing cycle is " + str(average_resistance_1))
                                                        print("The number of measurements in this testing cycle is " + str(adc_reading_count_1))
                                                        print("-------------------------------------\n")
                                                        
                                                        time_variable_1.append(current_time)
                                                        resistance_variable_1.append(average_resistance_1)
                                                        measurement_variable_1.append(adc_reading_count_1)
                                                        adc_variable_1.append(average_adc_1)
                                                        pin_variable_1.append(pin_value_1)
                                                        if len(time_variable_1) != 0 and len(resistance_variable_1) != 0:    
                                                                data = ['001', str(time_variable_1[-1]), str(resistance_variable_1[-1]), str(measurement_variable_1[-1]), str(adc_variable_1[-1]), str(pin_variable_1[-1]), Note]
                                                                writer.writerow(data)
                                                                plt.clf()
                                                                plt.plot(time_variable_1, resistance_variable_1)
                                                                plt.pause(0.05)        
                                                        average_adc_1 = 0
                                                        adc_reading_count_1 = 0
                                                else:
                                                        print("Device 001 sleeping. The current time is " + str(current_time) + ". The last reading is " + str(average_resistance_1))
                                        elif substring4 in screen_reading_string:
                                                if adc_reading_count_2 != 0:
                                                        average_adc_2 = average_adc_2 / adc_reading_count_2             
                                                        print("Device 002 finished this testing cycle. The current time is " + str(current_time))
                                                        average_resistance_2 = CalculateResistance(average_adc_2, pin_value_2)
                                                        print("The average strain reading of this testing cycle is " + str(average_adc_2) + " " + str(pin_value_2))
                                                        print("The average resistance value of this testing cycle is " + str(average_resistance_2))
                                                        print("The number of measurements in this testing cycle is " + str(adc_reading_count_2))
                                                        print("-------------------------------------\n")
                                                        
                                                        time_variable_2.append(current_time)
                                                        resistance_variable_2.append(average_resistance_2)
                                                        measurement_variable_2.append(adc_reading_count_2)
                                                        adc_variable_2.append(average_adc_2)
                                                        pin_variable_2.append(pin_value_2)
                                                        if len(time_variable_2) != 0 and len(resistance_variable_2) != 0:    
                                                                data = ['002', str(time_variable_2[-1]), str(resistance_variable_2[-1]), str(measurement_variable_2[-1]), str(adc_variable_2[-1]), str(pin_variable_2[-1]), Note]
                                                                writer.writerow(data)
                                                                plt.clf()
                                                                plt.plot(time_variable_2, resistance_variable_2)
                                                                plt.pause(0.05)        
                                                        average_adc_2 = 0
                                                        adc_reading_count_2 = 0
                                                                                        
                                                else:                                                
                                                        print("Device 002 sleeping. The current time is " + str(current_time) + ". The last reading is " + str(average_resistance_2))

                                        else:
                                                pass
                                except ValueError:
                                        print("ValueError in program loop")
                                except OSError:
                                        print("OSError in program loop")
                                except KeyboardInterrupt:
                                        print("You pressed Ctrl + C and quitted the program!")
                                        print('Exiting Program...')
                                        time.sleep(2)
                                        sys.exit()
                                except:
                                        print("Other errors")
                        cycle_end_time = time.time()
                        if cycle_end_time - start_experiment_time >= file_counter * time_of_each_file:
                                SavingFile = False
                                file_counter += 1

reader_list = [csv.reader(open(f'{filename_origin[:-4]}_{i}.csv', 'r')) for i in range(1, num_of_file + 1)]
writer = csv.writer(open(filename_origin, 'w', newline=''))
for i in range(1, num_of_file + 1):
        for row in reader_list[i-1]:
                writer.writerow(row)
                



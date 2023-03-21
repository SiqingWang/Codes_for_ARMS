
"""

  Voltage_divider_multiple_4 for device 002.py

    
             

"""

from synapse.pinWakeup import *
from synapse.platforms import *
from synapse.nvparams  import *
from synapse.switchboard import *
from synapse.RF200 import *

portalAddr = '\x00\x00\x01' # hard-coded address for Portal

getADCpin = 1
powerpin1 = GPIO_18
powerpin2 = GPIO_17
powerpin3 = GPIO_16
powerpin4 = GPIO_15
powerpin5 = GPIO_14
powerpin6 = GPIO_13
ThresholdADC = 200
#power_pin = [GPIO_18, GPIO_17, GPIO_16, GPIO_15, GPIO_14, GPIO_13]
#R_value = [3000000, 10000000, 30000000, 100000000, 300000000, 1000000000]
#R_value1 = ["3Mohm", "10Mohm", "30Mohm", "100Mohm", "300Mohm", "1Gohm"]
i = 0



@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""  
    global msCounter,secondCounter, StrainVal, StrainVal1, StrainVal2, StrainVal3, StrainVal4, StrainVal5, StrainVal6, pinDecision
    global Strain1Val, i

    secondCounter       = 0 # Used by the system for cycle count
    StrainVal = 0
    StrainVal1 = 0 
    StrainVal2 = 0
    StrainVal3 = 0 
    StrainVal4 = 0
    StrainVal5 = 0
    StrainVal6 = 0
    pinDecision = 0
    setPinDir(powerpin1, True) 
    writePin(powerpin1, True)
 
@setHook(HOOK_100MS)         # 1 Hz sampling rate    
def timer10msEvent():

    global secondCounter, pinDecision, pinNumber, StrainVal, StrainVal1, StrainVal2, StrainVal3, StrainVal4, StrainVal5, StrainVal6
      
    secondCounter   += 1


    if pinDecision <= 5:
        if secondCounter == 1:
            ChoosePin1()
        elif secondCounter == 6:
            StrainVal1 = StrainVal1 + readAdc(getADCpin)
            Closepin1()
            eventString =  "Deciding pin number: " + str(StrainVal1) + " "  + "1"
            rpc(portalAddr, "logEvent", eventString)
        elif secondCounter == 7:
            ChoosePin2()
        elif secondCounter == 12:
            StrainVal2 = StrainVal2 + readAdc(getADCpin)
            Closepin2()
            eventString =  "Deciding pin number: " + str(StrainVal2) + " "  + "2"
            rpc(portalAddr, "logEvent", eventString)
        elif secondCounter == 13:
            ChoosePin3()
        elif secondCounter == 18:
            StrainVal3 = StrainVal3 + readAdc(getADCpin)
            Closepin3() 
            eventString =  "Deciding pin number: " + str(StrainVal3) + " "  + "3"
            rpc(portalAddr, "logEvent", eventString)       
        elif secondCounter == 19:
            ChoosePin4()
        elif secondCounter == 24:
            StrainVal4 = StrainVal4 + readAdc(getADCpin)
            Closepin4()  
            eventString =  "Deciding pin number: " + str(StrainVal4) + " "  + "4"
            rpc(portalAddr, "logEvent", eventString)   
        elif secondCounter == 25:
            ChoosePin5()
        elif secondCounter == 30:
            StrainVal5 = StrainVal5 + readAdc(getADCpin)
            Closepin5()   
            eventString =  "Deciding pin number: " + str(StrainVal5) + " "  + "5"
            rpc(portalAddr, "logEvent", eventString)   
        elif secondCounter == 31:
            ChoosePin6()
        elif secondCounter == 36:
            StrainVal6 = StrainVal6 + readAdc(getADCpin)
            Closepin6()
            eventString =  "Deciding pin number: " + str(StrainVal6) + " "  + "6"
            rpc(portalAddr, "logEvent", eventString)
            secondCounter = 0
            pinDecision += 1
        else:
            pass
    else:    
        if secondCounter == 1:
            pinNumber = DecidePin(StrainVal1, StrainVal2, StrainVal3, StrainVal4, StrainVal5, StrainVal6)
        elif secondCounter >= 2 and secondCounter <= 600:
            if secondCounter % 3 == 0:
                StrainVal = readAdc(getADCpin)
                eventString =  "The 002 strain reading is 0000" + str(StrainVal) + " "  + str(pinNumber)
                rpc(portalAddr, "logEvent", eventString)        # Logs data to event window
        elif secondCounter == 601:
            writePin(powerpin1, False)
            setPinDir(powerpin1, False) 
            writePin(powerpin2, False)
            setPinDir(powerpin2, False) 
            writePin(powerpin3, False)
            setPinDir(powerpin3, False) 
            writePin(powerpin4, False)
            setPinDir(powerpin4, False) 
            writePin(powerpin5, False)
            setPinDir(powerpin5, False) 
            writePin(powerpin6, False)
            setPinDir(powerpin6, False)         
        elif secondCounter >= 602 and secondCounter <= 1200:
            if secondCounter % 3 == 0:
                rpc(portalAddr, "logEvent", "Device 002 Sleeping") 
        elif secondCounter >= 1201 and secondCounter <= 6000:
            rx(False)
        elif secondCounter >= 6001:
            secondCounter = 0
            pinDecision = 0
            StrainVal1 = 0 
            StrainVal2 = 0
            StrainVal3 = 0 
            StrainVal4 = 0
            StrainVal5 = 0
            StrainVal6 = 0
            rx(True)
           
def ChoosePin1():
    setPinDir(powerpin1, True) 
    writePin(powerpin1, True)

def Closepin1():
    setPinDir(powerpin1, False) 
    writePin(powerpin1, False)

def ChoosePin2():   
    setPinDir(powerpin2, True) 
    writePin(powerpin2, True)

def Closepin2():
    setPinDir(powerpin2, False) 
    writePin(powerpin2, False)

def ChoosePin3():
    setPinDir(powerpin3, True) 
    writePin(powerpin3, True)

def Closepin3():
    setPinDir(powerpin3, False) 
    writePin(powerpin3, False)

def ChoosePin4():   
    setPinDir(powerpin4, True) 
    writePin(powerpin4, True)

def Closepin4():
    setPinDir(powerpin4, False) 
    writePin(powerpin4, False)

def ChoosePin5():
    setPinDir(powerpin5, True) 
    writePin(powerpin5, True)

def Closepin5():
    setPinDir(powerpin5, False) 
    writePin(powerpin5, False)

def ChoosePin6():   
    setPinDir(powerpin6, True) 
    writePin(powerpin6, True)

def Closepin6():
    setPinDir(powerpin6, False) 
    writePin(powerpin6, False)

def abs(val):
    if val >= 0:
        return val
    else:
        return -val

def DecidePin(val_1, val_2, val_3, val_4, val_5, val_6):
    global pinDecision
    decision1 = val_1 - 150 * pinDecision
    decision2 = val_2 - 150 * pinDecision
    decision3 = val_3 - 150 * pinDecision
    decision4 = val_4 - 150 * pinDecision
    decision5 = val_5 - 150 * pinDecision
    decision6 = val_6 - 150 * pinDecision
    if abs(decision1) <= abs(decision2) and abs(decision1) <= abs(decision3) and abs(decision1) <= abs(decision4) and abs(decision1) <= abs(decision5) and abs(decision1) <= abs(decision6):
        ChoosePin1()
        pinNumber = 1
    elif abs(decision2) <= abs(decision1) and abs(decision2) <= abs(decision3) and abs(decision2) <= abs(decision4) and abs(decision2) <= abs(decision5) and abs(decision2) <= abs(decision6):
        ChoosePin2() 
        pinNumber = 2
    elif abs(decision3) <= abs(decision1) and abs(decision3) <= abs(decision2) and abs(decision3) <= abs(decision4) and abs(decision3) <= abs(decision5) and abs(decision3) <= abs(decision6):
        ChoosePin3()
        pinNumber = 3
    elif abs(decision4) <= abs(decision1) and abs(decision4) <= abs(decision2) and abs(decision4) <= abs(decision3) and abs(decision4) <= abs(decision5) and abs(decision4) <= abs(decision6):
        ChoosePin4()  
        pinNumber = 4
    elif abs(decision5) <= abs(decision1) and abs(decision5) <= abs(decision2) and abs(decision5) <= abs(decision3) and abs(decision5) <= abs(decision4) and abs(decision5) <= abs(decision6):
        ChoosePin5()
        pinNumber = 5
    else:
        ChoosePin6()
        pinNumber = 6
    return pinNumber




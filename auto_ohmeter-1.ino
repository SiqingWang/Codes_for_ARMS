//check Aref and digitalwrite high are same

#define ANALOG_READ_PIN A1
#define NUM_R 11
#define SAMPLE_INTERVAL 5
#define NUM_TEST_SAMPLES 5
#define NUM_REAL_SAMPLES 200

const int Rpin[NUM_R] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
const double Rval[NUM_R] = {10000.0, 30000.0, 100000.0, 300000.0, 1000000.0, 3000000.0, 10000000.0, 30000000.0, 100000000.0, 300000000.0, 1000000000.0};

void setup() {
    // put your setup code here, to run once:
    Serial.begin(115200);

    for (int i=0; i<NUM_R; ++i)
    {
        pinMode(Rpin[i], OUTPUT);
        digitalWrite(Rpin[i], LOW);
        pinMode(Rpin[i], INPUT);
    }
}

void loop() {
    // change to ticker function later
    int closestRpin = getClosestRpin();
    double closestRseries = Rval[closestRpin];

    pinMode(Rpin[closestRpin], OUTPUT);
    digitalWrite(Rpin[closestRpin], HIGH);
    delay(10);
    double ADCval = getAvgADCval(NUM_REAL_SAMPLES, SAMPLE_INTERVAL);
    digitalWrite(Rpin[closestRpin], LOW);
    pinMode(Rpin[closestRpin], INPUT);
    
    double R = convertADCvaltoR(ADCval, closestRseries);
    Serial.print("Closest Rseries: ");
    Serial.println(closestRseries);
    Serial.print("ADC measured");
    Serial.println(ADCval);
    Serial.print("Measured R: ");
    Serial.println(R);
}

int getClosestRpin()
{
    double minDiff = 1023.0;
    int closestPin = 0;
    for (int i=0; i<NUM_R; ++i)
    {
      //Serial.print("Rpin");
      //Serial.println(Rpin[i]);
        pinMode(Rpin[i], OUTPUT);
        digitalWrite(Rpin[i], HIGH);
        delay(10);
        double ADCvaldiff = abs(getAvgADCval(NUM_TEST_SAMPLES, SAMPLE_INTERVAL) - 511.5); //511.5 is the middle of the ADCval range
        //Serial.print("ADCvaldiff");
        //Serial.println(ADCvaldiff);
        digitalWrite(Rpin[i], LOW);
        pinMode(Rpin[i], INPUT);
        if (ADCvaldiff < minDiff)
        {
            minDiff = ADCvaldiff;
            closestPin = i;
        }
        //Serial.println(closestPin);
    }
    return closestPin;
    
}

double getAvgADCval(int numSamplesToAvg, int sampleInterval) {
    double ADCval = 0.0;
    for (int i=0; i<numSamplesToAvg; ++i)
    {
        ADCval += analogRead(ANALOG_READ_PIN);
        delay(sampleInterval);
    }
    ADCval = ADCval / numSamplesToAvg;
    return ADCval;
}

double convertADCvaltoR(double ADCval, double Rseries)
{
    double R = Rseries * ADCval / (1023.0 - ADCval);
    return R;
}

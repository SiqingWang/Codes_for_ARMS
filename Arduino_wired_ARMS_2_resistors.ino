//check Aref and digitalwrite high are same

#define ANALOG_READ_PIN1 A1
#define ANALOG_READ_PIN2 A2
#define NUM_R 11
#define SAMPLE_INTERVAL 5
#define NUM_TEST_SAMPLES 5
#define NUM_REAL_SAMPLES 200
unsigned long myTime;

const int Rpin[NUM_R] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
const double Rval[NUM_R] = {10000.0, 30000.0, 100000.0, 300000.0, 1000000.0, 3000000.0, 10000000.0, 30000000.0, 100000000.0, 300000000.0, 1000000000.0};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  for (int i = 0; i < NUM_R; ++i)
  {
    pinMode(Rpin[i], OUTPUT);
    digitalWrite(Rpin[i], LOW);
    pinMode(Rpin[i], INPUT);
  }
  Serial.print("Time, ");
  Serial.print("Resistance1, ");
  Serial.print("Resistance2\n");
}

void loop() {
  // change to ticker function later
  //delay(1000);
  int closestRpin = getClosestRpin();
  double closestRseries = Rval[closestRpin];

  pinMode(Rpin[closestRpin], OUTPUT);
  digitalWrite(Rpin[closestRpin], HIGH);
  delay(10);
  double ADCval1 = getAvgADCval1(NUM_REAL_SAMPLES, SAMPLE_INTERVAL);
  double ADCval2 = getAvgADCval2(NUM_REAL_SAMPLES, SAMPLE_INTERVAL);
  digitalWrite(Rpin[closestRpin], LOW);
  pinMode(Rpin[closestRpin], INPUT);

  double R1 = convertADCval1toR1(ADCval1, ADCval2, closestRseries);
  double R2 = convertADCval2toR2(ADCval1, ADCval2, closestRseries);
  //Serial.print("Time: ");
  myTime = millis();
  Serial.print(myTime);
  //Serial.print("Closest Rseries, ");
  //Serial.print(closestRseries);
  Serial.print(", ");
  //Serial.print("ADC measured, ");
  //Serial.print(ADCval);
  //Serial.print("\n");
  //Serial.print("Measured R, ");
  Serial.print(R1);
  Serial.print(", ");
  Serial.print(R2);
  Serial.print("\n");
}

int getClosestRpin()
{
  double minDiff = 1023.0;
  int closestPin = 0;
  for (int i = 0; i < NUM_R; ++i)
  {
    //Serial.print("Rpin");
    //Serial.println(Rpin[i]);
    pinMode(Rpin[i], OUTPUT);
    digitalWrite(Rpin[i], HIGH);
    delay(10);
    double ADCvaldiff = abs(getAvgADCval1(NUM_TEST_SAMPLES, SAMPLE_INTERVAL) - 341); //341 is one third of the ADCval range
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

double getAvgADCval1(int numSamplesToAvg, int sampleInterval) {
  double ADCval = 0.0;
  for (int i = 0; i < numSamplesToAvg; ++i)
  {
    ADCval += analogRead(ANALOG_READ_PIN1);
    delay(sampleInterval);
  }
  ADCval = ADCval / numSamplesToAvg;
  return ADCval;
}

double getAvgADCval2(int numSamplesToAvg, int sampleInterval) {
  double ADCval = 0.0;
  for (int i = 0; i < numSamplesToAvg; ++i)
  {
    ADCval += analogRead(ANALOG_READ_PIN2);
    delay(sampleInterval);
  }
  ADCval = ADCval / numSamplesToAvg;
  return ADCval;
}

double convertADCval1toR1(double ADCval1, double ADCval2, double Rseries)
{
  double R = Rseries * (ADCval1 - ADCval2) / (1023.0 - ADCval1);
  return R;
}


double convertADCval2toR2(double ADCval1, double ADCval2, double Rseries)
{
  double R = Rseries * ADCval2 / (1023.0 - ADCval1);
  return R;
}

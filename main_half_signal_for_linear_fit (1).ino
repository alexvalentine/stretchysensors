#include <linreg.h>

// #define DECAYMONITORING;
#define CAPACITANCE_MONITORING;
// #define LOOP_SPEED_MONITORING;



#include <math.h>


const int Signal =  3;      // the number of the LED pin

int Sensor_outputR1 = A0;

// The values of the two Resistors are:
// R1 1 MOhm
// R2 680 MOhm

// Values of the two resistors

 // Resistance is in MOhm
float R1 = 1.000000; // Resistance is in MOhm
float Rs = 0.0; // Sensor Resistance
float Cs = 0.0; // Sensor Capacitance

// # ---------------------------------------------------------------------------
// variables for the data aquisition

const int buffersize = 50;
int TimeSignalR1[buffersize];
int SensorResponseR1[buffersize];


// variables for the data processing
// # ---------------------------------------------------------------------------

double LogarithmOfSignal1[buffersize];
double TimeSignalhilf[buffersize];

double a1;

double b1;

double Rsquare;

int IndexDecayStart1;

int IndexDecayEnd1;


bool SendDataPoint = true;

// variables for averaging
// # ---------------------------------------------------------------------------

double sum_tau = 0.0;
double sum_intersects = 0.0 ;
double sum_weights = 0.0;

double average_tau = 0.0;
double average_intersects = 0.0;


int average_size = 3;


void setup() {
  // set the digital pin as output:
  pinMode(Signal, OUTPUT);


  // Increase the analog sample rate to 76 kHz.
  ADCSRA &= ~( _BV(ADPS0) | _BV(ADPS1) ); // clear bits 0 and 1.
  ADCSRA |= _BV(ADPS2); // set bit 2.
  // analogReference(INTERNAL);


  Serial.begin(115200);

}


void loop()
{   
    #ifdef LOOP_SPEED_MONITORING;

      unsigned long loopStartTime = micros();

    #endif
    
    #ifdef CAPACITANCE_MONITORING
    
       unsigned long loopStartTime = micros();
    
    #endif

    digitalWrite(Signal, LOW);
    
    sum_tau = 0.0;
    sum_weights = 0.0;
    average_tau = 0.0;
    sum_intersects = 0.0 ;
    average_intersects = 0.0;


      // the signal swichting ability has to be implemented as well.
    
    for(int i=0; i < average_size; i++){

        Measure_Time_response(Signal,Sensor_outputR1,TimeSignalR1,SensorResponseR1, buffersize);

        AddDataPoint(calcDecayTime1());

    }
    
#ifdef DECAYMONITORING

    DoDataLogging("RawSignalR1",TimeSignalR1,SensorResponseR1,buffersize,1);
    DoDataLogging("LogarithmR1",TimeSignalhilf,LogarithmOfSignal1,IndexDecayEnd1-IndexDecayStart1,4);
    DoDataLogging("Linfit1",&a1,&b1,1,7);

#endif     


    CalculateAverage();


    calcCapacitance();

    calcResistance();

   

    CheckforSerialMessage();

    // long current_millis = micros();
    // Serial.println(0);

#ifdef CAPACITANCE_MONITORING
    
    if(SendDataPoint == true){
        
        Serial.print(average_tau,4);

      Serial.print(",");

      Serial.print(Cs,4);

      Serial.print(",");

      Serial.print(Rs,4);

      Serial.print(",");
      
      Serial.print(micros()-loopStartTime);
       
      Serial.print(",");

      Serial.print("\n");

    }

    

#endif  

    // Serial.println(micros()-current_millis);

#ifdef LOOP_SPEED_MONITORING;

      Serial.println(micros()-loopStartTime);

#endif 


     
}

void CheckforSerialMessage() {

    if(Serial.available() > 0) {

    // char in order to contain the message that is sent over serial.
    
    char message;
    
    while (Serial.available() > 0) {
        
      message = char(Serial.read());
      
      // Serial.println(message);
      delay(2);

      // Case 'f'
      // "Start Sending the plotting data"
      if (message == 'f')
      {
          SendDataPoint = true;
      }

      // Case 'g'
      // "Stop Sending the plotting data"
      if (message == 'g')
      {
          SendDataPoint = false;
      }

    }

  }

}

// Functions for dataaquisition
// # ---------------------------------------------------------------------------


void Measure_Time_response(const int Signal,int Pin, int * TimeSignal, int * SensorResponse, const int buffersize) {
  
   digitalWrite(Signal, HIGH);

   unsigned long previousMillis = micros();
   
   for (int i = 0; i < buffersize; ++i)
   {  
     unsigned long currentMillis = micros();
     TimeSignal[i] = (currentMillis - previousMillis);
     SensorResponse[i] = analogRead(Pin);
   }
    
   digitalWrite(Signal, LOW);

}

// # ---------------------------------------------------------------------------
// functions for data processing

void IndexDecayStartandEnd() {
  
  int maximum1 = 0;

  IndexDecayStart1 = 0;

  IndexDecayEnd1 = buffersize - 1;

  for (int i = 0; i < buffersize; ++i)
  {
    if (maximum1 < SensorResponseR1[i])
    {
      maximum1 = SensorResponseR1[i];
      IndexDecayStart1 = i + 2;
    }
    
    
    if (SensorResponseR1[i] < maximum1 * 0.135)
    {
        
        IndexDecayEnd1 = i;
        IndexDecayStart1 = IndexDecayEnd1/2;

        break;
        
    }
  }

}

void TakeLogarithmOfSignal() {

  // take the logarithm of the sensor signal and determine the index at which the signal has dropped on 13.5 % of its original value
  
   for (int i = IndexDecayStart1; i < IndexDecayEnd1; ++i)
   { 
 
          LogarithmOfSignal1[i-IndexDecayStart1] = log(double(SensorResponseR1[i]));
   }

}

double calcDecayTime1() {

  IndexDecayStartandEnd();
  TakeLogarithmOfSignal();

  for (int i = IndexDecayStart1; i < IndexDecayEnd1; ++i)
  {
    TimeSignalhilf[i-IndexDecayStart1] = TimeSignalR1[i];
  }

  LinearRegression lr(TimeSignalhilf,LogarithmOfSignal1,IndexDecayEnd1-IndexDecayStart1);

  a1 = lr.getA();
  b1 = lr.getB();
  Rsquare = lr.getCoefDeterm();

  return (-1.0 / b1);

}




// # ---------------------------------------------------------------------------
// Functions for data logging


void DoDataLogging(String name, double * timer, double * data, int length,int accuracy) {

      Serial.println(name);
        
      Serial.println("Time, Signal");
                        
  
      for(int i = 0; i < length; i++) {
 
        Serial.print(timer[i],accuracy);
                
        Serial.print(",");
                
        Serial.print(data[i],accuracy);
                
        Serial.print(",");

        
        Serial.print("\n");
                
      
      }

      Serial.println("EndDataSet");

      Serial.flush();
      
}

void DoDataLogging(String name, int * timer, int * data, int length,int accuracy) {

      Serial.println(name);
        
      Serial.println("Time, Signal");
                        
  
      for(int i = 0; i < length; i++) {
 
        Serial.print(timer[i],accuracy);
                
        Serial.print(",");
                
        Serial.print(data[i],accuracy);
                
        Serial.print(",");

        Serial.print("\n");
                
      
      }

      Serial.println("EndDataSet");

      Serial.flush();
      
}

// Functions for data averaging
// # ---------------------------------------------------------------------------

void AddDataPoint(double tau) {
  
  sum_weights += 1;
  sum_tau += tau;
  sum_intersects += a1;
  
}

void CalculateAverage() {

  average_tau = sum_tau/sum_weights;
  average_intersects = sum_intersects/sum_weights;

}

// functions for capacitance and reistance calculation
// # ---------------------------------------------------------------------------

void calcCapacitance() {

  Cs =  average_tau/(Rs+R1);

}

// at the beginning of the step response, the voltage is equal to a voltage divider of the sensor resistance
// and the measurement resistance
void calcResistance() {
  // Serial.println(average_intersects);
  // Serial.println((double(1024)/exp(average_intersects)));

   Rs =  ((double(1024)/exp(average_intersects)) - 1)*R1;

}




    
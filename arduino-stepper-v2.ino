const int step_pin_x = 8;
const int dir_pin_x = 9;
const int home_switch_x = 3;

const int step_pin_y = 10;
const int dir_pin_y = 11;
const int home_switch_y = 4;

const int step_pin_z = 12;
const int dir_pin_z = 13;
const int home_switch_z = 5;
const int z = 240;
int x;
int y;
#include <Servo.h>
Servo myservo; 
int pos = 0;
void setup() {
	pinMode(step_pin_x,OUTPUT);
	pinMode(dir_pin_x,OUTPUT);
	pinMode(home_switch_x , INPUT);
	pinMode(step_pin_y,OUTPUT);
	pinMode(dir_pin_y,OUTPUT);
	pinMode(home_switch_y , INPUT);
	pinMode(step_pin_z,OUTPUT);
	pinMode(dir_pin_z,OUTPUT);
	pinMode(home_switch_z , INPUT); 
  
  myservo.attach(2);
	Serial.begin(9600);
 
	setHome(home_switch_x,dir_pin_x,step_pin_x);
	delay(1000);
	setHome(home_switch_y,dir_pin_y,step_pin_y);
	delay(1000);
	setHome(home_switch_z,dir_pin_z,step_pin_z);
	delay(1000);
  motorStep(z*25,step_pin_z );
  delay(1000);
  
  myservo.write(0); 
  delay(500);



}

void motorStep( int max, int step_pin){

   for(int i= 0; i < max; i++) {
        digitalWrite(step_pin,HIGH);
        delayMicroseconds(1000);
        digitalWrite(step_pin,LOW);
        delayMicroseconds(1000);
        }
}

void setHome(int home_switch,int dir_pin,int step_pin){

  // Start Homing procedure of Stepper Motor at startup
if ( home_switch != 5 ) {
    while (digitalRead(home_switch)) {  // Do this until the switch is activated   
      digitalWrite(dir_pin, HIGH);      // (HIGH = anti-clockwise / LOW = clockwise)
      digitalWrite(step_pin, HIGH);
      delayMicroseconds(1000);                       // Delay to slow down speed of Stepper
      digitalWrite(step_pin, LOW);
      delayMicroseconds(1000);   
      }

    while (!digitalRead(home_switch)) { // Do this until the switch is not activated
      digitalWrite(dir_pin, LOW); 
      digitalWrite(step_pin, HIGH);
      delayMicroseconds(1000);                       // More delay to slow even more while moving away from switch
      digitalWrite(step_pin, LOW);
      delayMicroseconds(1000);
      }
  // do Thing A
}

else if ( home_switch == 5 ) {  while (digitalRead(home_switch)) {  // Do this until the switch is activated   
      digitalWrite(dir_pin, LOW);      // (HIGH = anti-clockwise / LOW = clockwise)
      digitalWrite(step_pin, HIGH);
      delayMicroseconds(1000);                       // Delay to slow down speed of Stepper
      digitalWrite(step_pin, LOW);
      delayMicroseconds(1000);   
      }

    while (!digitalRead(home_switch)) { // Do this until the switch is not activated
      digitalWrite(dir_pin, HIGH); 
      digitalWrite(step_pin, HIGH);
      delayMicroseconds(1000);                       // More delay to slow even more while moving away from switch
      digitalWrite(step_pin, LOW);
      delayMicroseconds(1000);
      }
  // do Thing B
}


  }



void loop() {

	if (Serial.available() > 0) {
		String input = Serial.readStringUntil('\n'); // Read the input string until a newline character

    		// Find the position of the comma separator
    		int commaPos = input.indexOf(',');

    		if (commaPos != -1) {
      			// Split the input string into two substrings
      			String sx= input.substring(0, commaPos);
      			String sy= input.substring(commaPos + 1);

      			// Convert the substrings to integers
      			x= sx.toInt();
      			y= sy.toInt();
		}
	  Serial.print(x);
    Serial.print('/');
    Serial.print(y);
    Serial.println();

		motorStep(x*25,step_pin_x );	// no.of steps = x-cordinate * 25
		delay(1000);
		motorStep(y*25,step_pin_y );	// no.of steps = y-cordinate * 25
		delay(1000);
    setHome(home_switch_z,dir_pin_z,step_pin_z);
    delay(1000);
    
    myservo.write(130); 
    delay(500);  
    motorStep(z*25,step_pin_z );
    delay(1000);

		setHome(home_switch_x,dir_pin_x,step_pin_x);
		delay(1000);
		setHome(home_switch_y,dir_pin_y,step_pin_y);
		delay(1000);
    setHome(home_switch_z,dir_pin_z,step_pin_z);
    delay(1000);
    myservo.write(0); 
    delay(500);  
          // Print the input values as a single output separated by '/'
    Serial.print(x);
    Serial.print('/');
    Serial.print(y);
    Serial.println();

	}
	
   else{
    x=0;
    y=0;
//    motorStep(x*25,step_pin_x );  // no.of steps = x-cordinate * 25
//    delay(1000);
//    motorStep(y*25,step_pin_y );  // no.of steps = y-cordinate * 25
//    delay(1000);
//    
//    setHome(home_switch_z,dir_pin_z,step_pin_z);
//    delay(1000);
//    
//    myservo.write(130); 
//    delay(500);  
//
//
//    motorStep(z*25,step_pin_z );
//    delay(1000);
//    
//    setHome(home_switch_x,dir_pin_x,step_pin_x);
//    delay(1000);
//    setHome(home_switch_y,dir_pin_y,step_pin_y);
//    delay(1000);
//    setHome(home_switch_z,dir_pin_z,step_pin_z);
//    delay(1000);
//    
//    myservo.write(0); 
//    delay(500);  
//    delay(20000000000);
}
}

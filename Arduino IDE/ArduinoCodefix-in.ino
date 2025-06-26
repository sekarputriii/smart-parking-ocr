#include <Servo.h>
// #include <Firmata.h>

Servo servo;

int pinTrigger = 8; 
int pinEcho = 9; 

int x;


long duration, distance;

void setup() {
pinMode(pinTrigger, OUTPUT);   //pin trigger sebagai output
pinMode(pinEcho, INPUT);       //pin echo sebagai input

Serial.begin(9600);             //kecepatan komunikasi Serial dengan komputer

servo.attach(13);              //pin 11 untuk servo
servo.write(0);

}


void loop() {
// servo.write(90);

// Sensor Ultrasonik 
digitalWrite(pinTrigger, LOW);
delayMicroseconds(2);

digitalWrite(pinTrigger, HIGH);
delayMicroseconds(10);

digitalWrite(pinTrigger, LOW);
duration = pulseIn(pinEcho, HIGH);

// Hitung distance
distance = duration/58.2;

// Uji Sensor
// if (distance != 0){
//   Serial.print("Pintu Masuk : ");
//   Serial.print(distance);
//   Serial.println(" cm");
// }

// if (distance <= 15 && distance > 0) {
// Serial.println("Pintu Masuk : Terdapat Objek");
// }

// else {
//   Serial.println("Pintu Masuk : Tidak Terdapat Objek");
// }

// Uji Servo
// if (distance != 0){
//   Serial.print("Pintu Masuk : ");
//   Serial.print(distance);
//   Serial.println(" cm");
// }

// if (distance <= 15 && distance > 0) {
// Serial.println("Pintu Masuk : Palang Terbuka");
//   servo.write(90);
//   delay(3000);
//   servo.write(0);
// }

// else {
//   Serial.println("Pintu Masuk : Palang Tertutup");
  // servo.write(0);
// }

// Uji Sistem
if (distance <= 20 && distance > 0){
// delay(10000);
Serial.println("in");
}

if (Serial.available() > 0) {
  x = Serial.readString().toInt();

  if (x = 1){
    servo.write(90); 
    delay(3000);  
    servo.write(0);
  }
}
}

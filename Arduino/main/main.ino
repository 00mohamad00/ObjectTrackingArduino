#include <Servo.h>

Servo myServo;

int pos = 90;
int recived = 0;

void setup() {
  Serial.begin(9600);
  myServo.attach(9);

  delay(1000);
  myServo.write(0);
  delay(1000);
  myServo.write(180);
  delay(1000);
  myServo.write(90);
}

void loop() {
  if (Serial.available() > 0){
    recived = Serial.parseInt();
    if (recived > 90){
      pos += 10;
    }
    else if (recived < 90){
      pos -= 10;
    }
  }

  if (pos < 10){
    pos = 10;
  }
  else if (pos > 170){
    pos = 170;
  }
  myServo.write(pos);
}

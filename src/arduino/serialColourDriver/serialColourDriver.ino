#include <stdio.h> 

int incomingByte    = 0; // for incoming serial data
const int redPin    = 9;
const int greenPin  = 10;
const int bluePin   = 11;
// if "white" (R=255, G=255, B=255) doesn't look white, reduce the red, green, or blue max value.
const int max_red   = 255;
const int max_green = 255;
const int max_blue  = 255;

byte colors[3] ;//array to store led brightness values
byte lineEnding = 0x0A; //10 in decimal, ASCII newline character

void setup() {
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  printf("begin");
}

// Below only turns a pin on or off. 
void green() {
  analogWrite(redPin, map(0, 0, 255, 0, max_red));
  analogWrite(greenPin, map(255, 0, 255, 0, max_green));
  analogWrite(bluePin, map(0, 0, 255, 0, max_blue));
  delay(1000);
}

void yellow() {
  analogWrite(redPin, map(230, 0, 255, 0, max_red));
  analogWrite(greenPin, map(65, 0, 255, 0, max_green));
  analogWrite(bluePin, map(0, 0, 255, 0, max_blue));
  delay(1000);
}

void blue() {
  analogWrite(redPin, map(0, 0, 255, 0, max_red));
  analogWrite(greenPin, map(0, 0, 255, 0, max_green));
  analogWrite(bluePin, map(255, 0, 255, 0, max_blue));
  delay(1000);
}

void red() {
  analogWrite(redPin, map(255, 0, 255, 0, max_red));
  analogWrite(greenPin, map(0, 0, 255, 0, max_green));
  analogWrite(bluePin, map(0, 0, 255, 0, max_blue));
  delay(1000);
}

void white() {
  analogWrite(redPin, map(255, 0, 255, 0, max_red));
  analogWrite(greenPin, map(255, 0, 255, 0, max_green));
  analogWrite(bluePin, map(255, 0, 255, 0, max_blue));
  delay(1000);
}

void pink() {
  analogWrite(redPin, map(255, 0, 255, 0, max_red));
  analogWrite(greenPin, map(20, 0, 255, 0, max_green));
  analogWrite(bluePin, map(50, 0, 255, 0, max_blue));
  delay(1000);
}

void gold() {
  analogWrite(redPin, map(255, 0, 255, 0, max_red));
  analogWrite(greenPin, map(215, 0, 255, 0, max_green));
  analogWrite(bluePin, map(0, 0, 255, 0, max_blue));
  delay(1000);
}

void off() {
  analogWrite(redPin, map(0, 0, 255, 0, max_red));
  analogWrite(greenPin, map(0, 0, 255, 0, max_green));
  analogWrite(bluePin, map(0, 0, 255, 0, max_blue));
  delay(1000);
}

void loop() {
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    Serial.println(incomingByte);
  }

  switch (incomingByte) {
    case 'g':
      green();
      break;
    case 'w':
      white();
      break;
    case 'r':
      red();
      break;
    case 'y':
      yellow();
      off();
      break;
    case 'b':
      blue();
      break;
    case 'p':
      pink();
      break;
    case 'x':
      gold();
      break;
    case 'o':
      off();
      break;
    default: 
      // if nothing else matches, do nothing
      break;
  }
}



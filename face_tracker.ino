#include <Stepper.h>

// Steps per revolution (2048 for 28BYJ-48, 200 for NEMA17)
const int stepsPerRevolution = 2048;  

Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

String command = "";

void setup() {
  Serial.begin(9600);
  Serial.println("Stepper command interface ready.");
  Serial.println("Commands: CW <degrees>, CCW <degrees>, SPEED <rpm>");
  
  myStepper.setSpeed(5); // Default speed
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\n'); 
    command.trim(); 
    processCommand(command);
  }
}

void processCommand(String cmd) {
  cmd.toUpperCase(); 

  if (cmd.startsWith("CW")) {
    int degrees = cmd.substring(2).toInt();
    if (degrees <= 0) degrees = 360; // Default full revolution
    int steps = max(1, (degrees * stepsPerRevolution) / 360);
    Serial.print("Rotating clockwise for ");
    Serial.print(degrees);
    Serial.print(" degrees (");
    Serial.print(steps);
    Serial.println(" steps)...");
    myStepper.step(steps);

  } else if (cmd.startsWith("CCW")) {
    int degrees = cmd.substring(3).toInt();
    if (degrees <= 0) degrees = 360;
    int steps = max(1, (degrees * stepsPerRevolution) / 360);
    Serial.print("Rotating counter-clockwise for ");
    Serial.print(degrees);
    Serial.print(" degrees (");
    Serial.print(steps);
    Serial.println(" steps)...");
    myStepper.step(-steps);

  } else if (cmd.startsWith("SPEED")) {
    int rpm = cmd.substring(5).toInt();
    if (rpm > 0) {
      myStepper.setSpeed(rpm);
      Serial.print("Speed set to ");
      Serial.print(rpm);
      Serial.println(" RPM");
    } else {
      Serial.println("Invalid speed value.");
    }

  } else {
    Serial.println("Unknown command. Use CW <deg>, CCW <deg>, SPEED <rpm>");
  }
}

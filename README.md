# Jenkins Build Status Light
> A project to bring the build status of a Jenkins build into the physical world

A bunch of us worked on this during an innovation day at the office to bring our Jenkins build pipeline into the physical realm with a RGB LED strip, and Arduino and some Python.

Contributors are:

* Burt (https://github.com/BurtV)
* Cal
* Matt
* Rick (https://github.com/rick-roche)
* Sidd (https://github.com/Siddiqah)
* Pieter

## Required items
1. 1x Arduino Uno (it should work on all similar boards)
2. 1x RGB LED strip
3. 3x TIP31C power transistors
4. 3x 1kΩ resistors
5. 1x 12V power supply
6. Assorted cables and connectors
7. A breadboard for prototyping (we ended up building the circuit on some veroboard for the final solution)

## Installing / Getting started

Ensure you program your Arduino first and then run the Python script to start the build indicator.

### Arduino

You will need to install the Arduino IDE from https://www.arduino.cc/en/Main/Software
* This can be used to compile the .ino file and upload to your Arduino

### Python

You will need Python as well as PySerial (The scripts were developed using Python 2.7.x. and PySerial version 3.1.1). There is a great guide available [here](https://learn.adafruit.com/arduino-lesson-17-email-sending-movement-detector/installing-python-and-pyserial).

The two scripts are as follows
1. ```jenkinsBuildStatus.py``` - monitors the status of a normal Jenkins project
	* Simply changes the strip to be a solid colour if successful, failed or aborted and flashes on building
	* Usage: _jenkinsBuildStatus.py -j <jenkins_url> -b <baud_rate> -p <port> -f <poll_frequency_seconds> -a <b64(username:password)>_

```shell
python jenkinsBuildStatus.py -j https://jenkins.me/job/test -b 9600 -p COM11 -f 30 -a dXNlcm5hbWU6cGFzc3dvcmQ=
```

2. ```jenkinsPipelineStatus.py``` - monitors the status of a [Jenkins pipeline ](https://jenkins.io/doc/book/pipeline/)
	* Usage: _jenkinsPipelineStatus.py -j <jenkins_url> -b <baud_rate> -p <port> -f <poll_frequency_seconds> -a <b64(username:password)>_

```shell
python jenkinsPipelineStatus.py -j https://jenkins.me/job/test -b 9600 -p COM11 -f 30 -a dXNlcm5hbWU6cGFzc3dvcmQ=
```

## Licensing

The code in this project is licensed under MIT license.
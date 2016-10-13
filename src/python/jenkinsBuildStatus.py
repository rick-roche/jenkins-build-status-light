import json
import urllib2
import time
import serial
import sys, getopt

# Arduino colour configurations
SUCCESS     = 'g'   # Green
FAILURE     = 'r'   # Red
BUILDING    = 'y'   # Yellow
EXCEPTION   = 'w'   # White
ABORTED     = 'b'   # Blue
WAITING     = 'p'   # Pink
OFF         = 'o'   # No lights on

# Other constants
POLL_RATE_S = 30    # Period to wait between polls in seconds
DEFAULT_BAUD = 9600 # Default baud rate
USAGE = 'usage: ciTrafficLight.py -j <jenkins_url> -b <baud_rate> -p <port> -f <poll_frequency_seconds> -a <b64(username:password)>'    # Usage string

class BuildStatus:
    def __init__(self, sys_args):
        # Setup defaults
        self.baud_rate = DEFAULT_BAUD

        # Check the inputs
        try:
            opts, args = getopt.getopt(sys_args,"j:b:p:f:a:")
        except getopt.GetoptError:
            print USAGE
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print USAGE
                sys.exit()
            elif opt in "-j":
                self.jenkins_url = arg
                self.jenkins_url += "lastBuild/api/json"                # always get the last build
            elif opt in "-b":
                self.baud_rate = arg
            elif opt in "-p":
                self.com_port = arg
            elif opt in "-f":
                self.frequency = arg
            elif opt in "-a":
                self.auth = arg

        self.ser = serial.Serial(self.com_port, self.baud_rate)
        time.sleep(1) # Give the serial port time to settle

    def poll(self):
        print "Polling..."

        try:
            basic_auth = 'Basic %s' % self.auth
            headers = {'Authorization': basic_auth}                     # Basic auth is required
            request = urllib2.Request(self.jenkins_url, '', headers)    # Build the request
            jenkins_stream = urllib2.urlopen(request)                   # Make the HTTP request
            http_status_code = jenkins_stream.getcode()                 # Grab the HTTP status code

            if http_status_code == 200:
                try:
                    last_build = json.load(jenkins_stream)
                    is_building = last_build['building']
                    build_result = last_build['result']

                    print 'is_building: %s; build_result: %s' % (is_building, build_result)

                    if is_building:
                        self.ser.write(BUILDING)
                    else:
                        if build_result == "SUCCESS":
                            self.ser.write(SUCCESS)
                        elif build_result == "FAILURE":
                            self.ser.write(FAILURE)
                        elif build_result == "ABORTED":
                            self.ser.write(ABORTED)
                        elif build_result == "WAITING":
                            self.ser.write(WAITING) # No status from jenkins yet on how to check waiting for input
                        else:
                            self.ser.write(EXCEPTION)

                except:
                    print "Failed to parse json"
                    self.ser.write(EXCEPTION)

        except urllib2.HTTPError, e:
            print "HTTP error: %s" % e
            self.ser.write(EXCEPTION)

        time.sleep(POLL_RATE_S)
        self.poll()

    def __del__(self):
        if hasattr(self, 'ser'):
            self.ser.write(OFF) # turn the lights off
            self.ser.close()    # close the serial port

if __name__=="__main__":
    BuildStatus(sys.argv[1:]).poll()

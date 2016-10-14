import json
import urllib2
import time
import serial
import sys, getopt

# Arduino colour configurations
SUCCESS                 = 'g'   # Green
FAILED                  = 'r'   # Red
IN_PROGRESS             = 'y'   # Yellow
EXCEPTION               = 'w'   # White
ABORTED                 = 'p'   # Pink
PAUSED_PENDING_INPUT    = 'b'   # Blue
OFF                     = 'o'   # No lights on

# Other constants
POLL_RATE_S = 30                # Period to wait between polls of the Jenkins job in seconds
STAGE_CYCLE_TIME_S = 15         # Period to wait between showing off each stage
DEAD_TIME_S = 2                 # Period of dead time
DEFAULT_BAUD = 9600 # Default baud rate
USAGE = 'usage: jenkinsPipelineStatus.py -j <jenkins_url> -b <baud_rate> -p <port> -f <poll_frequency_seconds> -a <b64(username:password)>'    # Usage string

class PipelineStatus:
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
                self.jenkins_url += "lastBuild/wfapi/describe"          # always get the last build
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

    def write_status(self, status):
        if status == "SUCCESS":
            self.ser.write(SUCCESS)
        elif status == "FAILED":
            self.ser.write(FAILED)
        elif status == "ABORTED":
            self.ser.write(ABORTED)
        elif status == "IN_PROGRESS":
            self.ser.write(IN_PROGRESS)
        elif status == "PAUSED_PENDING_INPUT":
            self.ser.write(PAUSED_PENDING_INPUT)
        else:
            self.ser.write(EXCEPTION)

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

                    #
                    pipeline_status = last_build['status']

                    # we just want a solid colour here
                    if pipeline_status == "SUCCESS" or pipeline_status == "FAILED" or pipeline_status == "ABORTED":
                        self.write_status(pipeline_status)

                    # we want to iterate through the stages
                    elif pipeline_status == "IN_PROGRESS" or pipeline_status == "PAUSED_PENDING_INPUT":
                        print pipeline_status
                        stages = last_build['stages']

                        for i, stage_status in enumerate(d['status'] for d in stages):
                            print stage_status
                            self.ser.write(OFF)
                            time.sleep(DEAD_TIME_S)
                            self.write_status(stage_status)
                            time.sleep(STAGE_CYCLE_TIME_S)

                            if i == len(stages) -1:
                                time.sleep(STAGE_CYCLE_TIME_S)

                except:
                    print "Failed to parse json"
                    self.ser.write(EXCEPTION)

        except urllib2.HTTPError, e:
            print "HTTP error: %s" % e
            self.ser.write(EXCEPTION)

        time.sleep(POLL_RATE_S)

    def infinity(self):
        forever = True

        while forever:
            self.poll()

    def __del__(self):
        if hasattr(self, 'ser'):
            self.ser.write(OFF) # turn the lights off
            self.ser.close()    # close the serial port

if __name__=="__main__":
    PipelineStatus(sys.argv[1:]).infinity()

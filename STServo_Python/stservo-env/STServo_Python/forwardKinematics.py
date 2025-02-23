#!/usr/bin/env python
#
# *********     Gen Write Example      *********
#
#
# Available STServo model on this example : All models using Protocol STS
# This example is tested with a STServo and an URT
#

import sys
import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
        
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

sys.path.append("..")
from STservo_sdk import *                 # Uses STServo SDK library

# Default setting
STS_IDS                     = [0, 1, 2, 3, 4]  # STServo IDs
BAUDRATE                    = 1000000          # STServo default baudrate : 1000000
DEVICENAME                  = 'COM7'           # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"
STS_MINIMUM_POSITION_VALUE  = 0                # STServo will rotate between this value
STS_MAXIMUM_POSITION_VALUE  = 500              # Maximum position value
STS_MOVING_SPEED            = 1000             # STServo moving speed
STS_MOVING_ACC              = 10               # STServo moving acceleration
DEGREE_INCREMENT            = 7                # Degree increment per key press
MAX_ROTATION_ANGLE          = 180              # Maximum rotation angle in degrees

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Get methods and members of Protocol
packetHandler = sts(portHandler)
    
# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Function to convert degrees to servo position value
def degree_to_position(degree):
    return int((degree / 180.0) * (STS_MAXIMUM_POSITION_VALUE - STS_MINIMUM_POSITION_VALUE))

# Initialize servo positions
servo_positions = [degree_to_position(0) for _ in STS_IDS]

# Key mapping for servo control
# Each servo has two keys: one for clockwise (CW) and one for counter-clockwise (CCW)
key_mapping = {
    '1': (0, 'CW'),  # Servo 0 CW
    '2': (0, 'CCW'), # Servo 0 CCW
    '3': (1, 'CW'),  # Servo 1 CW
    '4': (1, 'CCW'), # Servo 1 CCW
    '5': (2, 'CW'),  # Servo 2 CW
    '6': (2, 'CCW'), # Servo 2 CCW
    '7': (3, 'CW'),  # Servo 3 CW
    '8': (3, 'CCW'), # Servo 3 CCW
    '9': (4, 'CW'),  # Servo 4 CW
    '0': (4, 'CCW'), # Servo 4 CCW
}

while 1:
    print("Press a key to control the servos (1-0 for CW/CCW, ESC to quit):")
    key = getch()
    
    if key == chr(0x1b):  # ESC key to exit
        break
    
    if key in key_mapping:
        servo_id, direction = key_mapping[key]
        current_position = servo_positions[servo_id]
        
        if direction == 'CW':
            new_position = current_position + degree_to_position(DEGREE_INCREMENT)
        else:
            new_position = current_position - degree_to_position(DEGREE_INCREMENT)
        
        # Ensure the new position is within the maximum rotation angle
        new_position = max(degree_to_position(-MAX_ROTATION_ANGLE), min(degree_to_position(MAX_ROTATION_ANGLE), new_position))
        
        # Update the servo position
        servo_positions[servo_id] = new_position
        
        # Write STServo goal position/moving speed/moving acc
        sts_comm_result, sts_error = packetHandler.WritePosEx(STS_IDS[servo_id], new_position, STS_MOVING_SPEED, STS_MOVING_ACC)
        if sts_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(sts_comm_result))
        if sts_error != 0:
            print("%s" % packetHandler.getRxPacketError(sts_error))
        
        print(f"Servo {servo_id} moved to {new_position} ({direction})")
    else:
        print("Invalid key. Use 1-0 for CW/CCW control, ESC to quit.")

# Close port
portHandler.closePort()
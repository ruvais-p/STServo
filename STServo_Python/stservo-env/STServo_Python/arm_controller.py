# import sys
# import os

# if os.name == 'nt':
#     import msvcrt
#     def getch():
#         return msvcrt.getch().decode()
# else:
#     import sys, tty, termios
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     def getch():
#         try:
#             tty.setraw(sys.stdin.fileno())
#             ch = sys.stdin.read(1)
#         finally:
#             termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#         return ch

# sys.path.append("..")
# from STservo_sdk import *  # Uses STServo SDK library

# # Default setting
# BAUDRATE = 1000000
# DEVICENAME = 'COM7'
# STS_MOVING_SPEED = 1000  # Reduced speed for smoother movement
# STS_MOVING_ACC = 10     # Reduced acceleration for smoother movement
# STS_MINIMUM_POSITION_VALUE = 0
# STS_MAXIMUM_POSITION_VALUE = 2000
# STS_STEP = 60  # 5-degree step rotation (assuming 0.29 degrees per unit)

# # Servo ID mapping
# key_to_id = {
#     'y': 4, 'h': 4,
#     'u': 3, 'j': 3,
#     'i': 2, 'k': 2,
#     'p': 1, 'l': 1,
#     'p': 0, 'l': 0  # Same button for ID 1 and 0
# }

# # Initialize PortHandler instance
# portHandler = PortHandler(DEVICENAME)
# packetHandler = sts(portHandler)

# if not portHandler.openPort():
#     print("Failed to open the port")
#     getch()
#     quit()

# if not portHandler.setBaudRate(BAUDRATE):
#     print("Failed to change the baudrate")
#     getch()
#     quit()

# servo_positions = {id: STS_MINIMUM_POSITION_VALUE for id in set(key_to_id.values())}

# while True:
#     print("Press a key to move the servo (ESC to quit):")
#     key = getch().lower()
#     if key == chr(0x1b):  # ESC key to exit
#         break
    
#     if key in key_to_id:
#         servo_id = key_to_id[key]
#         current_position = servo_positions[servo_id]
        
#         if key in 'yuiop':
#             new_position = min(current_position + STS_STEP, STS_MAXIMUM_POSITION_VALUE)
#         else:
#             new_position = max(current_position - STS_STEP, STS_MINIMUM_POSITION_VALUE)
        
#         sts_comm_result, sts_error = packetHandler.WritePosEx(servo_id, new_position, STS_MOVING_SPEED, STS_MOVING_ACC)
#         if sts_comm_result != COMM_SUCCESS:
#             print(f"Error: {packetHandler.getTxRxResult(sts_comm_result)}")
#         if sts_error:
#             print(f"Packet error: {packetHandler.getRxPacketError(sts_error)}")
        
#         servo_positions[servo_id] = new_position
#     else:
#         print("Invalid key! Use assigned keys for movement.")

# portHandler.closePort()
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
from STservo_sdk import *  # Uses STServo SDK library

# Default setting
BAUDRATE = 1000000
DEVICENAME = 'COM7'
STS_MOVING_SPEED = 100
STS_MOVING_ACC = 10
STS_MINIMUM_POSITION_VALUE = 0
STS_MAXIMUM_POSITION_VALUE = 3000

# Servo ID mapping
key_to_id = {
    'y': 4, 'h': 4,
    'u': 3, 'j': 3,
    'i': 2, 'k': 2,
    'o': 1, 'l': 1,
    'p': 0, ';': 0
}

# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)
packetHandler = sts(portHandler)

if not portHandler.openPort():
    print("Failed to open the port")
    getch()
    quit()

if not portHandler.setBaudRate(BAUDRATE):
    print("Failed to change the baudrate")
    getch()
    quit()

while True:
    print("Press a key to move the servo (ESC to quit):")
    key = getch().lower()
    if key == chr(0x1b):  # ESC key to exit
        break
    
    if key in key_to_id:
        servo_id = key_to_id[key]
        position = STS_MAXIMUM_POSITION_VALUE if key in 'yuiop' else STS_MINIMUM_POSITION_VALUE
        
        sts_comm_result, sts_error = packetHandler.WritePosEx(servo_id, position, STS_MOVING_SPEED, STS_MOVING_ACC)
        if sts_comm_result != COMM_SUCCESS:
            print(f"Error: {packetHandler.getTxRxResult(sts_comm_result)}")
        if sts_error:
            print(f"Packet error: {packetHandler.getRxPacketError(sts_error)}")
    else:
        print("Invalid key! Use assigned keys for movement.")

portHandler.closePort()
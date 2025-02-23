# STServo Arm Controller

This project provides a Python script to control STServo motors using keyboard inputs. The script is located at:

```
STServo_Python/stservo-env/STServo_Python/arm_controller.py
```

## Features
- Uses `STServo SDK` for communication with servo motors.
- Controls servo positions with assigned keyboard keys.
- Supports real-time servo movements using `getch()` for key inputs.
- Adjustable speed and acceleration settings.

## Requirements
- Python 3.x
- STServo SDK
- Compatible STServo hardware
- Windows (COM Port usage) or Linux/Mac (TTY settings required)

## Installation
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd STServo_Python/stservo-env/STServo_Python
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Ensure the STServo SDK is installed and accessible.

## Configuration
Modify the following parameters in `arm_controller.py` as needed:
```python
BAUDRATE = 1000000   # Set the baud rate
DEVICENAME = 'COM7'  # Change this based on your system
STS_MOVING_SPEED = 100  # Adjust speed
STS_MOVING_ACC = 10     # Adjust acceleration
```

## Key Mappings
The following keys control different servo motors:

| Key | Servo ID | Movement |
|-----|---------|----------|
| y/h | 4 | Up/Down |
| u/j | 3 | Up/Down |
| i/k | 2 | Up/Down |
| o/l | 1 | Up/Down |
| p/; | 0 | Up/Down |

Pressing `ESC` will exit the program.

## Running the Script
Execute the script using:
```sh
python arm_controller.py
```

Follow on-screen instructions to control the servos.

## Troubleshooting
- If the port does not open, check if the correct `DEVICENAME` is set.
- Ensure the STServo SDK is correctly installed and configured.
- If key inputs are unresponsive, verify keyboard settings and script execution permissions.

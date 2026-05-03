# How to Run

## Overview

This guide explains how to set up and run the heliostat system.

The system consists of:

* Arduino Mega (motor control)
* PC (Python software)
* HC-12 wireless communication
* Stepper drivers (TB6600)

---

## 1. Hardware Setup

1. Connect all components according to the wiring diagram:

   → See:  [Wiring](hardware/wiring.drawio.png)

2. Ensure:

   * Correct power supply for motors and drivers
   * HC-12 modules configured identically (baud, channel)

3. Power on the system.

---

## 2. Upload Firmware

1. Open the Arduino project in:

   ```
   firmware/
   ```

2. Select:

   * Board: Arduino Mega
   * Correct COM port

3. Upload the firmware.

---

## 3. Setup PC Software

1. Navigate to:

   ```
   software/
   ```

2. Install dependencies:

   ```bash
   pip install pyserial pyqt5
   ```

3. Check serial port in the code (e.g. COM7 or /dev/ttyUSB0)

---

## 4. Start the System

1. Run the Python application:

   ```bash
   python main.py
   ```

2. Wait for connection to establish.

---

## 5. Initial Alignment (IMPORTANT)

Before starting tracking:

1. Enable motors
2. Use the joystick to manually align the reflected beam to the target
3. Reset position (set current position as reference)

This step defines the system's reference frame.

---

## 6. Start Tracking

1. Press **START TRACKING**
2. The system will:

   * compute Sun position
   * compute mirror orientation
   * send commands to motors periodically

---

## 7. Normal Operation

* The system updates every ~30 seconds
* Commands are sent as absolute positions
* No user intervention is required

---

## 8. Stop the System

* Press **STOP TRACKING**
* Disable motors if needed

---

## Troubleshooting

### No communication

* Check HC-12 wiring
* Verify correct serial port
* Ensure modules share same configuration

### Motors not moving

* Check ENABLE signal
* Verify driver power supply
* Check wiring to TB6600

### Unstable behavior

* Verify power supply stability
* Check mechanical constraints
* Ensure no loose connections

---

## Notes

* The system is open-loop: accuracy depends on calibration and mechanical precision
* Recalibration may be required after mechanical adjustments

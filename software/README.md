# Software (PC Controller)

This folder contains two main applications:

- **Tracker** → the full heliostat control system (GUI + tracking + communication)
- **Single Controller** → a simplified tool used for debugging, testing, and direct command execution

This module contains the Python application responsible for controlling the heliostat system.

It handles:

* communication with Arduino (HC-12)
* solar position computation
* reflection geometry
* motor command generation
* user interface (GUI)

The implementation is contained in a single file (`main.py`) for simplicity and rapid development.

---

## General Structure

The code is organized in logical sections:

```
CONFIG → SERIAL → MATH → GUI → TRACKING → MAIN LOOP
```

Each section has a specific role in the system.

---

## Configuration

Defines all system parameters:

* serial port and baud rate
* geographic position (LAT, LON)
* update interval
* target coordinates (T)
* motor resolution (STEPS_AZ, STEPS_EL)

Important:

* `STEPS_AZ` and `STEPS_EL` are derived from real measurements
* they already include mechanical reduction

---

## Serial Communication

Handles communication with Arduino via HC-12.

### Protocol

Commands are sent using:

```
#ID:COMMAND;
```

Responses are:

```
@ID:OK;
@ID:ERR;
```

### Key Features

* incremental message ID
* ACK validation
* timeout handling
* input buffer parsing

---

### `send(cmd)`

Main function for communication.

Workflow:

1. Build packet with unique ID
2. Clear input buffer
3. Send command
4. Wait for ACK
5. Return success/failure

Example:

```
#12:PX1000;
→ @12:OK;
```

---

### `wait_ack(expected_id)`

Reads serial data and parses responses.

* accumulates incoming bytes
* splits messages using `;`
* matches response ID
* returns:

  * `OK`
  * `ERR`
  * `TIMEOUT`

This ensures reliable communication even with HC-12 latency.

---

## Motion Control Interface

High-level abstraction for motor movement.

### `move_to(px, py)`

Executes a full movement sequence:

1. ENABLE drivers
2. Send absolute positions (`PX`, `PY`)
3. Wait
4. DISABLE drivers

Design choice:

* drivers are enabled only during movement
* reduces heat and power consumption

---

## Mathematical Model

### Vector Normalization

```
normalize(v)
```

Ensures all vectors are unit vectors.

---

### Solar Position

```
get_sun_vector(lat, lon)
```

Computes Sun direction using:

* day of year
* UTC time
* solar declination
* hour angle

Output:

* 3D normalized vector (S)

---

### Reflection Geometry

```
get_normal(S)
```

Computes mirror normal:

```
N = normalize(S + T)
```

---

### Angle Conversion

```
normal_to_angles(N)
```

Converts the normal vector into:

* azimuth
* elevation

---

## Step Conversion

Angles are converted into motor steps:

```
step_x = azimuth * STEPS_AZ
step_y = elevation * STEPS_EL
```

Notes:

* conversion is linear
* calibration factors can be added if needed
* based on empirical system measurements

---

## GUI (PyQt5)

Main interface class:

```
Control(QWidget)
```

Provides:

* manual control buttons
* tracking control
* real-time status display
* joystick input

---

### Controls

* ENABLE / DISABLE → driver control
* START TRACKING → begins automatic tracking
* STOP TRACKING → stops tracking
* STOP → emergency stop

---

### Status Display

* countdown to next update
* number of corrections performed

---

## Joystick (Manual Mode)

Custom widget:

```
Joystick(QWidget)
```

Features:

* mouse-based control
* normalized range [-1, 1]
* converts movement into step commands

Used for:

* initial alignment
* manual corrections

---

## Tracking Logic

Activated via:

```
start_tracking()
```

### Initialization

* reset position (`R`)
* compute initial angles (`az0`, `el0`)
* store reference

---

### Update Loop

Executed periodically:

1. Compute Sun vector
2. Compute mirror normal
3. Convert to angles
4. Compute angle difference
5. Convert to steps
6. Send movement command

---

### Key Design Choices

* absolute positioning (no drift accumulation)
* periodic updates (~30 seconds)
* deterministic behavior

---

## Main Loop

Managed by Qt timer:

```
QTimer → update_loop()
```

Runs every 100 ms.

Responsibilities:

* update UI
* manage tracking timing
* handle joystick input

---

## Manual Mode

When tracking is OFF:

* joystick generates relative steps
* commands:

  * `SX` → X movement
  * `SY` → Y movement

Dead zone is applied to avoid noise.

---

## Known Limitations

* blocking calls (`time.sleep`) in communication
* single-threaded design
* no retry mechanism beyond timeout
* open-loop control (no feedback)

---

## Design Philosophy

The software prioritizes:

* simplicity
* transparency
* direct control

over abstraction and modular complexity.

This makes debugging easier in a hardware-dependent system.

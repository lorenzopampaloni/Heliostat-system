# Firmware (Arduino Controller)

This firmware runs on the Arduino Mega and is responsible for:

* receiving commands via HC-12 (Serial1)
* controlling stepper motors (2 axes)
* executing motion commands
* sending ACK responses to the PC

The firmware implements a simple and robust command-based protocol.

---

## Hardware Interface

### Serial Ports

* `Serial` → USB (debug output)
* `Serial1` → HC-12 (main communication channel)

---

### Stepper Drivers

Controlled using the AccelStepper library in DRIVER mode.

Pins:

* X axis:

  * STEP → pin 4
  * DIR → pin 5
  * ENABLE → pin 8

* Y axis:

  * STEP → pin 6
  * DIR → pin 7
  * ENABLE → pin 9

---

## Main Loop

```cpp
loop()
```

Execution flow:

1. Read incoming serial data
2. Parse complete packets
3. Execute commands
4. Run stepper motors (`run()`)

Important:

* motors run **only when enabled**
* motion is handled non-blocking via `run()`

---

## Serial Protocol

### Command Format

```
#ID:COMMAND;
```

Example:

```
#12:PX1000;
```

---

### Response Format

```
@ID:OK;
@ID:ERR;
```

Example:

```
@12:OK;
```

---

### Design Features

* ID-based matching → ensures correct ACK association
* stateless commands → no session dependency
* simple parsing → robust against noise

---

## Serial Parsing

### `readSerial()`

* reads bytes from `Serial1`
* accumulates data into a buffer
* detects end of packet (`;`)
* sends packet to parser

---

### `processPacket(String pkt)`

Steps:

1. trim input
2. verify format (`#ID:CMD`)
3. extract:

   * message ID
   * command
4. execute command
5. send ACK

Invalid packets are ignored.

---

## Command Execution

### `executeCommand(String s)`

Parses and executes all supported commands.

---

### System Commands

* `ENABLE` → enable drivers
* `DISABLE` → disable drivers
* `S` → stop movement
* `R` → reset position (0,0)

---

### Motion Parameters

* `VX<number>` → set max speed X
* `VY<number>` → set max speed Y
* `AX<number>` → set acceleration X
* `AY<number>` → set acceleration Y

---

### Absolute Positioning

* `PX<number>` → move X to position
* `PY<number>` → move Y to position

Uses:

```cpp
moveTo()
```

---

### Relative Movement

* `SX<number>` → relative move X
* `SY<number>` → relative move Y

Uses:

```cpp
move()
```

---

## ACK Handling

### `sendAck(id, ok)`

Sends response back to PC:

* `OK` → command executed
* `ERR` → invalid command

Important:

* ACK is always returned for valid packets
* ensures synchronization with PC

---

## Driver Control

### `enableDrivers()`

* sets ENABLE pins HIGH
* enables motor execution
* allows `run()` to operate

---

### `disableDrivers()`

* disables drivers
* stops motor execution

---

## Stepper Configuration

```cpp
setMaxSpeed()
setAcceleration()
```

Configured at startup and adjustable via commands.

---

### Inverted Pins

```cpp
setPinsInverted(false, false, true);
```

Important:

* STEP signal is inverted (LOW pulse active)
* required for correct TB6600 behavior

---

## Key Design Choices

* non-blocking motion control (`run()`)
* command-based architecture
* explicit ENABLE / DISABLE control
* simple and robust protocol
* separation between communication and execution

---

## Limitations

* no command queue (commands overwrite previous targets)
* no position feedback (open-loop system)
* limited error handling (only OK / ERR)

---

## Debug Output

Via USB serial:

* received packets
* driver state (ENABLED / DISABLED)

Useful for:

* debugging communication
* verifying command execution

---

## Summary

The firmware provides:

* deterministic motor control
* reliable serial communication
* simple and extensible command interface

It is designed to work as a low-level execution layer controlled by the PC.

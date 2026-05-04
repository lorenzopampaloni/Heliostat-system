# Heliostat System

## System Overview

![System](hardware/photos/system/System_complete_overview.jpeg)

A 2-axis heliostat capable of reflecting sunlight toward a fixed target using a fully model-based approach.

---

## Overview

This project implements a solar reflection system that computes mirror orientation in real time using:

* solar position (time + geographic location)
* vector-based reflection geometry
* stepper motor control (Arduino)
* wireless communication via HC-12

Unlike traditional systems, no sensors or cameras are used.
The system operates entirely in open-loop, relying on accurate modeling and mechanical stability.

---

## Core Principle

The mirror orientation is computed using reflection geometry:

N = normalize(S + T)

Where:

* **S** → Sun direction vector
* **T** → Target direction vector
* **N** → Mirror normal vector

This ensures that incoming sunlight is reflected exactly toward the target.

---

## Key Features

* Sensorless heliostat (no encoders, no vision)
* Fully model-based control
* Wireless communication (HC-12)
* Custom mechanical design with backlash mitigation
* Absolute positioning (no cumulative error)
* Real-time tracking updates

---

## System Architecture

### PC (Python)

* Solar position computation
* Reflection geometry
* Command generation

### Arduino

* Stepper motor control
* Serial protocol handling

---

## Engineering Highlights

This project involved the design and integration of multiple engineering domains:

### Mechanical Design & Fabrication

* Custom aluminum parts machined on a lathe
* Design of a 2-axis structure with worm gear reducers
* Mechanical backlash mitigation using preload system (cable + weight)
* Assembly and alignment of a multi-axis system

### Embedded Systems

* Development of Arduino firmware for real-time motor control
* Integration of AccelStepper
* Non-blocking motion control using acceleration profiles
* Driver control and signal inversion handling

### Electronics & Hardware Integration

* Wiring and integration of stepper drivers (TB6600)
* Serial communication setup with HC-12 modules
* USB-to-TTL interface for PC communication
* Debugging of hardware-level issues (grounding, signal inversion, noise)

### Communication Protocol Design

* Custom serial protocol with message ID and ACK system
* Packet structure: `#ID:CMD;` → `@ID:OK;`
* Handling of latency and packet parsing
* Robust communication over wireless link

### Mathematical Modeling

* Solar position computation based on time and location
* Vector-based reflection model (mirror normal computation)
* Conversion from geometry to motor control space

### System Integration

* Full-stack integration: software + firmware + hardware
* Open-loop deterministic control strategy
* Calibration of real-world system vs theoretical model


---

## Documentation

* [How it works](HOW_IT_WORKS.md)
* [How to run](HOW_TO_RUN.md)
* [Hardware](hardware/README.md)
* [Firmware](firmware/README.md)
* [Software](software/README.md)
* [Photos](hardware/photos/)
* [Wiring](hardware/wiring.drawio.png)

---

## Status

Working prototype:

* Stable wireless communication
* Functional tracking
* Calibrated motion system

---

## Limitations

* Open-loop (no feedback)
* Requires manual calibration
* Accuracy depends on mechanical precision





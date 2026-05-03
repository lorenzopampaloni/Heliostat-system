# Heliostat System

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

## Documentation

* [How it works](HOW_IT_WORKS.md)
* [How to run](HOW_TO_RUN.md)
* [Hardware](hardware/README.md)
* [Firmware](firmware/README.md)
* [Software](software/README.md)
* [Photos](photos/)
* [Wiring](hardware/wiring.drawio)

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



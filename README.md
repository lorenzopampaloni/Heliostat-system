# Heliostat System

A 2-axis heliostat designed to reflect sunlight toward a fixed target using a fully model-based approach.

## Overview

This system computes the required mirror orientation in real time by combining:

- solar position (based on time and location)
- reflection geometry (vector-based)
- stepper motor control (Arduino-based)
- wireless communication (HC-12)

Unlike traditional tracking systems, no sensors or cameras are used. The system operates entirely in open-loop, relying on accurate mechanical design and calibration.

## Core Principle

The mirror normal is computed as:

N = normalize(S + T)

Where:
- S = sun direction vector
- T = target direction vector

## Key Features

- Sensorless heliostat (no encoders, no vision)
- Wireless control via HC-12
- Custom mechanical structure with backlash mitigation
- Absolute positioning (no error accumulation)
- Real-time tracking updates

## Architecture

- **PC (Python):**
  - solar position computation
  - reflection geometry
  - command generation

- **Arduino:**
  - stepper motor control
  - serial protocol handling

## Status

Working prototype with:
- functional tracking
- stable communication
- calibrated motion system

## Limitations

- open-loop (no feedback)
- mechanical calibration required
- accuracy dependent on assembly precision

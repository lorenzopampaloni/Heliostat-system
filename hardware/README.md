# Hardware

This section describes all the physical components used in the heliostat system, including electronics, mechanical structure, and custom-built parts.

---

## Overview

The system is built around a 2-axis mechanism:

* **Azimuth axis** → base rotation
* **Elevation axis** → mirror tilt

It combines:

* stepper motors
* worm gear reducers
* custom machined structure
* wireless communication (HC-12)

---

## Bill of Materials (BOM)

### Electronics

* Arduino Mega
* 2× Stepper Drivers (TB6600 or compatible)
* 2× HC-12 wireless modules
* USB-to-TTL adapter (for PC ↔ HC-12 communication)

---

### Actuation

* 2× Stepper Motors (similar to NEMA 23 class)

---

### Transmission

* 2× Worm gear reducers (recovered from satellite dish positioning system)

Characteristics:

* high reduction ratio
* high torque
* low back-driving

---

### Mechanical Structure

Custom-built components:

* aluminum discs (machined on lathe)
* rotating base with flat bearing
* elevation support structure
* mirror frame

---

### Mirror System

* mirror mounted on custom frame
* 4 adjustment screws (corners)

Allows:

* fine alignment
* curvature adjustment (convex / concave)

---

### Backlash Mitigation System

Implemented using:

* cable (bike brake wire)
* pulley
* weight (lead mass)

Purpose:

* apply constant preload
* eliminate backlash in gear system
* ensure deterministic behavior

---

## Wiring

All electrical connections are documented here:

👉 See: `wiring_diagram.png`

Includes:

* Arduino ↔ drivers
* Arduino ↔ HC-12
* power connections

---

## Photos

System images and details:

👉 See: `photos/`

---

## Mechanical Fabrication

Several parts were manually manufactured:

* aluminum discs (lathe machining)
* custom supports
* mirror frame

This allowed:

* precise integration of components
* adaptation to reused mechanical parts
* increased structural rigidity

---

## Design Considerations

* backlash removed mechanically 
* real system resolution measured empirically
* reuse of existing mechanical components (worm gears)
* focus on robustness over complexity

---

## Summary

The hardware is a hybrid system combining:

* off-the-shelf electronics
* reused mechanical components
* custom-built structure

with a strong focus on mechanical stability and simplicity.

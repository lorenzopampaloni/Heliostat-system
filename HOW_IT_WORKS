# How It Works

## Overview

The system is a 2-axis heliostat designed to reflect sunlight toward a fixed target.

Instead of directly pointing at the Sun, the mirror is oriented such that incoming sunlight is reflected toward a desired point in space.

This is achieved using a fully model-based approach, without any sensors or feedback.

---

## Core Principle: Reflection Geometry

The system is based on the law of reflection:

> The angle of incidence equals the angle of reflection.

In vector form, this can be solved by computing the mirror normal as the bisector between:

* the Sun direction vector (**S**)
* the target direction vector (**T**)

The required mirror normal is:

N = normalize(S + T)

Where:

* **S** → unit vector pointing from the mirror toward the Sun
* **T** → unit vector pointing from the mirror toward the target
* **N** → unit normal vector of the mirror surface

This ensures that sunlight is reflected exactly toward the target.

---

## Sun Position Computation

The Sun position is calculated using:

* geographic coordinates (latitude, longitude)
* current date and time

From this, the system computes:

* azimuth angle
* elevation angle

These angles are then converted into a 3D unit vector **S**.

---

## Target Definition

The target is defined as a fixed point in space relative to the mirror.

Example:

T = (x, y, z)

This vector is normalized to obtain the direction **T**.

---

## From Normal Vector to Motor Angles

Once the mirror normal **N** is computed, it is converted into:

* azimuth angle
* elevation angle

These angles represent the required orientation of the mirror.

---

## Conversion to Motor Steps

The angular values are converted into motor steps using calibrated parameters:

step_x = azimuth * STEPS_AZ * Kx
step_y = elevation * STEPS_EL * Ky

Where:

* **STEPS_AZ / STEPS_EL** → steps per revolution (measured on the real system)
* **Kx / Ky** → calibration factors compensating mechanical imperfections

---

## Control Flow

The system operates in a loop:

1. Compute Sun position
2. Compute mirror normal
3. Convert to angles
4. Convert to motor steps
5. Send commands to Arduino

This process is repeated periodically (e.g. every 30 seconds).

---

## Open-Loop Strategy

The system does not use any sensors or feedback.

Accuracy is achieved through:

* mechanical rigidity
* backlash mitigation
* initial manual calibration
* precise mathematical modeling

To avoid error accumulation, the system always sends **absolute positions**, not incremental movements.

---

## Backlash Mitigation

Mechanical backlash is reduced using a preload system:

* cable + pulley + weight

This ensures that the gear system is always loaded in one direction, making the system deterministic and suitable for open-loop control.

---

## Summary

The system combines:

* astronomical computation
* vector-based reflection geometry
* calibrated motor control

to achieve accurate solar reflection without any feedback sensors.

This approach prioritizes simplicity, robustness, and physical modeling over complex sensing systems.

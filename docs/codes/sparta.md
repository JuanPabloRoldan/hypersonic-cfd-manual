---
status: outline
---

# SPARTA

Open-source direct simulation Monte Carlo (DSMC) code from Sandia National Laboratories.

## Purpose

Rarefied flows where the continuum assumption breaks down: high altitude, small features, wakes ([Track 1.9](../course/track-1.md)).

## Choices

DSMC with simulated particles on a hierarchical Cartesian grid with cut cells; adaptive grids; Kokkos for GPU portability. Collisions and chemistry are modelled statistically per particle pair rather than by continuum closures.

## What's cool

A completely different discretization family ([particles](../reference/spatial/discretization-families.md#particle-methods-dsmc)), and a production example of performance-portable GPU code.

!!! warning "Calibration"
    Outline only; to be filled from SPARTA documentation.

## References

Bird, *Molecular Gas Dynamics and the Direct Simulation of Gas Flows*; SPARTA documentation. See the [bibliography](../references.md).

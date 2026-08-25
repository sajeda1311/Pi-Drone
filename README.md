# Pi-Drone: ROS 2 Offboard-Control Prototype

A ROS 2 and PX4 simulation project for testing programmatic drone control, telemetry, and the transition into OFFBOARD flight mode before moving toward Raspberry Pi-based deployment.

## Motivation

Autonomous inspection and robotics projects need a safe way to validate control logic before hardware flight. Pi-Drone uses PX4 software-in-the-loop simulation and Gazebo to test command timing, middleware integration, and flight-state behaviour in a controlled environment.

## Goals

- Connect ROS 2 applications to PX4 through MAVROS and MAVLink.
- Stream setpoints at a rate suitable for OFFBOARD control.
- Test a simple takeoff, hover, and idle sequence in simulation.
- Inspect telemetry and sensor topics during preflight debugging.
- Build a foundation for companion-computer deployment on Raspberry Pi.

## Work completed

- Created a ROS 2 package for offboard-control experiments.
- Published `TwistStamped` velocity setpoints at **20 Hz**.
- Implemented timed takeoff, hover, and idle phases.
- Exercised PX4 SITL, Gazebo, ROS 2 Humble, MAVROS, and MAVLink integration.
- Investigated EKF and preflight checks that blocked arming during simulation.

## Control flow

```text
ROS 2 node → MAVROS → MAVLink → PX4 SITL → Gazebo vehicle
     ↑                                      │
     └──────────── telemetry and state ─────┘
```

## Technology

- ROS 2 Humble
- PX4 Autopilot / SITL
- Gazebo
- MAVROS and MAVLink
- Python
- Raspberry Pi as the intended companion-computer target

## Repository structure

```text
Pi-Drone/
├── package.xml
├── setup.py
├── resource/
└── pi_drone/
    └── offboard_control.py
```

## Build and run

Prerequisites include a working ROS 2 Humble workspace, PX4 SITL, Gazebo, and MAVROS.

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/sajeda1311/Pi-Drone.git
cd ..
colcon build --symlink-install
source install/setup.bash
```

Start PX4 SITL, Gazebo, and the MAVROS bridge using the configuration appropriate to your environment. Then run the package entry point defined in `setup.py`.

## Accomplishments

- Established the ROS 2-to-PX4 command path in simulation.
- Maintained the continuous setpoint stream required by OFFBOARD mode.
- Used telemetry and sensor streams to diagnose system readiness instead of treating arming failures as application-only bugs.
- Created a reusable base for future autonomous inspection behaviours.

## Current status

The node publishes OFFBOARD setpoints, but PX4 arming remained blocked by EKF2/preflight readiness during the documented tests. The repository represents active simulation and integration work; it does not claim a completed autonomous flight or hardware deployment.

## Next goals

- Add explicit vehicle-state checks before changing mode or arming.
- Resolve the EKF/preflight simulation configuration and document the fix.
- Add position or trajectory setpoints with a formal state machine.
- Include launch files, parameter files, and repeatable SITL commands.
- Add safety timeouts, geofencing, and command-loss handling.
- Validate the same interface on a Raspberry Pi companion computer.


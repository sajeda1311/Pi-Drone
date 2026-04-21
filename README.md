# PX4 + MAVROS + ROS 2 Drone Simulation Project

This repository contains a ROS 2 package used to control a PX4 simulated drone through MAVROS.
It was developed for a project based on a PX4 + Gazebo x500 simulation environment running on Ubuntu 22.04.

## Project Overview

The goal of this project is to connect:

- **PX4 SITL** as the flight controller
- **Gazebo** as the simulation environment
- **MAVROS** as the bridge between PX4 and ROS 2
- **ROS 2 Humble** as the control framework

A custom ROS 2 Python node publishes OFFBOARD control setpoints to the drone and attempts to support takeoff behavior.

## Repository Structure

```text
pidrone_project/
├── README.md
├── package.xml
├── setup.py
├── setup.cfg
├── launch/
│   └── pidrone_offboard.launch.py
├── pidrone_control/
│   ├── __init__.py
│   └── move_drone.py
├── resource/
│   └── pidrone_control
└── docs/
    └── run_commands.md
```

## Requirements

- Ubuntu 22.04
- ROS 2 Humble
- PX4 Autopilot
- Gazebo
- MAVROS and MAVROS extras

Install MAVROS:

```bash
sudo apt update
sudo apt install ros-humble-mavros ros-humble-mavros-extras geographiclib-tools
sudo geographiclib-get-geoids egm96-5
```

## Build

Create a ROS 2 workspace and place this repository inside the `src` folder.

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
# clone this repo here
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

## Run Procedure

### 1. Start PX4 SITL

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

### 2. Start MAVROS

```bash
source /opt/ros/humble/setup.bash
ros2 launch mavros px4.launch.py fcu_url:=udp://:14540@127.0.0.1:14557
```

If your MAVROS installation only provides `px4.launch`, check your distro-specific MAVROS package and adapt the command accordingly.

### 3. Run the control node

```bash
source /opt/ros/humble/setup.bash
cd ~/ros2_ws
source install/setup.bash
ros2 run pidrone_control move_drone
```

### 4. Set OFFBOARD mode

```bash
ros2 service call /mavros/set_mode mavros_msgs/srv/SetMode "{base_mode: 0, custom_mode: 'OFFBOARD'}"
```

### 5. Arm the drone

```bash
ros2 service call /mavros/cmd/arming mavros_msgs/srv/CommandBool "{value: true}"
```

## Important Note

In the original project work, the node successfully published setpoints and OFFBOARD mode could be requested,
but the drone could not arm consistently because PX4 reported preflight health check / EKF2 related issues.

So this repository reflects the **implementation developed for the project**, but successful flight may still
depend on resolving PX4 EKF2 / arming configuration in the simulation environment.

## Main Topics Used

- `/mavros/state`
- `/mavros/local_position/pose`
- `/mavros/setpoint_velocity/cmd_vel`
- `/mavros/setpoint_position/local`

## License

This project is provided for academic use.

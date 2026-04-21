# Run Commands

## Terminal 1: PX4 + Gazebo
```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

## Terminal 2: MAVROS
```bash
source /opt/ros/humble/setup.bash
ros2 launch mavros px4.launch.py fcu_url:=udp://:14540@127.0.0.1:14557
```

## Terminal 3: Build and run custom package
```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
ros2 run pidrone_control move_drone
```

## Terminal 4: Monitor MAVROS state
```bash
source /opt/ros/humble/setup.bash
ros2 topic echo /mavros/state
```

## Set OFFBOARD mode
```bash
ros2 service call /mavros/set_mode mavros_msgs/srv/SetMode "{base_mode: 0, custom_mode: 'OFFBOARD'}"
```

## Arm the drone
```bash
ros2 service call /mavros/cmd/arming mavros_msgs/srv/CommandBool "{value: true}"
```

## Monitor local pose
```bash
ros2 topic echo /mavros/local_position/pose
```

## Known issue
In the project environment, PX4 often refused arming with messages such as:
- Preflight Fail: ekf2 missing data
- Arming denied: Resolve system health failures first

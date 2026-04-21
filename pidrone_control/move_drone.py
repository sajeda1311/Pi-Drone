import math
from typing import Optional

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped


class DroneController(Node):
    """Publish velocity setpoints for PX4 through MAVROS.

    This node continuously publishes velocity commands to keep OFFBOARD mode alive.
    The current implementation performs a simple timed sequence:
    1. Publish upward velocity for a takeoff attempt
    2. Hold near-hover command
    3. Publish zero velocity after that

    Note:
        In the original project environment, OFFBOARD setpoints were published
        successfully, but PX4 arming was blocked by EKF2 / preflight issues.
    """

    def __init__(self) -> None:
        super().__init__('drone_controller')

        self.publisher_ = self.create_publisher(
            TwistStamped,
            '/mavros/setpoint_velocity/cmd_vel',
            10
        )

        self.timer_period = 0.05  # 20 Hz
        self.timer = self.create_timer(self.timer_period, self.publish_setpoint)

        self.start_time_ns = self.get_clock().now().nanoseconds
        self.takeoff_duration = 8.0
        self.hover_duration = 12.0

        self.get_logger().info('Drone controller node started.')
        self.get_logger().info('Publishing velocity setpoints to /mavros/setpoint_velocity/cmd_vel')

    def publish_setpoint(self) -> None:
        now_ns = self.get_clock().now().nanoseconds
        elapsed = (now_ns - self.start_time_ns) / 1e9

        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'

        # Basic control profile
        if elapsed < self.takeoff_duration:
            # Upward velocity during takeoff phase
            msg.twist.linear.z = 0.8
            phase = 'takeoff'
        elif elapsed < self.takeoff_duration + self.hover_duration:
            # Hover / hold command
            msg.twist.linear.z = 0.0
            phase = 'hover'
        else:
            # Stop sending movement
            msg.twist.linear.x = 0.0
            msg.twist.linear.y = 0.0
            msg.twist.linear.z = 0.0
            phase = 'idle'

        # Keep yaw rate at zero
        msg.twist.angular.z = 0.0

        self.publisher_.publish(msg)

        self.get_logger().info(
            f'Publishing {phase} setpoint: '
            f'vx={msg.twist.linear.x:.2f}, '
            f'vy={msg.twist.linear.y:.2f}, '
            f'vz={msg.twist.linear.z:.2f}'
        )


def main(args: Optional[list[str]] = None) -> None:
    rclpy.init(args=args)
    node = DroneController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down drone controller node.')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

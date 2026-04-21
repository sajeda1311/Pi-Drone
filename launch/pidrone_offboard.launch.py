from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='pidrone_control',
            executable='move_drone',
            name='drone_controller',
            output='screen'
        )
    ])

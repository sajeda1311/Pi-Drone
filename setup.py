from setuptools import setup

package_name = 'pidrone_control'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/pidrone_offboard.launch.py']),
        ('share/' + package_name + '/docs', ['docs/run_commands.md']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your_email@example.com',
    description='ROS 2 package for PX4 + MAVROS offboard drone control.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'move_drone = pidrone_control.move_drone:main',
        ],
    },
)

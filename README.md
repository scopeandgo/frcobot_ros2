# frcobot_ros2

## Linux architecture support (local customization)

This branch includes SDK 2.3.2 for Linux **AArch64/ARM64** and **x86-64**.
CMake selects the matching library automatically. ARM64 hosts and containers
can stay native; emulation and manual library replacement are not required.
Other architectures and non-Linux builds fail with a clear configuration error.
See [ARM64 SDK provenance](fairino_hardware/libfairino/ARM64_SOURCE.md).

After pulling this update inside the ROS workspace, rebuild the hardware
package with a fresh CMake configuration (adjust the workspace path if needed):

```bash
source /opt/ros/jazzy/setup.bash
cd ~/fairino_ws
colcon build --packages-up-to fairino_hardware --cmake-clean-cache
source install/setup.bash
```

The configure output should say `Fairino SDK 2.3.2: aarch64` on ARM64.
The selected SDK and SONAME links are installed into the package's `lib`
directory during installation; source-tree SDK links are not modified.
Target-container compilation and physical robot testing remain required.

## Runtime robot connection (local customization)

Build this checkout once, then select each robot's address when starting its
driver. No IP-specific source changes or rebuilds are required.

For the command server, use a startup-only ROS parameter:

```bash
ros2 run fairino_hardware ros2_cmd_server --ros-args \
  -p robot_ip:=192.168.57.100 -r __ns:=/arm_left
```

Alternatively, supply an environment variable to the driver process:

```bash
FAIRINO_ROBOT_IP=192.168.57.100 ros2 run fairino_hardware ros2_cmd_server \
  --ros-args -r __ns:=/arm_left
```

An explicit `robot_ip` parameter takes precedence over `FAIRINO_ROBOT_IP`.
Without either, the upstream default remains `192.168.58.2`. An empty explicit
parameter is rejected. Restart the driver to select a different robot.

The real `FairinoHardwareInterface` also reads `FAIRINO_ROBOT_IP` at startup.
For multiple hardware instances in one process, configure an explicit
`<param name="robot_ip">192.168.57.100</param>` inside each real hardware
instance's `<hardware>` element instead. That hardware parameter overrides the
environment variable. The supplied MoveIt demo still uses mock hardware;
this change does not switch it to real robot control.

Use a different ROS namespace for each command-server instance. This change
does not add the joint/link prefixes and controller configuration needed for
combined multi-arm MoveIt planning. ROS 2 Jazzy compatibility and physical
robot operation still need to be verified in the target Linux container.

This is the ROS2 API project of Fairino robot(sofeware version must greater than V3.7.1), a serial of functions which based on Fair SDK API but were simplified are created, user can call them through service message.
API_description.md list all API functions.
Tutorial of installing and uasage of ROS2 API, please refer to the Fair document platform:https://fair-documentation.readthedocs.io/en/latest/ROSGuide/index.html#frcobot-ros2.

Version histroy:
2023.7.18 V1.0

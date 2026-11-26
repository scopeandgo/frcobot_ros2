#pragma once

#include <cstdlib>
#include <string>

namespace fairino_hardware
{
// Read at startup; an explicit ROS/hardware parameter takes precedence.
inline std::string default_robot_ip(const char *fallback)
{
  const char *value = std::getenv("FAIRINO_ROBOT_IP");
  return value && value[0] ? std::string(value) : std::string(fallback);
}
}  // namespace fairino_hardware

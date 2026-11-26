# libfairino is supplied as a Linux ELF binary, not a portable source library.
if(NOT CMAKE_SYSTEM_NAME STREQUAL "Linux")
  message(FATAL_ERROR "Fairino SDK requires Linux; build inside the ROS container.")
endif()

string(TOLOWER "${CMAKE_SYSTEM_PROCESSOR}" _fairino_processor)
set(_fairino_sdk_root "${CMAKE_CURRENT_LIST_DIR}/../libfairino/lib")
if(_fairino_processor MATCHES "^(aarch64|arm64)$")
  set(FAIRINO_SDK_ARCH "aarch64")
  set(_fairino_sdk_source "${_fairino_sdk_root}/aarch64/libfairino.so.2.3.2")
elseif(_fairino_processor MATCHES "^(x86_64|amd64)$")
  set(FAIRINO_SDK_ARCH "x86_64")
  set(_fairino_sdk_source "${_fairino_sdk_root}/libfairino.so.2.3.2")
else()
  message(FATAL_ERROR "Unsupported Fairino SDK target architecture: ${CMAKE_SYSTEM_PROCESSOR}")
endif()

if(NOT EXISTS "${_fairino_sdk_source}")
  message(FATAL_ERROR "Missing ${FAIRINO_SDK_ARCH} Fairino SDK: ${_fairino_sdk_source}")
endif()

# Keep the real file and relative SONAME links together in the build directory.
# These are installed at install time, including under colcon --symlink-install.
set(_fairino_sdk_build_dir "${CMAKE_CURRENT_BINARY_DIR}/fairino_sdk")
file(MAKE_DIRECTORY "${_fairino_sdk_build_dir}")
configure_file("${_fairino_sdk_source}"
  "${_fairino_sdk_build_dir}/libfairino.so.2.3.2" COPYONLY)
file(CREATE_LINK "libfairino.so.2.3.2"
  "${_fairino_sdk_build_dir}/libfairino.so.2" SYMBOLIC)
file(CREATE_LINK "libfairino.so.2"
  "${_fairino_sdk_build_dir}/libfairino.so" SYMBOLIC)

add_library(FairinoSDK SHARED IMPORTED)
set_target_properties(FairinoSDK PROPERTIES
  IMPORTED_LOCATION "${_fairino_sdk_build_dir}/libfairino.so.2.3.2"
  IMPORTED_SONAME "libfairino.so.2")
install(FILES
  "${_fairino_sdk_build_dir}/libfairino.so.2.3.2"
  "${_fairino_sdk_build_dir}/libfairino.so.2"
  "${_fairino_sdk_build_dir}/libfairino.so"
  DESTINATION lib)
message(STATUS "Fairino SDK 2.3.2: ${FAIRINO_SDK_ARCH}")

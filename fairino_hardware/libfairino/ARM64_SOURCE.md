# ARM64 SDK provenance

`lib/aarch64/libfairino.so.2.3.2` is the unmodified library extracted from
`linux/libfairino/lib/arm3399.zip` in FAIRINO's official C++ SDK:

- Repository: https://github.com/FAIR-INNOVATION/fairino-cpp-sdk
- Tag: `v2.3.2-robot3.9.2`
- Commit: `2ba16e2373a541d4880cb970f421bbd249a749c1`
- Library SHA-256: `852b8f0d07446d7abc2c9225a7e50ffcefe559279a831565ac194f833df3964e`

Inspection confirms ELF64 AArch64, SONAME `libfairino.so.2`, and dependencies
on libc, libstdc++, libgcc_s, and libm. The binary references GLIBC 2.17 and
GLIBCXX versions up to 3.4.21. It exports all 530 FRRobot symbols exported by
the x86-64 library bundled with this ROS driver. The SDK's `robot.h`
declarations match the driver's after removing comments and whitespace;
`robot_types.h` also matches after that normalization.

The archive's board name does not itself prove compatibility with every ARM64
host. Full driver linking, library loading, and robot operation must still be
tested on the target Linux system. This addition does not establish general
ROS 2 Jazzy or real-time control compatibility.

The existing upstream x86-64 binary is unchanged. CMake selects by the target
`CMAKE_SYSTEM_PROCESSOR`, not by the robot model or robot IP.

"""Exercise SDK selection and installation without ROS or a robot.

Run with: python3 -m unittest discover -s fairino_hardware/tests -v
Requires CMake >= 3.14 on PATH. These checks do not link or execute the SDK.
"""

from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parents[1]


class SDKSelectionTest(unittest.TestCase):
    def configure(self, directory, processor, system="Linux"):
        source = directory / "source"
        build = directory / "build"
        source.mkdir()
        (source / "CMakeLists.txt").write_text(
            'cmake_minimum_required(VERSION 3.14)\n'
            'project(sdk_selection NONE)\n'
            f'set(CMAKE_SYSTEM_NAME "{system}")\n'
            f'set(CMAKE_SYSTEM_PROCESSOR "{processor}")\n'
            f'include("{PACKAGE.as_posix()}/cmake/FairinoSDK.cmake")\n'
        )
        result = subprocess.run(
            ["cmake", "-S", str(source), "-B", str(build)],
            capture_output=True, text=True,
        )
        return result, build

    def test_selected_library_and_installed_soname(self):
        for processor, machine, arch in (
            ("aarch64", 183, "aarch64"),
            ("arm64", 183, "aarch64"),
            ("x86_64", 62, "x86_64"),
            ("AMD64", 62, "x86_64"),
        ):
            with self.subTest(processor=processor), tempfile.TemporaryDirectory() as tmp:
                directory = Path(tmp)
                result, build = self.configure(directory, processor)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(f"Fairino SDK 2.3.2: {arch}", result.stdout)
                install = directory / "install"
                subprocess.run(
                    ["cmake", "--install", str(build), "--prefix", str(install)],
                    capture_output=True, text=True, check=True,
                )
                library = install / "lib/libfairino.so.2.3.2"
                data = library.read_bytes()
                self.assertEqual(data[:6], b"\x7fELF\x02\x01")
                self.assertEqual(struct.unpack_from("<H", data, 18)[0], machine)
                expected = PACKAGE / "libfairino/lib"
                if arch == "aarch64":
                    expected /= "aarch64"
                self.assertEqual(data, (expected / library.name).read_bytes())
                for name in ("libfairino.so", "libfairino.so.2"):
                    link = install / "lib" / name
                    self.assertTrue(link.is_symlink())
                    self.assertEqual(link.resolve(), library.resolve())
                # Relative SONAME links must survive moving the install prefix.
                moved = directory / "moved"
                shutil.move(str(install), moved)
                self.assertEqual((moved / "lib/libfairino.so").read_bytes(), data)

    def test_unsupported_architecture_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, _ = self.configure(Path(tmp), "armv7l")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unsupported Fairino SDK target architecture", result.stderr)

    def test_non_linux_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, _ = self.configure(Path(tmp), "arm64", "Darwin")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Fairino SDK requires Linux", result.stderr)


if __name__ == "__main__":
    unittest.main()

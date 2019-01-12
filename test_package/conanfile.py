
from conans import ConanFile, CMake, tools, RunEnvironment
import os


class TestPackageGeant4(ConanFile):
    settings = "os", "compiler", "build_type", "arch", "cppstd"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            bin_path = os.path.join("bin","test_g4_find_package")
            self.run(bin_path)

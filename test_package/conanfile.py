
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
        pass

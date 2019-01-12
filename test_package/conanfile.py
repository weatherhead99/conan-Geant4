
from conans import ConanFile, CMake, tools, RunEnvironment
import os
from shutil import copyfile


class TestPackageGeant4(ConanFile):
    settings = "os", "compiler", "build_type", "arch", "cppstd"
    generators = "cmake", "qt"
    requires = "Geant4/10.05@weatherhead99/testing"

    
    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

        self.output.info(self.deps_cpp_info["Geant4"].options)
        
        if self.options["Geant4"].Qt:
            copyfile("qt.conf", os.path.join(self.build_folder, "bin", "qt.conf"))
        

    def test(self):
        
        with tools.environment_append(RunEnvironment(self).vars):
            #so it can run on systems without display in case Qt is enabled...
            os.environ["QT_QPA_PLUGIN"] = "minimnal"
            bin_path = os.path.join("bin", "test_g4_find_package")
            self.run(bin_path)

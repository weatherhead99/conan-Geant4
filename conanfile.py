from conans import ConanFile, CMake, tools


class Geant4Conan(ConanFile):
    name = "Geant4"
    version = "10.04.p02"
    license = "g4sl (https://geant4.web.cern.ch/geant4/license/LICENSE.html)"
    url = "https://geant4.web.cern.ch/"
    description = "Geant4 is a toolkit for the simulation of the passage of particles through matter."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "build_cxxstd" : ["11","14","17"],
               "HDF5" : [True, False],
               "GDML" : [True, False],
               "inventor" : [True, False],
               "openGL" : [True, False],
               "Qt" : [True, False],
               "Motif" : [True, False],
               "Win32" : [True, False],
               "Wt" : [True, False],
               "install_data" : [True, False]
    }
    default_options = "shared=False","build_cxxstd=11","HDF5=False","install_data=True", "Wt=False", \
                               "GDML=False","inventor=False","openGL=True","Qt=True","Motif=False","Win32=False"
    generators = "cmake"

    requires = "zlib/1.2.11@conan/stable", "expat/2.2.5@bincrafters/stable"

    def source(self):
        tools.get("http://cern.ch/geant4-data/releases/geant4.%s.tar.gz" % self.version,
                  sha256="6491862ba2be32c902e488ceb6b0f5189ccb4c8827f4906eea6b23782ac81a59",
                  filename="geant4.%s.tar.gz" % self.version)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["GEANT4_BUILD_CXXSTD"] = self.options.build_cxxstd
        cmake.definitions["GEANT4_USE_QT"] = self.options.Qt
        cmake.definitions["GEANT4_INSTALL_DATA"] = self.options.install_data
        cmake.definitions["GEANT4_USE_INVENTOR"] = self.options.inventor
        cmake.definitions["GEANT4_USE_HDF5"] = self.options.HDF5
        cmake.definitions["GEANT4_USE_GDML"] = self.options.GDML
        cmake.definitions["GEANT4_USE_MOTIF"] = self.options.Motif
        #TODO: check is this for win32???
        cmake.definitions["GEANT4_USE_WT"] = self.options.Wt

        #disable using system libs (except CLHEP!!)
        cmake.definitions["GEANT4_USE_SYSTEM_EXPAT"] = False
        cmake.definitions["GEANT4_USE_SYSTEM_ZLIB"] = False

        if not self.options.shared:
            cmake.definitions["BUILD_STATIC_LIBS"] = True
        
        cmake.configure(source_folder="geant4.%s" % self.version)
        cmake.build()


    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]


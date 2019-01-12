from conans import ConanFile, CMake, tools

G4_10_04_p02_SHA = "6491862ba2be32c902e488ceb6b0f5189ccb4c8827f4906eea6b23782ac81a59"
G4_10_05_SHA = "2a86499d8327abc68456e5d7fc0303824e5704322291b331857cf4042286656e"

class Geant4Conan(ConanFile):
    name = "Geant4"
    version = "10.05"
    license = "g4sl (https://geant4.web.cern.ch/geant4/license/LICENSE.html)"
    url = "https://geant4.web.cern.ch/"
    description = "Geant4 is a toolkit for the simulation of the passage of particles through matter."
    settings = "cppstd", "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
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
    default_options = "shared=False","HDF5=False","install_data=True", "Wt=False", \
                               "GDML=False","inventor=False","openGL=True","Qt=True","Motif=False","Win32=False"
    generators = "cmake"

    requires = "zlib/1.2.11@conan/stable", "expat/2.2.5@bincrafters/stable"

    def requirements(self):
        if self.options.Qt:
            self.requires("qt/5.12.0@bincrafters/stable")
        if self.options.HDF5:
            self.requires("hdf5/1.10.3@arsen-studio/stable")
    
    def source(self):
        tools.get("http://cern.ch/geant4-data/releases/geant4.%s.tar.gz" % self.version,
                  sha256=G4_10_05_SHA,
                  filename="geant4.%s.tar.gz" % self.version)

    def build(self):
        cmake = CMake(self)
        
        cmake.definitions["GEANT4_BUILD_CXXSTD"] = str(self.settings.cppstd).strip("gnu")
        cmake.definitions["GEANT4_USE_QT"] = self.options.Qt
        cmake.definitions["GEANT4_INSTALL_DATA"] = self.options.install_data
        cmake.definitions["GEANT4_USE_INVENTOR"] = self.options.inventor
        cmake.definitions["GEANT4_USE_HDF5"] = self.options.HDF5
        cmake.definitions["GEANT4_USE_GDML"] = self.options.GDML
        cmake.definitions["GEANT4_USE_MOTIF"] = self.options.Motif
        cmake.definitions["GEANT4_USE_WT"] = self.options.Wt

        #disable using system libs (except CLHEP!!)
        cmake.definitions["GEANT4_USE_SYSTEM_EXPAT"] = False
        cmake.definitions["GEANT4_USE_SYSTEM_ZLIB"] = False

        if not self.options.shared:
            cmake.definitions["BUILD_STATIC_LIBS"] = True
        
        cmake.configure(source_folder="geant4.%s" % self.version)
        cmake.build()
        cmake.install()


    def package(self):
        pass
    
    def package_info(self):
        self.cpp_info.includedirs=["include/Geant4/","include"]
        self.cpp_info.libs=tools.collect_libs(self)
        
        


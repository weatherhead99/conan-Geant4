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
               "install_data" : [True, False],
               "multithreaded" : [True, False],
               "muonic_atoms" : [True, False],
               "verbose" : [True, False],
               "freetype" : [True, False]
    }
    default_options = "shared=False","HDF5=False","install_data=False", "Wt=False", \
                "GDML=False","inventor=False","openGL=True","Qt=True","Win32=False",\
                "Motif=False", "multithreaded=True", "muonic_atoms=False", "verbose=True",\
                "freetype=True"
    generators = "cmake"

    requires = "zlib/1.2.11@conan/stable", "expat/2.2.5@bincrafters/stable"

    def requirements(self):
        if self.options.Qt:
            self.requires("qt/5.12.0@bincrafters/stable")
        if self.options.HDF5:
            self.requires("hdf5/1.10.3@arsen-studio/stable")
        if self.options.freetype:
            self.requires("freetype/2.9.0@bincrafters/stable")
    
    def source(self):
        tools.get("http://cern.ch/geant4-data/releases/geant4.%s.tar.gz" % self.version,
                  sha256=G4_10_05_SHA,
                  filename="geant4.%s.tar.gz" % self.version)

    def build(self):
        cmake = CMake(self)

        if self.settings.cppstd:
            cmake.definitions["GEANT4_BUILD_CXXSTD"] = str(self.settings.cppstd).strip("gnu")
        else:
            self.output.warn("no settings.cppstd set, building geant4 in default mode")

        cmake.definitions["GEANT4_USE_QT"] = self.options.Qt
        cmake.definitions["GEANT4_INSTALL_DATA"] = self.options.install_data
        cmake.definitions["GEANT4_USE_INVENTOR"] = self.options.inventor
        cmake.definitions["GEANT4_USE_HDF5"] = self.options.HDF5
        cmake.definitions["GEANT4_USE_GDML"] = self.options.GDML
        cmake.definitions["GEANT4_USE_WT"] = self.options.Wt
        cmake.definitions["GEANT4_BUILD_MULTITHREADED"] = self.options.multithreaded
        cmake.definitions["GEANT4_BUILD_MUONIC_ATOMS_IN_USE"] = self.options.muonic_atoms
        cmake.definitions["GEANT4_BUILD_VERBOSE_CODE"] = self.options.verbose
        cmake.definitions["GEANT4_USE_OPENGL_X11"] = self.options.openGL
        
        #disable using system libs (except CLHEP!!)
        cmake.definitions["GEANT4_USE_SYSTEM_EXPAT"] = True
        cmake.definitions["GEANT4_USE_SYSTEM_ZLIB"] = True

        #examples just take up space
        cmake.definitions["GEANT4_INSTALL_EXAMPLES"] = False
        
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



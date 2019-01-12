project(test_conan_geant4)
cmake_minimum_required(VERSION 3.2)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

#test finding geant4 via find_package
find_package(Geant4 REQUIRED)

add_executable(test_g4_find_package main.cpp)
target_link_libraries(test_g4_find_package PUBLIC ${Geant4_LIBRARIES})
target_inculde_directories(test_g4_find_package PUBLIC ${Geant4_INCLUDE_DIR})


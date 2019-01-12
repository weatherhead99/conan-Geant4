project(test_conan_geant4)
cmake_minimum_required(VERSION 3.2)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

#test finding geant4 via find_package
find_package(Geant4 REQUIRED)

if(Geant4_multithreaded_FOUND)
find_package(Threads REQUIRED)
endif()

add_executable(test_g4_find_package main.cpp)
target_link_libraries(test_g4_find_package PUBLIC ${Geant4_LIBRARIES})
target_include_directories(test_g4_find_package PUBLIC ${Geant4_INCLUDE_DIR})
target_compile_definitions(test_g4_find_package PUBLIC ${Geant4_DEFINITIONS})

if(Geant4_multithreaded_FOUND)
target_link_libraries(test_g4_find_package PUBLIC Threads::Threads)
endif()


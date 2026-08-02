cmake_minimum_required(VERSION 3.18)
project(_hetero_edge_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 CONFIG REQUIRED)

# C++ Header Include Paths
include_directories(csrc/include)

# C++ Source Files & Pybind11 Bindings
file(GLOB_RECURSE SOURCES "csrc/src/*.cpp")
list(APPEND SOURCES hetero_edge/bindings.cpp)

# Define Pybind11 Module
pybind11_add_module(_hetero_edge_cpp ${SOURCES})

# ----------------------------------------------------------------------
# CRITICAL: Tells scikit-build-core to copy the compiled C++ binary
# into the top-level Python package directory.
# ----------------------------------------------------------------------
install(TARGETS _hetero_edge_cpp DESTINATION .)
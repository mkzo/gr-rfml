INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_RFML rfml)

FIND_PATH(
    RFML_INCLUDE_DIRS
    NAMES rfml/api.h
    HINTS $ENV{RFML_DIR}/include
        ${PC_RFML_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    RFML_LIBRARIES
    NAMES gnuradio-rfml
    HINTS $ENV{RFML_DIR}/lib
        ${PC_RFML_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/rfmlTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(RFML DEFAULT_MSG RFML_LIBRARIES RFML_INCLUDE_DIRS)
MARK_AS_ADVANCED(RFML_LIBRARIES RFML_INCLUDE_DIRS)

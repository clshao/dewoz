INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_WIZI_DET wizi_det)

FIND_PATH(
    WIZI_DET_INCLUDE_DIRS
    NAMES wizi_det/api.h
    HINTS $ENV{WIZI_DET_DIR}/include
        ${PC_WIZI_DET_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    WIZI_DET_LIBRARIES
    NAMES gnuradio-wizi_det
    HINTS $ENV{WIZI_DET_DIR}/lib
        ${PC_WIZI_DET_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(WIZI_DET DEFAULT_MSG WIZI_DET_LIBRARIES WIZI_DET_INCLUDE_DIRS)
MARK_AS_ADVANCED(WIZI_DET_LIBRARIES WIZI_DET_INCLUDE_DIRS)


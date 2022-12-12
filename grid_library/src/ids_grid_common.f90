module ids_grid_common_light

  use iso_c_binding, only: DP => c_double
  use imas_coordinate_identifier

  implicit none

  integer, parameter :: GRID_UNDEFINED = 0

  ! Data representation definitions
  integer, parameter :: GEO_TYPE_STANDARD = 1
  character(*), parameter :: GEO_TYPE_ID_STANDARD = "Standard"
  integer, parameter :: GEO_TYPE_FOURIER = 2
  character(*), parameter :: GEO_TYPE_ID_FOURIER = "Fourier"

 ! Field aligned vector definitions
  integer, parameter :: VEC_ALIGN_DEFAULT = 1
  character(len=132), parameter :: VEC_ALIGN_DEFAULT_ID = "DEFAULT"

  integer, parameter :: VEC_ALIGN_POLOIDAL = 1001
  character(len=132), parameter :: VEC_ALIGN_POLOIDAL_ID = "Poloidal"
  integer, parameter :: VEC_ALIGN_RADIAL = 1002
  character(len=132), parameter :: VEC_ALIGN_RADIAL_ID = "Radial"
  integer, parameter :: VEC_ALIGN_PARALLEL = 1003
  character(len=132), parameter :: VEC_ALIGN_PARALLEL_ID = "Parallel"

  integer, parameter :: VEC_ALIGN_TOROIDAL = 1004
  character(len=132), parameter :: VEC_ALIGN_TOROIDAL_ID = "Toroidal"


  integer, parameter :: LIST_COORDINATES(27)=(/ &
        0, 1, 2, 4, 5, 6, 7, 8, 107, 109, 110, 111, 112, 113, 114, 115, 116 , &
        117, 118, 119, 120, 121, 122, 123, 124, 125, 126 /)

end module ids_grid_common_light

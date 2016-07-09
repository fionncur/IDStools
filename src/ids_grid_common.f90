module ids_grid_common

  use iso_c_binding, only: DP => c_double

  implicit none

  !> unspecified
  integer, parameter :: COORDTYPE_unspecified = 0

  !> First cartesian coordinate in the horizontal plane [m]
  integer, parameter :: COORDTYPE_X = 1

  !> Second cartesian coordinate in the horizontal plane (grad(X) x grad(Y) = grad(Z)) [m]
  integer, parameter :: COORDTYPE_Y = 2

  !> Major radius [m]
  integer, parameter :: COORDTYPE_R = 4

  !> Vertical position Z [m]
  integer, parameter :: COORDTYPE_Z = 5

  !> Toroidal angle [rad]
  integer, parameter :: COORDTYPE_phi = 6

  !> Poloidal magnetic flux [T*m^2]
  integer, parameter :: COORDTYPE_psi = 7

  !> Geometrical poloidal angle
  integer, parameter :: COORDTYPE_theta = 8

  !> The square root of the toroidal flux, sqrt((Phi-Phi_axis)/pi/B0) [m]
  integer, parameter :: COORDTYPE_rho_tor = 107

  !> Straight field line poloidal angle [rad]
  integer, parameter :: COORDTYPE_theta_b = 109

  !> Velocity component in the x-direction [m/s]
  integer, parameter :: COORDTYPE_vx = 110

  !> Velocity component in the z-direction [m/s]
  integer, parameter :: COORDTYPE_vy = 111

  !> Velocity component in the z-direction [m/s]
  integer, parameter :: COORDTYPE_vz = 112

  !> Magnitude of the velocity [m/s]
  integer, parameter :: COORDTYPE_vel = 113

  !> Velocity component in the toroidal direction [m/s]
  integer, parameter :: COORDTYPE_vphi = 114

  !> Velocity component parallel to the magnetic field [m/s]
  integer, parameter :: COORDTYPE_vpar = 115

  !> Velocity perpendicular to the magnetic field [m/s]
  integer, parameter :: COORDTYPE_vperp = 116

  !> Hamiltonian energy [eV]
  integer, parameter :: COORDTYPE_E = 117

  !> Canonical toroidal angular momentum [kg m**2/s]
  integer, parameter :: COORDTYPE_pphi = 118

  !> magnetic moment [J/T]
  integer, parameter :: COORDTYPE_mu = 119

  !> mu/E [1/T]
  integer, parameter :: COORDTYPE_Lambda = 120

  !> vpar/v [1]
  integer, parameter :: COORDTYPE_pitch = 121

  !> Velocity normalised to the local thermal velocity of the thermal ions (of the relevant species)
  integer, parameter :: COORDTYPE_vel_thermal = 122

  !> Modulus of the relativistic momentum vector
  integer, parameter :: COORDTYPE_momentum = 123

  !> Component of the relativistic momentum vector parallel to the magnetic field
  integer, parameter :: COORDTYPE_parallel_momentum = 124

  !> Component of the relativistic momentum vector perpendicular to the magnetic field
  integer, parameter :: COORDTYPE_perpendicular_momentum = 125

  !> Pitch, i.e. ratio between the parallel over the perpendicular velocity, at the minimum value of the magnetic field strength...
  !> ...along the guiding centre orbit
  integer, parameter :: COORDTYPE_xi_at_min_B = 126

  integer, parameter :: LIST_COORDINATES(27)=(/ &
        0, 1, 2, 4, 5, 6, 7, 8, 107, 109, 110, 111, 112, 113, 114, 115, 116 , &
        117, 118, 119, 120, 121, 122, 123, 124, 125, 126 /)

end module ids_grid_common

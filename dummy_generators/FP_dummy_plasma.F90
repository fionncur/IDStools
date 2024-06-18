include 'mathematical_constants.f90'  ! Excellent math constant lives here
include 'codata_2018.f90'      ! Recommended physical constants since 2018

  program FP_dummy_plasma

!
! This program is intended to create a dummy plasma for FP synthetic diagnostics
!
! It takes as arguments the shot and run numbers, and, optionally, the parameters file
!
! If the parameters file is not present, the file 'FP_parameters.dat' is used.
!
! It takes as input, through an ASCII namelist in the FP_parameters.dat file:
!  - The location of the plasma, as R0 and Z0 (in meters)
!  - The radius of the plasma, as R_plasma (in meters)
!  - The peak electron and ion temperatures (in eV)
!  - The peak electron density (in m-3)
!  - A list of impurity species with their concentrations
!
! An example of such a namelist is:
! &FP_PARAMETERS
!  R0=6.2, Z0=0.0, RADIUS=1.0,
!  TE_MAX=400.0, TI_MAX=50.0, NE_MAX=1.0e19,
!  N_IMP_SPECIES=3,
!  IMPURITIES='Fe','C','O',
!  IMP_CONC=0.001,0.02,0.01,
! /
!
! It imports a standard wall IDS and limits the plasma radius if chosen so large
! that it intersects the wall
!
! It exports an IDS containing a minimal description to serve as a dummy target plasma,
! consisting of the core_profiles, equilibrium, summary, and wall IDSs
!
! Profiles will be assumed to be parabolic from the given maxima
!
! Compilation instructions for this program are:
! ifort -c `pkg-config imas-ifort amns --cflags` -o FP_dummy_plasma.o FP_dummy_plasma.F90
! ifort -o FP_dummy_plasma FP_dummy_plasma.o `pkg-config imas-ifort amns --libs`
!
!
  use ids_schemas
  use amns_types
  use amns_module
  use mathematical_constants, only: pi => m_pi
  use codata, only: amu => atomic_mass_constant
  use codata, only: me => electron_mass
  use codata, only: mp => proton_mass

  implicit none

  type (ids_summary) :: summary
  type (ids_equilibrium) :: equilibrium
  type (ids_core_profiles) :: core_profiles
  type (ids_wall) :: wall
  type (amns_handle_type) :: amns

  !! Local variables
  real(IDS_real) :: time_slice_value, time_step
  character(len=24) :: shot_string
  character(len=24) :: run_string
  character(len=24) :: argName, hlp_frm
  integer narg, cptArg, idx, status, shot, run, idxmd
  integer time_sind, num_time_slices, homogeneous_time
  character username*24, database*24, treename*24, version*24
  character imas_version*132, al_version*132, code_commit*132
  character systemarg*512
  character*8 date
  character*10 ctime
  character*5 zone
  integer tvalues(8)
  character*132 create_date, source, comment, string
  character*256 filename
  logical file_ok

  integer i, j, k, nc, mi
  integer n_imp_species
  character*2 impurities(92)
  real(IDS_real) :: R0, Z0, radius, Te_max, Ti_max, ne_max
  real(IDS_real) :: imp_conc(92), total_concentration
  real(IDS_real), allocatable :: coronal_density(:)
  integer, parameter :: N_TL = 19, N_DRS = 4, N_1D = 51
  real(IDS_real), parameter :: T_min = 1.0_IDS_real, ne_min = 1.0e8_IDS_real
  real(IDS_real) :: R_TL(N_TL), Z_TL(N_TL), R_DRS(N_DRS), Z_DRS(N_DRS)
  real(IDS_real) :: distance, closest, R_cl, Z_cl, R_lim, Z_lim
  real(IDS_real), allocatable :: density_sum(:)
  logical outside, intersect

! Reference contour for First Plasma Protection Components (FPPC)
! from IDM document ITER_D_5MKSSF
! Here we use the OT (Operating Temperature: 100 C) contour
! TL: Toroidal Limiter
! DRS: Divertor Replacement Sector

  data R_TL / 4.0852632   , 4.0852632  , 4.0852632  , 4.0852632  , 4.0852362   , &
    &         4.0852632   , 4.105340474, 4.307239623, 4.93172786 , 5.762083707 , &
    &         6.565134042 , 7.416531105, 7.923580299, 8.289163514, 8.413938512 , &
    &         8.325376904 , 7.91777713 , 7.29719206 , 6.27607607 /
  data Z_TL /-2.51524048  ,-1.50293629 ,-0.48762823 , 0.52868112 , 1.54499047  , &
    &         2.560496394 , 3.576406477, 4.338347497, 4.729420462, 4.541396188 , &
    &         3.929548314 , 3.181563866, 2.463244175, 1.678700584, 0.6241505981, &
    &        -0.4365759557,-1.358455938,-2.279778345,-3.070767305/
  data R_DRS/ 6.770665357 , 5.781724115, 4.829958467, 4.0852632  /
  data Z_DRS/-2.687642695 ,-2.603764794,-2.412754135,-2.172970445/

  integer, save :: nuclear_mass(92)
  data nuclear_mass /   1,   4,   7,   9,  11,  12,  14,  16,  18,  20, &
                   &   23,  24,  27,  28,  31,  32,  35,  40,  39,  40, &
                   &   45,  48,  51,  52,  55,  56,  59,  58,  63,  64, &
                   &   70,  73,  75,  80,  80,  84,  85,  88,  89,  90, &
                   &   93,  96,  98, 100, 103, 106, 108, 112, 115, 118, &
                   &  122, 128, 127, 132, 133, 138, 139, 140, 141, 144, &
                   &  145, 152, 152, 156, 159, 162, 165, 167, 169, 174, &
                   &  175, 180, 181, 184, 187, 192, 193, 195, 197, 200, &
                   &  205, 208, 209, 209, 210, 222, 223, 226, 227, 232, &
                   &  231, 238/

  namelist /FP_parameters/ R0, Z0, radius, Te_max, Ti_max, ne_max, &
    &  n_imp_species, impurities, imp_conc

  !! Set default value for IMAS major version and IDS treename
  status = 0
  version = '3'
  treename = 'ids'
  database = 'iter'
  call getenv ('USER', username)
  call getenv ('AL_VERSION', al_version)
  call getenv ('IMAS_VERSION', imas_version)
  call getenv ('EBVERSIONIDSTOOLS', code_commit)
  call date_and_time (date, ctime, zone, tvalues)
  call IMAS_AMNS_SETUP(amns)
  create_date = date//' '//ctime//' '//' '//zone
  comment = "Dummy circular plasma"
  source = "FP_dummy_plasma"

  narg = command_argument_count()
  if (narg.eq.0) then
    write(0,*) 'Call syntax:'
    write(0,*) '  --shot,-s shot_number '
    write(0,*) '  --run,-r run_number '
    write(0,*) '  --username,-u user_name (optional, default is '//trim(username)//')'
    write(0,*) '  --database,-d database (optional, default is '//trim(database)//')'
    write(0,*) '  --version,-v version (optional, default is '//trim(version)//')'
    write(0,*) 'and an additional (optional) last argument specifying the parameters file'
    write(0,*) 'The default parameters filename is "FP_parameters.dat"'
    stop
  end if
  do cptArg = 1, narg
    call get_command_argument( cptArg, argName )
    select case( adjustl( argName ) )
      case("--shot","-s")
        call get_command_argument( cptArg + 1, shot_string )
        !! Transform dummy string variable to integer
        read( shot_string, *) shot
      case("--run","-r")
        call get_command_argument( cptArg + 1, run_string )
        !! Transform dummy string variable to integer
        read( run_string, *) run
      case("--username","-u")
        call get_command_argument( cptArg + 1, username )
      case("--database","-d")
        call get_command_argument( cptArg + 1, database )
      case("--version","-v")
        call get_command_argument( cptArg + 1, version )
      case default
        call get_command_argument( cptArg, filename )
    end select
  end do
  if ( mod(narg,2).eq.0 ) then
    write(0,*) 'Using default FP_parameters.dat file'
    filename = 'FP_parameters.dat'
  end if

  if ( 0.ge.shot .or. shot.ge.214748) stop 'Invalid shot number !'
  if ( 0.gt.run .or. run.gt.99999) stop 'Invalid run number !'
  if ( streql(username,' ') ) stop 'User name not defined !'
  if ( streql(database,' ') ) stop 'Database not defined !'

  inquire(file=trim(filename),exist=file_ok)
  if (.not.file_ok) then
    write(0,*) 'Parameters file '//trim(filename)//' is missing'
    stop 'Parameters file not found !'
  end if
  n_imp_species=0
  imp_conc=0.0_IDS_real
  open(99,file=trim(filename),iostat=status)
  if (status.ne.0) stop 'Cannot open parameters file !'
  read(99,FP_parameters,iostat=status)
  if (status.ne.0) stop 'Error reading parameters file !'
  close(99)

  if ( R0.lt.0.0_IDS_real ) stop 'Invalid R0 value !'
  if ( radius.le.0.0_IDS_real ) stop 'Invalid radius value !'
  if ( Te_max.le.0.0_IDS_real ) stop 'Invalid Te_max value !'
  if ( Ti_max.le.0.0_IDS_real ) stop 'Invalid Ti_max value !'
  if ( ne_max.le.0.0_IDS_real ) stop 'Invalid ni_max value !'
  if ( n_imp_species.gt.0) then
    if ( minval(imp_conc(1:n_imp_species)).lt.0.0_IDS_real ) &
      &  stop 'Invalid impurity concentrations !'
  end if

  outside = .false.
  intersect = .false.
  closest = huge(1.0_IDS_real)
  do i = 1, N_TL-1
    outside = outside .or. &
      &  0.0_IDS_real .gt. ( (R0 - R_TL(I))*(Z_TL(I+1) - Z_TL(I)) - &
      &                      (Z0 - Z_TL(I))*(R_TL(I+1) - R_TL(I)) )
    distance = ( (R0 - R_TL(I))*(Z_TL(I+1) - Z_TL(I)) - &
      &          (Z0 - Z_TL(I))*(R_TL(I+1) - R_TL(I)) ) / &
      &   sqrt ( (R_TL(I+1) - R_TL(I))**2 + (Z_TL(I+1) - Z_TL(I))**2 )
    R_cl = R_TL(I) + &
      &  ( ( R_TL(I+1) - R_TL(I) ) * ( R0 - R_TL(I) ) + &
      &    ( Z_TL(I+1) - Z_TL(I) ) * ( Z0 - Z_TL(I) ) ) / &
      &  ( ( R_TL(I+1) - R_TL(I) )**2 + ( Z_TL(I+1) - Z_TL(I) )**2 ) * &
      &    ( R_TL(I+1) - R_TL(I) )
    Z_cl = Z_TL(I) + &
      &  ( ( R_TL(I+1) - R_TL(I) ) * ( R0 - R_TL(I) ) + &
      &    ( Z_TL(I+1) - Z_TL(I) ) * ( Z0 - Z_TL(I) ) ) / &
      &  ( ( R_TL(I+1) - R_TL(I) )**2 + ( Z_TL(I+1) - Z_TL(I) )**2 ) * &
      &    ( Z_TL(I+1) - Z_TL(I) )
    if (distance.lt.radius) then
      intersect = .true.
      radius = distance
    end if
    if (distance.lt.closest) then
      if ((R_cl-R_TL(I))*(R_cl-R_TL(I+1)).lt.1.0e-6_IDS_real .and. &
        & (Z_cl-Z_TL(I))*(Z_cl-Z_TL(I+1)).lt.1.0e-6_IDS_real) then
        closest = distance
        R_lim = R_cl
        Z_lim = Z_cl
      end if
    end if
  end do
  do i = 1, N_DRS-1
    outside = outside .or. &
      &  0.0_IDS_real .gt. ( (R0 - R_DRS(I))*(Z_DRS(I+1) - Z_DRS(I)) - &
      &                      (Z0 - Z_DRS(I))*(R_DRS(I+1) - R_DRS(I)) )
    distance = ( (R0 - R_DRS(I))*(Z_DRS(I+1) - Z_DRS(I)) - &
      &          (Z0 - Z_DRS(I))*(R_DRS(I+1) - R_DRS(I)) ) / &
      &   sqrt ( (R_DRS(I+1) - R_DRS(I))**2 + (Z_DRS(I+1) - Z_DRS(I))**2 )
    R_cl = R_DRS(I) + &
      &  ( ( R_DRS(I+1) - R_DRS(I) ) * ( R0 - R_DRS(I) ) + &
      &    ( Z_DRS(I+1) - Z_DRS(I) ) * ( Z0 - Z_DRS(I) ) ) / &
      &  ( ( R_DRS(I+1) - R_DRS(I) )**2 + ( Z_DRS(I+1) - Z_DRS(I) )**2 ) * &
      &    ( R_DRS(I+1) - R_DRS(I) )
    Z_cl = Z_DRS(I) + &
      &  ( ( R_DRS(I+1) - R_DRS(I) ) * ( R0 - R_DRS(I) ) + &
      &    ( Z_DRS(I+1) - Z_DRS(I) ) * ( Z0 - Z_DRS(I) ) ) / &
      &  ( ( R_DRS(I+1) - R_DRS(I) )**2 + ( Z_DRS(I+1) - Z_DRS(I) )**2 ) * &
      &    ( Z_DRS(I+1) - Z_DRS(I) )
    if (distance.lt.radius) then
      intersect = .true.
      radius = distance
    end if
    if (distance.lt.closest) then
      if ((R_cl-R_DRS(I))*(R_cl-R_DRS(I+1)).lt.1.0e-6_IDS_real .and. &
        & (Z_cl-Z_DRS(I))*(Z_cl-Z_DRS(I+1)).lt.1.0e-6_IDS_real) then
        closest = distance
        R_lim = R_cl
        Z_lim = Z_cl
      end if
    end if
  end do
  if (outside) stop 'Plasma is outside the First Plasma Protection contour !'
  if (intersect) then
    write(0,*) 'Plasma radius intersects the First Wall !'
    write(0,*) 'Reducing radius to tangency distance...'
  end if

  write(0,'(a)') 'Creating a dummy FP circular plasma centered at :'
  write(0,'(a,f6.2,a,f6.2,a)') ' R0 = ',R0,' m and Z0 = ',Z0,' m'
  write(0,'(a,f6.2,a)') ' of radius ',radius,' m'
  write(0,'(a)') 'Central parameters are :'
  write(0,'(a,f7.2,a,f7.2,a,1p,1e11.4,a)') &
   & ' Te = ',Te_max,' eV, Ti = ',Ti_max,' eV, and ne = ',ne_max,' m-3'
  if (n_imp_species.gt.0) then
    write(hlp_frm,'(a,i2,a)') '(',n_imp_species,'(a2,a,f6.2,a))'
    write(0,*) 'Impurity content is :'
    write(0,hlp_frm) &
      &  (impurities(i),' ',imp_conc(i)*100.0_IDS_real,' %, ',i=1,n_imp_species-1), &
      &   impurities(n_imp_species),' ',imp_conc(n_imp_species)*100.0_IDS_real,' %'
  else
    write(0,*) 'Plasma is assumed pure H'
  end if

  write(*,'(a,i8,a,i8,4a)') 'Writing data in IDS shot: ', shot, ' Run: ', run, &
     & ' User: ', trim(username), ' Database: ', trim(database)

  call imas_open_env(treename, shot, run, idx, username, database, version, status)
  if (status.ne.0) then
    write (0,*) 'Cannot open IDS file, will create a new one.'
    call imas_create_env( treename, shot, run, 0, 0, idx, username, &
             & database, version, status )
    if (status.ne.0) stop 'Error opening IMAS database !'
  end if

  homogeneous_time = 1
  time_sind = 1
  time_slice_value = 0.0_IDS_real
  time_step = IDS_REAL_INVALID
  num_time_slices = 1

  ! Import wall IDS from MD database
  call imas_open_env(treename, 116612, 1, idxmd, 'public', 'ITER_MD', version, status)
  if (status.ne.0) stop 'Error opening IMAS database !'
  call ids_get(idxmd, 'wall', wall, status)
  if (status.ne.0) stop 'Error reading wall IDS !'
  call imas_close(idxmd, status)
  if (status.ne.0) stop 'Error closing IMAS database !'
  call ids_put(idx, 'wall', wall, status)
  if (status.ne.0) stop 'Error saving wall IDS !'
  call ids_deallocate( wall )

  call write_ids_properties( core_profiles%ids_properties, &
   &  homogeneous_time, comment, source, create_date )
  call write_ids_properties( equilibrium%ids_properties, &
   &  homogeneous_time, comment, source, create_date )
  call write_ids_properties( summary%ids_properties, &
   &  homogeneous_time, comment, source, create_date )

  call write_ids_code( core_profiles%code, code_commit )
  call write_ids_code( equilibrium%code, code_commit )
  call write_ids_code( summary%code, code_commit )

  allocate( core_profiles%time(num_time_slices) )
  core_profiles%time(time_sind) = time_slice_value
  allocate( equilibrium%time(num_time_slices) )
  equilibrium%time(time_sind) = time_slice_value
  allocate( summary%time(num_time_slices) )
  summary%time(time_sind) = time_slice_value

  allocate( core_profiles%profiles_1d( num_time_slices ) )
  allocate( core_profiles%profiles_1d( time_sind )%grid%rho_tor_norm(N_1D) )
  allocate( core_profiles%profiles_1d( time_sind )%grid%volume(N_1D) )
  allocate( core_profiles%profiles_1d( time_sind )%grid%area(N_1D) )
  allocate( core_profiles%profiles_1d( time_sind )%grid%surface(N_1D) )
  allocate( core_profiles%profiles_1d( time_sind )%electrons%temperature(N_1D) )
  allocate( core_profiles%profiles_1d( time_sind )%electrons%density(N_1D) )
  allocate( core_profiles%profiles_1d( time_sind )%t_i_average(N_1D) )
  allocate( core_profiles%profiles_1d( time_sind )%n_i_total_over_n_e(N_1D) )
  allocate( core_profiles%profiles_1d( time_sind )%zeff(N_1D) )
  allocate( core_profiles%profiles_1d( time_sind )%ion(1+n_imp_species) )
  allocate( core_profiles%profiles_1d( time_sind )%neutral(1+n_imp_species) )
  do j = 1, 1+n_imp_species
    allocate( core_profiles%profiles_1d( time_sind )%ion(j)%element(1) )
    allocate( core_profiles%profiles_1d( time_sind )%ion(j)%label(1) )
    allocate( core_profiles%profiles_1d( time_sind )%neutral(j)%element(1) )
    allocate( core_profiles%profiles_1d( time_sind )%neutral(j)%label(1) )
    if (j.eq.1) then
      core_profiles%profiles_1d( time_sind )%ion(j)%label = 'H'
      core_profiles%profiles_1d( time_sind )%ion(j)%element(1)%a = 1.0_IDS_real
      core_profiles%profiles_1d( time_sind )%ion(j)%element(1)%z_n = 1.0_IDS_real
      core_profiles%profiles_1d( time_sind )%ion(j)%element(1)%atoms_n = 1
      core_profiles%profiles_1d( time_sind )%neutral(j)%label = 'H'
      core_profiles%profiles_1d( time_sind )%neutral(j)%element(1)%a = 1.0_IDS_real
      core_profiles%profiles_1d( time_sind )%neutral(j)%element(1)%z_n = 1.0_IDS_real
      core_profiles%profiles_1d( time_sind )%neutral(j)%element(1)%atoms_n = 1
      nc = 1
    else
      core_profiles%profiles_1d( time_sind )%ion(j)%label = impurities(j-1)
      core_profiles%profiles_1d( time_sind )%neutral(j)%label = impurities(j-1)
      nc = get_atomic_number( impurities(j-1) )
      if (nc.ne.1) then
        core_profiles%profiles_1d( time_sind )%ion(j)%element(1)%a = real(nuclear_mass(nc))
        core_profiles%profiles_1d( time_sind )%neutral(j)%element(1)%a = real(nuclear_mass(nc))
      else if (streql(impurities(j-1),'D')) then
        core_profiles%profiles_1d( time_sind )%ion(j)%element(1)%a = 2.0_IDS_real
        core_profiles%profiles_1d( time_sind )%neutral(j)%element(1)%a = 2.0_IDS_real
      else if (streql(impurities(j-1),'T')) then
        core_profiles%profiles_1d( time_sind )%ion(j)%element(1)%a = 3.0_IDS_real
        core_profiles%profiles_1d( time_sind )%neutral(j)%element(1)%a = 3.0_IDS_real
      end if
      core_profiles%profiles_1d( time_sind )%ion(j)%element(1)%z_n = real(nc)
      core_profiles%profiles_1d( time_sind )%ion(j)%element(1)%atoms_n = 1
      core_profiles%profiles_1d( time_sind )%neutral(j)%element(1)%z_n = real(nc)
      core_profiles%profiles_1d( time_sind )%neutral(j)%element(1)%atoms_n = 1
      if ( nc.eq.0 ) then
        write(0,*) ' Did not find a species match for ',impurities(j-1)
        stop 'Impurity not recognized !'
      end if
    end if
    core_profiles%profiles_1d( time_sind )%ion(j)%neutral_index = j
    core_profiles%profiles_1d( time_sind )%neutral(j)%ion_index = j
    core_profiles%profiles_1d( time_sind )%ion(j)%multiple_states_flag = 1
    core_profiles%profiles_1d( time_sind )%neutral(j)%multiple_states_flag = 0
    allocate( core_profiles%profiles_1d( time_sind )%ion(j)%z_ion_1d(N_1D) )
    allocate( core_profiles%profiles_1d( time_sind )%ion(j)%z_ion_square_1d(N_1D) )
    allocate( core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
    allocate( core_profiles%profiles_1d( time_sind )%ion(j)%state(nc) )
    allocate( core_profiles%profiles_1d( time_sind )%neutral(j)%density(N_1D) )
    do k = 1, nc
      core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%z_min = real(k)
      core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%z_max = real(k)
      core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%z_average = real(k)
      core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%z_square_average = real(k**2)
      allocate( core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%z_average_1d(N_1D) )
      core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%z_average_1d(1:N_1D) = real(k)
      allocate( core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%z_average_square_1d(N_1D) )
      core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%z_average_square_1d(1:N_1D) = real(k**2)
      allocate( core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%label(1) )
      if (j.eq.1) then
        string = 'H+'
      else if (k.eq.1) then
        write(string,'(a,a)') trim(impurities(j-1)),'+'
      else if (k.lt.10) then
        write(string,'(a,a,i1)') trim(impurities(j-1)),'+',k
      else
        write(string,'(a,a,i2)') trim(impurities(j-1)),'+',k
      end if
      core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%label = string
      allocate( core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%density(N_1D) )
    end do
  end do
  do i = 1, N_1D
    core_profiles%profiles_1d( time_sind )%grid%rho_tor_norm(i) = rratio(i-1,N_1D-1)
    core_profiles%profiles_1d( time_sind )%grid%volume(i) = &
       &  2.0_IDS_real*pi*R0*pi* &
       &  ( radius*rratio(i-1,N_1D-1) )**2
    core_profiles%profiles_1d( time_sind )%grid%area(i) = pi* &
       &  ( radius*rratio(i-1,N_1D-1) )**2
    core_profiles%profiles_1d( time_sind )%grid%surface(i) = &
       &  2.0_IDS_real*pi*R0*pi* &
       &  ( radius*rratio(i-1,N_1D-1) )
    core_profiles%profiles_1d( time_sind )%electrons%temperature(i) = max(T_min, &
       &  Te_max*( 1.0_IDS_real - rratio(i-1,N_1D-1)**2 ) )
    core_profiles%profiles_1d( time_sind )%electrons%density(i) = max(ne_min, &
       &  ne_max*( 1.0_IDS_real - rratio(i-1,N_1D-1)**2 ) )
    do j = 1, 1+n_imp_species
      core_profiles%profiles_1d( time_sind )%t_i_average(i) = max(T_min, &
       &  Ti_max*( 1.0_IDS_real - rratio(i-1,N_1D-1)**2 ) )
      if (j.eq.1) then
        nc = 1
        if (n_imp_species.eq.0) then
          total_concentration = 1.0_IDS_real
        else
          total_concentration = 1.0_IDS_real - sum(imp_conc(1:n_imp_species))
        end if
      else
        nc = get_atomic_number( impurities(j-1) )
        total_concentration = imp_conc(j-1)
      end if
      allocate( coronal_density(0:nc) )
      mi = nint(core_profiles%profiles_1d( time_sind )%ion(j)%element(1)%a)
      call get_coronal_distribution( nc, mi, &
         &  core_profiles%profiles_1d( time_sind )%electrons%temperature(i), &
         &  core_profiles%profiles_1d( time_sind )%electrons%density(i), &
         &  total_concentration, coronal_density )
      core_profiles%profiles_1d( time_sind )%neutral(j)%density(i) = coronal_density(0)
      do k = 1, nc
        core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%density(i) = coronal_density(k)
      end do
      deallocate( coronal_density )
      if (j.eq.1 .and. n_imp_species.gt.0) then
        core_profiles%profiles_1d( time_sind )%ion(j)%density(i) = &
          &  core_profiles%profiles_1d( time_sind )%electrons%density(i)* &
          &  ( 1.0_IDS_real - sum(imp_conc(1:n_imp_species)) )
      else if (j.eq.1 .and. n_imp_species.eq.0) then
        core_profiles%profiles_1d( time_sind )%ion(j)%density(i) = &
          &  core_profiles%profiles_1d( time_sind )%electrons%density(i)
      else
        allocate( density_sum( size( core_profiles%profiles_1d( time_sind )%ion(j)%state ) ) )
        do k = 1, size( density_sum )
          density_sum(k) = core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%density(i)
        end do
        core_profiles%profiles_1d( time_sind )%ion(j)%density(i) =  sum( density_sum )
        deallocate( density_sum )
      end if
      core_profiles%profiles_1d( time_sind )%ion(j)%z_ion_1d(i) = 0.0_IDS_real
      core_profiles%profiles_1d( time_sind )%ion(j)%z_ion_square_1d(i) = 0.0_IDS_real
      do k = 1, nc
        core_profiles%profiles_1d( time_sind )%ion(j)%z_ion_1d(i) = &
          &  core_profiles%profiles_1d( time_sind )%ion(j)%z_ion_1d(i) + &
          &  core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%density(i) * &
          &  core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%z_average
        core_profiles%profiles_1d( time_sind )%ion(j)%z_ion_square_1d(i) = &
          &  core_profiles%profiles_1d( time_sind )%ion(j)%z_ion_square_1d(i) + &
          &  core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%density(i) * &
          &  core_profiles%profiles_1d( time_sind )%ion(j)%state(k)%z_square_average
      end do
      core_profiles%profiles_1d( time_sind )%ion(j)%z_ion_1d(i) = &
          &  core_profiles%profiles_1d( time_sind )%ion(j)%z_ion_1d(i) / &
          &  core_profiles%profiles_1d( time_sind )%ion(j)%density(i)
      core_profiles%profiles_1d( time_sind )%ion(j)%z_ion_square_1d(i) = &
          &  core_profiles%profiles_1d( time_sind )%ion(j)%z_ion_square_1d(i) / &
          &  core_profiles%profiles_1d( time_sind )%ion(j)%density(i)
    end do
    allocate( density_sum( 1:n_imp_species+1 ) )
    do k = 1, n_imp_species+1
      density_sum( k ) = core_profiles%profiles_1d( time_sind )%ion( k )%density(i)
    end do
    core_profiles%profiles_1d( time_sind )%n_i_total_over_n_e(i) = &
      & sum(density_sum(1:n_imp_species+1) )/ &
      &     core_profiles%profiles_1d( time_sind )%electrons%density(i)
    deallocate( density_sum )
    core_profiles%profiles_1d( time_sind )%zeff(i) = &
      &   core_profiles%profiles_1d( time_sind )%ion(1)%z_ion_square_1d(i) * &
      &   core_profiles%profiles_1d( time_sind )%ion(1)%density(i)
    do j = 1, n_imp_species
      core_profiles%profiles_1d( time_sind )%zeff(i) = &
          &   core_profiles%profiles_1d( time_sind )%zeff(i) + &
          &   core_profiles%profiles_1d( time_sind )%ion(j+1)%z_ion_square_1d(i) * &
          &   core_profiles%profiles_1d( time_sind )%ion(j+1)%density(i)
    end do
    core_profiles%profiles_1d( time_sind )%zeff(i) = &
      &     core_profiles%profiles_1d( time_sind )%zeff(i) / &
      &     core_profiles%profiles_1d( time_sind )%electrons%density(i)
  end do

  allocate( equilibrium%time_slice( num_time_slices ) )
  equilibrium%time_slice( time_sind )%boundary_separatrix%psi = 0.0_IDS_real
  equilibrium%time_slice( time_sind )%boundary_separatrix%geometric_axis%r = R0
  equilibrium%time_slice( time_sind )%boundary_separatrix%geometric_axis%z = Z0
  equilibrium%time_slice( time_sind )%boundary_separatrix%minor_radius = radius
  equilibrium%time_slice( time_sind )%boundary_separatrix%elongation = 1.0_IDS_real
  equilibrium%time_slice( time_sind )%boundary_separatrix%elongation_upper = 1.0_IDS_real
  equilibrium%time_slice( time_sind )%boundary_separatrix%elongation_lower = 1.0_IDS_real
  equilibrium%time_slice( time_sind )%boundary_separatrix%triangularity = 0.0_IDS_real
  equilibrium%time_slice( time_sind )%boundary_separatrix%triangularity_upper = 0.0_IDS_real
  equilibrium%time_slice( time_sind )%boundary_separatrix%triangularity_lower = 0.0_IDS_real
  equilibrium%time_slice( time_sind )%boundary_separatrix%closest_wall_point%r = R_cl
  equilibrium%time_slice( time_sind )%boundary_separatrix%closest_wall_point%z = Z_cl
  equilibrium%time_slice( time_sind )%boundary_separatrix%closest_wall_point%distance = closest - radius
  equilibrium%time_slice( time_sind )%boundary_separatrix%dr_dz_zero_point%r = R0 + radius
  equilibrium%time_slice( time_sind )%boundary_separatrix%dr_dz_zero_point%z = Z0
  if (intersect) then
    equilibrium%time_slice( time_sind )%boundary_separatrix%type = 0
    equilibrium%time_slice( time_sind )%boundary_separatrix%active_limiter_point%r = R_cl
    equilibrium%time_slice( time_sind )%boundary_separatrix%active_limiter_point%z = Z_cl
  end if
  allocate( equilibrium%time_slice( time_sind )%boundary_separatrix%outline%r(N_1D) )
  allocate( equilibrium%time_slice( time_sind )%boundary_separatrix%outline%z(N_1D) )
  do i = 1, N_1D
    equilibrium%time_slice( time_sind )%boundary_separatrix%outline%r(i) = R0 + &
       & radius*cos( 2.0_IDS_real*pi*rratio(i,N_1D) )
    equilibrium%time_slice( time_sind )%boundary_separatrix%outline%z(i) = Z0 + &
       & radius*sin( 2.0_IDS_real*pi*rratio(i,N_1D) )
  end do
  equilibrium%time_slice( time_sind )%global_quantities%volume = &
       & 2.0_IDS_real*pi*R0*pi*radius**2
  equilibrium%time_slice( time_sind )%global_quantities%area = &
       & pi*radius**2
  equilibrium%time_slice( time_sind )%global_quantities%surface = &
       & 2.0_IDS_real*pi*R0*pi*radius
  equilibrium%time_slice( time_sind )%global_quantities%length_pol = &
       & pi*radius
  equilibrium%time_slice( time_sind )%global_quantities%psi_boundary = 0.0_IDS_real
  equilibrium%time_slice( time_sind )%global_quantities%magnetic_axis%r = R0
  equilibrium%time_slice( time_sind )%global_quantities%magnetic_axis%z = Z0
  equilibrium%time_slice( time_sind )%global_quantities%current_centre%r = R0
  equilibrium%time_slice( time_sind )%global_quantities%current_centre%z = Z0
  equilibrium%time_slice( time_sind )%convergence%iterations_n = 0
  equilibrium%time_slice( time_sind )%time = time_slice_value
  allocate( equilibrium%time_slice( time_sind )%profiles_1d%r_inboard(N_1D) )
  allocate( equilibrium%time_slice( time_sind )%profiles_1d%r_outboard(N_1D) )
  allocate( equilibrium%time_slice( time_sind )%profiles_1d%rho_tor_norm(N_1D) )
  allocate( equilibrium%time_slice( time_sind )%profiles_1d%geometric_axis%r(N_1D) )
  allocate( equilibrium%time_slice( time_sind )%profiles_1d%geometric_axis%z(N_1D) )
  allocate( equilibrium%time_slice( time_sind )%profiles_1d%elongation(N_1D) )
  allocate( equilibrium%time_slice( time_sind )%profiles_1d%triangularity_upper(N_1D) )
  allocate( equilibrium%time_slice( time_sind )%profiles_1d%triangularity_lower(N_1D) )
  allocate( equilibrium%time_slice( time_sind )%profiles_1d%area(N_1D) )
  allocate( equilibrium%time_slice( time_sind )%profiles_1d%surface(N_1D) )
  allocate( equilibrium%time_slice( time_sind )%profiles_1d%volume(N_1D) )
  allocate( equilibrium%time_slice( time_sind )%profiles_1d%rho_volume_norm(N_1D) )
  allocate( equilibrium%time_slice( time_sind )%profiles_1d%mass_density(N_1D) )
  do i = 1, N_1D
    equilibrium%time_slice( time_sind )%profiles_1d%r_inboard(i) = R0 - &
      & ( radius*rratio(i-1,N_1D-1) )
    equilibrium%time_slice( time_sind )%profiles_1d%r_outboard(i) = R0 + &
      & ( radius*rratio(i-1,N_1D-1) )
    equilibrium%time_slice( time_sind )%profiles_1d%rho_tor_norm(i) = rratio(i-1,N_1D-1)
    equilibrium%time_slice( time_sind )%profiles_1d%geometric_axis%r(i) = R0
    equilibrium%time_slice( time_sind )%profiles_1d%geometric_axis%z(i) = Z0
    equilibrium%time_slice( time_sind )%profiles_1d%elongation(i) = 1.0_IDS_real
    equilibrium%time_slice( time_sind )%profiles_1d%triangularity_upper(i) = 0.0_IDS_real
    equilibrium%time_slice( time_sind )%profiles_1d%triangularity_lower(i) = 0.0_IDS_real
    equilibrium%time_slice( time_sind )%profiles_1d%area(i) = &
      &  core_profiles%profiles_1d( time_sind )%grid%area(i)
    equilibrium%time_slice( time_sind )%profiles_1d%surface(i) = &
      &  core_profiles%profiles_1d( time_sind )%grid%surface(i)
    equilibrium%time_slice( time_sind )%profiles_1d%volume(i) = &
      &  core_profiles%profiles_1d( time_sind )%grid%volume(i)
    equilibrium%time_slice( time_sind )%profiles_1d%rho_volume_norm(i) = rratio(i-1,N_1D-1)
    equilibrium%time_slice( time_sind )%profiles_1d%mass_density(i) = &
      & (core_profiles%profiles_1d( time_sind )%ion(1)%density(i) + &
      &  core_profiles%profiles_1d( time_sind )%neutral(1)%density(i))* &
      &  mp + &
      &  core_profiles%profiles_1d( time_sind )%electrons%density(i)* &
      &  me
    do j = 1, n_imp_species
      equilibrium%time_slice( time_sind )%profiles_1d%mass_density(i) = &
         &  equilibrium%time_slice( time_sind )%profiles_1d%mass_density(i) + &
         & (core_profiles%profiles_1d( time_sind )%ion(j+1)%density(i)* &
         &  core_profiles%profiles_1d( time_sind )%ion(j+1)%element(1)%a + &
         &  core_profiles%profiles_1d( time_sind )%neutral(j+1)%density(i)* &
         &  core_profiles%profiles_1d( time_sind )%neutral(j+1)%element(1)%a)* &
         &  amu
    end do
  end do

  string = 'First Plasma circular dummy'
  call write_sourced_string( summary%configuration, string )
  call write_ids_midplane( summary%midplane, 1 )
  call write_sourced_time_value( summary%global_quantities%volume, &
    &  equilibrium%time_slice( time_sind )%global_quantities%volume )
  call write_sourced_constant( summary%global_quantities%r0, R0 )
  allocate( summary%local%magnetic_axis%position%rho_tor_norm( num_time_slices ) )
  allocate( summary%local%magnetic_axis%position%r( num_time_slices ) )
  allocate( summary%local%magnetic_axis%position%z( num_time_slices ) )
  summary%local%magnetic_axis%position%rho_tor_norm( time_sind ) = 0.0_IDS_real
  summary%local%magnetic_axis%position%r( time_sind ) = R0
  summary%local%magnetic_axis%position%z( time_sind ) = Z0
  call write_sourced_time_value( summary%local%magnetic_axis%t_e, Te_max )
  call write_sourced_time_value( summary%local%magnetic_axis%t_i_average, Ti_max )
  call write_sourced_time_value( summary%local%magnetic_axis%n_e, ne_max )
  allocate ( density_sum( n_imp_species+1 ) )
  do k = 1, n_imp_species+1
    density_sum(k) = core_profiles%profiles_1d( time_sind )%ion(k)%density(1)
  end do
  call write_sourced_time_value( summary%local%magnetic_axis%n_i_total, &
    &   sum( density_sum(:) ) )
  deallocate( density_sum )
  call write_sourced_time_value( summary%local%magnetic_axis%zeff, &
    &   core_profiles%profiles_1d( time_sind )%zeff(1) )
  call write_sourced_time_value2( summary%local%magnetic_axis%n_i%hydrogen, &
    &   core_profiles%profiles_1d( time_sind )%ion(1)%density(1) )
  allocate( summary%local%separatrix%position%rho_tor_norm( num_time_slices ) )
  summary%local%separatrix%position%rho_tor_norm( time_sind ) = 1.0_IDS_real
  call write_sourced_time_value( summary%local%separatrix%t_e, &
    &   core_profiles%profiles_1d( time_sind )%electrons%temperature(N_1D) )
  call write_sourced_time_value( summary%local%separatrix%t_i_average, &
    &   core_profiles%profiles_1d( time_sind )%t_i_average(N_1D) )
  call write_sourced_time_value( summary%local%separatrix%n_e, &
    &   core_profiles%profiles_1d( time_sind )%electrons%density(N_1D) )
  allocate ( density_sum( n_imp_species+1 ) )
  do k = 1, n_imp_species+1
    density_sum(k) = core_profiles%profiles_1d( time_sind )%ion(k)%density(N_1D)
  end do
  call write_sourced_time_value( summary%local%separatrix%n_i_total, &
    &   sum( density_sum(:) ) )
  call write_sourced_time_value( summary%local%separatrix%zeff, &
    &   core_profiles%profiles_1d( time_sind )%zeff(N_1D) )
  call write_sourced_time_value2( summary%local%separatrix%n_i%hydrogen, &
    &   core_profiles%profiles_1d( time_sind )%ion(1)%density(N_1D) )
  if (intersect) then
    call write_sourced_time_value( summary%local%limiter%t_e, &
      &   core_profiles%profiles_1d( time_sind )%electrons%temperature(N_1D) )
    call write_sourced_time_value( summary%local%limiter%t_i_average, &
      &   core_profiles%profiles_1d( time_sind )%t_i_average(N_1D) )
    call write_sourced_time_value( summary%local%limiter%n_e, &
      &   core_profiles%profiles_1d( time_sind )%electrons%density(N_1D) )
    call write_sourced_time_value( summary%local%limiter%n_i_total, &
      &   sum( density_sum(:) ) )
    call write_sourced_time_value( summary%local%limiter%zeff, &
      &   core_profiles%profiles_1d( time_sind )%zeff(N_1D) )
    call write_sourced_time_value2( summary%local%limiter%n_i%hydrogen, &
      &   core_profiles%profiles_1d( time_sind )%ion(1)%density(N_1D) )
  end if
  deallocate( density_sum )
  call write_sourced_time_integer( summary%boundary%type, 0 )
  call write_sourced_time_value( summary%boundary%geometric_axis_r, R0 )
  call write_sourced_time_value( summary%boundary%geometric_axis_z, Z0 )
  call write_sourced_time_value( summary%boundary%magnetic_axis_r, R0 )
  call write_sourced_time_value( summary%boundary%magnetic_axis_z, Z0 )
  call write_sourced_time_value( summary%boundary%minor_radius, radius )
  call write_sourced_time_value( summary%boundary%elongation, 1.0_IDS_real )
  call write_sourced_time_value( summary%boundary%triangularity_upper, 0.0_IDS_real )
  call write_sourced_time_value( summary%boundary%triangularity_lower, 0.0_IDS_real )
  call write_sourced_time_value( summary%boundary%gap_limiter_wall, closest - radius )
  do j = 1, n_imp_species
    select case ( trim(impurities(j)) )
    case( 'D' )
      call write_sourced_time_value2( summary%local%magnetic_axis%n_i%deuterium, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(1) )
      call write_sourced_time_value2( summary%local%separatrix%n_i%deuterium, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      if ( intersect ) then
        call write_sourced_time_value2( summary%local%limiter%n_i%deuterium, &
          &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      end if
    case( 'T' )
      call write_sourced_time_value2( summary%local%magnetic_axis%n_i%tritium, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(1) )
      call write_sourced_time_value2( summary%local%separatrix%n_i%tritium, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      if ( intersect ) then
        call write_sourced_time_value2( summary%local%limiter%n_i%tritium, &
          &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      end if
    case( 'He' )
      call write_sourced_time_value2( summary%local%magnetic_axis%n_i%helium_4, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(1) )
      call write_sourced_time_value2( summary%local%separatrix%n_i%helium_4, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      if ( intersect ) then
        call write_sourced_time_value2( summary%local%limiter%n_i%helium_4, &
          &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      end if
    case( 'Li' )
      call write_sourced_time_value2( summary%local%magnetic_axis%n_i%lithium, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(1) )
      call write_sourced_time_value2( summary%local%separatrix%n_i%lithium, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      if ( intersect ) then
        call write_sourced_time_value2( summary%local%limiter%n_i%lithium, &
          &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      end if
    case( 'Be' )
      call write_sourced_time_value2( summary%local%magnetic_axis%n_i%beryllium, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(1) )
      call write_sourced_time_value2( summary%local%separatrix%n_i%beryllium, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      if ( intersect ) then
        call write_sourced_time_value2( summary%local%limiter%n_i%beryllium, &
          &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      end if
    case( 'C' )
      call write_sourced_time_value2( summary%local%magnetic_axis%n_i%carbon, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(1) )
      call write_sourced_time_value2( summary%local%separatrix%n_i%carbon, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      if ( intersect ) then
        call write_sourced_time_value2( summary%local%limiter%n_i%carbon, &
          &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      end if
    case( 'N' )
      call write_sourced_time_value2( summary%local%magnetic_axis%n_i%nitrogen, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(1) )
      call write_sourced_time_value2( summary%local%separatrix%n_i%nitrogen, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      if ( intersect ) then
        call write_sourced_time_value2( summary%local%limiter%n_i%nitrogen, &
          &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      end if
    case( 'O' )
      call write_sourced_time_value2( summary%local%magnetic_axis%n_i%oxygen, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(1) )
      call write_sourced_time_value2( summary%local%separatrix%n_i%oxygen, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      if ( intersect ) then
        call write_sourced_time_value2( summary%local%limiter%n_i%oxygen, &
          &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      end if
    case( 'Ne' )
      call write_sourced_time_value2( summary%local%magnetic_axis%n_i%neon, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(1) )
      call write_sourced_time_value2( summary%local%separatrix%n_i%neon, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      if ( intersect ) then
        call write_sourced_time_value2( summary%local%limiter%n_i%neon, &
          &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      end if
    case( 'Ar' )
      call write_sourced_time_value2( summary%local%magnetic_axis%n_i%argon, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(1) )
      call write_sourced_time_value2( summary%local%separatrix%n_i%argon, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      if ( intersect ) then
        call write_sourced_time_value2( summary%local%limiter%n_i%argon, &
          &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      end if
    case( 'Fe' )
      call write_sourced_time_value2( summary%local%magnetic_axis%n_i%iron, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(1) )
      call write_sourced_time_value2( summary%local%separatrix%n_i%iron, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      if ( intersect ) then
        call write_sourced_time_value2( summary%local%limiter%n_i%iron, &
          &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      end if
    case( 'Kr' )
      call write_sourced_time_value2( summary%local%magnetic_axis%n_i%krypton, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(1) )
      call write_sourced_time_value2( summary%local%separatrix%n_i%krypton, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      if ( intersect ) then
        call write_sourced_time_value2( summary%local%limiter%n_i%krypton, &
          &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      end if
    case( 'Xe' )
      call write_sourced_time_value2( summary%local%magnetic_axis%n_i%xenon, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(1) )
      call write_sourced_time_value2( summary%local%separatrix%n_i%xenon, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      if ( intersect ) then
        call write_sourced_time_value2( summary%local%limiter%n_i%xenon, &
          &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      end if
    case( 'W' )
      call write_sourced_time_value2( summary%local%magnetic_axis%n_i%tungsten, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(1) )
      call write_sourced_time_value2( summary%local%separatrix%n_i%tungsten, &
        &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      if ( intersect ) then
        call write_sourced_time_value2( summary%local%limiter%n_i%tungsten, &
          &   core_profiles%profiles_1d( time_sind )%ion(j)%density(N_1D) )
      end if
    end select
  end do

! Put the synthetic data in the IDS
  call ids_put( idx, "core_profiles", core_profiles, status )
  if (status.ne.0) stop 'Error saving core_profiles IDS !'
  call ids_put( idx, "equilibrium", equilibrium, status )
  if (status.ne.0) stop 'Error saving equilibrium IDS !'
  call ids_put( idx, "summary", summary, status )
  if (status.ne.0) stop 'Error saving summary IDS !'

  call ids_deallocate( core_profiles )
  call ids_deallocate( equilibrium )
  call ids_deallocate( summary )

  call IMAS_AMNS_FINISH(amns)
  call imas_close(idx, status)
  if (status.ne.0) stop 'Error closing IMAS database !'

  stop

  contains

  subroutine write_ids_properties( properties, homo, &
    & comment, source, create_date)
    type(ids_ids_properties), intent(inout) :: properties
                !< Type of IDS data structure, designed for IDS properties
    integer, intent(in) :: homo
    character(len=ids_string_length), intent(in) :: comment
    character(len=ids_string_length), intent(in) :: source
    character(len=ids_string_length), intent(in) :: create_date

    properties%homogeneous_time = homo
    allocate( properties%comment(1) )
    properties%comment = comment
    allocate( properties%source(1) )
    properties%source = source
    allocate( properties%creation_date(1) )
    properties%creation_date = create_date
    allocate( properties%provider(1) )
    properties%provider = username
    allocate( properties%version_put%data_dictionary(1) )
    properties%version_put%data_dictionary = imas_version
    allocate( properties%version_put%access_layer(1) )
    properties%version_put%access_layer = al_version
    allocate( properties%version_put%access_layer_language(1) )
    properties%version_put%access_layer_language = 'FORTRAN'
    return

  end subroutine write_ids_properties

  subroutine write_ids_code( code, commit )
    type(ids_code), intent(inout) :: code
        !< Type of IDS data structure, designed for code data handling
    character(len=ids_string_length), intent(in) :: commit
    integer :: nlibs !< Number of declared libraries in IDS description
    character(len=ids_string_length) :: repository
    type (amns_query_type) :: query
    type (amns_answer_type) :: answer
    type (amns_error_type) :: amns_status
    character*256 hlp_frm
    character*512 string

    allocate( code%name(1) )
    code%name = source
    allocate( code%commit(1) )
    code%commit = commit
    allocate( code%repository(1) )
    code%repository(1) = "ssh://git@git.iter.org/imas/idstools.git"
    allocate( code%output_flag( num_time_slices ) )
    code%output_flag( time_sind ) = 0

    nlibs = 1
    allocate( code%library( nlibs ) )

    allocate( code%library( nlibs )%name(1) )
    code%library( nlibs )%name = 'AMNS'
    query%string = 'code_version'
    call IMAS_AMNS_QUERY(amns,query,answer,amns_status)
    if (.not.amns_status%flag) then
      allocate( code%library( nlibs )%version(1) )
      code%library( nlibs )%version = answer%string
    end if
    query%string = 'code_commit'
    call IMAS_AMNS_QUERY(amns,query,answer,amns_status)
    if (.not.amns_status%flag) then
      allocate( code%library( nlibs )%commit(1) )
      code%library( nlibs )%commit = answer%string
    end if
    query%string = 'code_repository'
    call IMAS_AMNS_QUERY(amns,query,answer,amns_status)
    if (.not.amns_status%flag) then
      allocate( code%library( nlibs )%repository(1) )
      code%library( nlibs )%repository = answer%string
    end if

    allocate( code%parameters(1) )
    if (n_imp_species.eq.0) then
      write( hlp_frm, '(a)' ) &
         & '(a,f6.2,a,f6.2,a,f6.2,a,f7.2,a,f7.2,a,1p,1e11.4,a,i2)'
      write( string, hlp_frm ) &
         &  ' R0 = ',R0,', Z0 = ',Z0,', RADIUS = ',radius, &
         & ', Te_max =  ',Te_max,', Ti_max = ',Ti_max,', ne_max = ',ne_max, &
         & ', N_imp_species = ',n_imp_species
    else
      write( hlp_frm, '(a,i2,a,i2,a)' ) &
         & '(a,f6.2,a,f6.2,a,f6.2,a,f7.2,a,f7.2,a,1p,1e11.4,a,i2,a,', &
         &   n_imp_species,'(a2,a1),a,',n_imp_species-1,'(1e11.4,a1),1e11.4)'
      write( string, hlp_frm ) &
         &  ' R0 = ',R0,', Z0 = ',Z0,', RADIUS = ',radius, &
         & ', Te_max =  ',Te_max,', Ti_max = ',Ti_max,', ne_max = ',ne_max, &
         & ', N_imp_species = ',n_imp_species, &
         & ', Impurities = ',(impurities(i),' ',i=1,n_imp_species), &
         & ', imp_conc = ',(imp_conc(i),',',i=1,n_imp_species-1), imp_conc(n_imp_species)
    end if
    code%parameters = trim(string)

    return

    end subroutine write_ids_code

    subroutine write_ids_midplane( midplane, midplane_id )
    type(ids_identifier_static) :: midplane
    integer, intent(in) :: midplane_id

    midplane%index = midplane_id
    allocate( midplane%name(1) )
    allocate( midplane%description(1) )
    select case (midplane_id)
    case (1)
      midplane%name = 'magnetic_axis'
      midplane%description = &
        &  'Height of equilibrium O-point'
    case (2)
      midplane%name = 'dr_dz_zero_sep'
      midplane%description = &
        &  'Maximum radius location along separatrix'
    case (3)
      midplane%name = 'z_zero'
      midplane%description = &
        &  'Z = 0 plane'
    case (4)
      midplane%name = 'ggd_subset'
      midplane%description = &
        &  'Location specified by GGD outer midplane grid subset'
    end select
    return
    end subroutine write_ids_midplane

    subroutine write_sourced_constant( val, value )
    type(ids_summary_constant_flt_0d) :: val
       !< Type of IDS data structure, designed for sourced dynamic real data handling
    real(ids_real), intent(in) :: value

    val%value = value
    allocate( val%source(1) )
    val%source = source
    return
    end subroutine write_sourced_constant

    subroutine write_sourced_time_value( val, value )
    type(ids_summary_dynamic_flt_1d_root) :: val
       !< Type of IDS data structure, designed for sourced dynamic real data handling
    real(ids_real), intent(in) :: value

    if (.not.associated( val%value ) ) allocate( val%value( num_time_slices ) )
    val%value( time_sind ) = value
    if (.not.associated( val%source )) then
      allocate( val%source(1) )
      val%source = source
    end if
    return
    end subroutine write_sourced_time_value

    subroutine write_sourced_time_value2( val, value )
    type(ids_summary_dynamic_flt_1d_root_parent_2) :: val
       !< Type of IDS data structure, designed for sourced dynamic real data handling
    real(ids_real), intent(in) :: value

    if (.not.associated( val%value ) ) allocate( val%value( num_time_slices ) )
    val%value( time_sind ) = value
    if (.not.associated( val%source )) then
      allocate( val%source(1) )
      val%source = source
    end if
    return
    end subroutine write_sourced_time_value2

    subroutine write_sourced_time_integer( ival, ivalue )
    type(ids_summary_dynamic_int_1d_root) :: ival
       !< Type of IDS data structure, designed for sourced dynamic real data handling
    integer, intent(in) :: ivalue

    if (.not.associated( ival%value ) ) allocate( ival%value( num_time_slices ) )
    ival%value( time_sind ) = ivalue
    if (.not.associated( ival%source )) then
      allocate( ival%source(1) )
      ival%source = source
    end if
    return
    end subroutine write_sourced_time_integer

    subroutine write_sourced_string( val, string )
    type(ids_summary_static_str_0d) :: val
        !< Type of IDS data structure, designed for sourced string data handling
    character(len=ids_string_length), intent(in) :: string

    allocate( val%value(1) )
    val%value = string
    allocate( val%source(1) )
    val%source = source
    return
    end subroutine write_sourced_string

    function rratio (m, n)
    implicit none
    real (kind=IDS_real) :: rratio
    integer, intent(in) :: m, n
!   ------------------------------------------------------------------
!   RATIO evaluates very carefully the real*8 ratio of two integers.
!   rratio(m,n) evaluates the mathematical expression real(m)/real(n).
!   It is ensured that the expressions rratio(m,n) and rratio(k*m,k*n)
!   give identical numerical results for any nonzero integer k.
!   ------------------------------------------------------------------
    integer m0, n0, k
    intrinsic max, abs, mod, real
!   ------------------------------------------------------------------
    if (n.eq.0) stop 'ratio--error, n.eq.0'
!   (compute  k = gcd(abs(m),abs(n)))
    m0 = abs(m)
    n0 = abs(n)
  1 if (m0.ne.0.and.m0.le.n0) then
      n0 = mod(n0,m0)
      goto 1
    else if (n0.ne.0.and.n0.le.m0) then
      m0 = mod(m0,n0)
      goto 1
    endif
    k = max(m0,n0)
!   (compute ratio)
    rratio = real(m/k)/real(n/k)
    return
!   ------------------------------------------------------------------
    end function rratio

    integer function get_atomic_number(name)
    implicit none
    character*(*) name
    integer i

    character*2, save :: elements(92)
    data elements / 'H' ,'He','Li','Be','B' ,'C' ,'N' ,'O' ,'F' ,'Ne', &
                  & 'Na','Mg','Al','Si','P' ,'S' ,'Cl','Ar','K' ,'Ca', &
                  & 'Sc','Ti','V' ,'Cr','Mn','Fe','Co','Ni','Cu','Zn', &
                  & 'Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y' ,'Zr', &
                  & 'Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn', &
                  & 'Sb','Te','I' ,'Xe','Cs','Ba','La','Ce','Pr','Nd', &
                  & 'Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb', &
                  & 'Lu','Hf','Ta','W' ,'Re','Os','Ir','Pt','Au','Hg', &
                  & 'Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th', &
                  & 'Pa','U '/

    get_atomic_number = 0
    do i = 1, 92
      if(streql(name,elements(i))) then
        get_atomic_number = i
        return
      end if
    end do
    if (streql(name,'D').or.streql(name,'T')) get_atomic_number=1

    return
    end function get_atomic_number

    subroutine get_coronal_distribution( nc, mi, te, ne, total_conc, densities )
    implicit none
    integer, intent(in) :: nc, mi
    real(IDS_real), intent(in) :: te, ne, total_conc
    real(IDS_real), intent(out) :: densities(0:nc)

    integer is, isref
    real(IDS_real) ted, ned, sum
    real(IDS_real), allocatable :: u(:), d(:), l(:), rhs(:)
    real(IDS_real), allocatable :: rate_ei(:), rate_rc(:)
    type (amns_handle_rx_type), allocatable :: amns_ei(:), amns_rc(:)
    type (amns_reactants_type), allocatable :: species_m1(:), species_p1(:)
    type (amns_reaction_type) :: xx_rx

    densities = 0.0_IDS_real

    allocate(u(0:nc), d(0:nc), l(0:nc), rhs(0:nc))
    allocate(species_m1(0:nc), species_p1(0:nc))
    allocate(amns_ei(0:nc), amns_rc(0:nc))
    allocate(rate_ei(0:nc), rate_rc(0:nc))

    do is = 0, nc
      allocate(species_m1(is)%components(4))
      allocate(species_p1(is)%components(4))
      species_m1(is)%components = &
        &  (/ amns_reactant_type(nc, is  , mi, 0), amns_reactant_type(0, -1, 0, 0), &
        &     amns_reactant_type(nc, is-1, mi, 1), amns_reactant_type(0, -1, 0, 1) /)
      species_p1(is)%components = &
        &  (/ amns_reactant_type(nc, is  , mi, 0), amns_reactant_type(0, -1, 0, 0), &
        &     amns_reactant_type(nc, is+1, mi, 1), amns_reactant_type(0, -1, 0, 1) /)
    end do

    xx_rx%string = 'EI'
    do is = 0, nc-1
      call imas_amns_setup_table(amns, xx_rx, species_p1(is), amns_ei(is))
      call imas_amns_rx(amns_ei(is),rate_ei(is),te,ne)
      call imas_amns_finish_table(amns_ei(is))
    end do

    xx_rx%string = 'RC'
    do is = 1, nc
      call imas_amns_setup_table(amns, xx_rx, species_m1(is), amns_rc(is))
      call imas_amns_rx(amns_rc(is),rate_rc(is),te,ne)
      call imas_amns_finish_table(amns_rc(is))
    end do

! set up the matrix
    l(0) = 0.0_IDS_real
    d(0) =-rate_ei(0)
    u(0) = rate_rc(1)
    rhs(0) = 0.0_IDS_real
    do is = 1, nc-1
      l(is) = rate_ei(is-1)
      d(is) =-rate_ei(is)-rate_rc(is)
      u(is) = rate_rc(is+1)
      rhs(is) = 0.0_IDS_real
    end do
    l(nc) = rate_ei(nc-1)
    d(nc) =-rate_rc(nc)
    u(nc) = 0.0_IDS_real
    rhs(nc) = 0.0_IDS_real

! we set the total density
    isref = 0
    do is = 0, nc
      if (rate_ei(is) .lt. rate_rc(is)) then
        exit
      else
        if (isref.lt.nc) isref = isref + 1
      end if
    end do
    u(isref) = 0.0_IDS_real
    d(isref) = 1.0_IDS_real
    l(isref) = 0.0_IDS_real
    rhs(isref) = 1.0_IDS_real

    call solve_tridiag(l,d,u,rhs,densities,nc+1)
    sum = 0.0_IDS_real
    do is = 0, nc
      sum = sum + is * densities(is)
    end do
    densities(:) = densities(:) * (ne*total_conc)/sum

    deallocate(u, d, l, rhs)
    deallocate(species_m1, species_p1)
    deallocate(amns_ei, amns_rc)
    deallocate(rate_ei, rate_rc)

    return
    end subroutine get_coronal_distribution

    subroutine solve_tridiag(a,b,c,v,x,n)
    implicit none
!      a - sub-diagonal (means it is the diagonal below the main diagonal)
!      b - the main diagonal
!      c - sup-diagonal (means it is the diagonal above the main diagonal)
!      v - right part
!      x - the answer
!      n - number of equations

    integer, intent(in) :: n
    real(kind=ids_real), dimension(n), intent(in) :: a,b,c,v
    real(kind=ids_real), dimension(n), intent(out) :: x
    real(kind=ids_real), dimension(n) :: bp,vp
    real(kind=ids_real) :: m
    integer i

! Make copies of the b and v variables so that they are unaltered by this sub
    bp(1) = b(1)
    vp(1) = v(1)

  !The first pass (setting coefficients):
    firstpass: do i = 2,n
     m = a(i)/bp(i-1)
     bp(i) = b(i) - m*c(i-1)
     vp(i) = v(i) - m*vp(i-1)
    end do firstpass

    x(n) = vp(n)/bp(n)
  !The second pass (back-substition)
    backsub:do i = n-1, 1, -1
     x(i) = (vp(i) - c(i)*x(i+1))/bp(i)
    end do backsub

    return
    end subroutine solve_tridiag

    logical function streql (str0, str1)
    implicit none
    character str0*(*), str1*(*)
!   ------------------------------------------------------------------
!   STREQL checks for equality between two strings, ignoring case
!   shift and trailing blanks.
!!  The text of this routine is case-sensitive.
!   ------------------------------------------------------------------
    integer len0, len1, k
    character ch0, ch1
    intrinsic len, ichar
    logical upcase, chreql
    upcase(ch0,ch1) = &
   &  ichar('a').le.ichar(ch0).and.ichar(ch0).le.ichar('z').and. &
   &  ichar(ch1)-ichar(ch0).eq.ichar('A')-ichar('a')
    chreql(ch0,ch1) = ch0.eq.ch1.or.upcase(ch0,ch1).or.upcase(ch1,ch0)
!   ------------------------------------------------------------------
!   ..test installation
!    (protection against errors of case conversion.)
    if (ichar('a').eq.ichar('A')) then
      stop 'streql--installation error'
    endif
!   ..preliminaries
    len0 = len(str0)
    len1 = len(str1)
!   ..search for mismatch
    k = 0
  1 continue
    if (k.lt.min(len0,len1)) then
      if (chreql(str0(k+1:k+1),str1(k+1:k+1))) then
        k = k+1
        goto 1
      endif
    endif
!   ..set return value
    if (len0.eq.len1) then
      streql = k.eq.len0
    else if (len0.lt.len1) then
      streql = k.eq.len0.and.str1(len0+1:len1).eq.' '
    else if (len1.lt.len0) then
      streql = k.eq.len1.and.str0(len1+1:len0).eq.' '
    endif
    return
!    ------------------------------------------------------------------
    end function streql

 end program FP_dummy_plasma

!!!Local Variables:
 !!! mode: f90
 !!! End:


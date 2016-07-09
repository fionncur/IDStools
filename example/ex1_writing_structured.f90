program ex1_writing_structured

  use ids_schemas
  use ids_grid_structured, only: gridSetupStructured
  use ids_grid_common, only: COORDTYPE_theta , COORDTYPE_rho_tor

  ! Dimensions
  integer, parameter :: Nx=5
  integer, parameter :: Ny=7
  
  ! Data to be stored
  integer :: coordtype(2)
  integer :: gshape(2)
  real(DP) :: x(Nx)
  real(DP) :: y(Ny)
  real(DP) :: grid_matrix( max(Nx,Ny) , 2 )

  ! The grid to store it in
  type(ids_generic_grid_dynamic) :: grid

  ! Error handling
  integer :: output_flag
  character(len=:), allocatable :: output_message

  ! Internal
  integer :: j
    
  write(*,*)'=== START: ex1_writing_structured test1'

  ! Initialise the grid coordinates: x and y
  x(1:Nx) = (/ ( real(j-1,DP) , j=1,gshape(1) ) /)
  y(1:Ny) = (/ ( real(j-1,DP) , j=1,gshape(2) ) /)

  ! In the GGD you need to put your grid in a matrix, here we call this matrix grid_matrix:
  grid_matrix( 1:Nx , 1 ) = x(:)
  grid_matrix( 1:Ny , 2 ) = y(:)

  ! Dimensions of coordinate system
  gshape(1) = Nx
  gshape(2) = Ny

  ! Describe which coordinates are being used
  coordtype(1) = COORDTYPE_rho_tor
  coordtype(2) = COORDTYPE_theta

  ! Push data to the grid
  call gridSetupStructured( grid, coordtype, gshape, grid_matrix, output_flag, output_message)

  ! Check that the pushing was successful
  if ( output_flag /= 0 ) then
     write(*,*)'ERROR recieved from gridSetupStructured:'
     write(*,*)output_message
     deallocate(output_message)
     stop
  end if

  write(*,*)'=== END: ex1_writing_structured test1'

end program ex1_writing_structured

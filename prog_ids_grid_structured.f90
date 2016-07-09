program prog_ids_grid_structured

  use ids_schemas
  use ids_grid_structured

  implicit none

  call test1
  call test2

contains

  subroutine test1

    type(ids_generic_grid_dynamic) :: grid 
    integer, dimension(2) :: coordtype = (/ 1 , 2 /)
    integer, dimension(2) :: gshape = (/ 13 , 7 /)
    real(DP), dimension(13, 2) :: x
    character(64) :: id='COORD_X'
    integer :: output_flag
    character(len=:), allocatable :: output_message

    write(*,*)'=== START: test1'

    call gridSetupStructured( grid, coordtype, gshape, x, output_flag, output_message, id)

    write(*,*)'=== END: test1'
    
  end subroutine test1
  


  subroutine test2

    type(ids_generic_grid_dynamic) :: grid 

    integer, dimension(2) :: coordtype_in = (/ 1 , 2 /)
    integer, dimension(2) :: gshape_in = (/ 13 , 7 /)
    real(DP), dimension(13, 2) :: x_in

    integer, allocatable, dimension(:) :: coordtype_out
    integer, allocatable, dimension(:) :: gshape_out
    real(DP), allocatable, dimension(:,:) :: x_out

    character(64) :: id='COORD_X'
    integer :: output_flag
    character(len=:), allocatable :: output_message

    write(*,*)'=== START: test1'

    call gridSetupStructured( grid, coordtype_in , gshape_in, x_in , output_flag, output_message, id)
    if ( output_flag /= 0 ) then
       write(*,*)'ERROR recieved from gridSetupStructured'
       stop
    end if
    call gridStructGetAxes( grid, coordtype_out, gshape_out, x_out, output_flag, output_message)

    write(*,*)'=== END: test2'

  end subroutine test2
  


end program prog_ids_grid_structured

program prog_ids_grid_structured

  use ids_schemas
  use ids_grid_structured
  use ids_grid_access
  use ids_grid_common, only: COORDTYPE_X , COORDTYPE_Y , COORDTYPE_theta , COORDTYPE_rho_tor

  implicit none

  call test1
  call test2
  call test3

contains

  subroutine test1

    type(ids_generic_grid_dynamic) :: grid
    integer, dimension(2) :: coordtype = (/ COORDTYPE_X , COORDTYPE_Y /)
    integer, dimension(2) :: gshape = (/ 13 , 7 /)
    real(DP), dimension(13, 2) :: x
    integer :: output_flag
    character(len=:), allocatable :: output_message

    ! Internal
    integer :: j
    
    write(*,*)'=== START: test1 (writing grids)'

    x(1:gshape(1) , 1) = (/ ( real(j-1,DP) , j=1,gshape(1) ) /)
    x(1:gshape(2) , 2) = (/ ( real(j-1,DP) , j=1,gshape(2) ) /)
    
    call gridSetupStructured( grid, coordtype, gshape, x, output_flag, output_message)

    if ( output_flag /= 0 ) then
       write(*,*)'ERROR recieved from gridSetupStructured:'
       if (allocated(output_message)) then
          write(*,*)output_message
          deallocate(output_message)
       endif
       stop
    end if

    write(*,*)'=== END: test1'
    
  end subroutine test1
  


  subroutine test2

    type(ids_generic_grid_dynamic) :: grid 

    integer, dimension(2) :: coordtype_in = (/ COORDTYPE_theta , COORDTYPE_rho_tor /)
    integer, dimension(2) :: gshape_in = (/ 13 , 7 /)
    real(DP), dimension(13, 2) :: x_in = 0_DP

    integer, allocatable, dimension(:) :: coordtype_out
    integer, allocatable, dimension(:) :: gshape_out
    real(DP), allocatable, dimension(:,:) :: x_out

    character(64) :: id='my 2d grid'
    integer :: output_flag = -999999999
    character(len=:), allocatable :: output_message

    ! Internal
    integer :: j
    
    write(*,*)'=== START: test2 (writing and reading grids)'
    write(*,*)

    write(*,*)'Writing...'
    x_in(1:gshape_in(1) , 1) = (/ ( real(j-1,DP) / real(gshape_in(1)-1,DP) , j=1,gshape_in(1) ) /)
    x_in(1:gshape_in(2) , 2) = (/ ( real(j-1,DP) / real(gshape_in(2)-1,DP) , j=1,gshape_in(2) ) /)

    call gridSetupStructured( grid, coordtype_in , gshape_in, x_in , output_flag, output_message, id=id)
    if ( output_flag /= 0 ) then
       write(*,*)'ERROR recieved from gridSetupStructured'
       write(*,*)output_message
       deallocate(output_message)
       stop
    end if

    write(*,*)'Reading...'
    write(*,*)'- gridUId=', gridUId(grid)
    write(*,*)'- gridId=', gridId(grid)
    write(*,*)'- gridNdim=', gridNdim(grid)
    write(*,*)'- gridNSpace=', gridNSpace(grid)
    write(*,*)'- gridSpaceNDim( grid % space(1) )=', gridSpaceNDim( grid % space(1) )
    write(*,*)'- gridSpaceNDim( grid % space(2) )=', gridSpaceNDim( grid % space(2) )
    write(*,*)'- gridSpaceNDims=', gridSpaceNDims(grid)
    write(*,*)'- gridSpaceMaxObjDim=', gridSpaceMaxObjDim( grid % space(1) )

    write(*,*)'- gridSpaceNNodes=', gridSpaceNNodes( grid % space(1) )
    write(*,*)'- gridSpaceNObject( grid % space(1) , 1)=', gridSpaceNObject( grid % space(1) , 1)
    write(*,*)'- gridSpaceNObject( grid % space(2) , 1)=', gridSpaceNObject( grid % space(2) , 1)

!    write(*,*)'- gridSpaceMaxNBoundaries( grid % space(1) , 1)=', gridSpaceMaxNBoundaries( grid % space(1) , 1)
!    write(*,*)'- gridSpaceMaxNBoundaries( grid % space(2) , 1)=', gridSpaceMaxNBoundaries( grid % space(2) , 1)


!    write(*,*)'- =', (grid)
!    write(*,*)'- =', ( grid % space(1) )
    

    call gridStructGetShape( grid , gshape_out )
    write(*,*)'- gridStructGetShape: ', gshape_out

    call gridStructGetAxes( grid, coordtype_out, gshape_out, x_out, output_flag, output_message)
    if ( output_flag /= 0 ) then
       write(*,*)'ERROR recieved from gridStructGetAxes'
       write(*,*)output_message
       deallocate(output_message)
       stop
    end if

    write(*,*)'- x_out(:,1)=',x_out(1:gshape_out(1) , 1)
    write(*,*)'- x_out(:,2)=',x_out(1:gshape_out(2) , 2)

    write(*,*)
    write(*,*)'=== END: test2'

  end subroutine test2
  

  subroutine test3

    type(ids_generic_grid_dynamic) :: grid 

    integer, dimension(2) :: coordtype = (/ COORDTYPE_theta , COORDTYPE_rho_tor /)
    integer, dimension(2) :: gshape = (/ 13 , 7 /)
    real(DP), dimension(13, 2) :: x = 0_DP

    type(ids_generic_grid_scalar) :: cpofield
    integer :: subgrid
    real(DP), dimension(13,2) :: data_in
    real(DP), dimension(13,2) :: data_out

    integer, allocatable, dimension(:) :: coordtype_out
    integer, allocatable, dimension(:) :: gshape_out
    real(DP), allocatable, dimension(:,:) :: x_out

    character(64) :: id='my 2d grid'
    integer :: output_flag = -999999999
    character(len=:), allocatable :: output_message

    ! Internal
    integer :: j, k
    
    write(*,*)
    write(*,*)'=== START: test3 (writing and reading grids)'

    write(*,*)'Writing grid...'
    x(1:gshape(1) , 1) = (/ ( real(j-1,DP) / real(gshape(1)-1,DP) , j=1,gshape(1) ) /)
    x(1:gshape(2) , 2) = (/ ( real(j-1,DP) / real(gshape(2)-1,DP) , j=1,gshape(2) ) /)

    call gridSetupStructured( grid, coordtype , gshape, x , output_flag, output_message, id)
    if ( output_flag /= 0 ) then
       write(*,*)'ERROR recieved from gridSetupStructured'
       write(*,*)output_message
       deallocate(output_message)
       stop
    end if

    do j=1,gshape(1)
       do k=1,gshape(2)
          data_in(j,k) = atan( real(j,DP) * log( real(k,DP)-0.2_DP ) )
       enddo
    enddo

    write(*,*)'Writing data...'
    call gridStructWriteData( grid , cpofield , subgrid , data_in )

    write(*,*)'Reading data...'
    call gridStructReadData( grid, cpofield, subgrid, data_out, output_flag, output_message)
    
    write(*,*)'range of data_in: ',minval(data_in), ' -- ', maxval(data_in)
    write(*,*)'maxval(abs(data_in - data_out))=',maxval(abs(data_in - data_out))
    
    write(*,*)
    write(*,*)'=== END: test3'

  end subroutine test3

end program prog_ids_grid_structured

program ids_grid_example1_2dstructured_servicelibrary

  !> This example program demonstrates how to use the general grid description
  !> to store a simple 2d structured grid and write some data given on it to the IDS.
  !>
  !> The focus of this example program is delegate as much work as possible onto the
  !> grid service library. This is the recommended way to use the general grid description.
  !>
  !> If you want to learn how to do everything manually, step-by-step, without hiding any
  !> complexity behind high-level calls, have a look at the file ids_grid_example1_2dstructured_manual.f90
  !> in this directory.
  !>

  ! IMAS data structure/IDS definitions
  use ids_schemas, only: DP, ids_edge_profiles

  use ids_routines ! , only: imas_create, ids_put, imas_close

  ! IMAS grid service library: constant definitions like COORDTYPE_R, COORDTYPE_Z
  use ids_grid_common, only: COORDTYPE_R, COORDTYPE_Z

  ! IMAS grid service libary, routines for handling structured grids
  use ids_grid_structured, only: gridSetupStructuredSep, gridStructWriteData2d, GRID_STRUCT_FACES

  implicit none

  ! parameters
  integer, parameter :: NPOINTR = 6
  integer, parameter :: NPOINTZ = 5   

  integer, parameter :: SHOTNUM = 9001
  integer, parameter :: RUNNUM = 1

  ! variables
  type (ids_edge_profiles) :: edgeids => null()
  integer :: idx
  integer :: ir, iz, i
  real(DP) :: cellData(NPOINTR - 1, NPOINTZ - 1)
  real(DP) :: nodeData(NPOINTR, NPOINTZ)
  real(DP) :: x1(NPOINTR)
  real(DP) :: x2(NPOINTZ)
  integer :: output_flag
  character(len=:), allocatable :: output_message

  write(*,*)'START: program ids_grid_example1_2dstructured_servicelibrary'
  
  ! === 1. Set up IDS ===
  write(*,*)' === 1. Set up IDS ==='

  allocate( edgeids % time(1) )
  edgeids % time(1) = 3.1415_DP

  allocate( edgeids % code % name(1) )
  edgeids % code % name(1)="ids_grid_example1_2dstructured_service"

  ! Allocate one time-slice:
  allocate(edgeids % ggd(1) )
  edgeids % ggd(1) % time = 3.1415_DP

  ! === 2. Set up grid ===
  write(*,*)' === 2. Set up grid ==='
  x1(:) = (/ ( 1.0_DP * i, i=0,NPOINTR-1) /)
  x2(:) = (/ ( 0.5_DP * i, i=0,NPOINTZ-1) /)

  call gridSetupStructuredSep( &
      & grid = edgeids % ggd(1) % grid, &
      & ndim = 2, &
      & c1 = COORDTYPE_R, &
      & x1 = x1, &
      & c2 = COORDTYPE_Z, &
      & x2 = x2, &
      & id = '2d_structured', &
      & output_flag = output_flag, &
      & output_message = output_message)

  if (output_flag /= 0) then
     write(*,*)'in ids_grid_example1_2dstructured_servicelibrary ',&
          & 'error recieved from gridSetupStructuredSep'
     if (allocated(output_message)) then
        write(*,*)output_message
     end if
     return
  end if

  ! === 3. Set up subgrid for 2d cells ("faces") ===
  write(*,*)' === 3. SKIP!!  (set up subgrid) ==='
  ! Not necessary, a default set of subgrids is automatically created by gridSetupStructured.
  ! You can disable this behaviour by calling gridSetupStructuredSep with the optional
  ! argument createSubgrids = .false. 
  ! 
  ! The easiest way to manually create the subgrid for all (1,1) cells ("faces") is 
  ! allocate(edgeids%subgrids(1))  
  ! call createSubGridForClass(edgeids%grid, edgeids%subgrids(1), (/ 1, 1 /), "Cells")

  ! === 4. Write some fake scalar data to the edge ids ===
  write(*,*)' === 4. Write some fake scalar data to the edge ids ==='

  ! Make up some data
  do ir = 1, NPOINTR - 1 
      do iz = 1, NPOINTZ - 1
          cellData(ir, iz) = ir * iz          
      enddo
  enddo

  do ir = 1, NPOINTR
      do iz = 1, NPOINTZ
          nodeData(ir, iz) = ir * iz
      enddo
  enddo

  ! Write the data on the grid
  allocate( edgeids % ggd(1) % electrons % density(1) )
  call gridStructWriteData2d( edgeids % ggd(1) % grid, &
       edgeids % ggd(1) % electrons % density(1), &
       GRID_STRUCT_FACES, cellData )

  allocate(edgeids%time(1))
  edgeids%time(1) = 0.0
  edgeids%ids_properties%homogeneous_time = 1

  ! === 5. Write the edge IDS to the UAL ===
  write(*,*)' === 5. Write the edge IDS to the UAL ==='
  write(*,*) "Example 1: writing to shot ", SHOTNUM, ", run ", RUNNUM
  call imas_create( 'ids', SHOTNUM, RUNNUM, 0, 0, idx)
  call ids_put(idx, "edge", edgeids)
  call imas_close(idx)
  call ids_deallocate(edgeids)
  deallocate(edgeids)

  write(*,*)'END: program ids_grid_example1_2dstructured_servicelibrary'

end program ids_grid_example1_2dstructured_servicelibrary

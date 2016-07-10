program ids_grid_example1_2dstructured_servicelibrary

  !> This example program demonstrates how to use the general grid description
  !> to store a simple 2d structured grid and write some data given on it to the CPO.
  !>
  !> The focus of this example program is delegate as much work as possible onto the
  !> grid service library. This is the recommended way to use the general grid description.
  !>
  !> If you want to learn how to do everything manually, step-by-step, without hiding any
  !> complexity behind high-level calls, have a look at the file itm_grid_example1_2dstructured_manual.f90
  !> in this directory.
  !>
  !> The used grid is described in detail here on the ITM Documentation Website (https://www.efda-itm.eu/ITM/html/)
  !> Then go to IMP3 -> IMP3 general grid description & service library -> Example grids -> Example grid #1
  !> Direct link (might be broken): https://www.efda-itm.eu/ITM/html/imp3_gridexamples.html#imp3_gridexamples_5 

  ! ITM data structure/CPO definitions
  use ids_schemas, only: DP, ids_edge_profiles     

  !  use ids_routines    ! ITM UAL routines

  ! ITM grid service library: constant definitions like COORDTYPE_R, COORDTYPE_Z
  use ids_grid_common, only: COORDTYPE_R, COORDTYPE_Z

  ! ITM grid service libary, routines for handling structured grids
  use ids_grid_structured, only: gridSetupStructuredSep, gridStructWriteData2d, GRID_STRUCT_FACES

  implicit none

  ! parameters
  integer, parameter :: NPOINTR = 6
  integer, parameter :: NPOINTZ = 5   

  integer, parameter :: SHOTNUM = 9001
  integer, parameter :: RUNNUM = 1

  ! variables
  type (ids_edge_profiles),pointer :: edgecpo(:) => null()
  integer :: idx
  integer :: ir, iz, i
  real(DP) :: cellData(NPOINTR - 1, NPOINTZ - 1)
  real(DP) :: nodeData(NPOINTR, NPOINTZ)
  real(DP) :: x1(NPOINTR)
  real(DP) :: x2(NPOINTZ)

  write(*,*)'START: program ids_grid_example1_2dstructured_servicelibrary'
  
  ! === 1. Set up CPO ===
  write(*,*)' === 1. Set up CPO ==='

  allocate( edgecpo(1) )    
  allocate( edgecpo(1) % code % name(1) )
  edgecpo(1) % code % name(1)="ids_grid_example1_2dstructured_service"

  ! Allocate one time-slice:
  allocate(edgecpo(1) % profiles_ggd(1) )

  ! === 2. Set up grid ===
  write(*,*)' === 2. Set up grid ==='
  write(*,*)'COORDTYPE_R=',COORDTYPE_R
  write(*,*)'COORDTYPE_Z=',COORDTYPE_Z

  x1(:) = (/ ( 1.0_DP * i, i=0,NPOINTR-1) /)
  x2(:) = (/ ( 0.5_DP * i, i=0,NPOINTZ-1) /)
  write(*,*)'x1=',x1
  write(*,*)'x2=',x2
  call gridSetupStructuredSep( &
      & grid = edgecpo(1) % profiles_ggd(1) % grid, &
      & ndim = 2, &
      & c1 = COORDTYPE_R, &
      & x1 = x1, &
      & c2 = COORDTYPE_Z, &
      & x2 = x2, &
      & id = '2d_structured' )

  ! === 3. Set up subgrid for 2d cells ("faces") ===
  write(*,*)' === 3. Set up subgrid for 2d cells ("faces") ==='
  ! Not necessary, a default set of subgrids is automatically created by gridSetupStructured.
  ! You can disable this behaviour by calling gridSetupStructuredSep with the optional
  ! argument createSubgrids = .false. 
  ! 
  ! The easiest way to manually create the subgrid for all (1,1) cells ("faces") is 
  ! allocate(edgecpo(1)%subgrids(1))  
  ! call createSubGridForClass(edgecpo(1)%grid, edgecpo(1)%subgrids(1), (/ 1, 1 /), "Cells")

  ! === 4. Write some fake scalar data to the edge cpo ===
  write(*,*)' === 4. Write some fake scalar data to the edge cpo ==='

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
  allocate( edgecpo(1) % profiles_ggd(1) % electrons % density(1) )
  call gridStructWriteData2d( edgecpo(1) % profiles_ggd(1) % grid, &
       edgecpo(1) % profiles_ggd(1) % electrons % density(1), &
       GRID_STRUCT_FACES, cellData )

  ! === 5. Write the edge CPO to the UAL ===
  write(*,*)' === 5. Write the edge CPO to the UAL ==='
!  write (*,*) "Example 1: writing to shot ", SHOTNUM, ", run ", RUNNUM
!  call euitm_create( 'euitm', SHOTNUM, RUNNUM, 0, 0, idx)
!  call euitm_put(idx, "edge", edgecpo)
!  call euitm_close(idx)
!  call euitm_deallocate(edgecpo)   

  write(*,*)'END: program ids_grid_example1_2dstructured_servicelibrary'

end program ids_grid_example1_2dstructured_servicelibrary

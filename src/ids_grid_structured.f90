module ids_grid_structured

  !> This modules provides simple interfaces to the Generic Grid Description (GGD) 
  !> to handle rectangular grids and data stored on rectangular grids.
  !>
  !> Data can either be stored/recovered using high or low level routines, although
  !> for rectangular grids, the high level routines should be sufficient. The main
  !> high-level read and write routines are:
  !> 1. The main subroutine for writing data to a grid is: \c gridSetupStructuredSep.
  !>    An alternative subroutine is \c gridSetupStructured.
  !> 2. To recover a grid from the GGD, use \c gridStructGetAxes
  !> 3. To store a data field represented on a GGD grid, use \c gridStructWriteData
  !> 4. To recover a data field represented on a GGD grid, use \c gridStructReadData
  !>
  !> @author Hajo Klignshirn (for the ITM), adapted to IMAS by Thomas Jonsson 2016

  use ids_schemas, only: &
       DP, &
       ids_generic_grid_dynamic, &
       ids_generic_grid_dynamic_space, &
       ids_generic_grid_scalar

  use ids_grid_access, only: &
       gridNDim, &
       gridCoordTypes, &
       gridSpaceNNodes
  
  implicit none

  !> Definition of default subgrids
  integer, parameter :: GRID_STRUCT_SUBGRID_0D = 1 ! all 0d objects
  integer, parameter :: GRID_STRUCT_SUBGRID_1D = 2 ! all 1d objects
  integer, parameter :: GRID_STRUCT_SUBGRID_2D = 3 ! all 2d objects
  integer, parameter :: GRID_STRUCT_SUBGRID_3D = 4 ! all 3d objects
  integer, parameter :: GRID_STRUCT_SUBGRID_4D = 5 ! all 4d objects
  integer, parameter :: GRID_STRUCT_SUBGRID_5D = 6 ! all 5d objects
  integer, parameter :: GRID_STRUCT_SUBGRID_6D = 7 ! all 6d objects

  ! Same as above, with human-readable names
  integer, parameter :: GRID_STRUCT_NODES = GRID_STRUCT_SUBGRID_0D ! all 0d objects
  integer, parameter :: GRID_STRUCT_EDGES = GRID_STRUCT_SUBGRID_1D ! all 1d objects
  integer, parameter :: GRID_STRUCT_FACES = GRID_STRUCT_SUBGRID_2D ! all 2d objects
  integer, parameter :: GRID_STRUCT_CELLS = GRID_STRUCT_SUBGRID_3D ! all 3d objects


  interface gridStructWriteData
     module procedure gridStructWriteData1d, gridStructWriteData2d , gridStructWriteData3d ,&
          & gridStructWriteData4d, gridStructWriteData5d, gridStructWriteData6d !, &
!          & gridStructWriteData1dComplex, gridStructWriteData2dComplex
  end interface gridStructWriteData

  ! These routines have no EU-IM equivalent. The should be used for the nodes of the
  ! derived type "ids_generic_grid_vector_components"
  interface gridWriteDataVectorComponent
     module procedure gridWriteDataVectorComponent1d, gridWriteDataVectorComponent2d, &
          gridWriteDataVectorComponent3d, gridWriteDataVectorComponent4d, &
          gridWriteDataVectorComponent5d
  end interface gridWriteDataVectorComponent

  interface gridStructReadData
     module procedure gridStructReadData1d, gridStructReadData2d, gridStructReadData3d , &
          & gridStructReadData4d, gridStructReadData5d, gridStructReadData6d !, &
!          & gridStructReadData1dComplex, gridStructReadData2dComplex
  end interface gridStructReadData

  ! These routines have no EU-IM equivalent. The should be used for the nodes of the
  ! derived type "ids_generic_grid_vector_components"
  interface gridStructReadDataVectorComponent
     module procedure gridStructReadDataVectorComponent1d, gridStructReadDataVectorComponent2d, &
          gridStructReadDataVectorComponent3d, gridStructReadDataVectorComponent4d
  end interface gridStructReadDataVectorComponent

contains

  !============================================================================
  ! WRITE A GRID
  !============================================================================

  !> Write a n-dimensional structured grid 
  !> into a grid descriptor, as well as the default subgrids for objects of all dimensions.
  !>
  !> The dimension n of the grid is taken as size(coordtype).
  !> 
  !> @param grid      Grid descriptor to fill
  !> @param coordtype Dimension(n). Defines coordinate types / labels for the 
  !>                  individual axes. See the 
  !>                  constants defined in itm_grid.f90 (COORDTYPE_*)
  !> @param gshape    Dimension(n). Shape of the grid. In dimension i the grid 
  !>                  has shape(i) grid points.
  !> @param x         Dimension( maxval( gshape(n) ), n ). 
  !>                  Grid node coordinates in the individual dimensions. 
  !>                  The node positions in  space i are given by 
  !>                  x( 1 : gshape( i ), id ).
  !> @param id        Name / identifier string for this grid
  !> @param createSubgrids Optional flag controlling whether default subgrids
  !>                  are created. Default is .true.
  !> @param periodicSpaces Optional integer array containing the indices
  !>                  of the coordinate directions that are periodic. This will
  !>                  result in the last node in these coordinate directions to
  !>                  be connected to the first node by an edge. Note that if periodic
  !>                  spaces are present, no metric information is computed.
  !> @param computeMeasures NOT IMPLEMENTED.
  !> @param uid       Unique index of this grid. Used for handling multiple grids.
  !>
  !> @see gridSetupStructuredSep
  !>
  !> NOTE: This routines is a modified version of the ITM (EUIM) routine \c gridSetupStructured
  !>       adapted to IDSs by Thomas Jonsson 8 July 2016.
  !>       During the adaptation the functionality was reduced:
  !>        - sub-grid are no longer generated;
  !>        - metric information is no longer calculated on the grid.
  !>        - uid seemms not to have a placeholder in the IDS grid description.
  !>       During the adaptation calls to the itm_assert library were replaced by returning
  !>       \c output_flag and an \c output_message. This modification may be forwarded  
  !>       to the ITM version of the subroutine. 
  !>
  subroutine gridSetupStructured( grid, coordtype, gshape, x, &
       output_flag, output_message, id, createSubgrids, &
       periodicSpaces, uid, computeMeasures)
    type(ids_generic_grid_dynamic), intent(out) :: grid 
    integer, dimension(:), intent(in) :: coordtype
    integer, dimension(size(coordtype)), intent(in) :: gshape
    real(DP), dimension(:, :), intent(in) :: x
    integer, intent(out) :: output_flag
    character(len=:), allocatable, intent(out) :: output_message
    character(*), intent(in), optional :: id
    logical, intent(in), optional :: createSubgrids
    integer, intent(in), optional :: periodicSpaces(:)
    integer, intent(in), optional :: uid
    logical, intent(in), optional :: computeMeasures 

    ! Internal
    integer :: ndim, idim
    logical :: periodic

    if ( size( coordtype ) /= size( gshape ) ) then
       allocate(character(len("gridWriteStructured: size of coordtype and gshape don't match")) :: output_message )
       output_message =       "gridWriteStructured: size of coordtype and gshape don't match"
       output_flag = -1001
       return
    endif
    if ( maxval( shape( x ) ) < maxval( gshape ) ) then
       allocate(character(len("gridWriteStructured: shape of x seems to be inconsistent with gshape")) :: output_message )
       output_message =       "gridWriteStructured: shape of x seems to be inconsistent with gshape"
       output_flag = -1002
       return
    endif

    if (present(createSubgrids)) then
       if (createSubgrids) then
          output_flag = -1010
          allocate(character(len( &
               & "gridSetupStructuredSep: createSubgrids requested, but not yet implemented!")) :: output_message )
          output_message = &
               & "gridSetupStructuredSep: createSubgrids requested, but not yet implemented!"
          return
       end if
    end if

    if (present(computeMeasures)) then
       if (computeMeasures) then
          output_flag = -1011
          allocate(character(len( &
               & "gridSetupStructuredSep: computeMeasures requested, but not yet implemented!")) :: output_message )
          output_message = &
               & "gridSetupStructuredSep: computeMeasures requested, but not yet implemented!"
          return
       end if
    end if

    output_flag = 0

    if (present(uid)) then
!!! Are there any place holder for "uid" in the IDSs???
    end if

    if (present(id)) then
        allocate( grid%identifier%name(1) )
        grid%identifier%name(1) = id
    end if

    ndim = size(coordtype)
    allocate( grid % space(ndim) )

    ! ... fill in the grid data
    do idim = 1, ndim
        periodic = .false.
        if (present(periodicSpaces)) then
            periodic = any(periodicSpaces == idim)
        end if
        call gridSetupStruct1dSpace( grid % space(idim), &
            & coordtype( idim ), x( 1 : gshape(idim) ,idim ), periodic )   
    end do
    
  end subroutine gridSetupStructured




  !> Write a n-dimensional structured grid into a grid descriptor (alternate version
  !> with separate dimension vectors)
  !>
  !> Alternate wrapper for \c gridSetupStructured, which makes it easier
  !> to give the node positions as individual arrays
  !>
  !> The dimension n of the grid is given by \c ndim and has to be consistent with
  !> the number of arguments x<j> recieved (j=1...6).
  !>
  !> @param grid      Grid descriptor to fill
  !> @param ndim      Dimensions of the grid.
  !> @param c1        Type of coordinate no. 1 (integer)
  !> @param x1        Grid in the space spanned by coordinate no. 1
  !> @param c2        Type of coordinate no. 2 (integer)
  !> @param x2        Grid in the space spanned by coordinate no. 2
  !> @param c3        Type of coordinate no. 3 (integer)
  !> @param x3        Grid in the space spanned by coordinate no. 3
  !> @param c4        Type of coordinate no. 4 (integer)
  !> @param x4        Grid in the space spanned by coordinate no. 4
  !> @param c5        Type of coordinate no. 5 (integer)
  !> @param x5        Grid in the space spanned by coordinate no. 5
  !> @param c6        Type of coordinate no. 6 (integer)
  !> @param x6        Grid in the space spanned by coordinate no. 6
  !> @param id        Name / identifier string for this grid
  !> @param createSubgrids Optional flag controlling whether default subgrids
  !>                  are created. Default is .true.
  !> @param periodicSpaces Optional integer array containing the indices
  !>                  of the coordinate directions that are periodic. This will
  !>                  result in the last node in these coordinate directions to
  !>                  be connected to the first node by an edge. Note that if periodic
  !>                  spaces are present, no metric information is computed.
  !> @param uid       Unique index of this grid. Used for handling multiple grids.
  !> @param computeMeasures NOT IMPLEMENTED.
  !> @param output_flag Flag to identify different errors tha may occur;
  !>                  output_flag=0 means that no error has occured.
  !> @param output_message String-message describing errors.
  !>
  !> @see gridSetupStructured
  subroutine gridSetupStructuredSep( grid, ndim, &
       c1, x1, c2, x2, c3, x3, c4, x4, c5, x5, c6, x6, &
       id, createSubgrids, periodicSpaces, uid, computeMeasures, &
       output_flag, output_message )
    type(ids_generic_grid_dynamic), intent(out) :: grid
    integer, intent(in) :: ndim
    real(DP), intent(in), dimension(:) :: x1 ! have to have at least one dimension
    integer, intent(in) :: c1 ! have to have at least one dimension
    real(DP), intent(in), dimension(:), optional :: x2, x3, x4, x5, x6
    integer, intent(in),optional :: c2, c3, c4, c5, c6
    character(*), intent(in), optional :: id
    logical, intent(in), optional :: createSubgrids
    integer, intent(in), optional :: periodicSpaces(:)
    integer, intent(in), optional :: uid
    logical, intent(in), optional :: computeMeasures
    integer, intent(out), optional :: output_flag
    character(len=:), allocatable, intent(out), optional :: output_message


    ! internal
    integer :: lndim, nmax, i
    real(DP), dimension(:,:), allocatable :: x
    integer, dimension(:), allocatable :: gshape, coordtype
    integer :: internal_output_flag
    character(len=:), allocatable :: internal_output_message

    if (present(createSubgrids)) then
       if (createSubgrids) then
          if (present(output_flag)) then
             output_flag = -2010
          end if
          if (present(output_message)) then
             allocate(character(len( &
                  & "gridSetupStructuredSep: createSubgrids requested, but not yet implemented!")) :: output_message )
             output_message = &
                  & "gridSetupStructuredSep: createSubgrids requested, but not yet implemented!"
             return
          end if
       end if
    end if

    if (present(computeMeasures)) then
       if (computeMeasures) then
          if (present(output_flag)) then
             output_flag = -2011
          end if
          if (present(output_message)) then
             allocate(character(len( &
                  & "gridSetupStructuredSep: computeMeasures requested, but not yet implemented!")) :: output_message )
             output_message = &
                  & "gridSetupStructuredSep: computeMeasures requested, but not yet implemented!"
          end if
          return
       end if
    end if

    lndim = 1
    nmax = size( x1 )
    if ( present( x2 ) ) then
       lndim = 2
       nmax = max( nmax, size( x2 ) )
       if ( .not. present( c2 ) ) then
          if (present(output_flag)) then
             output_flag = -2002
          else
             stop
          end if
          if (present(output_message)) then
             allocate(character(len("gridSetupStructuredSep: x2 given, but not c2")) :: output_message )
             output_message =       "gridSetupStructuredSep: x2 given, but not c2"
          end if
       end if
    end if
    if ( present( x3 ) ) then
       lndim = 3
       nmax = max( nmax, size( x3 ) )
       if (.not. present( c3 )) then
          if (present(output_flag)) then
             output_flag = -2003
          else
             stop
          end if
          if (present(output_message)) then
             allocate(character(len("gridSetupStructuredSep: x3 given, but not c3")) :: output_message )
             output_message =       "gridSetupStructuredSep: x3 given, but not c3"
          end if
       end if
    end if
    if ( present( x4 ) ) then
       lndim = 4
       nmax = max( nmax, size( x4 ) )
       if (.not. present( c4 ))then
          if (present(output_flag)) then
             output_flag = -2004
          else
             stop
          end if
          if (present(output_message)) then
             allocate(character(len("gridSetupStructuredSep: x4 given, but not c4")) :: output_message )
             output_message =       "gridSetupStructuredSep: x4 given, but not c4"
          end if
       end if
    end if
    if ( present( x5 ) ) then
       lndim = 5
       nmax = max( nmax, size( x5 ) )
       if (.not. present( c5 )) then
          if (present(output_flag)) then
             output_flag = -2005
          else
             stop
          end if
          if (present(output_message)) then
             allocate(character(len("gridSetupStructuredSep: x5 given, but not c5")) :: output_message )
             output_message =       "gridSetupStructuredSep: x5 given, but not c5"
          end if
       end if
    end if
    if ( present( x6 ) ) then
       lndim = 6
       nmax = max( nmax, size( x6 ) )
       if (.not. present( c6 )) then
          if (present(output_flag)) then
             output_flag = -2006
          else
             stop
          end if
          if (present(output_message)) then
             allocate(character(len("gridSetupStructuredSep: x6 given, but not c6")) :: output_message )
             output_message =       "gridSetupStructuredSep: x6 given, but not c6"
          end if
       end if
    end if

    if ( lndim /= ndim ) then
       if (present(output_flag)) then
          output_flag = -2001
       else
          stop
       end if
       if (present(output_message)) then
          allocate(character(len("gridWriteStructured: error in call, ndim does not match number of arguments")) :: output_message )
          output_message =       "gridWriteStructured: error in call, ndim does not match number of arguments"
       end if
    endif

    ! allocate and assemble temporary data structure
    allocate( x( nmax, ndim ) )
    allocate( gshape( ndim ) )
    allocate( coordtype( ndim ) )

    do i = 1, ndim

            select case( i )
            case( 1 )
                    x( 1:size( x1 ), 1 ) = x1
                    gshape(1) = size( x1 )
                    coordtype(1) = c1
            case( 2 )
                    x( 1:size( x2 ), 2 ) = x2
                    gshape(2) = size( x2 )
                    coordtype(2) = c2
            case( 3 )
                    x( 1:size( x3 ), 3 ) = x3
                    gshape(3) = size( x3 )
                    coordtype(3) = c3
            case( 4 )
                    x( 1:size( x4 ), 4 ) = x4
                    gshape(4) = size( x4 )
                    coordtype(4) = c4
            case( 5 )
                    x( 1:size( x5 ), 5 ) = x5
                    gshape(5) = size( x5 )
                    coordtype(5) = c5
            case( 6 )
                    x( 1:size( x6 ), 6 ) = x6
                    gshape(6) = size( x6 )
                    coordtype(6) = c6
            end select

    end do

    if (present(id) .and. present(periodicSpaces)) then
       call gridSetupStructured( grid, coordtype, gshape, x, internal_output_flag, &
            internal_output_message, id=id, periodicSpaces=periodicSpaces)
    elseif (present(id) .and. (.not. present(periodicSpaces))) then
       call gridSetupStructured( grid, coordtype, gshape, x, internal_output_flag, &
            internal_output_message, id=id)
    elseif ((.not. present(id)) .and. present(periodicSpaces)) then
       call gridSetupStructured( grid, coordtype, gshape, x, internal_output_flag, &
            internal_output_message, periodicSpaces=periodicSpaces)
    else
       call gridSetupStructured( grid, coordtype, gshape, x, internal_output_flag, &
            internal_output_message)
    end if

    if (present(output_flag)) then
       output_flag = internal_output_flag
    endif

    if (internal_output_flag /= 0) then
       if (present(output_message)) then
          if (allocated(internal_output_message)) then
             allocate( character(len(internal_output_message)) :: output_message)
             output_message = internal_output_message
             deallocate(internal_output_message)
          end if
          return
       else
          write(*,*)'in gridSetupStructuredSep, error recieved from gridSetupStructured'
          write(*,*)'   output_flag =',output_flag
          stop 'in ids_grid_structured.f90::gridSetupStructuredSep'
       end if
    endif

    if (allocated(internal_output_message)) deallocate(internal_output_message)

    deallocate(x)
    deallocate(gshape)
    deallocate(coordtype)

  end subroutine gridSetupStructuredSep


  !> Set up a 1d structured space.
  !>
  !> Helper routine used by gridSetupStructured. Sets up a space descriptor for the case
  !> of a simple 1d structured grid with standard connectivity

  subroutine gridSetupStruct1dSpace( space, coordtype, nodes, periodic )
    
    type(ids_generic_grid_dynamic_space), intent(inout) :: space !> The space descriptor to fill
    integer, intent(in) :: coordtype !> The coordinate type of the space
    real(DP), intent(in), dimension(:) :: nodes !> The node positions in the space (assumed to be in increasing order)
    logical, intent(in), optional :: periodic

    ! internal
    integer, parameter :: NDIM = 1 ! this is a 1d grid
    integer :: j_obj

    ! Set coordinate types
    ! (dimension of space = NDIM = size( coordtype )
    allocate( space % coordinates_type(NDIM) )    
    space % coordinates_type(:) = (/ coordtype /)

    ! Allocate object definition arrays
    allocate( space % objects_per_dimension(1) )
    allocate( space % objects_per_dimension(1) % object(NDIM + 1) )

    do j_obj = 1 , NDIM+1
       allocate( space % objects_per_dimension(1) % object(j_obj) % geometry( size(nodes)) )
       space % objects_per_dimension(1) % object(j_obj) % geometry(:) = nodes(:)
    enddo

  end subroutine gridSetupStruct1dSpace


  !> Test whether the given grid descriptor contains a structured
  !> grid in the sense of this service module.
  logical function gridIsStructured( grid )
    type(ids_generic_grid_dynamic),  intent(in) :: grid 
    gridIsStructured = .true.

    !> \todo Function gridIsStructured not properly implemented yet!!

  end function gridIsStructured

  !> Return the axes description of a structured grid. Essentially the equivalent read routine to gridSetupStructured.
  !> 
  !> @param grid The grid descriptor to read from
  !> @param coordtype The coordinate types of the individual axes/spaces
  !> @param gshape Number of grid nodes on the individual axes/spaces
  !> @param x The position of the grid nodes. x(i,s) is the position of node i in space s. 
  !>          All nodes in space s are given by x( 1:gshape(s), s )
  !> @see gridSetupStructured
  subroutine gridStructGetAxes( grid, coordtype, gshape, x, output_flag, output_message)
    type(ids_generic_grid_dynamic),  intent(in) :: grid 
    integer, dimension(:), allocatable, intent(out) :: coordtype, gshape
    real(DP), dimension(:,:), allocatable, intent(out) :: x
    integer, intent(out) :: output_flag
    character(len=:), allocatable :: output_message

    ! internal
    integer :: id, ndim

    if (.not. gridIsStructured( grid ) ) then
       allocate(character(len("gridStructGetAxes: not a structured grid: cpofield%scalar not associated")) :: output_message )
       output_message =       "gridStructGetAxes: not a structured grid"
       output_flag = -3001
       return
    endif
    output_flag=0
    
    ndim = gridNDim( grid )

    allocate( coordtype( ndim ) )
    allocate( gshape( ndim ) )

    coordtype = gridCoordTypes( grid )
    do id = 1, ndim
       gshape( id ) = gridSpaceNNodes( grid%space(id) )
    end do

    allocate( x( 1 : maxval( gshape ), ndim ) )
    
    x = 0.0_DP
    do id = 1, ndim
       ! TODO: support multiple geometries
       x( 1 : gshape( id ), id ) = &
            grid % space( id ) % objects_per_dimension(1) % object(1) % geometry(:)
    end do

  end subroutine gridStructGetAxes


  !> Return the shape (number of points in every dimension) of a structured grid. 
  !> 
  !> @param grid The grid descriptor to read from
  !> @param gshape Number of grid nodes on the individual axes/space
  !> @see gridSetupStructured
  subroutine gridStructGetShape( grid, gshape )
    type(ids_generic_grid_dynamic),  intent(in) :: grid 
    integer, dimension(:), allocatable, intent(out) ::  gshape

    ! internal
    integer :: id, ndim

    if (.not. gridIsStructured( grid )) then
       write(*,*) "gridStructGetShape: not a structured grid"
       stop
    endif

    ndim = gridNDim( grid )

    allocate( gshape( ndim ) )

    do id = 1, ndim
       gshape( id ) = gridSpaceNNodes( grid%space(id) )
    end do

  end subroutine gridStructGetShape




  !============================================================================
  ! WRITE PHYSICAL DATA ON A GRID
  !============================================================================

  subroutine gridStructWriteData1d( grid, cpofield, subgrid, data )
    type(ids_generic_grid_dynamic),  intent(in) :: grid
    integer, intent(in) :: subgrid
    type(ids_generic_grid_scalar), intent(inout) :: cpofield
    real(DP), dimension(:), intent(in) :: data

    call gridWriteDataScalar( cpofield, subgrid, reshape(data, (/ size( data ) /)) )   
  end subroutine gridStructWriteData1d

  subroutine gridStructWriteData2d( grid, cpofield, subgrid, data )
    type(ids_generic_grid_dynamic),  intent(in) :: grid
    integer, intent(in) :: subgrid
    type(ids_generic_grid_scalar), intent(inout) :: cpofield
    real(DP), dimension(:,:), intent(in) :: data

    call gridWriteDataScalar( cpofield, subgrid, reshape(data, (/ size( data ) /)) )  
  end subroutine gridStructWriteData2d

  subroutine gridStructWriteData3d( grid, cpofield, subgrid, data )
    type(ids_generic_grid_dynamic),  intent(in) :: grid
    integer, intent(in) :: subgrid
    type(ids_generic_grid_scalar), intent(inout) :: cpofield
    real(DP), dimension(:,:,:), intent(in) :: data

    call gridWriteDataScalar( cpofield, subgrid, reshape(data, (/ size( data ) /)) )   
  end subroutine gridStructWriteData3d

  subroutine gridStructWriteData4d( grid, cpofield, subgrid, data )
    type(ids_generic_grid_dynamic),  intent(in) :: grid
    integer, intent(in) :: subgrid
    type(ids_generic_grid_scalar), intent(inout) :: cpofield
    real(DP), dimension(:,:,:,:), intent(in) :: data

    call gridWriteDataScalar( cpofield, subgrid, reshape(data, (/ size( data ) /)) )   
  end subroutine gridStructWriteData4d

  subroutine gridStructWriteData5d( grid, cpofield, subgrid, data )
    type(ids_generic_grid_dynamic)r,  intent(in) :: grid
    integer, intent(in) :: subgrid
    type(ids_generic_grid_scalar), intent(inout) :: cpofield
    real(DP), dimension(:,:,:,:,:), intent(in) :: data

    call gridWriteDataScalar( cpofield, subgrid, reshape(data, (/ size( data ) /)) )   
  end subroutine gridStructWriteData5d

  subroutine gridStructWriteData6d( grid, cpofield, subgrid, data )
    type(ids_generic_grid_dynamic),  intent(in) :: grid
    integer, intent(in) :: subgrid
    type(ids_generic_grid_scalar), intent(inout) :: cpofield
    real(DP), dimension(:,:,:,:,:,:), intent(in) :: data

    call gridWriteDataScalar( cpofield, subgrid, reshape(data, (/ size( data ) /)) )   
  end subroutine gridStructWriteData6d

!!$
!!$  subroutine gridStructWriteData1dComplex( grid, cpofield, subgrid, data )
!!$    type(ids_generic_grid_dynamic),  intent(in) :: grid
!!$    integer, intent(in) :: subgrid
!!$    type(type_complexgrid_scalar_cplx), intent(inout) :: cpofield
!!$    complex(DP), dimension(:), intent(in) :: data
!!$
!!$    call gridWriteDataScalarComplex( cpofield, subgrid, reshape(data, (/ size( data ) /)) )   
!!$  end subroutine gridStructWriteData1dComplex
!!$
!!$  subroutine gridStructWriteData2dComplex( grid, cpofield, subgrid, data )
!!$    type(ids_generic_grid_dynamic),  intent(in) :: grid
!!$    integer, intent(in) :: subgrid
!!$    type(type_complexgrid_scalar_cplx), intent(inout) :: cpofield
!!$    complex(DP), dimension(:,:), intent(in) :: data
!!$
!!$    call gridWriteDataScalarComplex( cpofield, subgrid, reshape(data, (/ size( data ) /)) )   
!!$  end subroutine gridStructWriteData2dComplex
!!$


  subroutine gridWriteDataScalar( cpofield, subgrid , data )
    type(ids_generic_grid_scalar), intent(inout) :: cpofield
    integer, intent(in) :: subgrid
    real(DP), dimension(:), intent(in) :: data

    ! Make sure the data field is properly allocated
    if ( associated( cpoField % values ) ) then
        if ( .not. size( cpoField % values ) == size(data) ) then
            deallocate( cpoField % values )
        end if
    end if
    ! If required, allocate storage
    if ( .not. associated( cpoField % values ) ) then
        allocate( cpoField % values ( size(data) ))
    end if

    ! copy data
    cpoField % values (:) = data (:)

  end subroutine gridWriteDataScalar


  !============================================================================
  ! WRITE VECTOR COMPONENTS
  !============================================================================

  subroutine gridWriteDataVectorComponent1d( cpofield, subgrid , data )
    real(DP), pointer :: cpofield(:)
    integer, intent(in) :: subgrid
    real(DP), dimension(:), intent(in) :: data

    ! Make sure the data field is properly allocated
    if ( associated( cpofield ) ) then
        if ( .not. size( cpofield ) == size(data) ) then
            deallocate( cpofield )
        end if
    end if
    ! If required, allocate storage
    if ( .not. associated( cpofield ) ) then
        allocate( cpofield ( size(data) ))
    end if

    ! copy data
    cpofield (:) = data (:)
  end subroutine gridWriteDataVectorComponent1d

  subroutine gridWriteDataVectorComponent2d( cpofield, subgrid , data )
    real(DP), pointer :: cpofield(:)
    integer, intent(in) :: subgrid
    real(DP), dimension(:,:), intent(in) :: data

    ! Make sure the data field is properly allocated
    if ( associated( cpofield ) ) then
        if ( .not. size( cpofield ) == size(data) ) then
            deallocate( cpofield )
        end if
    end if
    ! If required, allocate storage
    if ( .not. associated( cpofield ) ) then
        allocate( cpofield ( size(data) ))
    end if

    ! copy data
    cpofield (:) = reshape( data , size(data) )
  end subroutine gridWriteDataVectorComponent2d
  
  subroutine gridWriteDataVectorComponent3d( cpofield, subgrid , data )
    real(DP), pointer :: cpofield(:)
    integer, intent(in) :: subgrid
    real(DP), dimension(:,:,:), intent(in) :: data

    ! Make sure the data field is properly allocated
    if ( associated( cpofield ) ) then
        if ( .not. size( cpofield ) == size(data) ) then
            deallocate( cpofield )
        end if
    end if
    ! If required, allocate storage
    if ( .not. associated( cpofield ) ) then
        allocate( cpofield ( size(data) ))
    end if

    ! copy data
    cpofield (:) = reshape( data , size(data) )
  end subroutine gridWriteDataVectorComponent3d

  subroutine gridWriteDataVectorComponent4d( cpofield, subgrid , data )
    real(DP), pointer :: cpofield(:)
    integer, intent(in) :: subgrid
    real(DP), dimension(:,:,:,:), intent(in) :: data

    ! Make sure the data field is properly allocated
    if ( associated( cpofield ) ) then
        if ( .not. size( cpofield ) == size(data) ) then
            deallocate( cpofield )
        end if
    end if
    ! If required, allocate storage
    if ( .not. associated( cpofield ) ) then
        allocate( cpofield ( size(data) ))
    end if

    ! copy data
    cpofield (:) = reshape( data , size(data) )
  end subroutine gridWriteDataVectorComponent4d

  subroutine gridWriteDataVectorComponent5d( cpofield, subgrid , data )
    real(DP), pointer :: cpofield(:)
    integer, intent(in) :: subgrid
    real(DP), dimension(:,:,:,:,:), intent(in) :: data

    ! Make sure the data field is properly allocated
    if ( associated( cpofield ) ) then
        if ( .not. size( cpofield ) == size(data) ) then
            deallocate( cpofield )
        end if
    end if
    ! If required, allocate storage
    if ( .not. associated( cpofield ) ) then
        allocate( cpofield ( size(data) ))
    end if

    ! copy data
    cpofield (:) = reshape( data , size(data) )
  end subroutine gridWriteDataVectorComponent5d

  !============================================================================
  ! READ A DATA BODY
  !============================================================================


  !> Body of the data read routine for data arrays with arbitrary rank
  subroutine gridStructReadDataBody( grid, cpofield, subgrid, gshape, output_flag, output_message )
    type(ids_generic_grid_dynamic),  intent(in) :: grid
    integer, intent(in) :: subgrid
    type(ids_generic_grid_scalar), intent(in) :: cpofield
    integer, dimension(:),  intent(in) :: gshape
    integer, intent(out) :: output_flag
    character(len=:), allocatable :: output_message

    if (.not. associated( cpofield%values ) ) then
       allocate(character(len("gridStructReadDataBody: cpofield%scalar not associated")) :: output_message )
       output_message =       "gridStructReadDataBody: cpofield%scalar not associated"
       output_flag = -4001
       return
    endif
    output_flag=0

  end subroutine gridStructReadDataBody


  subroutine gridStructReadData1d( grid, cpofield, subgrid, data, output_flag, output_message)
    type(ids_generic_grid_dynamic),  intent(in) :: grid
    integer, intent(in) :: subgrid
    type(ids_generic_grid_scalar), intent(in) :: cpofield
    real(DP), dimension(:), intent(out) :: data
    integer :: output_flag
    character(len=:), allocatable :: output_message
    call gridStructReadDataBody( grid, cpofield, subgrid, shape(data), output_flag, output_message)
    if (output_flag == 0) then
       data = reshape( cpofield%values, shape(data) )
    endif
  end subroutine gridStructReadData1d

  subroutine gridStructReadData2d( grid, cpofield, subgrid, data, output_flag, output_message)
    type(ids_generic_grid_dynamic),  intent(in) :: grid
    integer, intent(in) :: subgrid
    type(ids_generic_grid_scalar), intent(in) :: cpofield
    real(DP), dimension(:,:), intent(out) :: data
    integer :: output_flag
    character(len=:), allocatable :: output_message
    call gridStructReadDataBody( grid, cpofield, subgrid, shape(data), output_flag, output_message)
    if (output_flag == 0) then
       data = reshape( cpofield%values, shape(data) )
    endif
  end subroutine gridStructReadData2d

  subroutine gridStructReadData3d( grid, cpofield, subgrid, data, output_flag, output_message)
    type(ids_generic_grid_dynamic),  intent(in) :: grid
    integer, intent(in) :: subgrid
    type(ids_generic_grid_scalar), intent(in) :: cpofield
    real(DP), dimension(:,:,:), intent(out) :: data
    integer :: output_flag
    character(len=:), allocatable :: output_message
    call gridStructReadDataBody( grid, cpofield, subgrid, shape(data), output_flag, output_message)
    if (output_flag == 0) then
       data = reshape( cpofield%values, shape(data) )
    endif
  end subroutine gridStructReadData3d

  subroutine gridStructReadData4d( grid, cpofield, subgrid, data, output_flag, output_message)
    type(ids_generic_grid_dynamic),  intent(in) :: grid
    integer, intent(in) :: subgrid
    type(ids_generic_grid_scalar), intent(in) :: cpofield
    real(DP), dimension(:,:,:,:), intent(out) :: data
    integer :: output_flag
    character(len=:), allocatable :: output_message
    call gridStructReadDataBody( grid, cpofield, subgrid, shape(data), output_flag, output_message)
    if (output_flag == 0) then
       data = reshape( cpofield%values, shape(data) )
    endif
  end subroutine gridStructReadData4d

  subroutine gridStructReadData5d( grid, cpofield, subgrid, data, output_flag, output_message)
    type(ids_generic_grid_dynamic),  intent(in) :: grid
    integer, intent(in) :: subgrid
    type(ids_generic_grid_scalar), intent(in) :: cpofield
    real(DP), dimension(:,:,:,:,:), intent(out) :: data
    integer :: output_flag
    character(len=:), allocatable :: output_message
    call gridStructReadDataBody( grid, cpofield, subgrid, shape(data), output_flag, output_message)
    if (output_flag == 0) then
       data = reshape( cpofield%values, shape(data) )
    endif
  end subroutine gridStructReadData5d

  subroutine gridStructReadData6d( grid, cpofield, subgrid, data, output_flag, output_message)
    type(ids_generic_grid_dynamic),  intent(in) :: grid
    integer, intent(in) :: subgrid
    type(ids_generic_grid_scalar), intent(in) :: cpofield
    real(DP), dimension(:,:,:,:,:,:), intent(out) :: data
    integer :: output_flag
    character(len=:), allocatable :: output_message
    call gridStructReadDataBody( grid, cpofield, subgrid, shape(data), output_flag, output_message)
    if (output_flag == 0) then
       data = reshape( cpofield%values, shape(data) )
    endif
  end subroutine gridStructReadData6d

  !============================================================================
  ! READ A DATA BODY OF VECTOR COMPONENT
  !============================================================================

  subroutine gridStructReadDataVectorComponent1d( cpofield , data , output_flag, output_message)
    real(DP), dimension(:), intent(in) :: cpofield
    real(DP), dimension(:), intent(inout) :: data
    integer :: output_flag
    character(len=:), allocatable :: output_message

    if (.not.associated(cpofield)) then
       output_flag = -1
       output_message = "Error in gridStructReadData1d: Input field no associated"
       return
    end if
    if (associated(data)) then
       if (size(data) .ne. size(cpofield)) then
          deallocate(data)
       end if
    end if
    if (.not.associated(data)) then
       allocate(data(size(cpofield)))
    endif
    if (output_flag == 0) then
       data = reshape( cpofield , shape(data) )
    endif
  end subroutine gridStructReadDataVectorComponent1d

  subroutine gridStructReadDataVectorComponent2d( cpofield , data , output_flag, output_message)
    real(DP), dimension(:), intent(in) :: cpofield
    real(DP), dimension(:,:), intent(inout) :: data
    integer :: output_flag
    character(len=:), allocatable :: output_message

    if (.not.associated(cpofield)) then
       output_flag = -1
       output_message = "Error in gridStructReadData2d: Input field no associated"
       return
    end if
    if (associated(data)) then
       if (size(data) .ne. size(cpofield)) then
          output_flag = -2
          output_message = "Error in gridStructReadData2d: Output field has the wrong size"
          return
       end if
    else
       output_flag = -3
       output_message = "Error in gridStructReadData2d: Output field no associated"
       return
    endif
    if (output_flag == 0) then
       data = reshape( cpofield , shape(data) )
    endif
  end subroutine gridStructReadDataVectorComponent2d

  subroutine gridStructReadDataVectorComponent3d( cpofield , data , output_flag, output_message)
    real(DP), dimension(:), intent(in) :: cpofield
    real(DP), dimension(:,:,:), intent(inout) :: data
    integer :: output_flag
    character(len=:), allocatable :: output_message

    if (.not.associated(cpofield)) then
       output_flag = -1
       output_message = "Error in gridStructReadData3d: Input field no associated"
       return
    end if
    if (associated(data)) then
       if (size(data) .ne. size(cpofield)) then
          output_flag = -2
          output_message = "Error in gridStructReadData3d: Output field has the wrong size"
          return
       end if
    else
       output_flag = -3
       output_message = "Error in gridStructReadData3d: Output field no associated"
       return
    endif
    if (output_flag == 0) then
       data = reshape( cpofield , shape(data) )
    endif
  end subroutine gridStructReadDataVectorComponent3d

  subroutine gridStructReadDataVectorComponent4d( cpofield , data , output_flag, output_message)
    real(DP), dimension(:), intent(in) :: cpofield
    real(DP), dimension(:,:,:,:), intent(inout) :: data
    integer :: output_flag
    character(len=:), allocatable :: output_message

    if (.not.associated(cpofield)) then
       output_flag = -1
       output_message = "Error in gridStructReadData4d: Input field no associated"
       return
    end if
    if (associated(data)) then
       if (size(data) .ne. size(cpofield)) then
          output_flag = -2
          output_message = "Error in gridStructReadData4d: Output field has the wrong size"
          return
       end if
    else
       output_flag = -3
       output_message = "Error in gridStructReadData34: Output field no associated"
       return
    endif
    if (output_flag == 0) then
       data = reshape( cpofield , shape(data) )
    endif
  end subroutine gridStructReadDataVectorComponent4d

end module ids_grid_structured

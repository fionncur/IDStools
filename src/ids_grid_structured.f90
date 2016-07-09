module ids_grid_structured

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

  interface gridStructWriteData
     module procedure gridStructWriteData1d, gridStructWriteData2d , gridStructWriteData3d ,&
          & gridStructWriteData4d, gridStructWriteData5d, gridStructWriteData6d !, &
!          & gridStructWriteData1dComplex, gridStructWriteData2dComplex
  end interface

  interface gridStructReadData
     module procedure gridStructReadData1d, gridStructReadData2d, gridStructReadData3d , &
          & gridStructReadData4d, gridStructReadData5d, gridStructReadData6d !, &
!          & gridStructReadData1dComplex, gridStructReadData2dComplex
  end interface

contains

  !============================================================================
  ! WRITE A GRID
  !============================================================================

  !> Write a n-dimensional structured grid 
  !> into a grid descriptor, as well as the default subgrids for objects of all dimensions.
  !>
  !> The dimension n of the grid is taken as size(coordtype).
  !> 
  !> @param grid Grid descriptor to fill
  !> \param coordtype Dimension(n). Defines coordinate types / labels for the 
  !>                  individual axes. See the 
  !>                  constants defined in itm_grid.f90 (COORDTYPE_*)
  !> \param gshape    Dimension(n). Shape of the grid. In dimension i the grid 
  !>                  has shape(i) grid points.
  !> @param x         Dimension( maxval( gshape(n) ), n ). 
  !>                  Grid node coordinates in the individual dimensions. 
  !>                  The node positions in  space i are given by 
  !>                  x( 1 : gshape( i ), id ).
  !> @param periodicSpaces Optional integer array containing the indices
  !>                  of the coordinate directions that are periodic. This will
  !>                  result in the last node in these coordinate directions to
  !>                  be connected to the first node by an edge. Note that if periodic
  !>                  spaces are present, no metric information is computed.
  !> @param uid A unique identifier number for the          
  !>
  !> @see gridSetupStructuredSep
  !>
  !> NOTE: This routines is a modified version of the ITM (EUIM) routine \c gridSetupStructured
  !>       adapted to IDSs by Thomas Jonsson 8 July 2016.
  !>       During the adaptation the functionality was reduced:
  !>        - sub-grid are no longer generated (removed optional input \c createSubgrids);
  !>        - metric information is no longer calculated on the grid (removed optional
  !>          input \c computeMeasures).
  !>       During the adaptation calls to the itm_assert library were replaced by returning
  !>       \c output_flag and an \c output_message. This modification may be forwarded  
  !>       to the ITM version of the subroutine. 
  !>
  subroutine gridSetupStructured( grid, coordtype, gshape, x, output_flag, output_message, id, periodicSpaces)
    type(ids_generic_grid_dynamic), intent(out) :: grid 
    integer, dimension(:), intent(in) :: coordtype
    integer, dimension(size(coordtype)), intent(in) :: gshape
    real(DP), dimension(:, :), intent(in) :: x
    character(*), intent(in), optional :: id
    integer, intent(in), optional :: periodicSpaces(:)
    integer, intent(out) :: output_flag
    character(len=:), allocatable, intent(out) :: output_message

    ! Internal
    integer :: ndim, idim
    logical :: periodic
    
    if ( size( coordtype ) /= size( gshape ) ) then
       allocate(character(len("gridWriteStructured: size of coordtype and gshape don't match")) :: output_message )
       output_message =       "gridWriteStructured: size of coordtype and gshape don't match"
       output_flag = -1
       return
    endif
    if ( maxval( shape( x ) ) < maxval( gshape ) ) then
       allocate(character(len("gridWriteStructured: shape of x seems to be inconsistent with gshape")) :: output_message )
       output_message =       "gridWriteStructured: shape of x seems to be inconsistent with gshape"
       output_flag = -2
       return
    endif
    output_flag = 0

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


  subroutine gridSetupStruct1dSpace( space, coordtype, nodes, periodic )
    !
    !  space%geometry_type% <- identifier
    !  space%coordinates_type(:)% <- integer = coordtype!!
    !  space%objects_per_dimension(:)  <- ids_generic_grid_dynamic_space_dimension
    !  space%objects_per_dimension(:)%object(:)  <- ids_generic_grid_dynamic_space_dimension_object
    !   - ids_generic_grid_dynamic_space_dimension_object: { boundary , geometry , geometry_error_upper , geometry_error_lower , geometry_error_index , measure , measure_error_upper , measure_error_lower , measure_error_index }
    
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
       output_flag = 1010
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


  logical function gridIsStructured( grid )
    type(ids_generic_grid_dynamic),  intent(in) :: grid 
    gridIsStructured = .true.
  end function gridIsStructured


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
    type(ids_generic_grid_dynamic),  intent(in) :: grid
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
       output_flag = 1003
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


end module ids_grid_structured

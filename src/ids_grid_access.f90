module ids_grid_access_light
  !>
  !> Translations of all subroutines and functions in EU-ITM (EUIM) module itm_grid_access.
  !> The only exception is \c gridNodeCoord for which the translation is
  !> incomplete (it is not clear how to index the arrays).
  !>
  !> Relations between types in IMAS (ids_schemas) and EU-ITM (euitm_schemas):
  !>   type_complexgrid -> ids_generic_grid_dynamic
  !>   type_complexgrid_space -> ids_generic_grid_dynamic_space
  !>
  !> Warning 1: There are stops in the functions:
  !>            gridSpaceNObject, gridSpaceMaxNBoundaries, gridNodeIndex
  !> Warning 2: The translation from ITM to IMAS is assumes we never use more
  !>            than one "objects_per_dimension".
  !> Warning 3: The translation of gridNodeCoord is incomplete.
  
  use ids_schemas, only: DP=>ids_real, ids_generic_grid_dynamic, ids_generic_grid_dynamic_space

  implicit none

contains

  !> Return the UID number of this grid
  pure integer function gridUid( grid )
    type(ids_generic_grid_dynamic), intent(in) :: grid

    gridUid = grid % identifier % index
  end function gridUid

  !> Return the ID string of this grid
  character(132) function gridId(grid) 
    type(ids_generic_grid_dynamic), intent(in) :: grid

    gridId = repeat(' ', 132)
    if (associated( grid % identifier % name )) then
        if (len( grid % identifier % name ) > 0) then
            gridId = grid % identifier % name (1)
        end if
    end if
  end function gridId

  !> Return total dimension of the grid described by a given grid descriptor.
  pure integer function gridNDim( grid )
    type(ids_generic_grid_dynamic), intent(in) :: grid

    ! internal
    integer :: i

    gridNDim = 0
    do i = 1, size( grid % space ) 
       gridNDim = gridNDim + size( grid % space( i ) % coordinates_type )
    end do

  end function gridNDim

  !> Return the number of spaces in a grid description.
  pure integer function gridNSpace( grid )
    type(ids_generic_grid_dynamic), intent(in) :: grid
    
    gridNSpace = size( grid % space ) 
  end function gridNSpace

  !> Return the dimension of an individual space.
  pure integer function gridSpaceNDim( space )
    type(ids_generic_grid_dynamic_space), intent(in) :: space

    gridSpaceNDim = size( space % coordinates_type )
  end function gridSpaceNDim

  !> Returns the dimension of all individual spaces
  pure function gridSpaceNDims( grid ) result( dims )
    type(ids_generic_grid_dynamic), intent(in) :: grid
    integer, dimension( size( grid % space ) ) :: dims

    ! internal
    integer :: i

    do i = 1, size( grid % space ) 
       dims( i ) = gridSpaceNDim( grid % space( i ) ) 
    end do

  end function gridSpaceNDims

  !> Returns the highest dimension for which objects are defined in the space
  pure function gridSpaceMaxObjDim( space ) result( dim )
    type(ids_generic_grid_dynamic_space), intent(in) :: space
    integer :: dim
   
    dim = 0
    if (associated(space % objects_per_dimension)) then
       if (size(space % objects_per_dimension) > 0) then
          if (associated(space % objects_per_dimension(1) % object)) then
             dim = size(space % objects_per_dimension(1) % object) - 1
          end if
       end if
    end if
  end function gridSpaceMaxObjDim

  !> Return number of nodes (0d-objects) in the space.
  pure integer function gridSpaceNNodes( space )
    type(ids_generic_grid_dynamic_space), intent(in) :: space

    gridSpaceNNodes = 0
    if (associated(space % objects_per_dimension)) then
       if (size(space % objects_per_dimension) > 0) then
          if (associated( space % objects_per_dimension(1) % object(1) % geometry )) then
             gridSpaceNNodes = size( space % objects_per_dimension(1) % object(1) % geometry, 1 )
          end if
       end if
    end if
  end function gridSpaceNNodes

  !> Get the total number of objects 
  !> of the given dimension in the given space
  integer function gridSpaceNObject( space, dim ) result( objcount )
    type(ids_generic_grid_dynamic_space), intent(in) :: space
    integer, intent(in) :: dim

    if (.not. ( &
         ( dim >= 0 ) .and. ( dim <= gridSpaceNdim( space ) ) )) then
       write(*,*) "ERROR in gridSpaceNObject: dim out of bounds"
       stop
    endif

    if ( dim == 0 ) then
        objcount = gridSpaceNNodes( space )
    else
        objcount = 0
        if (associated(space % objects_per_dimension)) then
           if (size(space % objects_per_dimension) > 0) then
              if (associated(space % objects_per_dimension(1) % object)) then
                 if ( dim <= size(space % objects_per_dimension(1) % object) ) then
                    objcount = size( space % objects_per_dimension(1) % object(dim+1) % boundary, 1 )
                 end if
              end if
           end if
        end if
     end if
   end function gridSpaceNObject

  !> Return maximum number of boundaries an object of dimension dim can have in the space.
  integer function gridSpaceMaxNBoundaries( space, dim ) 
    type(ids_generic_grid_dynamic_space), intent(in) :: space
    integer, intent(in) :: dim

    logical :: valid

    valid=.false.

    if (associated(space % objects_per_dimension)) then
       if (size(space % objects_per_dimension) > 0) then
          if (associated(space % objects_per_dimension(1) % object)) then
             if (size(space % objects_per_dimension(1) % object) >= dim+1) then
                if (associated(space % objects_per_dimension(1) % object(dim+1) % boundary)) then
                   gridSpaceMaxNBoundaries = size( space % objects_per_dimension(1) % object(dim+1) % boundary )
                   valid = .true.
                end if
             end if
          end if
       end if
    end if

    if (.not. valid) then
       write(*,*)'ERROR in gridSpaceMaxNBoundaries: the requested object ', &
            '( space % objects_per_dimension(1) % object(dim+1) % boundary )',&
            'is not associated for dim=',dim
       stop 'in ids_grid_access::gridSpaceMaxNBoundaries'
    endif
  end function gridSpaceMaxNBoundaries

  !> Returns the coordinate types for the individual dimensions of the grid
  !> @note Can be made pure by replacing gridSpaceNDim
  function gridCoordTypes( grid ) result( coordtype ) 
    type(ids_generic_grid_dynamic), intent(in) :: grid
    integer, dimension( gridNDim( grid ) ) :: coordtype

    ! internal
    integer :: is, ic, sdim

    ic = 0
    do is = 1, gridNSpace( grid )
       sdim = gridSpaceNDim( grid % space(is) )
       ! TODO: add treatement of multiple geometries here 
       coordtype( ic + 1 : ic + sdim ) &
            & = grid % space(is) % coordinates_type ( 1 : sdim )
       ic = ic + sdim
    end do

  end function gridCoordTypes

  !> Returns index of a node according to the implicit ordering rules for the grid descriptor
  integer function gridNodeIndex( grid, nodeind ) result( index )
    type(ids_generic_grid_dynamic), intent(in) :: grid
    integer, dimension(:), intent(in) :: nodeind
    
    ! internal
    integer :: i, s

    if (.not. ( size( nodeind ) == size( grid % space ) )) then
       write(*,*) "gridNodeIndex: size of nodeind does not match the grid description"
       stop
    end if
    
    index = nodeind(1)
    s = gridSpaceNNodes( grid % space(1) )

    do i = 2, size( grid % space )
       index = index + s * ( nodeind( i ) - 1 )
       s = s * gridSpaceNNodes( grid % space(i) ) 
    end do
    
  end function gridNodeIndex


  !> Get the coordinates of a node according to it's index tuple (assuming
  !> the default geometry representation.
  function gridNodeCoord( grid, nodeind ) result ( coord )
    type(ids_generic_grid_dynamic), intent(in) :: grid
    integer, dimension(gridNSpace(grid)), intent(in) :: nodeind
    real(DP), dimension( gridNDim( grid ) ) :: coord
    
    ! internal   
    integer :: is, id, nd

    if (.not. ( size( nodeind ) == size( grid % space ) )) then
       write(*,*) "gridNodeCoord: size of nodeind does not match the grid description"
       stop
    end if
    
    ! FIXME: add test for default geometry representation.

    coord = 0.0_DP

    id = 0 ! coordinate counter
    do is = 1, gridNSpace( grid )
       ! get dimension of current space
       nd = gridSpaceNDim( grid % space(is) )
       ! copy coordinates
       ! TODO: add handling of multiple geometries here



       write(*,*)'=============================================='
       write(*,*)'ABORTING IN gridNodeCoord'
       write(*,*)'Function still under construction.'
       write(*,*)'Do not know how to index object.'
       write(*,*)'=============================================='
       stop 'in ids_grid_access::gridNodeCoord'

!!!!       coord(id + 1 : id + nd ) = grid % space( is ) % objects_per_dimension( ? ) % object(1) % geometry( ? )




       ! increase coordinate counter
       id = id + nd
    end do

  end function gridNodeCoord

end module ids_grid_access_light

% Returns the coordinate types for the individual dimensions of the grid
% @note Can be made pure by replacing gridSpaceNDim
function [coordtype]=gridCoordTypes( grid )
  ic = 0;
  for is = 1:gridNSpace( grid )
    sdim = gridSpaceNDim( grid.space(is) );
    % TODO: add treatement of multiple geometries here 
    coordtype( ic + 1 : ic + sdim ) = grid.space(is).coordinates_type( 1 : sdim, 1 );
    ic = ic + sdim;
  end
end

% Returns the dimension of all individual spaces
function [dims] = gridSpaceNDims( grid )
  if isfield(grid , 'space')
    dims=zeros( 1 , length( grid.space ) );
    for i = 1:length( grid.space ) 
      dims( i ) = gridSpaceNDim( grid.space( i ) ) ;
    end
  else
    disp('Warning in gridSpaceNDims: grid-struct has no field space');
    dims = [];
  end
end

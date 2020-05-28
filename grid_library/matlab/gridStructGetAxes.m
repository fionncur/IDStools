function [ axes, coordtype , gshape , x ] = gridStructGetAxes( grid )
  %
  % function [ axes, coordtype , gshape , x ] = gridStructGetAxes( grid )
  %

  axes=[];
  if not( gridIsStructured( grid ) )
    ME = MException('ids:ggd:gridStructGetAxes:grid_not_structured',...
		    'The input argument grid does not represent a structured grid');
    throw(ME);
  end

  ndim = gridNDim( grid );

  % Output 1: coordtype
  coordtype = gridCoordTypes( grid );
  
  % Output 2: gshape
  gshape = gridStructGetShape( grid );

  % Output 3: x
  x = zeros( max( gshape ) , ndim );
  for id = 1:ndim
    x( 1 : gshape( id ), id ) = grid.space( id ).objects_per_dimension(1).object(1).geometry(:);

    new.coordtype = coordtype(id);
    new.values = x( 1 : gshape( id ), id );
    axes = [axes , new];
  end

end

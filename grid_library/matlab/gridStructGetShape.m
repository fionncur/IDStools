function [gshape] = gridStructGetShape( grid )
  %
  % function [gshape] = gridStructGetShape( grid )
  %
  if not( gridIsStructured( grid ) )
    ME = MException('ids:ggd:gridStructGetShape:not_structured',...
		    'The input argument grid does not describe a structured grid');
    throw(ME);
  end

  ndim = gridNDim( grid );

  gshape = zeros( 1, ndim );
  for id = 1:ndim
    gshape( id ) = gridSpaceNNodes( grid.space(id) );
  end

end

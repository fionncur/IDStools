function ndim = gridNDim( grid )

  if nargin<1
    ME = MException('ids:ggd:gridNDim:Missing_input',...
		    'The function gridNDim requires at least 1 input argument; recieved %d',nargin);
    throw(ME);
  end

  ndim = 0;
  for i = 1:length( grid.space )
    if not( isfield( grid.space(i) , 'coordinates_type' ) )
      ME = MException('ids:ggd:gridNDim:no_field_coordtype',...
		      'Input grid.spaces(%d) has no field coordtype',i);
      throw(ME);
    end
    ndim = ndim + length( grid.space( i ).coordinates_type );
  end
end

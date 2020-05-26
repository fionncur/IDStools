% Body of the data read routine for data arrays with arbitrary rank
function [data] = gridStructReadData( cpofield, grid )

  if nargin<2
    ME = MException('ids:ggd:gridStructReadData:missing_input',...
		    'The function gridStructReadData requires exactly 2 arguments; recieved only %d', nargin);
    throw(ME);
  end
  
  % check whether inputs make basic sense
  if not( isfield( cpofield, 'scalar' ) )
    ME = MException('ids:ggd:gridStructReadData:cpofield_has_no_field_scalar',...
		    'The input argument cpofield has no field scalar');
    throw(ME);
  end

  [gshape] = gridStructGetShape( grid );
  data = reshape( cpofield.scalar , gshape );
end

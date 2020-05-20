% Returns the dimension of all individual spaces
function [n] = gridSpaceNDim( space )
  if isfield(space , 'coordinates_type');
    n = length( space.coordinates_type );
  else
    ME = MException('ids:ggd:gridSpaceNDim:no_coordtype',...
		    'Input argument space has no struct-field coordtype');
    throw(ME);
  end
end

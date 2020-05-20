% Return number of nodes (0d-objects) in the space.
function [n] = gridSpaceNNodes(space)
  n = 0;
  if isfield( space.objects_per_dimension(1).object(1), 'geometry' )
    n = length( space.objects_per_dimension(1).object(1).geometry )
  else
    ME = MException('ids:ggd:gridSpaceNNodes:no_member_geometry',...
		    'Input spaces has no member space.objects_per_dimension(1).object(1).geometry',i);
    throw(ME);
  end
end

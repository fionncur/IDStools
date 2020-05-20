function [isValid,flag] = gridIsValidStructured( grid )
  %
  % function [isValid,flag] = gridValidStructured( grid )
  %
  % Test if grid is a valid structured complex-grid as defined by the IMAS data structure, IDS.
  %
  isValid=false;
  if not( isstruct( grid ) )
    flag=1;
    return
  elseif not( isfield( grid , 'space' ) )
    flag=2;
    return
  elseif not( isvector( grid.space ) )
    flag=3;
    return
  elseif length( grid.space ) == 0
    flag=4;
    return
  end

  for j=1:length(grid.space)

    if not( isfield( grid.space(j) , 'coordinates_type' ) )
      flag=5;
      return
    elseif not( isnumeric( grid.space(j).coordinates_type(1) ) )
      % Note that in general grid.space(j).coordtype is a vector of
      % integers, but for structured grids it has to be a scalar integer
      flag=6;
      return
    elseif not( isfield( grid.space(j) , 'objects_per_dimension' ) )
      flag=7;
      return
    elseif not( length( grid.space(j).objects_per_dimension ) == 1 )
      flag=8;
      return
    end

    for k=1:length( grid.space(j).objects_per_dimension )

      if not( isfield( grid.space(j).objects_per_dimension(k) , 'object' ) )
	flag=9;
	return
      elseif not( length( grid.space(j).objects_per_dimension(k)object ) == 1 )
	flag=10;
	return
      end

      for  n=1:length( grid.space(j).objects_per_dimension(k).object )
	if not( isfield( grid.space(j).objects_per_dimension(k).object(n) , 'geometry' ) )
	  flag=11;
	  return
	elseif not( length( grid.space(j).objects_per_dimension(k).object(n).geometry ) == 1 )
	  flag=12;
	  return
	elseif not( isnumeric( grid.space(j).objects_per_dimension(k).object(n).geometry(1) ) )
	  flag=13;
	  return
	end
      end

    end

  end

  flag=0;
  isValid=true;
end

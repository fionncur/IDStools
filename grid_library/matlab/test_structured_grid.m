
ndim_spaces=[3,5];

clear grid
grid.space=[];
for j=1:length(ndim_spaces)

  clear object objects_per_dimension space
  object.geometry=linspace(0,1,ndim_spaces(j));
  objects_per_dimension.object = [object];
  space.objects_per_dimension = [objects_per_dimension];
  space.coordinates_type = [j];
  grid.space=[grid.space , space];

end


cpofield.scalar = zeros( ndim_spaces );

%----------------------------------------------------

[isValid, flag] = gridIsValidStructured( grid )
disp( sprintf( '--- TEST 1: Is the grid valid? isValid=%d, flag=%d',isValid, flag ) )

disp( sprintf( '--- TEST 2: Is grid striuctured? %d', gridIsStructured( grid ) ) )

disp( sprintf( '--- TEST 3: Dimensionality of the grid = %d', gridNDim( grid ) ) )

disp( sprintf( '--- TEST 4: gridSpaceNNodes') )
NrNodes = gridSpaceNNodes(grid.space(1))
NrNodes = gridSpaceNNodes(grid.space(2))

disp( sprintf( '--- TEST 5: gridCoordTypes') )
coordinates_type = gridCoordTypes( grid )

disp( sprintf( '--- TEST 6: gridGetSpaceDims') )
SpaceDims = gridGetSpaceDims( grid )

disp( sprintf( '--- TEST 7: gridStructGetShape') )
shape = gridStructGetShape( grid )

[ axes, coordtype , gshape , x ] = gridStructGetAxes( grid )

data = gridStructReadData( cpofield , grid )

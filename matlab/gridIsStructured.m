function [isStructured] = gridIsStructured( grid )
  isStructured = min( gridSpaceNDims(grid) == 1 ) == 1;
end

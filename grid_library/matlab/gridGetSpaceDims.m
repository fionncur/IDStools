function SpaceDims = gridGetSpaceDims(grid)

NSpace = length(grid.space);
SpaceDims = zeros(NSpace, 1);
for iSpace = 1 : NSpace;
    SpaceDims(iSpace) = length(grid.space(iSpace).coordinates_type);
end;

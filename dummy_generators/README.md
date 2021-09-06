# Dummy plasma generator for first Plasma

## Description

This program is intended to create a dummy plasma for FP synthetic diagnostics. It takes as arguments the shot and run numbers, and, optionally, the parameters file.

If the parameters file is not present, the file 'FP_parameters.dat' is used.

It takes as input, through an ASCII namelist in the FP_parameters.dat file:
- The location of the plasma, as R0 and Z0 (in meters)
- The radius of the plasma, as R_plasma (in meters)
- The peak electron and ion temperatures (in eV)
- The peak electron density (in m-3)
- A list of impurity species with their concentrations

An example of such a namelist is:
```
 &FP_PARAMETERS
  R0=6.2, Z0=0.0, RADIUS=1.0,
  TE_MAX=400.0, TI_MAX=50.0, NE_MAX=1.0e19,
  N_IMP_SPECIES=3,
  IMPURITIES='Fe','C','O',
  IMP_CONC=0.001,0.02,0.01,
 /
```

It imports a standard wall IDS and limits the plasma radius if chosen so large
that it intersects the wall. It exports an IDS containing a minimal description to serve as a dummy target plasma, consisting of the core_profiles, equilibrium, summary, and wall IDSs. Profiles will be assumed to be parabolic from the given maxima.

## Build instructions

1. Loading dependent modules
```module load IMAS AMNS```
2. Selecting the fortran compiler through FC env variable and compiling
```FC=ifort make```
3. Running with the default parameters
```./FP_dummy_plasma.exe```

## Known issues

Current version of the Fortran code does not compile with gfortran version 10.2.0

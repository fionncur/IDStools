#!/usr/bin/env python
from __future__ import print_function

import imas,os,sys,argparse,copy


def z_shift(equin, shift):
    """Rigidly shift an equilibrium
    Args:
        equil (equilibrium IDS): initial equilibrium
        shift (float): vertical shift in meters
    Returns:
        equilibrium IDS: vertically shifted equilibrium
    """

    equout = copy.deepcopy(equin)
    for itime in range(len(equin.time_slice)):

        for iz in range(len(equin.time_slice[itime].boundary.outline.z)):
            equout.time_slice[itime].boundary.outline.z[iz] = equin.time_slice[itime].boundary.outline.z[iz] + shift

        for iz in range(len(equin.time_slice[itime].boundary.lcfs.z)):
            equout.time_slice[itime].boundary.lcfs.z[iz] = equin.time_slice[itime].boundary.lcfs.z[iz] + shift
        equout.time_slice[itime].boundary.geometric_axis.z = equin.time_slice[itime].boundary.geometric_axis.z + shift

        for ixpt in range(len(equin.time_slice[itime].boundary.x_point)):
            equout.time_slice[itime].boundary.x_point[ixpt].z = equin.time_slice[itime].boundary.x_point[ixpt].z + shift

        for istr in range(len(equin.time_slice[itime].boundary.strike_point)):
            equout.time_slice[itime].boundary.strike_point[istr].z = equin.time_slice[itime].boundary.strike_point[istr].z + shift
        equout.time_slice[itime].boundary.active_limiter_point.z = equin.time_slice[itime].boundary.active_limiter_point.z + shift

        for iz in range(len(equin.time_slice[itime].boundary_separatrix.outline.z)):
            equout.time_slice[itime].boundary_separatrix.outline.z[iz] = equin.time_slice[itime].boundary_separatrix.outline.z[iz] + shift
        equout.time_slice[itime].boundary_separatrix.geometric_axis.z = equin.time_slice[itime].boundary_separatrix.geometric_axis.z + shift

        for ixpt in range(len(equin.time_slice[itime].boundary_separatrix.x_point)):
            equout.time_slice[itime].boundary.x_point[ixpt].z = equin.time_slice[itime].boundary.x_point[ixpt].z + shift

        for istr in range(len(equin.time_slice[itime].boundary.strike_point)):
            equout.time_slice[itime].boundary.strike_point[istr].z = equin.time_slice[itime].boundary.strike_point[istr].z + shift
        equout.time_slice[itime].boundary.active_limiter_point.z = equin.time_slice[itime].boundary.active_limiter_point.z + shift

        for iq in range(len(equin.time_slice[itime].constraints.q)):
            equout.time_slice[itime].constraints.q[iq].position.z = equin.time_slice[itime].constraints.q[iq].position.z + shift

        for ixpt in range(len(equin.time_slice[itime].constraints.x_point)):
            equout.time_slice[itime].constraints.x_point[ixpt].position_measured.z = equin.time_slice[itime].constraints.x_point[ixpt].position_measured.z + shift
        equout.time_slice[itime].constraints.x_point[ixpt].position_reconstructed.z = equin.time_slice[itime].constraints.x_point[ixpt].position_reconstructed.z + shift

        for istr in range(len(equin.time_slice[itime].constraints.strike_point)):
            equout.time_slice[itime].constraints.strike_point[istr].position_measured.z = equin.time_slice[itime].constraints.strike_point[istr].position_measured.z + shift
        equout.time_slice[itime].constraints.strike_point[istr].position_reconstructed.z = equin.time_slice[itime].constraints.strike_point[istr].position_reconstructed.z + shift
        equout.time_slice[itime].global_quantities.magnetic_axis.z = equin.time_slice[itime].global_quantities.magnetic_axis.z + shift

        for iz in range(len(equin.time_slice[itime].profiles_1d.geometric_axis.z)):
            equout.time_slice[itime].profiles_1d.geometric_axis.z[iz] = equin.time_slice[itime].profiles_1d.geometric_axis.z[iz] + shift

        for i2d in range(len(equin.time_slice[itime].profiles_2d)):

            if equin.time_slice[itime].profiles_2d[i2d].grid_type == 1:
                for iz in range(len(equin.time_slice[itime].profiles_2d[i2d].grid.dim2)):
                    equout.time_slice[itime].profiles_2d[i2d].grid.dim2[iz] = equin.time_slice[itime].profiles_2d[i2d].grid.dim2[iz] + shift

            for i1 in range(len(equin.time_slice[itime].profiles_2d[i2d].z)):
                for i2 in range(len(equin.time_slice[itime].profiles_2d[i2d].z[i1])):
                    equout.time_slice[itime].profiles_2d[i2d].z[i1][i2] = equin.time_slice[itime].profiles_2d[i2d].z[i1][i2] + shift

        for iggd in range(len(equin.time_slice[itime].ggd)):
            for iz in range(len(equin.time_slice[itime].ggd[iggd].z)):
                for i in range(len(equin.time_slice[itime].ggd[iggd].z[iz].values)):
                    equout.time_slice[itime].ggd[iggd].z[iz].values[i] = equin.time_slice[itime].ggd[iggd].z[iz].values[i] + shift

        if equin.time_slice[itime].coordinate_system.grid_type == 1:
            for iz in range(len(equin.time_slice[itime].coordinate_system.grid.dim2)):
                equout.time_slice[itime].coordinate_system.grid.dim2[iz] = equin.time_slice[itime].coordinate_system.grid.dim2[iz] + shift

        for i1 in range(len(equin.time_slice[itime].coordinate_system.z)):
            for i2 in range(len(equin.time_slice[itime].coordinate_system.z[i1])):
                equout.time_slice[itime].coordinate_system.z[i1][i2] = equin.time_slice[itime].coordinate_system.z[i1][i2] + shift

    equout.ids_properties.comment = equin.ids_properties.comment+' (shifted vertically by '+str(shift)+' m)'
    return equout



if __name__ == "__main__":
    # This script imports an equilibrium IDS, rigidly shifts it vertically, and then adds it to the output IDS

    # Management of input arguments
    parser = argparse.ArgumentParser(description='Rigidly shifts vertically an equilibrium, storing the output into another entry of the same DB')
    parser.add_argument('-si','--shot_input',help='Input shot number', required=True,type=int)
    parser.add_argument('-ri','--run_input',help='Input run number', required=True,type=int)
    parser.add_argument('-so','--shot_output',help='Output shot number', required=True,type=int)
    parser.add_argument('-ro','--run_output',help='Output run number', required=True,type=int)
    parser.add_argument('-u','--user_or_path',help='User or absolute path name of the DB where the data-entry is located (default=%(default)s)',type=str,default=os.getenv('USER'))
    parser.add_argument('-d','--database',help='Database name of the DB where the data-entry is located (default=%(default)s)',type=str,default='iter')
    parser.add_argument('-s','--shift',help='Upward shift of equilibrium (m)',type=float,required=True)

    args = parser.parse_args()
    # ids_shift_eq -si 131035 -ri 124 -so 123001 -ro 1 -s -0.01 -u bonninx -d iter

    shot_in      = args.shot_input
    run_in       = args.run_input
    shot_out     = args.shot_output
    run_out      = args.run_output
    shift        = args.shift
    user_or_path = args.user_or_path
    database     = args.database
    #version      = os.getenv('IMAS_VERSION')[0]

    # OPEN INPUT
    input = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,database,shot_in,run_in,user_or_path)
    status,idx = input.open()
    if (status!=0):
        print("Can't open the input pulse file!")
        sys.exit(1)
        
    equin = input.get("equilibrium")

    # OPEN OUTPUT
    output = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,database,shot_out,run_out,user_or_path)
    status,idx = output.open()
    if (status!=0):
        print("Can't open the output pulse file!")
        sys.exit(1)

    print ('Shifting equilibrium by '+str(shift)+' m')
    equout = z_shift(equin, shift)

    # PUT IDS INTO OUTPUT
    output.put(equout)

    # CLOSE FILES
    input.close()
    output.close()


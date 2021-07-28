#!/usr/bin/env python
from __future__ import print_function

import imas,os,sys,argparse,copy
from imas import imasdef
import distutils.version as version

def equilibrium_rescale(equin, rescale):
    """Rescale the magnetic field in an equilibrium
    Args:
        equil (equilibrium IDS): initial equilibrium
        rescale (float): rescaling factor for magnetic field
    Returns:
        equilibrium IDS: rescaled equilibrium
    """

    dd_version = equin.ids_properties.version_put.data_dictionary

    equout = copy.deepcopy(equin)

    for itime in range(len(equin.vacuum_toroidal_field.b0)):
        equout.vacuum_toroidal_field.b0[itime] = equin.vacuum_toroidal_field.b0[itime] * rescale

    for itime in range(len(equin.time_slice)):

        if (imasdef.isFieldValid(equin.time_slice[itime].boundary.psi)):
            equout.time_slice[itime].boundary.psi = equin.time_slice[itime].boundary.psi * rescale

        if (imasdef.isFieldValid(equin.time_slice[itime].boundary_separatrix.psi)):
            equout.time_slice[itime].boundary_separatrix.psi = equin.time_slice[itime].boundary_separatrix.psi * rescale

        if (version.StrictVersion(dd_version) > version.StrictVersion('3.31.0')):
            if (imasdef.isFieldValid(equin.time_slice[itime].boundary_secondary_separatrix.psi)):
                equout.time_slice[itime].boundary_secondary_separatrix.psi = equin.time_slice[itime].boundary_secondary_separatrix.psi * rescale

        if (imasdef.isFieldValid(equin.time_slice[itime].constraints.b_field_tor_vacuum_r.measured)):
            equout.time_slice[itime].constraints.b_field_tor_vacuum_r.measured = equin.time_slice[itime].constraints.b_field_tor_vacuum_r.measured * rescale

        if (imasdef.isFieldValid(equin.time_slice[itime].constraints.b_field_tor_vacuum_r.reconstructed)):
            equout.time_slice[itime].constraints.b_field_tor_vacuum_r.reconstructed = equin.time_slice[itime].constraints.b_field_tor_vacuum_r.reconstructed * rescale

        for i1 in range(len(equin.time_slice[itime].constraints.bpol_probe)):
            equout.time_slice[itime].constraints.bpol_probe[i1].measured = equin.time_slice[itime].constraints.bpol_probe[i1].measured * rescale
            equout.time_slice[itime].constraints.bpol_probe[i1].reconstructed = equin.time_slice[itime].constraints.bpol_probe[i1].reconstructed * rescale

        if (imasdef.isFieldValid(equin.time_slice[itime].constraints.diamagnetic_flux.measured)):
            equout.time_slice[itime].constraints.diamagnetic_flux.measured = equin.time_slice[itime].constraints.diamagnetic_flux.measured * rescale

        if (imasdef.isFieldValid(equin.time_slice[itime].constraints.diamagnetic_flux.reconstructed)):
            equout.time_slice[itime].constraints.diamagnetic_flux.reconstructed = equin.time_slice[itime].constraints.diamagnetic_flux.reconstructed * rescale

        for i1 in range(len(equin.time_slice[itime].constraints.faraday_angle)):
            equout.time_slice[itime].constraints.faraday_angle[i1].measured = equin.time_slice[itime].constraints.faraday_angle[i1].measured * rescale
            equout.time_slice[itime].constraints.faraday_angle[i1].reconstructed = equin.time_slice[itime].constraints.faraday_angle[i1].reconstructed * rescale

        for i1 in range(len(equin.time_slice[itime].constraints.flux_loop)):
            equout.time_slice[itime].constraints.flux_loop[i1].measured = equin.time_slice[itime].constraints.flux_loop[i1].measured * rescale
            equout.time_slice[itime].constraints.flux_loop[i1].reconstructed = equin.time_slice[itime].constraints.flux_loop[i1].reconstructed * rescale

        if (imasdef.isFieldValid(equin.time_slice[itime].constraints.ip.measured)):
            equout.time_slice[itime].constraints.ip.imeasured = equin.time_slice[itime].constraints.ip.measured * rescale

        if (imasdef.isFieldValid(equin.time_slice[itime].constraints.ip.reconstructed)):
            equout.time_slice[itime].constraints.ip.reconstructed = equin.time_slice[itime].constraints.ip.reconstructed * rescale

        if (imasdef.isFieldValid(equin.time_slice[itime].global_quantities.ip)):
            equout.time_slice[itime].global_quantities.ip = equin.time_slice[itime].global_quantities.ip * rescale

        if (imasdef.isFieldValid(equin.time_slice[itime].global_quantities.psi_axis)):
            equout.time_slice[itime].global_quantities.psi_axis = equin.time_slice[itime].global_quantities.psi_axis * rescale

        if (imasdef.isFieldValid(equin.time_slice[itime].global_quantities.psi_boundary)):
            equout.time_slice[itime].global_quantities.psi_boundary = equin.time_slice[itime].global_quantities.psi_boundary * rescale

        if (imasdef.isFieldValid(equin.time_slice[itime].global_quantities.magnetic_axis.b_field_tor)):
            equout.time_slice[itime].global_quantities.magnetic_axis.b_field_tor = equin.time_slice[itime].global_quantities.magnetic_axis.b_field_tor * rescale

        if (version.StrictVersion(dd_version) > version.StrictVersion('3.31.0')):
            if (imasdef.isFieldValid(equin.time_slice[itime].global_quantities.psi_external_average)):
                equout.time_slice[itime].global_quantities.psi_external_average = equin.time_slice[itime].global_quantities.psi_external_average * rescale

        for i1d in range(len(equin.time_slice[itime].profiles_1d.psi)):
            equout.time_slice[itime].profiles_1d.psi[i1d] = equin.time_slice[itime].profiles_1d.psi[i1d] * rescale

        for i1d in range(len(equin.time_slice[itime].profiles_1d.phi)):
            equout.time_slice[itime].profiles_1d.phi[i1d] = equin.time_slice[itime].profiles_1d.phi[i1d] * rescale

        for i1d in range(len(equin.time_slice[itime].profiles_1d.pressure)):
            equout.time_slice[itime].profiles_1d.pressure[i1d] = equin.time_slice[itime].profiles_1d.pressure[i1d] * rescale**2

        for i1d in range(len(equin.time_slice[itime].profiles_1d.f)):
            equout.time_slice[itime].profiles_1d.f[i1d] = equin.time_slice[itime].profiles_1d.f[i1d] * rescale

        for i1d in range(len(equin.time_slice[itime].profiles_1d.dpressure_dpsi)):
            equout.time_slice[itime].profiles_1d.dpressure_dpsi[i1d] = equin.time_slice[itime].profiles_1d.dpressure_dpsi[i1d] * rescale

        for i1d in range(len(equin.time_slice[itime].profiles_1d.f_df_dpsi)):
            equout.time_slice[itime].profiles_1d.f_df_dpsi[i1d] = equin.time_slice[itime].profiles_1d.f_df_dpsi[i1d] * rescale

        for i1d in range(len(equin.time_slice[itime].profiles_1d.j_tor)):
            equout.time_slice[itime].profiles_1d.j_tor[i1d] = equin.time_slice[itime].profiles_1d.j_tor[i1d] * rescale

        for i1d in range(len(equin.time_slice[itime].profiles_1d.j_parallel)):
            equout.time_slice[itime].profiles_1d.j_parallel[i1d] = equin.time_slice[itime].profiles_1d.j_parallel[i1d] * rescale

        for i1d in range(len(equin.time_slice[itime].profiles_1d.gm4)):
            equout.time_slice[itime].profiles_1d.gm4[i1d] = equin.time_slice[itime].profiles_1d.gm4[i1d] / rescale**2

        for i1d in range(len(equin.time_slice[itime].profiles_1d.gm5)):
            equout.time_slice[itime].profiles_1d.gm5[i1d] = equin.time_slice[itime].profiles_1d.gm5[i1d] * rescale**2

        for i1d in range(len(equin.time_slice[itime].profiles_1d.gm6)):
            equout.time_slice[itime].profiles_1d.gm6[i1d] = equin.time_slice[itime].profiles_1d.gm6[i1d] / rescale**2

        for i1d in range(len(equin.time_slice[itime].profiles_1d.b_field_average)):
            equout.time_slice[itime].profiles_1d.b_field_average[i1d] = equin.time_slice[itime].profiles_1d.b_field_average[i1d] * rescale

        for i1d in range(len(equin.time_slice[itime].profiles_1d.b_field_min)):
            equout.time_slice[itime].profiles_1d.b_field_min[i1d] = equin.time_slice[itime].profiles_1d.b_field_min[i1d] * rescale

        for i1d in range(len(equin.time_slice[itime].profiles_1d.b_field_max)):
            equout.time_slice[itime].profiles_1d.b_field_max[i1d] = equin.time_slice[itime].profiles_1d.b_field_max[i1d] * rescale

        for i2d in range(len(equin.time_slice[itime].profiles_2d)):

            for ir in range(len(equin.time_slice[itime].profiles_2d[i2d].psi)):
                for iz in range(len(equin.time_slice[itime].profiles_2d[i2d].psi[ir])):
                    equout.time_slice[itime].profiles_2d[i2d].psi[ir][iz] = equin.time_slice[itime].profiles_2d[i2d].psi[ir][iz] * rescale

            for ir in range(len(equin.time_slice[itime].profiles_2d[i2d].phi)):
                for iz in range(len(equin.time_slice[itime].profiles_2d[i2d].phi[ir])):
                    equout.time_slice[itime].profiles_2d[i2d].phi[ir][iz] = equin.time_slice[itime].profiles_2d[i2d].phi[ir][iz] * rescale

            for ir in range(len(equin.time_slice[itime].profiles_2d[i2d].j_tor)):
                for iz in range(len(equin.time_slice[itime].profiles_2d[i2d].j_tor[ir])):
                    equout.time_slice[itime].profiles_2d[i2d].j_tor[ir][iz] = equin.time_slice[itime].profiles_2d[i2d].j_tor[ir][iz] * rescale

            for ir in range(len(equin.time_slice[itime].profiles_2d[i2d].j_parallel)):
                for iz in range(len(equin.time_slice[itime].profiles_2d[i2d].j_parallel[ir])):
                    equout.time_slice[itime].profiles_2d[i2d].j_parallel[ir][iz] = equin.time_slice[itime].profiles_2d[i2d].j_parallel[ir][iz] * rescale

            for ir in range(len(equin.time_slice[itime].profiles_2d[i2d].b_field_r)):
                for iz in range(len(equin.time_slice[itime].profiles_2d[i2d].b_field_r[ir])):
                    equout.time_slice[itime].profiles_2d[i2d].b_field_r[ir][iz] = equin.time_slice[itime].profiles_2d[i2d].b_field_r[ir][iz] * rescale

            for ir in range(len(equin.time_slice[itime].profiles_2d[i2d].b_field_z)):
                for iz in range(len(equin.time_slice[itime].profiles_2d[i2d].b_field_z[ir])):
                    equout.time_slice[itime].profiles_2d[i2d].b_field_z[ir][iz] = equin.time_slice[itime].profiles_2d[i2d].b_field_z[ir][iz] * rescale

            for ir in range(len(equin.time_slice[itime].profiles_2d[i2d].b_field_tor)):
                for iz in range(len(equin.time_slice[itime].profiles_2d[i2d].b_field_tor[ir])):
                    equout.time_slice[itime].profiles_2d[i2d].b_field_tor[ir][iz] = equin.time_slice[itime].profiles_2d[i2d].b_field_tor[ir][iz] * rescale

        for iggd in range(len(equin.time_slice[itime].ggd)):
            for i2 in range(len(equin.time_slice[itime].ggd[iggd].psi)):
                for i in range(len(equin.time_slice[itime].ggd[iggd].psi[i2].values)):
                    equout.time_slice[itime].ggd[iggd].psi[i2].values[i] = equin.time_slice[itime].ggd[iggd].psi[i2].values[i] * rescale
                    for j in range(len(equin.time_slice[itime].ggd[iggd].psi[i2].values[i])):
                        equout.time_slice[itime].ggd[iggd].psi[i2].coefficients[i][j] = equin.time_slice[itime].ggd[iggd].psi[i2].coefficients[i][j] * rescale

                for i in range(len(equin.time_slice[itime].ggd[iggd].phi[i2].values)):
                    equout.time_slice[itime].ggd[iggd].phi[i2].values[i] = equin.time_slice[itime].ggd[iggd].phi[i2].values[i] * rescale
                    for j in range(len(equin.time_slice[itime].ggd[iggd].phi[i2].values[i])):
                        equout.time_slice[itime].ggd[iggd].phi[i2].coefficients[i][j] = equin.time_slice[itime].ggd[iggd].phi[i2].coefficients[i][j] * rescale

                for i in range(len(equin.time_slice[itime].ggd[iggd].j_tor[i2].values)):
                    equout.time_slice[itime].ggd[iggd].j_tor[i2].values[i] = equin.time_slice[itime].ggd[iggd].j_tor[i2].values[i] * rescale
                    for j in range(len(equin.time_slice[itime].ggd[iggd].j_tor[i2].values[i])):
                        equout.time_slice[itime].ggd[iggd].j_tor[i2].coefficients[i][j] = equin.time_slice[itime].ggd[iggd].j_tor[i2].coefficients[i][j] * rescale

                for i in range(len(equin.time_slice[itime].ggd[iggd].j_parallel[i2].values)):
                    equout.time_slice[itime].ggd[iggd].j_parallel[i2].values[i] = equin.time_slice[itime].ggd[iggd].j_parallel[i2].values[i] * rescale
                    for j in range(len(equin.time_slice[itime].ggd[iggd].j_parallel[i2].values[i])):
                        equout.time_slice[itime].ggd[iggd].j_parallel[i2].coefficients[i][j] = equin.time_slice[itime].ggd[iggd].j_parallel[i2].coefficients[i][j] * rescale

                for i in range(len(equin.time_slice[itime].ggd[iggd].b_field_r[i2].values)):
                    equout.time_slice[itime].ggd[iggd].b_field_r[i2].values[i] = equin.time_slice[itime].ggd[iggd].b_field_r[i2].values[i] * rescale
                    for j in range(len(equin.time_slice[itime].ggd[iggd].b_field_r[i2].values[i])):
                        equout.time_slice[itime].ggd[iggd].b_field_r[i2].coefficients[i][j] = equin.time_slice[itime].ggd[iggd].b_field_r[i2].coefficients[i][j] * rescale

                for i in range(len(equin.time_slice[itime].ggd[iggd].b_field_z[i2].values)):
                    equout.time_slice[itime].ggd[iggd].b_field_z[i2].values[i] = equin.time_slice[itime].ggd[iggd].b_field_z[i2].values[i] * rescale
                    for j in range(len(equin.time_slice[itime].ggd[iggd].b_field_z[i2].values[i])):
                        equout.time_slice[itime].ggd[iggd].b_field_z[i2].coefficients[i][j] = equin.time_slice[itime].ggd[iggd].b_field_z[i2].coefficients[i][j] * rescale

                for i in range(len(equin.time_slice[itime].ggd[iggd].b_field_tor[i2].values)):
                    equout.time_slice[itime].ggd[iggd].b_field_tor[i2].values[i] = equin.time_slice[itime].ggd[iggd].b_field_tor[i2].values[i] * rescale
                    for j in range(len(equin.time_slice[itime].ggd[iggd].b_field_tor[i2].values[i])):
                        equout.time_slice[itime].ggd[iggd].b_field_tor[i2].coefficients[i][j] = equin.time_slice[itime].ggd[iggd].b_field_tor[i2].coefficients[i][j] * rescale

    equout.ids_properties.comment = equin.ids_properties.comment+' (field rescaled by '+str(rescale)+')'
    return equout



if __name__ == "__main__":
    from idstools.cli import *
    # This script imports an equilibrium IDS, rescales its magnetic field components,
    # and then stores it to the output IDS
    # Management of input arguments
    parser = argparse.ArgumentParser(description='Rescaling an equilibrium magnetic field, storing the output into another entry of the same DB', parents=[imas_parser])
    parser.add_argument('-si','--shot_input',
                        help='Input shot number', required=True,type=int)
    parser.add_argument('-ri','--run_input',
                        help='Input run number', required=True,type=int)
    parser.add_argument('-so','--shot_output',
                        help='Output shot number', required=True,type=int)
    parser.add_argument('-ro','--run_output',
                        help='Output run number', required=True,type=int)
    parser.add_argument('-do','--database_output',type=str,default=None,
                        help='Database name for the destination data-entry')
    parser.add_argument('-bo','--backend_output',type=str,
                        help='Backend name for the destination data-entry')
    parser.add_argument('-r','--rescale',
                        help='Rescaling factor of the equilibrium magnetic field',type=float,required=True)

    args = parser.parse_args()

    if args.database_output == None:
        args.database_output = args.database

    if args.backend_output == None:
        args.backend_output = args.backend

    rescale      = args.rescale

    if (rescale==0):
        print("Rescale factor cannot be zero!")
        sys.exit(1)

    # OPEN INPUT
    input = imas.DBEntry(get_backend_id(args.backend),args.database,
                         args.shot_input,args.run_input,args.user)
    status,_ = input.open()
    if (status!=0):
        print("Can't open the input pulse file!")
        sys.exit(1)
        
    equin = input.get("equilibrium")

    # OPEN OUTPUT
    output = imas.DBEntry(get_backend_id(args.backend),args.database_output,
                          args.shot_output,args.run_output,user_name=os.environ['USER'])
    status,_ = output.open()
    if (status!=0):
        print("Can't open the output pulse file!")
        print("Trying to create a new one")
        status,_ = output.create()
        if (status!=0):
            print("Can't create the output pulse file!")
            sys.exit(1)

    print ('Rescaling equilibrium magnetic field by '+str(rescale))
    equout = equilibrium_rescale(equin, rescale)

    # PUT IDS INTO OUTPUT
    output.put(equout)

    # CLOSE FILES
    input.close()
    output.close()


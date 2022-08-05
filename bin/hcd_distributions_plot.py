from __future__ import print_function
import database_tools.init_mendeleiev as mend

# MODULES
# --------
from numpy import *
import imas,argparse,sys,os
import matplotlib
matplotlib.use('TKagg')
import matplotlib.pyplot as plt

# MANAGEMENT OF INPUT ARGUMENTS
# ------------------------------
# When hcd_distributions_plot is called directly
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= \
                                         '---- Display NBI or fusion results')
    parser.add_argument('-s','--shot',help='Shot number', required=True,type=int)
    parser.add_argument('-r','--run',help='Run number',required=True)
    parser.add_argument('-u','--user_or_path',help='User or absolute path name where the data-entry is located', required=False)
    parser.add_argument('-d','--database',help='Database name where the data-entry is located', required=False)
    parser.add_argument('-t','--time',help='time', required=False,type=float)

    args = vars(parser.parse_args())

###################################################################################

def distributions_prep(args):

    shot = args["shot"]
    run = args["run"]

    # To handle multiple datafiles (for scans)
    if '-' in run:
        [runmin,runmax]=[int(x) for x in run.split('-')] #int(run.split('-'))
    else:
        runmin = int(run)
        runmax = int(run)

    # User or absolute path name
    if args['user_or_path'] != None:
        user_or_path = args['user_or_path']
    else:
        user_or_path = 'public'

    # Database name
    if args['database'] != None:
        database = args['database']
    else:
        database = 'iter'

    # Time
    if args['time'] != None:
        time = args['time']
    else:
        time = -99.

    # Mendeleiev table
    table_mendeleiev = mend.create_table_mendeleiev()

    ###################################################################################

    # READ IDS'S FROM LOCAL DATABASE
    # -------------------------------
    input={}
    isample = 0
    distributions = {}
    for irun in range(runmin,runmax+1):
        input[isample] = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,database,shot,irun,user_or_path)
        err,n=input[isample].open()
        if err != 0:
            print('Shot ' + str(shot) + ', run ' + str(run) +' for user_or_path = '\
                  +user_or_path+' and database = '+database+' does not exist', file=sys.stderr)
            print('----> Aborted.', file=sys.stderr)
            exit()
        distributions[isample] = input[isample].get('distributions')
        if distributions[isample].ids_properties.homogeneous_time<0:
            print('The distributions IDS is not present in the input file => Abort.')
            exit()
        input[isample].close()
        isample+=1
    nsample = isample

    # TIME VECTOR AND TIME INDEX
    # ---------------------------

    nbfus_profiles = {}
    for isample in range(nsample):
        nbfus_profiles[isample] = {}
        nbfus_profiles[isample]['timevec'] = distributions[isample].time
        nbfus_profiles[isample]['ntime'] = len(nbfus_profiles[isample]['timevec'])
        if nbfus_profiles[isample]['ntime'] == 1:
            if len(nbfus_profiles[isample]['timevec']) > 0:
                nbfus_profiles[isample]['tc'] = nbfus_profiles[isample]['timevec'][0]
            else:
                nbfus_profiles[isample]['tc'] = 0
            nbfus_profiles[isample]['it'] = 0
        else:
            if time>=0:
                [nbfus_profiles[isample]['tc'],nbfus_profiles[isample]['it']] = find_nearest(nbfus_profiles[isample]['timevec'],time)
            else:
                nbfus_profiles[isample]['it'] = int(nbfus_profiles[isample]['ntime']/2)
                nbfus_profiles[isample]['tc'] = nbfus_profiles[isample]['timevec'][nbfus_profiles[isample]['it']]
        print('--------------------------------------------------------------------------', file=sys.stderr)
        print(' Time  = '+'%.2f' % nbfus_profiles[isample]['tc']+' s in range ['+'%.2f' % nbfus_profiles[isample]['timevec'][0]+','+'%.2f' \
              % nbfus_profiles[isample]['timevec'][nbfus_profiles[isample]['ntime']-1]+'] s', file=sys.stderr)
        print(' Index = ',str(nbfus_profiles[isample]['it']), file=sys.stderr)
        print(' Averaged resolution = ', (nbfus_profiles[isample]['timevec'][nbfus_profiles[isample]['ntime']-1]\
                                          -nbfus_profiles[isample]['timevec'][0])/(nbfus_profiles[isample]['ntime']-1),' s', file=sys.stderr)
        print('--------------------------------------------------------------------------', file=sys.stderr)

        nbfus_profiles[isample]['time'] = nbfus_profiles[isample]['tc']

        nbfus_profiles[isample]['ndistributions'] = len(distributions[isample].distribution)
        nbfus_profiles[isample]['is_active'] = [0]*nbfus_profiles[isample]['ndistributions']
        nbfus_profiles[isample]['cur_calc'] = 1
        for idistrib in range(nbfus_profiles[isample]['ndistributions']):
            if len(distributions[isample].distribution[idistrib].global_quantities[0].collisions.ion)>0:
                nbfus_profiles[isample]['is_active'][idistrib] = 1
                if distributions[isample].distribution[idistrib].global_quantities[0].current_tor==-9e40:
                    nbfus_profiles[isample]['cur_calc'] = 0
                try:
                    nbfus_profiles[isample]['rho_tor_norm'] = 0
                    if len(distributions[isample].distribution[idistrib].profiles_1d[nbfus_profiles[isample]['it']].grid.rho_tor_norm) > 0:
                        nbfus_profiles[isample]['nrho'] = len(distributions[isample].distribution[idistrib].profiles_1d[nbfus_profiles[isample]['it']].grid.rho_tor_norm)
                        nbfus_profiles[isample]['rho_tor_norm'] = distributions[isample].distribution[idistrib].profiles_1d[nbfus_profiles[isample]['it']].grid.rho_tor_norm
                    elif len(distributions[isample].distribution[idistrib].profiles_1d[nbfus_profiles[isample]['it']].grid.rho_tor) > 0:
                        nbfus_profiles[isample]['nrho'] = len(distributions[isample].distribution[idistrib].profiles_1d[nbfus_profiles[isample]['it']].grid.rho_tor)
                        nbfus_profiles[isample]['rho_tor_norm'] = distributions[isample].distribution[idistrib].\
                            profiles_1d[nbfus_profiles[isample]['it']].grid.rho_tor/distributions[isample].\
                            distribution[idistrib].profiles_1d[nbfus_profiles[isample]['it']].grid.rho_tor[nbfus_profiles[isample]['nrho']-1]
                except:
                    print('distributions.distribution[idistrib].profiles_1d[it].grid.rho_tor_norm and rho_tor could not be read', file=sys.stderr)
                    print('----> Aborted.', file=sys.stderr)
                    exit()
                if nbfus_profiles[isample]['nrho']==0:
                    print('distributions.distribution[idistrib].profiles_1d[it].grid.rho_tor_norm and rho_tor are empty', file=sys.stderr)
                    print('----> Aborted.', file=sys.stderr)
                    exit()

        if sum(nbfus_profiles[isample]['is_active'])==0:
            print('The distributions IDS appears empty ----> Abort.', file=sys.stderr)
            exit()

        # --------------------------------------------------------------

        # INJECTOR NAME
        nbfus_profiles[isample]['single_nf_source_name'] = dict()

        # WAVEFORMS
        nbfus_profiles[isample]['all_injectors_current_waveform']               = [0]*nbfus_profiles[isample]['ntime']
        nbfus_profiles[isample]['all_injectors_electron_power_waveform']        = [0]*nbfus_profiles[isample]['ntime']
        nbfus_profiles[isample]['all_injectors_ion_power_waveform']             = [0]*nbfus_profiles[isample]['ntime']
        nbfus_profiles[isample]['all_injectors_total_power_waveform']           = [0]*nbfus_profiles[isample]['ntime']
        nbfus_profiles[isample]['single_current_waveform']                      = dict()
        nbfus_profiles[isample]['single_electron_power_waveform']               = dict()
        nbfus_profiles[isample]['single_ion_power_waveform']                    = dict()
        nbfus_profiles[isample]['single_total_power_waveform']                  = dict()

        # PROFILES
        nbfus_profiles[isample]['all_injectors_current_density_profile']        = [0]*nbfus_profiles[isample]['nrho']
        nbfus_profiles[isample]['all_injectors_electron_power_density_profile'] = [0]*nbfus_profiles[isample]['nrho']
        nbfus_profiles[isample]['all_injectors_ion_power_density_profile']      = [0]*nbfus_profiles[isample]['nrho']
        nbfus_profiles[isample]['all_injectors_total_power_density_profile']    = [0]*nbfus_profiles[isample]['nrho']
        nbfus_profiles[isample]['single_current_density_profile']               = dict()
        nbfus_profiles[isample]['single_electron_power_density_profile']        = dict()
        nbfus_profiles[isample]['single_ion_power_density_profile']             = dict()
        nbfus_profiles[isample]['single_total_power_density_profile']           = dict()

        # LOOP OVER ALL SOURCE
        for idistrib in range(nbfus_profiles[isample]['ndistributions']):
            # INJECTOR NAME
            if len(distributions[isample].distribution[idistrib].process)>0:
                if len(distributions[isample].distribution[idistrib].process[0].type.description)>0:
                    nbfus_profiles[isample]['single_nf_source_name'][idistrib] = \
                        distributions[isample].distribution[idistrib].process[0].type.description+str(idistrib)
                else:
                    nbfus_profiles[isample]['single_nf_source_name'][idistrib] = 'Beam_'+str(idistrib)
            else:
                nbfus_profiles[isample]['single_nf_source_name'][idistrib] = 'Beam_'+str(idistrib)
            if nbfus_profiles[isample]['is_active'][idistrib]:
                # WAVEFORMS
                nbfus_profiles[isample]['single_current_waveform'][idistrib]        \
                    = [0]*nbfus_profiles[isample]['ntime']
                nbfus_profiles[isample]['single_electron_power_waveform'][idistrib] \
                    = [0]*nbfus_profiles[isample]['ntime']
                nbfus_profiles[isample]['single_ion_power_waveform'][idistrib]      \
                    = [0]*nbfus_profiles[isample]['ntime']
                nbfus_profiles[isample]['single_total_power_waveform'][idistrib]    \
                    = [0]*nbfus_profiles[isample]['ntime']
                nions = len(distributions[isample].distribution[idistrib].global_quantities[0].collisions.ion)
                for itime in range(nbfus_profiles[isample]['ntime']):
                    if nbfus_profiles[isample]['cur_calc'] == 1:
                        nbfus_profiles[isample]['single_current_waveform'][idistrib][itime]    \
                            = distributions[isample].distribution[idistrib]\
                            .global_quantities[itime].current_tor
                    nbfus_profiles[isample]['single_electron_power_waveform'][idistrib][itime] \
                        = distributions[isample].distribution[idistrib]\
                        .global_quantities[itime].collisions.electrons.power_thermal
                    for iion in range(nions):
                        nbfus_profiles[isample]['single_ion_power_waveform'][idistrib][itime] \
                            = nbfus_profiles[isample]['single_ion_power_waveform'][idistrib][itime]   \
                            + distributions[isample].distribution[idistrib].global_quantities[itime].collisions.ion[iion].power_thermal
                    nbfus_profiles[isample]['single_total_power_waveform'][idistrib][itime]    \
                        = nbfus_profiles[isample]['single_electron_power_waveform'][idistrib][itime] \
                        + nbfus_profiles[isample]['single_ion_power_waveform'][idistrib][itime]
                    nbfus_profiles[isample]['all_injectors_current_waveform'][itime]           \
                        = nbfus_profiles[isample]['all_injectors_current_waveform'][itime]        \
                        + nbfus_profiles[isample]['single_current_waveform'][idistrib][itime]
                    nbfus_profiles[isample]['all_injectors_electron_power_waveform'][itime]    \
                        = nbfus_profiles[isample]['all_injectors_electron_power_waveform'][itime] \
                        + nbfus_profiles[isample]['single_electron_power_waveform'][idistrib][itime]
                    nbfus_profiles[isample]['all_injectors_ion_power_waveform'][itime]         \
                        = nbfus_profiles[isample]['all_injectors_ion_power_waveform'][itime]      \
                        + nbfus_profiles[isample]['single_ion_power_waveform'][idistrib][itime]
                    nbfus_profiles[isample]['all_injectors_total_power_waveform'][itime]       \
                        = nbfus_profiles[isample]['all_injectors_total_power_waveform'][itime]    \
                        + nbfus_profiles[isample]['single_electron_power_waveform'][idistrib][itime] \
                        + nbfus_profiles[isample]['single_ion_power_waveform'][idistrib][itime]
                # PROFILES
                nbfus_profiles[isample]['single_current_density_profile'][idistrib]        \
                    = [0]*nbfus_profiles[isample]['nrho']
                nbfus_profiles[isample]['single_electron_power_density_profile'][idistrib] \
                    = [0]*nbfus_profiles[isample]['nrho']
                nbfus_profiles[isample]['single_ion_power_density_profile'][idistrib]      \
                    = [0]*nbfus_profiles[isample]['nrho']
                nbfus_profiles[isample]['single_total_power_density_profile'][idistrib]    \
                    = [0]*nbfus_profiles[isample]['nrho']
                if nbfus_profiles[isample]['cur_calc'] == 1:
                    nbfus_profiles[isample]['single_current_density_profile'][idistrib]    \
                        = distributions[isample].distribution[idistrib]\
                        .profiles_1d[nbfus_profiles[isample]['it']].current_tor
                nbfus_profiles[isample]['single_electron_power_density_profile'][idistrib] \
                    = distributions[isample].distribution[idistrib]\
                    .profiles_1d[nbfus_profiles[isample]['it']].collisions.electrons.power_thermal
                for iion in range(nions):
                    nbfus_profiles[isample]['single_ion_power_density_profile'][idistrib]  \
                        = nbfus_profiles[isample]['single_ion_power_density_profile'][idistrib]      \
                        + distributions[isample].distribution[idistrib]\
                        .profiles_1d[nbfus_profiles[isample]['it']].collisions.ion[iion].power_thermal
                nbfus_profiles[isample]['single_total_power_density_profile'][idistrib]    \
                    = nbfus_profiles[isample]['single_electron_power_density_profile'][idistrib] \
                    + nbfus_profiles[isample]['single_ion_power_density_profile'][idistrib]
                nbfus_profiles[isample]['all_injectors_current_density_profile']           \
                    = nbfus_profiles[isample]['all_injectors_current_density_profile']           \
                    + nbfus_profiles[isample]['single_current_density_profile'][idistrib]
                nbfus_profiles[isample]['all_injectors_electron_power_density_profile']    \
                    = nbfus_profiles[isample]['all_injectors_electron_power_density_profile']    \
                    + nbfus_profiles[isample]['single_electron_power_density_profile'][idistrib]
                nbfus_profiles[isample]['all_injectors_ion_power_density_profile']         \
                    = nbfus_profiles[isample]['all_injectors_ion_power_density_profile']         \
                    + nbfus_profiles[isample]['single_ion_power_density_profile'][idistrib]
                nbfus_profiles[isample]['all_injectors_total_power_density_profile']       \
                    = nbfus_profiles[isample]['all_injectors_total_power_density_profile']       \
                    + nbfus_profiles[isample]['single_electron_power_density_profile'][idistrib] \
                    + nbfus_profiles[isample]['single_ion_power_density_profile'][idistrib]

        print('--------------------------------------------------------------------------', file=sys.stderr)
        print(' Total power  = {:.2f}'.format(nbfus_profiles[isample]\
            ['all_injectors_total_power_waveform'][nbfus_profiles[isample]['it']]*1.e-6)+' MW',file = sys.stderr)
        print(' To electrons = {:.2f}'.format(nbfus_profiles[isample]\
            ['all_injectors_electron_power_waveform'][nbfus_profiles[isample]['it']]*1.e-6)+' MW',file = sys.stderr)
        print(' To ions      = {:.2f}'.format(nbfus_profiles[isample]\
            ['all_injectors_ion_power_waveform'][nbfus_profiles[isample]['it']]*1.e-6)+' MW',file = sys.stderr)

        # Power absorbed to individual ions
        nbfus_profiles[isample]['all_injectors_total_power_waveform_per_ion'] = [0]*nions
        nbfus_profiles[isample]['element'] = [0]*nions
        nbfus_profiles[isample]['compo_detail'] = 0
        for idistrib in range(nbfus_profiles[isample]['ndistributions']):
            if nbfus_profiles[isample]['is_active'][idistrib]:
                for iion in range(nions):
                    nbfus_profiles[isample]['all_injectors_total_power_waveform_per_ion'][iion] \
                        = nbfus_profiles[isample]['all_injectors_total_power_waveform_per_ion'][iion] \
                        + distributions[isample].distribution[idistrib].global_quantities\
                        [nbfus_profiles[isample]['it']].collisions.ion[iion].power_thermal
                    if len(distributions[isample].distribution[idistrib].global_quantities\
                           [nbfus_profiles[isample]['it']].collisions.ion[iion].element) > 0:
                        nbfus_profiles[isample]['compo_detail'] = 1
                        a = int(distributions[isample].distribution[idistrib].global_quantities\
                                [nbfus_profiles[isample]['it']].collisions.ion[iion].element[0].a)
                        z = int(distributions[isample].distribution[idistrib].global_quantities\
                                [nbfus_profiles[isample]['it']].collisions.ion[iion].element[0].z_n)
                        nbfus_profiles[isample]['element'][iion] = table_mendeleiev[z][a].element

        if nbfus_profiles[isample]['compo_detail'] == 1:
            for iion in range(nions):
                print('      - '+nbfus_profiles[isample]['element'][iion]+' = {:.2f}'\
                      .format(nbfus_profiles[isample]['all_injectors_total_power_waveform_per_ion']\
                              [iion]*1.e-3)+' kW',file = sys.stderr)

        if nbfus_profiles[isample]['cur_calc'] == 1:
            print('--------------------------------------------------------------------------', file=sys.stderr)
            print(' Total CD        = {:.2f}'.format(nbfus_profiles[isample]\
                  ['all_injectors_current_waveform'][nbfus_profiles[isample]['it']]*1.e-3)\
                  +' kA',file = sys.stderr)

        if sum(nbfus_profiles[isample]['is_active'])>1:
            print('--------------------------------------------------------------------------', file=sys.stderr)
            for idistrib in range(nbfus_profiles[isample]['ndistributions']):
                if nbfus_profiles[isample]['is_active'][idistrib]:
                    print(' Distribution #'+str(idistrib+1)+' - power = {:.2f}'\
                          .format(nbfus_profiles[isample]['single_total_power_waveform']\
                          [idistrib][nbfus_profiles[isample]['it']]*1.e-6)+' MW',file = sys.stderr)
                    if nbfus_profiles[isample]['cur_calc'] == 1:
                        print(' Distribution #'+str(idistrib+1)+' - CD    = {:.2f}'\
                              .format(nbfus_profiles[isample]['single_current_waveform']\
                              [idistrib][nbfus_profiles[isample]['it']]*1.e-3)+' kA',file = sys.stderr)

        print('--------------------------------------------------------------------------', file=sys.stderr)

        nbfus_param = {}
        nbfus_param['nsample'] = nsample
        nbfus_param['shot'] = shot
        nbfus_param['run'] = run
        
    return nbfus_profiles, nbfus_param

###################################################################################

def find_nearest(a, a0):
    'Element in nd array `a` closest to the scalar value `a0`'
    idx = abs(a - a0).argmin()
    return a.flat[idx],idx

###################################################################################

def CustomLegend(legend):
    fontleg = 12
    frame = legend.get_frame()
    frame.set_facecolor('0.95')
    for label in legend.get_texts():
        label.set_fontsize(fontleg)
    for label in legend.get_lines():
        label.set_linewidth(1.5)  # the legend line width
    return

###################################################################################

def distributions_display(nbfus_profiles,nbfus_param):

    nsample = nbfus_param['nsample']
    shot    = nbfus_param['shot']
    run     = nbfus_param['run']
   
    # DISPLAY PARAMETERS
    # -------------------
    fontsize = 12
    figure_width  = 5
    figure_height = 4

    plt.rcParams['font.size'] = fontsize
    plt.rcParams['axes.linewidth'] = 1.5
    plt.rcParams['grid.alpha'] = 1.0

    font = {'family': 'serif',
            'color':  'darkred',
            'weight': 'normal',
            'size': fontsize,
            }

    torcol = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']*100
   
    # PROFILE OF ABSORBED POWER DENSITY ON ELECTRONS+IONS FOR ALL INJECTORS AND EACH OF THEM INDIVIDUALLY [MW/M3]
    fig_flag = 0
    for isample in range(nsample):
        if sum(nbfus_profiles[isample]['is_active'])>1:
            if fig_flag == 0:
                fig,ax =plt.subplots(1,1)
                fig_flag = 1
            ax.plot(nbfus_profiles[isample]['rho_tor_norm'], nbfus_profiles\
                    [isample]['all_injectors_total_power_density_profile']*1.e-6,\
                    label=r'All injectors',color='black')
            for idistrib in range(nbfus_profiles[isample]['ndistributions']):
                if nbfus_profiles[isample]['is_active'][idistrib]:
                    ax.plot(nbfus_profiles[isample]['rho_tor_norm'], \
                            nbfus_profiles[isample]['single_total_power_density_profile'][idistrib]*1.e-6,\
                            label=nbfus_profiles[isample]['single_nf_source_name'][idistrib],color=torcol[idistrib])
    if fig_flag == 1:
        ax.set_ylabel('Absorbed power $\mathrm{[MW/m^{3}]}$')
        ax.set_xlabel('Normalized toroidal flux coordinate')
        plt.grid()
        #legend = plt.legend()
        #CustomLegend(legend)
        fig.set_size_inches(figure_width,figure_height)
        fig.tight_layout()
        fig.savefig('NF_power_individuals_injectors_profile_shot_{0}_run_{1}.png'.format(shot,run),bbox_inches="tight")
        #plt.title('Whatever')
        plt.show(block=False)

    # PROFILE OF ABSORBED POWER DENSITY ON ELECTRONS+IONS, ELECTRONS, IONS FOR ALL INJECTORS [MW/M3]
    fig,ax =plt.subplots(1,1)
    for isample in range(nsample):
        if sum(nbfus_profiles[isample]['is_active'])>0:
            ax.plot(nbfus_profiles[isample]['rho_tor_norm'], nbfus_profiles[isample]\
                    ['all_injectors_total_power_density_profile']*1.e-6,label=r'Electrons+Ions',color=torcol[1])
            ax.plot(nbfus_profiles[isample]['rho_tor_norm'], nbfus_profiles[isample]\
                    ['all_injectors_electron_power_density_profile']*1.e-6,label=r'Electrons',color=torcol[2])
            ax.plot(nbfus_profiles[isample]['rho_tor_norm'], nbfus_profiles[isample]\
                    ['all_injectors_ion_power_density_profile']*1.e-6,label=r'Ions',color=torcol[3])
    ax.set_ylabel('Absorbed power $\mathrm{[MW/m^{3}]}$')
    ax.set_xlabel('Normalized toroidal flux coordinate')
    plt.grid()
    legend = plt.legend()
    CustomLegend(legend)
    fig.set_size_inches(figure_width,figure_height)
    fig.tight_layout()
    fig.savefig('NF_power_all_injectors_el_ion_profile_shot_{0}_run_{1}.png'.format(shot,run),bbox_inches="tight")
    #plt.title('Whatever')
    plt.show(block=False)

    # CD PROFILE [MA/M2]
    fig_flag = 0
    for isample in range(nsample):
        if nbfus_profiles[isample]['cur_calc'] == 1:
            if fig_flag == 0:
                fig,ax =plt.subplots(1,1)
                fig_flag = 1
            if sum(nbfus_profiles[isample]['is_active'])>1:
                ax.plot(nbfus_profiles[isample]['rho_tor_norm'], \
                        nbfus_profiles[isample]['all_injectors_current_density_profile']*1.e-6,color=torcol[1])
            for idistrib in range(nbfus_profiles[isample]['ndistributions']):
                if nbfus_profiles[isample]['is_active'][idistrib]:
                    ax.plot(nbfus_profiles[isample]['rho_tor_norm'], nbfus_profiles[isample]\
                            ['single_current_density_profile']\
                            [idistrib]*1.e-6,label=nbfus_profiles[isample]\
                            ['single_nf_source_name'][idistrib],color=torcol[2])
            ax.set_ylabel('Current density $\mathrm{[MA/m^{2}]}$')
            ax.set_xlabel('Normalized toroidal flux coordinate')
            plt.grid()
            #legend = plt.legend()
            #CustomLegend(legend)
            fig.set_size_inches(figure_width,figure_height)
            fig.tight_layout()
            fig.savefig('NF_power_profile_shot_{0}_run_{1}.png'.format(shot,run),bbox_inches="tight")
            #plt.title('Whatever')

    # NBI/FUS POWER AND CD WAVEFORMS
    if nbfus_profiles[isample]['ntime']==1:
        print('Only one time slice --> Power and CD waveforms not displayed', file=sys.stderr)
        plt.show(block=True)
    else:
        plt.show(block=False)
        # NBI/FUS POWER WAVEFORM
        fig,ax =plt.subplots(1,1)
        for isample in range(nsample):
            if sum(nbfus_profiles[isample]['is_active'])>1:
                ax.plot(nbfus_profiles[isample]['timevec'], array(nbfus_profiles[isample]\
                    ['all_injectors_total_power_waveform'])*1.e-6,label=r'Total',color=torcol[1])
                ax.plot(nbfus_profiles[isample]['timevec'], array(nbfus_profiles[isample]\
                    ['all_injectors_electron_power_waveform'])*1.e-6,label=r'To electrons',color=torcol[2])
                ax.plot(nbfus_profiles[isample]['timevec'], array(nbfus_profiles[isample]\
                    ['all_injectors_ion_power_waveform']) * 1.e-6, label=r'To ions',color=torcol[3])
            for idistrib in range(nbfus_profiles[isample]['ndistributions']):
                if nbfus_profiles[isample]['is_active'][idistrib]:
                    ax.plot(nbfus_profiles[isample]['timevec'], array(nbfus_profiles[isample]\
                        ['single_total_power_waveform'][idistrib])\
                        *1.e-6,label=nbfus_profiles[isample]['single_nf_source_name']\
                        [idistrib],color=torcol[idistrib])
    ax.set_ylabel('Power to the bulk $\mathrm{[MW]}$')
    ax.set_xlabel('Time (s)')
    plt.grid()
    #legend = plt.legend()
    #CustomLegend(legend)
    fig.set_size_inches(figure_width,figure_height)
    fig.tight_layout()
    fig.savefig('NF_power_waveform_shot_{0}_run_{1}.png'.format(shot,run),bbox_inches="tight")
    #plt.title('Whatever')
    plt.gca().set_ylim(0,max(nbfus_profiles[isample]['all_injectors_total_power_waveform'])*1.2e-6)
    plt.show(block=False)

    # CD WAVEFORM
    if nbfus_profiles[isample]['cur_calc'] == 1:
        fig,ax =plt.subplots(1,1)
        for isample in range(nsample):
            if sum(nbfus_profiles[isample]['is_active'])>1:
                ax.plot(nbfus_profiles[isample]['timevec'], array(nbfus_profiles[isample]\
                    ['all_injectors_current_waveform'])*1.e-6,label=r'Total',color=torcol[1])
            for idistrib in range(nbfus_profiles[isample]['ndistributions']):
                if nbfus_profiles[isample]['is_active'][idistrib]:
                    ax.plot(nbfus_profiles[isample]['timevec'], array(nbfus_profiles[isample]\
                    ['single_current_waveform'][idistrib])*1.e-6,label=nbfus_profiles[isample]\
                    ['single_nf_source_name'][idistrib])
        ax.set_ylabel('Current Drive $\mathrm{[MA]}$')
        ax.set_xlabel('Time (s)')
        plt.grid()
        #legend = plt.legend()
        #CustomLegend(legend)
        fig.set_size_inches(figure_width,figure_height)
        fig.tight_layout()
        fig.savefig('NF_CD_waveform_shot_{0}_run_{1}.png'.format(shot,run),bbox_inches="tight")
        #plt.title('Whatever')
        #plt.gca().set_ylim(0,max(array(nbfus_profiles[isample]['all_injectors_current_waveform']))*1.2e-3)
        plt.show(block=True)

###################################################################################
def run(args):
  nbfus_profiles,nbfus_param = distributions_prep(args)
  distributions_display(nbfus_profiles,nbfus_param)

# When hcd_distributions_plot is called directly
if __name__ == "__main__":
   run(args)

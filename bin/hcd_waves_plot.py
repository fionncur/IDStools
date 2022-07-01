from __future__ import print_function

# MODULES
# --------
from numpy import *
import imas,argparse,sys,os
import matplotlib
matplotlib.use('TKagg')
import matplotlib.pyplot as plt

# MANAGEMENT OF INPUT ARGUMENTS
# ------------------------------
# When hcd_waves_plot is called directly
if __name__ == "__main__":
   parser = argparse.ArgumentParser(description=\
            '---- Display EC results')
   parser.add_argument('-s','--shot',help='Shot number', required=True,type=int)
   parser.add_argument('-r','--run',help='Run number',required=True)
   parser.add_argument('-u','--user_or_path',help\
                       ='User or absolute path name where the data-entry is located', required=False)
   parser.add_argument('-d','--database',help='Database name where the data-entry is located', required=False)
   parser.add_argument('-t','--time',help='Time', required=False,type=float)
   parser.add_argument('-f','--force_psi',help='= 1 to force displaying the profiles versus poloidal flux', required=False)

   args  = vars(parser.parse_args())

###################################################################################

def ec_prep(args):

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

   # Flag to force psi radial coordinate to be used
   if args['force_psi'] != None:
       force_psi = int(args['force_psi'])
   else:
       force_psi = 0
       
   # READ IDS'S FROM LOCAL DATABASE
   # -------------------------------
   input={}
   isample = 0
   waves = {}
   for irun in range(runmin,runmax+1):
       input[isample]=imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND, database, shot, irun, user_name=user_or_path)
       err,n=input[isample].open()
       if err != 0:
           print(f'Shot {shot}, run {run} for user {user_or_path} and database {database} does not exist', file=sys.stderr)
           print('----> Aborted.', file=sys.stderr)
           exit()
       waves[isample] = input[isample].get('waves')
       input[isample].close()
       isample+=1
   nsample = isample

   # TIME VECTOR AND TIME INDEX
   # ---------------------------

   ec_profiles = {}
   for isample in range(nsample):
       ec_profiles[isample] = {}
       ec_profiles[isample]['time'] = time
       ec_profiles[isample]['timevec'] = waves[isample].time
       ec_profiles[isample]['ntime'] = len(ec_profiles[isample]['timevec'])
       if ec_profiles[isample]['ntime']==1:
           if len(ec_profiles[isample]['timevec']) > 0:
               ec_profiles[isample]['tc'] = ec_profiles[isample]['timevec'][0]
           else:
               ec_profiles[isample]['tc'] = 0
           ec_profiles[isample]['it'] = 0
       else:
           if ec_profiles[isample]['time']>=0:
               [ec_profiles[isample]['tc'],ec_profiles[isample]['it']] = \
                  find_nearest(ec_profiles[isample]['timevec'],ec_profiles[isample]['time'])
           else:
               ec_profiles[isample]['it'] = int(ec_profiles[isample]['ntime']/2)
               ec_profiles[isample]['tc'] = ec_profiles[isample]['timevec'][ec_profiles[isample]['it']]
           print('--------------------------------------------------------------------------', file=sys.stderr)
           print(' Time  = '+'%.2f' % ec_profiles[isample]['tc']+' s in range ['+'%.2f'
                 % ec_profiles[isample]['timevec'][0]+','+'%.2f' \
                 % ec_profiles[isample]['timevec'][ec_profiles[isample]['ntime']-1]+'] s', file=sys.stderr)
           print(' Index = ',str(ec_profiles[isample]['it']), file=sys.stderr)
           print(' Averaged resolution = ', (ec_profiles[isample]['timevec'][ec_profiles[isample]['ntime']-1]
                                             -ec_profiles[isample]['timevec'][0])\
                 /(ec_profiles[isample]['ntime']-1),' s', file=sys.stderr)  
           print('--------------------------------------------------------------------------', file=sys.stderr)
       ec_profiles[isample]['time'] = ec_profiles[isample]['tc']

       ec_profiles[isample]['nwaves'] = len(waves[isample].coherent_wave)
       ec_profiles[isample]['is_active'] = [0]*ec_profiles[isample]['nwaves']
       ec_profiles[isample]['nrho'] = 0
       psi_based = 0
       psi_there = 0
       for iwave in range(ec_profiles[isample]['nwaves']):
           if size(waves[isample].coherent_wave[iwave].global_quantities) > 0:
               for itime in range(len(waves[isample].time)):
                   if waves[isample].coherent_wave[iwave].global_quantities[itime].power>0:
                       ec_profiles[isample]['is_active'][iwave] = 1
                       try:
                           ec_profiles[isample]['rho_tor_norm'] = 0
                           if len(waves[isample].coherent_wave[iwave].\
                                  profiles_1d[ec_profiles[isample]['it']].grid.rho_tor_norm) > 0:
                               ec_profiles[isample]['nrho'] = len(waves[isample].coherent_wave[iwave].\
                                    profiles_1d[ec_profiles[isample]['it']].grid.rho_tor_norm)
                               ec_profiles[isample]['rho_tor_norm'] = waves[isample].coherent_wave[iwave].\
                                  profiles_1d[ec_profiles[isample]['it']].grid.rho_tor_norm
                           elif len(waves[isample].coherent_wave[iwave].\
                                    profiles_1d[ec_profiles[isample]['it']].grid.rho_tor) > 0:
                               ec_profiles[isample]['nrho'] = len(waves[isample].coherent_wave[iwave].\
                                    profiles_1d[ec_profiles[isample]['it']].grid.rho_tor)
                               ec_profiles[isample]['rho_tor_norm'] = waves[isample].coherent_wave[iwave].\
                                  profiles_1d[ec_profiles[isample]['it']]\
                                   .grid.rho_tor/waves[isample].coherent_wave[iwave].\
                                   profiles_1d[ec_profiles[isample]['it']]\
                                   .grid.rho_tor[ec_profiles[isample]['nrho']-1]
                           elif len(waves[isample].coherent_wave[iwave].\
                                    profiles_1d[ec_profiles[isample]['it']].grid.psi) > 0:
                               psi_based = 1
                               ec_profiles[isample]['nrho'] = len(waves[isample].\
                                    coherent_wave[iwave].profiles_1d[ec_profiles[isample]['it']].grid.psi)
                               ec_profiles[isample]['rho_tor_norm'] = -waves[isample].\
                                  coherent_wave[iwave].profiles_1d[ec_profiles[isample]['it']].grid.psi
                       except:
                           print('waves.coherent_wave[iwave].profiles_1d[it]'+\
                                 '.grid.rho_tor_norm, rho_tor and psi could not be read', file=sys.stderr)
                           print('----> Aborted.', file=sys.stderr)
                           exit()
                       if ec_profiles[isample]['nrho']==0:
                           print('waves.coherent_wave[iwave].profiles_1d[it]'+\
                                 '.grid.rho_tor_norm, rho_tor and psi are empty', file=sys.stderr)
                           print('----> Aborted.', file=sys.stderr)
                           exit()
                       if len(waves[isample].coherent_wave[iwave].profiles_1d\
                              [ec_profiles[isample]['it']].grid.psi) > 0:
                           psi_there = 1
                           ec_profiles[isample]['psi'] = len(waves[isample].\
                              coherent_wave[iwave].profiles_1d[ec_profiles[isample]['it']].grid.psi)
                           ec_profiles[isample]['psi1d'] = -waves[isample].\
                              coherent_wave[iwave].profiles_1d[ec_profiles[isample]['it']].grid.psi
           else:
               print('waves.coherent_wave[iwave].global_quantities has not been allocated')
               print('----> Aborted.', file=sys.stderr)
               exit()

       if force_psi == 1:
           if psi_there == 0:
               print('The psi radial coordinate forced but the 1D psi profile is not filled')
               print('----> Aborted.', file=sys.stderr)
               exit()
           else:
               ec_profiles[isample]['nrho'] = ec_profiles[isample]['psi']
               ec_profiles[isample]['rho_tor_norm'] = ec_profiles[isample]['psi1d']

       if sum(ec_profiles[isample]['is_active'])==0:
           print('The waves IDS appears empty ----> Abort.', file=sys.stderr)
           exit()

       # LOOP OVER ALL EC LAUNCHERS
       ec_profiles[isample]['single_ec_launcher_name']         = {}
       ec_profiles[isample]['single_injected_power']           = {}   # for the chosen time slice
       ec_profiles[isample]['single_absorbed_power']           = {}   # for the chosen time slice
       ec_profiles[isample]['single_eccd']                     = {}   # for the chosen time slice
       ec_profiles[isample]['total_injected_power']            = 0    # for the chosen time slice

       ec_profiles[isample]['total_power_density_profile']     = [0]*ec_profiles[isample]['nrho'] # profile
       ec_profiles[isample]['total_current_density_profile']   = [0]*ec_profiles[isample]['nrho'] # profile
       ec_profiles[isample]['single_power_density_profile']    = {}   # profile
       ec_profiles[isample]['single_current_density_profile']  = {}   # profile

       ec_profiles[isample]['total_power_waveform']    = [0]*ec_profiles[isample]['ntime'] # waveform
       ec_profiles[isample]['total_current_waveform']  = [0]*ec_profiles[isample]['ntime'] # waveform
       ec_profiles[isample]['single_power_waveform']   = {}    # waveform
       ec_profiles[isample]['single_current_waveform'] = {}    # waveform

       for iwave in range(ec_profiles[isample]['nwaves']):
           ec_profiles[isample]['single_injected_power'][iwave] = 0

       for iwave in range(ec_profiles[isample]['nwaves']):
           if(len(waves[isample].coherent_wave[iwave].identifier.antenna_name)>0):
               ec_profiles[isample]['single_ec_launcher_name'][iwave] = \
                  waves[isample].coherent_wave[iwave].identifier.antenna_name
           else:
               ec_profiles[isample]['single_ec_launcher_name'][iwave] = 'Launcher'+str(iwave+1)
           if ec_profiles[isample]['is_active'][iwave]:
               ec_profiles[isample]['single_power_waveform'][iwave]   = []
               ec_profiles[isample]['single_current_waveform'][iwave] = []
               for itime in range(ec_profiles[isample]['ntime']):
                   ec_profiles[isample]['single_power_waveform'][iwave].\
                       append(waves[isample].coherent_wave[iwave].global_quantities[itime].electrons.power_thermal)
                   ec_profiles[isample]['single_current_waveform'][iwave].\
                       append(waves[isample].coherent_wave[iwave].global_quantities[itime].current_tor)
                   ec_profiles[isample]['total_power_waveform'][itime] = \
                       ec_profiles[isample]['total_power_waveform'][itime] \
                       + waves[isample].coherent_wave[iwave].global_quantities[itime].electrons.power_thermal
                   ec_profiles[isample]['total_current_waveform'][itime] = \
                       ec_profiles[isample]['total_current_waveform'][itime] \
                       + waves[isample].coherent_wave[iwave].global_quantities[itime].current_tor
               ec_profiles[isample]['total_power_density_profile']  = \
                   ec_profiles[isample]['total_power_density_profile']  \
                   + waves[isample].coherent_wave[iwave].profiles_1d[ec_profiles[isample]['it']].power_density
               ec_profiles[isample]['single_power_density_profile'][iwave] = \
                   waves[isample].coherent_wave[iwave].profiles_1d[ec_profiles[isample]['it']].power_density
               ec_profiles[isample]['total_current_density_profile'] = \
                   ec_profiles[isample]['total_current_density_profile'] \
                   + waves[isample].coherent_wave[iwave].profiles_1d[ec_profiles[isample]['it']].current_parallel_density
               ec_profiles[isample]['single_current_density_profile'][iwave] = \
                   waves[isample].coherent_wave[iwave].profiles_1d[ec_profiles[isample]['it']].current_parallel_density
               ec_profiles[isample]['single_injected_power[iwave]'] = 0.
               if len(waves[isample].coherent_wave[iwave].beam_tracing) > 0:
                  for ibeam in range(len(waves[isample].coherent_wave[iwave].beam_tracing[ec_profiles[isample]['it']].beam)):
                      ec_profiles[isample]['total_injected_power'] = \
                          ec_profiles[isample]['total_injected_power'] + \
                          waves[isample].coherent_wave[iwave].beam_tracing[ec_profiles[isample]['it']].beam[ibeam].power_initial
                      if imas.imasdef.isFieldValid(waves[isample].coherent_wave[iwave]\
                                                   .beam_tracing[ec_profiles[isample]['it']].beam[ibeam].power_initial):
                        ec_profiles[isample]['single_injected_power'][iwave] = \
                          ec_profiles[isample]['single_injected_power'][iwave] \
                          + waves[isample].coherent_wave[iwave].\
                          beam_tracing[ec_profiles[isample]['it']].beam[ibeam].power_initial
               ec_profiles[isample]['single_absorbed_power'][iwave] = \
                   waves[isample].coherent_wave[iwave].global_quantities[ec_profiles[isample]['it']].power
               ec_profiles[isample]['single_eccd'][iwave] = \
                   waves[isample].coherent_wave[iwave].global_quantities[ec_profiles[isample]['it']].current_tor
               print(' '+ec_profiles[isample]['single_ec_launcher_name'][iwave]\
                     +' is active with a power of {:.2f}'.format(ec_profiles[isample]['single_injected_power'][iwave]*1.e-6)\
                     +' MW --> Absorbed power = {:.2f}'.format(ec_profiles[isample]['single_absorbed_power'][iwave]*1.e-6)\
                     +' MW', file=sys.stderr)
               print('                                           --> ECCD =  {:.2e}'\
                     .format(ec_profiles[isample]['single_eccd'][iwave]*1.e-3)+' kA', file=sys.stderr)
           else:
               print(' '+ec_profiles[isample]['single_ec_launcher_name'][iwave]+' is off', file=sys.stderr)
       print('--------------------------------------------------------------------------', file=sys.stderr)

   ec_param={}
   ec_param['nsample']=nsample
   ec_param['psi_based']=psi_based
   ec_param['force_psi']=force_psi
   ec_param['shot']=shot
   ec_param['run']=run
   
   return ec_profiles,ec_param
       
###################################################################################

def find_nearest(a, a0):
    'Element in nd array `a` closest to the scalar value `a0`'
    idx = abs(a - a0).argmin()
    return a.flat[idx],idx

###################################################################################

def CustomLegend(legend):
    legfont = 12
    frame = legend.get_frame()
    frame.set_facecolor('0.95')
    for label in legend.get_texts():
        label.set_fontsize(legfont)
    for label in legend.get_lines():
        label.set_linewidth(1.5)  # the legend line width    
    return

###################################################################################

def ec_display(ec_profiles,ec_param):

   nsample   = ec_param['nsample']
   psi_based = ec_param['psi_based']
   force_psi = ec_param['force_psi']
   shot      = ec_param['shot']
   run       = ec_param['run']

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

   torcol = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']*10

   # PROFILE OF ABSORBED POWER DENSITY [MW/M3]
   fig,ax =plt.subplots(1,1)
   for isample in range(nsample):
       ec_profiles[isample]['single_ec_launcher_name'][3]='UL/USM'
       ec_profiles[isample]['single_ec_launcher_name'][4]='UL/BSM'
       if sum(ec_profiles[isample]['is_active'])>1 and nsample == 0:
           ax.plot(ec_profiles[isample]['rho_tor_norm'], \
                   ec_profiles[isample]['total_power_density_profile']*1.e-6,label=r'Total')
       for iwave in range(ec_profiles[isample]['nwaves']):
           if ec_profiles[isample]['is_active'][iwave]:
               if isample != 0:
                   ec_profiles[isample]['single_ec_launcher_name'][iwave]=''
               ax.plot(ec_profiles[isample]['rho_tor_norm'], \
                   ec_profiles[isample]['single_power_density_profile'][iwave]*1.e-6,\
                       label=ec_profiles[isample]['single_ec_launcher_name'][iwave],color=torcol[iwave])
   ax.set_ylabel('Absorbed power $\mathrm{[MW/m^{3}]}$')
   if psi_based == 0 and force_psi ==0:
       ax.set_xlabel('Normalized toroidal flux coordinate')
   else:
       ax.set_xlabel('-(Poloidal flux coordinate) [Wb]')
   plt.grid()
   legend = plt.legend()
   CustomLegend(legend)
   fig.set_size_inches(figure_width,figure_height)
   fig.tight_layout()
   fig.savefig('ECRH_profile_shot_{0}_run_{1}.png'.format(shot,run),bbox_inches="tight")
   #plt.title('Whatever')
   plt.show(block=False)

   # ECCD PROFILE [MA/M2]
   fig,ax =plt.subplots(1,1)
   for isample in range(nsample):
       if sum(ec_profiles[isample]['is_active'])>1 and nsample == 0:
           ax.plot(ec_profiles[isample]['rho_tor_norm'], \
                   ec_profiles[isample]['total_current_density_profile']*1.e-6,label=r'Total')
       for iwave in range(ec_profiles[isample]['nwaves']):
           if ec_profiles[isample]['is_active'][iwave]:
               ax.plot(ec_profiles[isample]['rho_tor_norm'], \
                       ec_profiles[isample]['single_current_density_profile'][iwave]*1.e-6,\
                       label=ec_profiles[isample]['single_ec_launcher_name'][iwave],color=torcol[iwave])
   ax.set_ylabel('$\mathrm{ECCD} [MA/m^{2}]}$')
   if psi_based == 0 and force_psi ==0:
       ax.set_xlabel('Normalized toroidal flux coordinate')
   else:
       ax.set_xlabel('-(Poloidal flux coordinate) [Wb]')
   plt.grid()
   legend = plt.legend()
   CustomLegend(legend)
   fig.set_size_inches(figure_width,figure_height)
   fig.tight_layout()
   fig.savefig('ECCD_profile_shot_{0}_run_{1}.png'.format(shot,run),bbox_inches="tight")
   #plt.title('Whatever')

   # EC POWER AND ECCD WAVEFORMS
   if ec_profiles[isample]['ntime']==1:
       print('Only one time slice --> ECRH and ECCD waveforms not displayed', file=sys.stderr)
       plt.show(block=True)
   else:
       plt.show(block=False)
       # EC POWER WAVEFORM
       fig,ax =plt.subplots(1,1)
       for isample in range(nsample):
           if sum(ec_profiles[isample]['is_active'])>1 and nsample == 0:
               ax.plot(ec_profiles[isample]['timevec'], \
                       array(ec_profiles[isample]['total_power_waveform'])*1.e-6,label=r'Total')
           for iwave in range(ec_profiles[isample]['nwaves']):
               if ec_profiles[isample]['is_active'][iwave]:
                   ax.plot(ec_profiles[isample]['timevec'], \
                           array(ec_profiles[isample]['single_power_waveform'][iwave])*1.e-6,\
                           label=ec_profiles[isample]['single_ec_launcher_name'][iwave])
       ax.set_ylabel('Power to the electrons $\mathrm{[MW]}$')
       ax.set_xlabel('Time (s)')
       plt.grid()
       legend = plt.legend()
       CustomLegend(legend)
       fig.set_size_inches(figure_width,figure_height)
       fig.tight_layout()
       fig.savefig('ECRH_waveform_shot_{0}_run_{1}.png'.format(shot,run),bbox_inches="tight")
       #plt.title('Whatever')
       #plt.gca().set_ylim(0,max(total_power_waveform)*1.2e-6)
       plt.show(block=False)

       # ECCD WAVEFORM
       fig,ax =plt.subplots(1,1)
       for isample in range(nsample):
           if sum(ec_profiles[isample]['is_active'])>1 and nsample == 0:
               ax.plot(ec_profiles[isample]['timevec'], \
                       array(ec_profiles[isample]['total_current_waveform'])*1.e-3,label=r'Total')
           for iwave in range(ec_profiles[isample]['nwaves']):
               if ec_profiles[isample]['is_active'][iwave]:
                   ax.plot(ec_profiles[isample]['timevec'], \
                           array(ec_profiles[isample]['single_current_waveform'][iwave])*1.e-3,
                           label=ec_profiles[isample]['single_ec_launcher_name'][iwave])
       ax.set_ylabel('ECCD $\mathrm{[kA]}$')
       ax.set_xlabel('Time (s)')
       plt.grid()
       legend = plt.legend()
       CustomLegend(legend)
       fig.set_size_inches(figure_width,figure_height)
       fig.tight_layout()
       fig.savefig('ECCD_waveform_shot_{0}_run_{1}.png'.format(shot,run),bbox_inches="tight")
       #plt.title('Whatever')
       #plt.gca().set_ylim(0,max(array(total_current_waveform))*1.2e-3)
       plt.show(block=True)

###################################################################################
def run(args):
  ec_profiles,ec_param = ec_prep(args)
  ec_display(ec_profiles,ec_param)

# When hcd_waves_plot is called directly
if __name__ == "__main__":
   run(args)


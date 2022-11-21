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
   parser.add_argument('-l','--legoff',help='= 1 to remove the legend from graphs', required=False)

   args  = vars(parser.parse_args())

###################################################################################

def waves_prep(args):

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
       
   if args['legoff'] != None:
      legoff = int(args['legoff'])
   else:
      legoff = 0

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

   hcd_profiles = {}
   for isample in range(nsample):
       hcd_profiles[isample] = {}
       hcd_profiles[isample]['time'] = time
       hcd_profiles[isample]['timevec'] = waves[isample].time
       hcd_profiles[isample]['ntime'] = len(hcd_profiles[isample]['timevec'])
       if hcd_profiles[isample]['ntime']==1:
           if len(hcd_profiles[isample]['timevec']) > 0:
               hcd_profiles[isample]['tc'] = hcd_profiles[isample]['timevec'][0]
           else:
               hcd_profiles[isample]['tc'] = 0
           hcd_profiles[isample]['it'] = 0
       else:
           if hcd_profiles[isample]['time']>=0:
               [hcd_profiles[isample]['tc'],hcd_profiles[isample]['it']] = \
                  find_nearest(hcd_profiles[isample]['timevec'],hcd_profiles[isample]['time'])
           else:
               hcd_profiles[isample]['it'] = int(hcd_profiles[isample]['ntime']/2)
               hcd_profiles[isample]['tc'] = hcd_profiles[isample]['timevec'][hcd_profiles[isample]['it']]
           print('--------------------------------------------------------------------------', file=sys.stderr)
           print(' Time  = '+'%.2f' % hcd_profiles[isample]['tc']+' s in range ['+'%.2f'
                 % hcd_profiles[isample]['timevec'][0]+','+'%.2f' \
                 % hcd_profiles[isample]['timevec'][hcd_profiles[isample]['ntime']-1]+'] s', file=sys.stderr)
           print(' Index = ',str(hcd_profiles[isample]['it']), file=sys.stderr)
           print(' Averaged resolution = ', (hcd_profiles[isample]['timevec'][hcd_profiles[isample]['ntime']-1]
                                             -hcd_profiles[isample]['timevec'][0])\
                 /(hcd_profiles[isample]['ntime']-1),' s', file=sys.stderr)  
           print('--------------------------------------------------------------------------', file=sys.stderr)
       hcd_profiles[isample]['time'] = hcd_profiles[isample]['tc']

       hcd_profiles[isample]['nwaves'] = len(waves[isample].coherent_wave)
       hcd_profiles[isample]['is_active'] = [0]*hcd_profiles[isample]['nwaves']
       hcd_profiles[isample]['nrho'] = 0
       psi_based = 0
       psi_there = 0
       for iwave in range(hcd_profiles[isample]['nwaves']):
           if size(waves[isample].coherent_wave[iwave].global_quantities) > 0:
               for itime in range(len(waves[isample].time)):
                   if waves[isample].coherent_wave[iwave].global_quantities[itime].power>0:
                       hcd_profiles[isample]['is_active'][iwave] = 1
                       try:
                           hcd_profiles[isample]['rho_tor_norm'] = 0
                           if len(waves[isample].coherent_wave[iwave].\
                                  profiles_1d[hcd_profiles[isample]['it']].grid.rho_tor_norm) > 0:
                               hcd_profiles[isample]['nrho'] = len(waves[isample].coherent_wave[iwave].\
                                    profiles_1d[hcd_profiles[isample]['it']].grid.rho_tor_norm)
                               hcd_profiles[isample]['rho_tor_norm'] = waves[isample].coherent_wave[iwave].\
                                  profiles_1d[hcd_profiles[isample]['it']].grid.rho_tor_norm
                           elif len(waves[isample].coherent_wave[iwave].\
                                    profiles_1d[hcd_profiles[isample]['it']].grid.rho_tor) > 0:
                               hcd_profiles[isample]['nrho'] = len(waves[isample].coherent_wave[iwave].\
                                    profiles_1d[hcd_profiles[isample]['it']].grid.rho_tor)
                               hcd_profiles[isample]['rho_tor_norm'] = waves[isample].coherent_wave[iwave].\
                                  profiles_1d[hcd_profiles[isample]['it']]\
                                   .grid.rho_tor/waves[isample].coherent_wave[iwave].\
                                   profiles_1d[hcd_profiles[isample]['it']]\
                                   .grid.rho_tor[hcd_profiles[isample]['nrho']-1]
                           elif len(waves[isample].coherent_wave[iwave].\
                                    profiles_1d[hcd_profiles[isample]['it']].grid.psi) > 0:
                               psi_based = 1
                               hcd_profiles[isample]['nrho'] = len(waves[isample].\
                                    coherent_wave[iwave].profiles_1d[hcd_profiles[isample]['it']].grid.psi)
                               hcd_profiles[isample]['rho_tor_norm'] = -waves[isample].\
                                  coherent_wave[iwave].profiles_1d[hcd_profiles[isample]['it']].grid.psi
                       except:
                           print('waves.coherent_wave[iwave].profiles_1d[it]'+\
                                 '.grid.rho_tor_norm, rho_tor and psi could not be read', file=sys.stderr)
                           print('----> Aborted.', file=sys.stderr)
                           exit()
                       if hcd_profiles[isample]['nrho']==0:
                           print('waves.coherent_wave[iwave].profiles_1d[it]'+\
                                 '.grid.rho_tor_norm, rho_tor and psi are empty', file=sys.stderr)
                           print('----> Aborted.', file=sys.stderr)
                           exit()
                       if len(waves[isample].coherent_wave[iwave].profiles_1d\
                              [hcd_profiles[isample]['it']].grid.psi) > 0:
                           psi_there = 1
                           hcd_profiles[isample]['psi'] = len(waves[isample].\
                              coherent_wave[iwave].profiles_1d[hcd_profiles[isample]['it']].grid.psi)
                           hcd_profiles[isample]['psi1d'] = -waves[isample].\
                              coherent_wave[iwave].profiles_1d[hcd_profiles[isample]['it']].grid.psi
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
               hcd_profiles[isample]['nrho'] = hcd_profiles[isample]['psi']
               hcd_profiles[isample]['rho_tor_norm'] = hcd_profiles[isample]['psi1d']

       if sum(hcd_profiles[isample]['is_active'])==0:
           print('The waves IDS appears empty ----> Abort.', file=sys.stderr)
           exit()

       # LOOP OVER ALL EC LAUNCHERS
       hcd_profiles[isample]['single_hcd_launcher_name']         = {}
       hcd_profiles[isample]['single_injected_power']           = {}   # for the chosen time slice
       hcd_profiles[isample]['single_absorbed_power']           = {}   # for the chosen time slice
       hcd_profiles[isample]['single_cd']                     = {}   # for the chosen time slice
       hcd_profiles[isample]['total_injected_power']            = 0    # for the chosen time slice

       hcd_profiles[isample]['total_power_density_profile']     = [0]*hcd_profiles[isample]['nrho'] # profile
       hcd_profiles[isample]['total_current_density_profile']   = [0]*hcd_profiles[isample]['nrho'] # profile
       hcd_profiles[isample]['single_power_density_profile']    = {}   # profile
       hcd_profiles[isample]['single_current_density_profile']  = {}   # profile

       hcd_profiles[isample]['total_power_waveform']    = [0]*hcd_profiles[isample]['ntime'] # waveform
       hcd_profiles[isample]['total_current_waveform']  = [0]*hcd_profiles[isample]['ntime'] # waveform
       hcd_profiles[isample]['single_power_waveform']   = {}    # waveform
       hcd_profiles[isample]['single_current_waveform'] = {}    # waveform

       for iwave in range(hcd_profiles[isample]['nwaves']):
           hcd_profiles[isample]['single_injected_power'][iwave] = 0

       for iwave in range(hcd_profiles[isample]['nwaves']):
           if(len(waves[isample].coherent_wave[iwave].identifier.antenna_name)>0):
               hcd_profiles[isample]['single_hcd_launcher_name'][iwave] = \
                  waves[isample].coherent_wave[iwave].identifier.antenna_name
           else:
               hcd_profiles[isample]['single_hcd_launcher_name'][iwave] = 'Launcher'+str(iwave+1)
           if hcd_profiles[isample]['is_active'][iwave]:
               hcd_profiles[isample]['single_power_waveform'][iwave]   = []
               hcd_profiles[isample]['single_current_waveform'][iwave] = []
               for itime in range(hcd_profiles[isample]['ntime']):
                   hcd_profiles[isample]['single_power_waveform'][iwave].\
                       append(waves[isample].coherent_wave[iwave].global_quantities[itime].electrons.power_thermal)
                   hcd_profiles[isample]['single_current_waveform'][iwave].\
                       append(waves[isample].coherent_wave[iwave].global_quantities[itime].current_tor)
                   hcd_profiles[isample]['total_power_waveform'][itime] = \
                       hcd_profiles[isample]['total_power_waveform'][itime] \
                       + waves[isample].coherent_wave[iwave].global_quantities[itime].electrons.power_thermal
                   hcd_profiles[isample]['total_current_waveform'][itime] = \
                       hcd_profiles[isample]['total_current_waveform'][itime] \
                       + waves[isample].coherent_wave[iwave].global_quantities[itime].current_tor
               hcd_profiles[isample]['total_power_density_profile']  = \
                   hcd_profiles[isample]['total_power_density_profile']  \
                   + waves[isample].coherent_wave[iwave].profiles_1d[hcd_profiles[isample]['it']].power_density
               hcd_profiles[isample]['single_power_density_profile'][iwave] = \
                   waves[isample].coherent_wave[iwave].profiles_1d[hcd_profiles[isample]['it']].power_density
               hcd_profiles[isample]['total_current_density_profile'] = \
                   hcd_profiles[isample]['total_current_density_profile'] \
                   + waves[isample].coherent_wave[iwave].profiles_1d[hcd_profiles[isample]['it']].current_parallel_density
               hcd_profiles[isample]['single_current_density_profile'][iwave] = \
                   waves[isample].coherent_wave[iwave].profiles_1d[hcd_profiles[isample]['it']].current_parallel_density
               hcd_profiles[isample]['single_injected_power[iwave]'] = 0.
               if len(waves[isample].coherent_wave[iwave].beam_tracing) > 0:
                  for ibeam in range(len(waves[isample].coherent_wave[iwave].beam_tracing[hcd_profiles[isample]['it']].beam)):
                      hcd_profiles[isample]['total_injected_power'] = \
                          hcd_profiles[isample]['total_injected_power'] + \
                          waves[isample].coherent_wave[iwave].beam_tracing[hcd_profiles[isample]['it']].beam[ibeam].power_initial
                      if imas.imasdef.isFieldValid(waves[isample].coherent_wave[iwave]\
                                                   .beam_tracing[hcd_profiles[isample]['it']].beam[ibeam].power_initial):
                        hcd_profiles[isample]['single_injected_power'][iwave] = \
                          hcd_profiles[isample]['single_injected_power'][iwave] \
                          + waves[isample].coherent_wave[iwave].\
                          beam_tracing[hcd_profiles[isample]['it']].beam[ibeam].power_initial
               hcd_profiles[isample]['single_absorbed_power'][iwave] = \
                   waves[isample].coherent_wave[iwave].global_quantities[hcd_profiles[isample]['it']].power
               hcd_profiles[isample]['single_cd'][iwave] = \
                   waves[isample].coherent_wave[iwave].global_quantities[hcd_profiles[isample]['it']].current_tor
               print(' '+hcd_profiles[isample]['single_hcd_launcher_name'][iwave]\
                     +' is active with a power of {:.2f}'.format(hcd_profiles[isample]['single_injected_power'][iwave]*1.e-6)+' MW')
               print('   --> Absorbed power = {:.2f}'.format(hcd_profiles[isample]['single_absorbed_power'][iwave]*1.e-6)\
                     +' MW', file=sys.stderr)
               print('   --> Curent Drive =  {:.2e}'.format(hcd_profiles[isample]['single_cd'][iwave]*1.e-3)+' kA', file=sys.stderr)
           else:
               print(' '+hcd_profiles[isample]['single_hcd_launcher_name'][iwave]+' is off', file=sys.stderr)
       print('--------------------------------------------------------------------------', file=sys.stderr)

   hcd_param={}
   hcd_param['nsample']=nsample
   hcd_param['psi_based']=psi_based
   hcd_param['force_psi']=force_psi
   hcd_param['legoff']=legoff
   hcd_param['shot']=shot
   hcd_param['run']=run
   
   return hcd_profiles,hcd_param
       
###################################################################################

def find_nearest(a, a0):
    'Element in nd array `a` closest to the scalar value `a0`'
    idx = abs(a - a0).argmin()
    return a.flat[idx],idx

###################################################################################

def CustomLegend(legend):
    legfont = 6
    frame = legend.get_frame()
    frame.set_facecolor('0.95')
    for label in legend.get_texts():
        label.set_fontsize(legfont)
    for label in legend.get_lines():
        label.set_linewidth(1.5)  # the legend line width    
    return

###################################################################################

def waves_display(hcd_profiles,hcd_param):

   nsample   = hcd_param['nsample']
   psi_based = hcd_param['psi_based']
   force_psi = hcd_param['force_psi']
   shot      = hcd_param['shot']
   run       = hcd_param['run']
   legoff    = hcd_param['legoff']

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
       hcd_profiles[isample]['single_hcd_launcher_name'][3]='UL/USM'
       hcd_profiles[isample]['single_hcd_launcher_name'][4]='UL/BSM'
       if sum(hcd_profiles[isample]['is_active'])>1 and nsample == 0:
           ax.plot(hcd_profiles[isample]['rho_tor_norm'], \
                   hcd_profiles[isample]['total_power_density_profile']*1.e-6,label=r'Total')
       for iwave in range(hcd_profiles[isample]['nwaves']):
           if hcd_profiles[isample]['is_active'][iwave]:
               if isample != 0:
                   hcd_profiles[isample]['single_hcd_launcher_name'][iwave]=''
               ax.plot(hcd_profiles[isample]['rho_tor_norm'], \
                   hcd_profiles[isample]['single_power_density_profile'][iwave]*1.e-6,\
                       label=hcd_profiles[isample]['single_hcd_launcher_name'][iwave],color=torcol[iwave])
   ax.set_ylabel('Absorbed power $\mathrm{[MW/m^{3}]}$')
   if psi_based == 0 and force_psi ==0:
       ax.set_xlabel('Normalized toroidal flux coordinate')
   else:
       ax.set_xlabel('-(Poloidal flux coordinate) [Wb]')
   plt.grid()
   if legoff == 0:
      legend = plt.legend()
      CustomLegend(legend)
   fig.set_size_inches(figure_width,figure_height)
   fig.tight_layout()
   fig.savefig('ECRH_profile_shot_{0}_run_{1}.png'.format(shot,run),bbox_inches="tight")
   #plt.title('Whatever')
   plt.show(block=False)

   # CD PROFILE [MA/M2]
   fig,ax =plt.subplots(1,1)
   for isample in range(nsample):
       if sum(hcd_profiles[isample]['is_active'])>1 and nsample == 0:
           ax.plot(hcd_profiles[isample]['rho_tor_norm'], \
                   hcd_profiles[isample]['total_current_density_profile']*1.e-6,label=r'Total')
       for iwave in range(hcd_profiles[isample]['nwaves']):
           if hcd_profiles[isample]['is_active'][iwave]:
               ax.plot(hcd_profiles[isample]['rho_tor_norm'], \
                       hcd_profiles[isample]['single_current_density_profile'][iwave]*1.e-6,\
                       label=hcd_profiles[isample]['single_hcd_launcher_name'][iwave],color=torcol[iwave])
   ax.set_ylabel('$\mathrm{CD} [MA/m^{2}]}$')
   if psi_based == 0 and force_psi ==0:
       ax.set_xlabel('Normalized toroidal flux coordinate')
   else:
       ax.set_xlabel('-(Poloidal flux coordinate) [Wb]')
   plt.grid()
   if legoff == 0:
      legend = plt.legend()
      CustomLegend(legend)
   fig.set_size_inches(figure_width,figure_height)
   fig.tight_layout()
   fig.savefig('CD_profile_shot_{0}_run_{1}.png'.format(shot,run),bbox_inches="tight")
   #plt.title('Whatever')

   # EC POWER AND CD WAVEFORMS
   if hcd_profiles[isample]['ntime']==1:
       print('Only one time slice --> ECRH and CD waveforms not displayed', file=sys.stderr)
       plt.show(block=True)
   else:
       plt.show(block=False)
       # EC POWER WAVEFORM
       fig,ax =plt.subplots(1,1)
       for isample in range(nsample):
           if sum(hcd_profiles[isample]['is_active'])>1 and nsample == 0:
               ax.plot(hcd_profiles[isample]['timevec'], \
                       array(hcd_profiles[isample]['total_power_waveform'])*1.e-6,label=r'Total')
           for iwave in range(hcd_profiles[isample]['nwaves']):
               if hcd_profiles[isample]['is_active'][iwave]:
                   ax.plot(hcd_profiles[isample]['timevec'], \
                           array(hcd_profiles[isample]['single_power_waveform'][iwave])*1.e-6,\
                           label=hcd_profiles[isample]['single_hcd_launcher_name'][iwave])
       ax.set_ylabel('Power to the electrons $\mathrm{[MW]}$')
       ax.set_xlabel('Time (s)')
       plt.grid()
       if legoff == 0:
          legend = plt.legend()
          CustomLegend(legend)
       fig.set_size_inches(figure_width,figure_height)
       fig.tight_layout()
       fig.savefig('ECRH_waveform_shot_{0}_run_{1}.png'.format(shot,run),bbox_inches="tight")
       #plt.title('Whatever')
       #plt.gca().set_ylim(0,max(total_power_waveform)*1.2e-6)
       plt.show(block=False)

       # CD WAVEFORM
       fig,ax =plt.subplots(1,1)
       for isample in range(nsample):
           if sum(hcd_profiles[isample]['is_active'])>1 and nsample == 0:
               ax.plot(hcd_profiles[isample]['timevec'], \
                       array(hcd_profiles[isample]['total_current_waveform'])*1.e-3,label=r'Total')
           for iwave in range(hcd_profiles[isample]['nwaves']):
               if hcd_profiles[isample]['is_active'][iwave]:
                   ax.plot(hcd_profiles[isample]['timevec'], \
                           array(hcd_profiles[isample]['single_current_waveform'][iwave])*1.e-3,
                           label=hcd_profiles[isample]['single_hcd_launcher_name'][iwave])
       ax.set_ylabel('CD $\mathrm{[kA]}$')
       ax.set_xlabel('Time (s)')
       plt.grid()
       if legoff == 0:
          legend = plt.legend()
          CustomLegend(legend)
       fig.set_size_inches(figure_width,figure_height)
       fig.tight_layout()
       fig.savefig('CD_waveform_shot_{0}_run_{1}.png'.format(shot,run),bbox_inches="tight")
       #plt.title('Whatever')
       #plt.gca().set_ylim(0,max(array(total_current_waveform))*1.2e-3)
       plt.show(block=True)

###################################################################################
def run(args):
  hcd_profiles,hcd_param = waves_prep(args)
  waves_display(hcd_profiles,hcd_param)

# When hcd_waves_plot is called directly
if __name__ == "__main__":
   run(args)


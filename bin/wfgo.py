# -------------------------------------------------------------------------------------
# PURPOSE:
# - TO CONFIGURE WAVEFORM OF DYNAMIC DATA FOR ANY IDS
# - TO RE-GENERATE STATIC MACHINE DESCRIPTION DATA FOR EC_LAUNCHERS, IC_LAUNCHERS, NBI
# -------------------------------------------------------------------------------------

def add_dynamic(configuration_file,ksave=0,kplot=0,kverif=0):

    import yaml, imas, os
    import numpy as np

    # -----------------------------------------------------------------------------------------

    # READ CONFIGURATION FILE
    file = open(configuration_file, 'r')
    config = yaml.load(file,Loader=yaml.CLoader)
    file.close()

    idsname    = config['ids']
    shot       = int(config['database']['shot'])
    run        = int(config['database']['run'])
    user       = config['database']['user']
    db         = config['database']['db']
    time_array = config['time']

    #shot = 0 # Test re-generation of static data
    
    # -----------------------------------------------------------------------------------------

    # CREATE DATA FROM SCRATCH (I.E. CREATE ALSO STATIC DATA)
    if shot == 0:
        print('MD data created from scratch')
        if idsname == 'ec_launchers':
            ids = imas.ec_launchers()
            ids.launcher.resize(config['nlaunchers'])
            for key,value in config['static_variables'].items():
                if type(value) == str:
                    data = value
                elif type(value) == list:
                    data = np.array([float(i) for i in value])
                else:
                    data = value
                exec('ids.'+key+' = data')
        elif idsname == 'ic_antennas':
            ids = imas.ic_antennas()
            ids.antenna.resize(config['nantenna'])
            for antenna in range(len(ids.antenna)):
                ids.antenna[antenna].module.resize(config['nmodule'])
                for module in range(len(ids.antenna[antenna].module)):
                    ids.antenna[antenna].module[module].strap.resize(config['nstrap'])
            for key,value in config['static_variables'].items():
                if type(value) == str:
                    data = value
                elif type(value) == list:
                    data = np.array([float(i) for i in value])
                else:
                    data = value
                exec('ids.'+key+' = data')
        elif idsname == 'nbi':
            ids = imas.nbi()
            ids.unit.resize(config['nunit'])
            for unit in range(len(ids.unit)):
                ids.unit[unit].beamlets_group.resize(config['nbeamletgroup'])
                for bg in range(len(ids.unit[unit].beamlets_group)):
                    ids.unit[unit].beamlets_group[bg].divergence_component.resize(config['ndivcomponent'])
                    ids.unit[unit].beamlets_group[bg].beamlets.positions.r.resize(config['nbeamlet'])
                    ids.unit[unit].beamlets_group[bg].beamlets.positions.z.resize(config['nbeamlet'])
                    ids.unit[unit].beamlets_group[bg].beamlets.positions.phi.resize(config['nbeamlet'])
                    ids.unit[unit].beamlets_group[bg].beamlets.tangency_radii.resize(config['nbeamlet'])
                    ids.unit[unit].beamlets_group[bg].beamlets.angles.resize(config['nbeamlet'])
                    ids.unit[unit].beamlets_group[bg].beamlets.power_fractions.resize(config['nbeamlet'])
            for key,value in config['static_variables'].items():
                if type(value) == str:
                    data = value
                elif type(value) == list:
                    data = np.array([float(i) for i in value])
                else:
                    data = value
                exec('ids.'+key+' = data')
        else:
            print('IDS not implemented yet')
            return []
        ids.code.name = 'wfgo'
        ids.code.version = 'beta'
        ids.code.repository = 'tbd'
        ids.ids_properties.provider = 'Mireille Schneider'

    # READ INPUT DATAFILE TO GET STATIC DATA FROM MD DATABASE
    else:
        print('IDS to modify      = ',idsname)
        print('Shot/run/user/db   = ',str(shot)+'/'+str(run)+'/'+user+'/'+db)
        print('General time array = ',time_array)

        input = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,db,shot,run,user)
        retstatus, idx = input.open()
        if retstatus != 0:
            print("   ERROR while reading the input datafile",str(shot)+'/'+str(run)+'/'+user+'/'+db)
            print("   Please check that the file exists.")
            print("   --> Aborted.")
            exit()
        ids = input.get(idsname)
        input.close()

   # -----------------------------------------------------------------------------------------

    # A PRIORI THE TIME IS HOMOGENEOUS (UNLESS CONFIGURED DIFFERENTLY IN YAML FILE)
    ids.time = np.array([float(i) for i in time_array])
    ids.ids_properties.homogeneous_time = 1

    for key,value in config['dynamic_variables'].items():
        if not hasattr(value,'__len__'):
            data = value
        elif type(value[0]) != list:
            dim = 1 # 1D arrays
            data = np.array([float(i) for i in value])
        else:
            dim = 2 # 2D arrays
            data = np.array(value)
        time = np.array([float(i) for i in time_array])
        if hasattr(data,'__len__') and len(data)!=len(time_array):# Single values transformed into arrays vs. time
            if dim==1 and data.shape[0] == 1:
                data = np.array([data[0]]*len(time_array))
            if dim==2 and data.shape[1] == 1:
                data = np.squeeze(np.transpose(np.array([data]*len(time_array))),axis=0)
        exec('ids.'+key+' = data')
        exec('.'.join(str('ids.'+key).split('.')[0:-1])+'.time = time')
        if '.time' in key:
            exec('ids.'+key+' = data')
            ids.ids_properties.homogeneous_time = 0

    # -----------------------------------------------------------------------------------------

    # -------------------------
    # EXTRA OPTIONAL OPERATIONS
    # -------------------------

    if kverif == 1:
        ksave = 1

    # SAVE THE DATAFILE
    if ksave == 1:

        # IF LOCAL DATABASE DOES NOT EXIST: CREATE IT
        local_database = os.getenv("HOME") + "/public/imasdb/" + db + "/3/0"
        if os.path.isdir(local_database) == False:
            print("-- Create local database " + local_database)
            os.makedirs(local_database)

        # CREATE OUTPUT DATAFILE
        run_out = run+100
        output = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,db,shot,run_out,os.getenv("USER"))
        retstatus, idx = output.create()
        if retstatus != 0:
            print("   ERROR while creating the output datafile ",str(shot)+'/'+str(run_out)+'/'+user+'/'+db)
            print("   --> Aborted.")
            exit()
        try:
            output.put(ids)
            print("--> File saved into",str(shot)+'/'+str(run_out)+'/'+os.getenv("USER")+'/'+db)
        except Exception as err:
            print(err)
            print("Save failed: something is wrong in the data configuration.")
        output.close()

    # VERIFY THAT GET_SLICE IS HAPPY
    if kverif == 1:
        input = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,db,shot,run_out,os.getenv("USER"))
        input.open()
        idstest = input.get_slice(idsname,200.,1,0)
        input.close()

    # PLOT THE RESULT (PART OF THE VERIFICATION PROCEDURE)
    if kplot == 1 or kverif == 1:
        
        import matplotlib
        matplotlib.use('TKagg')
        import matplotlib.pyplot as plt
        plt.figure()

        if idsname == 'ec_launchers':
        
            # Can sum up only for homoegeneous times, since no interpolation is implemented
            if ids.ids_properties.homogeneous_time == 1: 
                power_launched = np.zeros(len(ids.launcher[0].power_launched.data))
                for launcher in range(len(ids.launcher)):
                    power_launched = power_launched + ids.launcher[launcher].power_launched.data

            if ids.ids_properties.homogeneous_time == 1 and len(ids.launcher)>1:
                plt.plot(ids.time,power_launched*1.e-6,label='Total',color='r',linewidth=2)
            for launcher in range(len(ids.launcher)):    
                plt.plot(ids.launcher[launcher].power_launched.time,ids.launcher[launcher].power_launched.data*1.e-6, \
                        label=ids.launcher[launcher].name)
                
        elif idsname == 'ic_antennas':
            
            # Can sum up only for homoegeneous times, since no interpolation is implemented
            if ids.ids_properties.homogeneous_time == 1: 
                power_launched = np.zeros(len(ids.antenna[0].power_launched.data))
                for antenna in range(len(ids.antenna)):
                    power_launched = power_launched + ids.antenna[antenna].power_launched.data

            if ids.ids_properties.homogeneous_time == 1 and len(ids.antenna)>1:
                plt.plot(ids.time,power_launched*1.e-6,label='Total',color='r',linewidth=2)
            for antenna in range(len(ids.antenna)):    
                plt.plot(ids.antenna[antenna].power_launched.time,ids.antenna[antenna].power_launched.data*1.e-6, \
                        label=ids.antenna[antenna].name)

        elif idsname == 'nbi':
            
            # Can sum up only for homoegeneous times, since no interpolation is implemented
            if ids.ids_properties.homogeneous_time == 1: 
                power_launched = np.zeros(len(ids.unit[0].power_launched.data))
                for unit in range(len(ids.unit)):
                    power_launched = power_launched + ids.unit[unit].power_launched.data

            if ids.ids_properties.homogeneous_time == 1 and len(ids.unit)>1:
                plt.plot(ids.time,power_launched*1.e-6,label='Total',color='r',linewidth=2)
            for unit in range(len(ids.unit)):    
                plt.plot(ids.unit[unit].power_launched.time,ids.unit[unit].power_launched.data*1.e-6, \
                        label=ids.unit[unit].name)

        else:
            print('Visualization not implemented for this IDS yet')
            return ids
                
        plt.xlabel('Time (s)')
        plt.ylabel('Power (MW)')
        plt.grid()
        legend = plt.legend(loc='upper right')
        if kplot == 1:
            plt.show(block=True)

    return ids

# --------------------------------------------------------------------------------------------

# TEST THE TOOL
#ids = add_dynamic('input/ec_waveforms.yaml',ksave=1,kplot=1,kverif=1)
#ids = add_dynamic('input/ic_waveforms.yaml',ksave=1,kplot=1,kverif=1)
#ids = add_dynamic('input/nb_waveforms.yaml',ksave=1,kplot=1,kverif=1)

# Verif ec_launchers: use unique t=0, [10, 0, 0, 10, 0 ] MW
# idsdiff  -u public --database ITER_MD --userB schneim --databaseB ITER_MD 120000 1 120000 101 ec_launchers --skip-provenance

# Verif ic_antennas: use unique t=200s, 10MW
# idsdiff  -u public --database ITER_MD --userB schneim --databaseB ITER_MD 110000 1 110000 101 ic_antennas --skip-provenance

# Verif nbi: use unique t=300s, 16.5 MW / 1 MeV on each box
# idsdiff  -u public --database ITER_MD --userB schneim --databaseB ITER_MD 130000 2301 130000 2401 nbi --skip-provenance


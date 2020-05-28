import imas,os

version = os.getenv('IMAS_VERSION')[0]

# ----------------------------------------------------------------------
def get_equilibrium(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.equilibrium.get()
    else:
      input.equilibrium.get(occ)
    input.close()
    return input.equilibrium

# ----------------------------------------------------------------------
def get_core_profiles(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.core_profiles.get()
    else:
      input.core_profiles.get(occ)
    input.close()
    return input.core_profiles

# ----------------------------------------------------------------------
def get_nbi(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.nbi.get()
    else:
      input.nbi.get(occ)
    input.close()
    return input.nbi

# ----------------------------------------------------------------------
def get_ic_antennas(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.ic_antennas.get()
    else:
      input.ic_antennas.get(occ)
    input.close()
    return input.ic_antennas

# ----------------------------------------------------------------------
def get_ec_antennas(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.ec_antennas.get()
    else:
      input.ec_antennas.get(occ)
    input.close()
    return input.ec_antennas

# ----------------------------------------------------------------------
def get_ec_launchers(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.ec_launchers.get()
    else:
      input.ec_launchers.get(occ)
    input.close()
    return input.ec_launchers

# ----------------------------------------------------------------------
def get_summary(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.summary.get()
    else:
      input.summary.get(occ)
    input.close()
    return input.summary

# ----------------------------------------------------------------------
def get_charge_exchange(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.charge_exchange.get()
    else:
      input.charge_exchange.get(occ)
    input.close()
    return input.charge_exchange

# ----------------------------------------------------------------------
def get_core_sources(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.core_sources.get()
    else:
      input.core_sources.get(occ)
    input.close()
    return input.core_sources

# ----------------------------------------------------------------------
def get_core_transport(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.core_transport.get()
    else:
      input.core_transport.get(occ)
    input.close()
    return input.core_transport

# ----------------------------------------------------------------------
def get_dataset_description(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.dataset_description.get()
    else:
      input.dataset_description.get(occ)
    input.close()
    return input.dataset_description

# ----------------------------------------------------------------------
def get_distributions(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.distributions.get()
    else:
      input.distributions.get(occ)
    input.close()
    return input.distributions

# ----------------------------------------------------------------------
def get_distribution_sources(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.distribution_sources.get()
    else:
      input.distribution_sources.get(occ)
    input.close()
    return input.distribution_sources

# ----------------------------------------------------------------------
def get_edge_profiles(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.edge_profiles.get()
    else:
      input.edge_profiles.get(occ)
    input.close()
    return input.edge_profiles

# ----------------------------------------------------------------------
def get_edge_sources(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.edge_sources.get()
    else:
      input.edge_sources.get(occ)
    input.close()
    return input.edge_sources

# ----------------------------------------------------------------------
def get_magnetics(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.magnetics.get()
    else:
      input.magnetics.get(occ)
    input.close()
    return input.magnetics

# ----------------------------------------------------------------------
def get_pf_active(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.pf_active.get()
    else:
      input.pf_active.get(occ)
    input.close()
    return input.pf_active

# ----------------------------------------------------------------------
def get_pulse_schedule(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.pulse_schedule.get()
    else:
      input.pulse_schedule.get(occ)
    input.close()
    return input.pulse_schedule

# ----------------------------------------------------------------------
def get_temporary(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.temporary.get()
    else:
      input.temporary.get(occ)
    input.close()
    return input.temporary

# ----------------------------------------------------------------------
def get_tf(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.tf.get()
    else:
      input.tf.get(occ)
    input.close()
    return input.tf

# ----------------------------------------------------------------------
def get_transport_solver_numerics(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.transport_solver_numerics.get()
    else:
      input.transport_solver_numerics.get(occ)
    input.close()
    return input.transport_solver_numerics

# ----------------------------------------------------------------------
def get_wall(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.wall.get()
    else:
      input.wall.get(occ)
    input.close()
    return input.wall

# ----------------------------------------------------------------------
def get_waves(shot,run,user_or_path,database,occ=None):
    input=imas.ids(shot,run,0,0)
    input.open_env(user_or_path,database,version)
    if occ==None:
      input.waves.get()
    else:
      input.waves.get(occ)
    input.close()
    return input.waves



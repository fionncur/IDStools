import imas,os

version = os.getenv('IMAS_VERSION')[0]

# ----------------------------------------------------------------------
def put_equilibrium(shot,run,user_or_path,database,equilibrium):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.equilibrium=equilibrium
    output.equilibrium.put()
    output.close()

# ----------------------------------------------------------------------
def put_core_profiles(shot,run,user_or_path,database,core_profiles):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.core_profiles=core_profiles
    output.core_profiles.put()
    output.close()

# ----------------------------------------------------------------------
def put_nbi(shot,run,user_or_path,database,nbi):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.nbi=nbi
    output.nbi.put()
    output.close()

# ----------------------------------------------------------------------
def put_ic_antennas(shot,run,user_or_path,database,ic_antennas):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.ic_antennas=ic_antennas
    output.ic_antennas.put()
    output.close()

# ----------------------------------------------------------------------
def put_ec_antennas(shot,run,user_or_path,database,ec_antennas):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.ec_antennas=ec_antennas
    output.ec_antennas.put()
    output.close()

# ----------------------------------------------------------------------
def put_ec_launchers(shot,run,user_or_path,database,ec_launchers):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.ec_launchers=ec_launchers
    output.ec_launchers.put()
    output.close()

# ----------------------------------------------------------------------
def put_summary(shot,run,user_or_path,database,summary):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.summary=summary
    output.summary.put()
    output.close()

# ----------------------------------------------------------------------
def put_charge_exchange(shot,run,user_or_path,database,charge_exchange):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.charge_exchange=charge_exchange
    output.charge_exchange.put()
    output.close()

# ----------------------------------------------------------------------
def put_core_sources(shot,run,user_or_path,database,core_sources):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.core_sources=core_sources
    output.core_sources.put()
    output.close()

# ----------------------------------------------------------------------
def put_core_transport(shot,run,user_or_path,database,core_transport):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.core_transport=core_transport
    output.core_transport.put()
    output.close()

# ----------------------------------------------------------------------
def put_dataset_description(shot,run,user_or_path,database,dataset_description):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.dataset_description=dataset_description
    output.dataset_description.put()
    output.close()

# ----------------------------------------------------------------------
def put_distributions(shot,run,user_or_path,database,distributions):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.distributions=distributions
    output.distributions.put()
    output.close()

# ----------------------------------------------------------------------
def put_distribution_sources(shot,run,user_or_path,database,distribution_sources):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.distribution_sources=distribution_sources
    output.distribution_sources.put()
    output.close()

# ----------------------------------------------------------------------
def put_edge_profiles(shot,run,user_or_path,database,edge_profiles):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.edge_profiles.put()
    output.close()

# ----------------------------------------------------------------------
def put_edge_sources(shot,run,user_or_path,database,edge_sources):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.edge_sources=edge_sources
    output.edge_sources.put()
    output.close()

# ----------------------------------------------------------------------
def put_magnetics(shot,run,user_or_path,database,magnetics):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.magnetics=magnetics
    output.magnetics.put()
    output.close()

# ----------------------------------------------------------------------
def put_pf_active(shot,run,user_or_path,database,pf_active):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.pf_active=pf_active
    output.pf_active.put()
    output.close()

# ----------------------------------------------------------------------
def put_pulse_schedule(shot,run,user_or_path,database,pulse_schedule):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.pulse_schedule=pulse_schedule
    output.pulse_schedule.put()
    output.close()

# ----------------------------------------------------------------------
def put_temporary(shot,run,user_or_path,database,temporary):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.temporary=temporary
    output.temporary.put()
    output.close()

# ----------------------------------------------------------------------
def put_tf(shot,run,user_or_path,database,tf):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.tf=tf
    output.tf.put()
    output.close()

# ----------------------------------------------------------------------
def put_transport_solver_numerics(shot,run,user_or_path,database,transport_solver_numerics):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.transport_solver_numerics=transport_solver_numerics
    output.transport_solver_numerics.put()
    output.close()

# ----------------------------------------------------------------------
def put_wall(shot,run,user_or_path,database,wall):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.wall=wall
    output.wall.put()
    output.close()

# ----------------------------------------------------------------------
def put_waves(shot,run,user_or_path,database,waves):
    output=imas.ids(shot,run,0,0)
    output.open_env(user_or_path,database,version)
    output.waves=waves
    output.waves.put()
    output.close()





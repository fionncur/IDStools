import imas

# ----------------------------------------------------------------------
def put_equilibrium(shot,run,user,machine,equilibrium):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.equilibrium=equilibrium
    output.equilibrium.put()
    output.close()

# ----------------------------------------------------------------------
def put_core_profiles(shot,run,user,machine,core_profiles):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.core_profiles=core_profiles
    output.core_profiles.put()
    output.close()

# ----------------------------------------------------------------------
def put_nbi(shot,run,user,machine,nbi):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.nbi=nbi
    output.nbi.put()
    output.close()

# ----------------------------------------------------------------------
def put_ic_antennas(shot,run,user,machine,ic_antennas):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.ic_antennas=ic_antennas
    output.ic_antennas.put()
    output.close()

# ----------------------------------------------------------------------
def put_ec_antennas(shot,run,user,machine,ec_antennas):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.ec_antennas=ec_antennas
    output.ec_antennas.put()
    output.close()

# ----------------------------------------------------------------------
def put_ec_launchers(shot,run,user,machine,ec_launchers):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.ec_launchers=ec_launchers
    output.ec_launchers.put()
    output.close()

# ----------------------------------------------------------------------
def put_summary(shot,run,user,machine,summary):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.summary=summary
    output.summary.put()
    output.close()

# ----------------------------------------------------------------------
def put_charge_exchange(shot,run,user,machine,charge_exchange):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.charge_exchange=charge_exchange
    output.charge_exchange.put()
    output.close()

# ----------------------------------------------------------------------
def put_core_sources(shot,run,user,machine,core_sources):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.core_sources=core_sources
    output.core_sources.put()
    output.close()

# ----------------------------------------------------------------------
def put_core_transport(shot,run,user,machine,core_transport):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.core_transport=core_transport
    output.core_transport.put()
    output.close()

# ----------------------------------------------------------------------
def put_dataset_description(shot,run,user,machine,dataset_description):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.dataset_description=dataset_description
    output.dataset_description.put()
    output.close()

# ----------------------------------------------------------------------
def put_distributions(shot,run,user,machine,distributions):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.distributions=distributions
    output.distributions.put()
    output.close()

# ----------------------------------------------------------------------
def put_distribution_sources(shot,run,user,machine,distribution_sources):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.distribution_sources=distribution_sources
    output.distribution_sources.put()
    output.close()

# ----------------------------------------------------------------------
def put_edge_profiles(shot,run,user,machine,edge_profiles):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.edge_profiles.put()
    output.close()

# ----------------------------------------------------------------------
def put_edge_sources(shot,run,user,machine,edge_sources):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.edge_sources=edge_sources
    output.edge_sources.put()
    output.close()

# ----------------------------------------------------------------------
def put_magnetics(shot,run,user,machine,magnetics):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.magnetics=magnetics
    output.magnetics.put()
    output.close()

# ----------------------------------------------------------------------
def put_pf_active(shot,run,user,machine,pf_active):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.pf_active=pf_active
    output.pf_active.put()
    output.close()

# ----------------------------------------------------------------------
def put_pulse_schedule(shot,run,user,machine,pulse_schedule):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.pulse_schedule=pulse_schedule
    output.pulse_schedule.put()
    output.close()

# ----------------------------------------------------------------------
def put_temporary(shot,run,user,machine,temporary):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.temporary=temporary
    output.temporary.put()
    output.close()

# ----------------------------------------------------------------------
def put_tf(shot,run,user,machine,tf):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.tf=tf
    output.tf.put()
    output.close()

# ----------------------------------------------------------------------
def put_transport_solver_numerics(shot,run,user,machine,transport_solver_numerics):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.transport_solver_numerics=transport_solver_numerics
    output.transport_solver_numerics.put()
    output.close()

# ----------------------------------------------------------------------
def put_wall(shot,run,user,machine,wall):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.wall=wall
    output.wall.put()
    output.close()

# ----------------------------------------------------------------------
def put_waves(shot,run,user,machine,waves):
    output=imas.ids(shot,run,0,0)
    output.open_env(user,machine,'3')
    output.waves=waves
    output.waves.put()
    output.close()





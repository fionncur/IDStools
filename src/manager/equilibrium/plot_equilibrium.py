from ...framework.data_providers.data_provider import DataProvider
from ...framework.compute.equilibrium import EquilibriumCompute
from ...framework.compute.common import compute_time_index
from ...framework.view.equilibrium import EquilibriumPlot, EquilibriumPlotDataInterface

#TODO Modify this code to Use builder pattern here
class PlotEquilibrium:
    def __init__(self, database, backend, shot, run, user, occurrence, time, allInfo):

        dataprovider = DataProvider(
            database=database,
            backend=backend,
            shot=shot,
            run=run,
            user=user,
        )
        ids_name = "equilibrium"
        ids_object = dataprovider.get_ids(ids_name)
        hostdir = dataprovider.get_database_path(database, user)
        ids_object.time = dataprovider.get_time(
            ids_name, occurrence
        )  # Fill time series

        # Get time slice
        time_index, time_value = compute_time_index(
            ids_object.time, time
        )  # Calculate time index for time of interest
        ids_object.time_slice.resize(1)
        ids_object.time_slice[0] = dataprovider.get_time_slice(
            ids_name, time_index, occurrence
        )
        # Prepare data for EquilibriumPlot
        equilibrium_compute = EquilibriumCompute(ids_object)
        data_object = equilibrium_compute.get_cartesian_r_z_grids()

        equilibriumDataInterface = EquilibriumPlotDataInterface()
        equilibriumDataInterface.time = ids_object.time
        equilibriumDataInterface.hostdir = dataprovider.database_path
        equilibriumDataInterface.shot = shot
        equilibriumDataInterface.run = run
        equilibriumDataInterface.user = user
        equilibriumDataInterface.allInfo = allInfo

        equilibriumDataInterface.plotrho = data_object.plotrho
        equilibriumDataInterface.r2d = data_object.r2d
        equilibriumDataInterface.z2d = data_object.z2d
        equilibriumDataInterface.rho2d = data_object.rho2d
        equilibriumDataInterface.psi2d = data_object.psi2d
        equilibriumDataInterface.levels = 30

        equilibriumPlot = EquilibriumPlot(equilibriumDataInterface)
        equilibriumPlot.set_plot()
        equilibriumPlot.set_info()
        equilibriumPlot.show()

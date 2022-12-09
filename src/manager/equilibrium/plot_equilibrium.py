from os import stat
from ...framework.data_providers.data_provider import DataProvider
from ...framework.compute.equilibrium import EquilibriumCompute
from ...framework.compute.common import compute_time_index
from ...framework.view.equilibrium import EquilibriumPlot, EquilibriumPlotDataInterface


class PlotEquilibrium:
    def __init__(
        self, ax, database, backend, shot, run, user, occurrence, time, is_show_info
    ):
        self.ids_name = "equilibrium"
        self.ids_object = None
        self.data_provider = None

        self.ax = ax
        self.database = database
        self.backend = backend
        self.shot = shot
        self.run = run
        self.user = user
        self.occurrence = occurrence
        self.time = time
        self.is_show_info = is_show_info

    def generate(self):
        self.retrieve()
        data = self.compute()
        self.plot(data)

    def retrieve(self):
        self.data_provider = DataProvider(
            database=self.database,
            backend=self.backend,
            shot=self.shot,
            run=self.run,
            user=self.user,
        )

        self.ids_object = self.data_provider.get_ids(self.ids_name)
        # Fill time series
        self.ids_object.time = self.data_provider.get_time(
            self.ids_name, self.occurrence
        )

        # Get relevant time slice
        time_index, time_value = compute_time_index(self.ids_object.time, self.time)
        self.ids_object.time_slice.resize(1)
        self.ids_object.time_slice[0] = self.data_provider.get_time_slice(
            self.ids_name, time_index, self.occurrence
        )

    def compute(self):
        # Prepare data for EquilibriumPlot
        equilibrium_compute = EquilibriumCompute(self.ids_object)
        return equilibrium_compute.get_cartesian_r_z_grids()

    def plot(self, data_object):
        equilibriumDataInterface = EquilibriumPlotDataInterface()
        equilibriumDataInterface.time = self.ids_object.time
        equilibriumDataInterface.hostdir = self.data_provider.database_path
        equilibriumDataInterface.shot = self.shot
        equilibriumDataInterface.run = self.run
        equilibriumDataInterface.user = self.user
        equilibriumDataInterface.is_show_info = self.is_show_info

        equilibriumDataInterface.plotrho = data_object.plotrho
        equilibriumDataInterface.r2d = data_object.r2d
        equilibriumDataInterface.z2d = data_object.z2d
        equilibriumDataInterface.rho2d = data_object.rho2d
        equilibriumDataInterface.psi2d = data_object.psi2d
        equilibriumDataInterface.levels = 30

        equilibriumPlot = EquilibriumPlot(self.ax)
        equilibriumPlot.overlay(equilibriumDataInterface)

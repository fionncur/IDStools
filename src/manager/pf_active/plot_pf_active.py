from os import stat
from ...framework.data_providers.data_provider import DataProvider
from ...framework.compute.pf_active import PFCoilsCompute

from ...framework.view.pf_active import PFCoilsPlot


class PlotPFActiveCoils:
    def __init__(self, ax, database, backend, shot, run, user, occurrence):
        self.ids_name = "pf_active"
        self.ids_object = None
        self.data_provider = None

        self.ax = ax
        self.database = database
        self.backend = backend
        self.shot = shot
        self.run = run
        self.user = user
        self.occurrence = occurrence

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

        self.ids_object = self.data_provider.connection.get(self.ids_name)

    def compute(self):
        # Prepare data for EquilibriumPlot
        pf_coils_compute = PFCoilsCompute(self.ids_object)
        return pf_coils_compute.get_pf_coils()

    def plot(self, data_object):

        pfcoils_Plot = PFCoilsPlot(self.ax)
        pfcoils_Plot.overlay(data_object)

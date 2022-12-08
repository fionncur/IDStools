import argparse

from src.framework.data_providers import DataProvider
from src.framework.compute.equilibrium import EquilibriumCompute
from src.framework.compute import common

from src.framework.view.equilibrium import EquilibriumPlotDataInterface
from src.framework.view.equilibrium import EquilibriumPlot

from idstools.cli import imas_parser

parser = argparse.ArgumentParser(
    description="---- Display the plasma equilibrium from the equilibrium IDS",
    parents=[imas_parser],
)
parser.add_argument("-s", "--shot", help="Shot number", required=True, type=int)
parser.add_argument("-r", "--run", help="Run number", required=True, type=int)
parser.add_argument(
    "-t", "--time", help="Time (default=middle)", type=float, default=-99.0
)
parser.add_argument(
    "-o",
    "--occurrence",
    help="Occurrence number (default=%(default)s)",
    type=int,
    default=0,
)
parser.add_argument("-p", "--plotrho", help="Plots rho(R,Z)", action="store_true")
parser.add_argument(
    "-a",
    "--allInfo",
    help="Adds all extra provenance info to the plot",
    action="store_true",
)

args = parser.parse_args()

dataprovider = DataProvider(
    database=args.database,
    backend=args.backend,
    shot=args.shot,
    run=args.run,
    user=args.user,
)
ids_name = "equilibrium"
ids_object = dataprovider.get_ids(ids_name)
hostdir = dataprovider.get_database_path(args.database, args.user)
# Create ids object
equilibrium_compute = EquilibriumCompute(ids_object)

# Fill time series
ids_object.time = dataprovider.get_time(ids_name, args.occurrence)
if ids_object.time is None:
    print(
        "The "
        + ids_name
        + " IDS for this occurence is empty in the input"
        + " data-entry because "
        + ids_name
        + ".time is empty",
        file=sys.stderr,
    )
    exit()
# Calculate time index for time of interest
time_index, time_value = common.compute_time_index(ids_object.time, args.time)

# Ask for time slice
ids_object.time_slice.resize(1)
ids_object.time_slice[0] = dataprovider.get_time_slice(
    ids_name, time_index, args.occurrence
)
data_object = equilibrium_compute.get_cartesian_r_z_grids()

equilibriumDataInterface = EquilibriumPlotDataInterface()
equilibriumDataInterface.time = ids_object.time
equilibriumDataInterface.hostdir = dataprovider.database_path
equilibriumDataInterface.shot = args.shot
equilibriumDataInterface.run = args.run
equilibriumDataInterface.user = args.user
equilibriumDataInterface.allInfo = args.allInfo

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

# #!/usr/bin/env python

import datetime
import logging
import re

import imas
from idstools.cli import *
import numpy as np

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)
from src.compute.common.functions import compare_ids
from src.utils.dd_helper import DDHelper


def setup_logger(name, verbose=False, log_dir="."):
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARN)  # default
    if verbose:
        logger.setLevel(logging.DEBUG)
    # Create stream handler for logging to stdout (log all five levels)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(stdout_handler)
    # enable_console_output()

    """Add a file handler for this logger with the specified `name` (and store the log file
    under `log_dir`)."""
    # Format for file log
    fmt = "%(asctime)s | %(levelname)9s | %(filename)s:%(lineno)d | %(message)s"
    formatter = logging.Formatter(fmt)

    file_name = get_log_filename(name, log_dir)

    log_file = file_name + ".log"

    # Create file handler for logging to a file (log all five levels)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger, file_name


def get_log_filename(name, log_dir):
    # Determine log path and file name; create log path if it does not exist
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_name = f'{str(name).replace(" ", "_")}_{now}'
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except:
            print(
                f"Cannot create directory {log_dir}. ",
                end="",
                file=sys.stderr,
            )
            log_dir = "/tmp" if sys.platform.startswith("linux") else "."
            print(f"Defaulting to {log_dir}.", file=sys.stderr)
    return os.path.join(log_dir, log_name)


if __name__ == "__main__":
    logger, file_name = setup_logger("module", verbose=True, log_dir="logs")
    logger.info("logger is initiated")
    logger.debug("logger is in debug mode")
    # Management of input arguments
    parser = argparse.ArgumentParser(
        description="Compare a IDS from 2 datasets", parents=[imas_parser]
    )
    parser.add_argument("shotA", type=int, help="shot number of first dataset")
    parser.add_argument("runA", type=int, help="run number of first dataset")
    parser.add_argument("shotB", type=int, help="shot number of second dataset")
    parser.add_argument("runB", type=int, help="run number of second dataset")
    parser.add_argument(
        "ids",
        nargs="*",
        type=str,
        help="Name (or space separated list of names) of IDS to compare (leave empty to compare all IDSs)",
    )
    parser.add_argument(
        "--backendB",
        type=str,
        default=None,
        help="Specifies the backend of second dataset (default: same as first dataset)",
    )
    parser.add_argument(
        "--databaseB",
        type=str,
        default=None,
        help="Specifies the database name of second dataset (default: same as first dataset)",
    )
    parser.add_argument(
        "--userB",
        type=str,
        default=None,
        help="Specifies the owner (username) of second dataset (default: same as first dataset)",
    )
    parser.add_argument(
        "--skip-provenance",
        action="store_true",
        help="Discards provenance data differences (optional)",
    )

    args = parser.parse_args()

    # set defaults for second dataset
    if args.databaseB is None:
        args.databaseB = args.database
    if args.backendB is None:
        args.backendB = args.backend
    if args.userB is None:
        args.userB = args.user

    inputA = imas.DBEntry(
        get_backend_id(args.backend),
        args.database,
        args.shotA,
        args.runA,
        user_name=args.user,
    )
    status, _ = inputA.open()
    if status != 0:
        logger.error(
            "Error opening first dataset! Please check existence.", file=sys.stderr
        )
        sys.exit(status)

    inputB = imas.DBEntry(
        get_backend_id(args.backendB),
        args.databaseB,
        args.shotB,
        args.runB,
        user_name=args.userB,
    )
    status, _ = inputB.open()
    if status != 0:
        logger.error(
            "Error opening second dataset! Please check existence.", file=sys.stderr
        )
        sys.exit(status)
    #
    if args.ids == []:
        args.ids = [ids.value for ids in list(imas.IDSName)]

    dd_helper = DDHelper()

    file_object = open(file_name + ".html", "w")

    report_title = f"Differences : {args.shotA}/{args.runA} ~ {args.shotB}/{args.runB}"
    report_header_string = (
        """<head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
                <title>"""
        + report_title
        + """</title>
            </head>"""
    )
    shotA = f"{args.shotA} / {args.runA}"
    shotB = f"{args.shotB} / {args.runB}"
    report_table_header = f"""
    <thead class="table-primary">
    <tr>
                        <th>Field Name</th>
                        <th>{args.shotA}/{args.runA}</th>
                        <th>{args.shotB}/{args.runB}</th>
                        <th>Comments</th>
                        <th>Details</th>
                        <tr>
                    </thead>"""
    file_object.write(
        f"""<!DOCTYPE html>
            <html lang="en">
                {report_header_string}
                
                <body>
                <div class="jumbotron jumbotron-fluid text-center">
                    <div class="container">
                        <p class="h4">{report_title}</p>
                        <small class="text-muted">Result generated by idsdiff tool show difference between quantities and shows plots</small>
                    </div>
                </div>
                    <div class="table-responsive" >
                    <table class="table table-bordered table-striped table-hover table-sm align-top">
                    <caption>List of differences</caption>
                        {report_table_header}<tbody>"""
    )
    plot_counter = 0
    for idsname in args.ids:
        idsA = inputA.get(idsname)
        idsB = inputB.get(idsname)
        compare_result, output = compare_ids(
            idsA, idsB, field=idsname, ignore_version=args.skip_provenance, output={}
        )

        report_field_difference = ""
        report_details = ""
        report_diff_line = f"""<tr class="table-secondary">
                        <th scope="row" colspan="5">{idsname}</td>
                    </tr>"""
        report_field_difference += report_diff_line
        for key, values in output.items():
            badge_color = "bg-secondary"
            if values[3] is not None:
                if values[3] == "different values":
                    badge_color = "bg-primary"
                elif values[3] == "different length":
                    badge_color = "bg-warning"

            if values[2] is np.ndarray:
                import matplotlib.pyplot as plt
                import base64
                from io import BytesIO
                import re

                field_path = re.sub("\[(.*?)\]", "", key)
                field_path = field_path[field_path.index(".") + 1 :]
                field_path = field_path.replace(".", "/")
                coordinate_path = dd_helper.get_coordinate(idsname, field_path)
                if coordinate_path[0] == r"/":
                    coordinate_path = coordinate_path[1:]
                if "itime" in coordinate_path:
                    coordinate_path = coordinate_path.replace("itime", "0")
                print(coordinate_path)
                print(key)
                timeA = inputA.partial_get(idsname, coordinate_path)
                timeB = inputB.partial_get(idsname, coordinate_path)
                minA = np.amin(timeA)
                minB = np.amin(timeB)

                maxA = np.amax(timeA)
                maxB = np.amax(timeB)
                ax_timeA = np.linspace(
                    minA if minA < minB else minB,
                    maxA if maxA > maxB else maxB,
                    len(values[0]),
                )
                ax_timeB = np.linspace(
                    minA if minA < minB else minB,
                    maxA if maxA > maxB else maxB,
                    len(values[1]),
                )
                fig = plt.figure()
                plt.title(key)
                plt.xlabel("time")
                plt.ylabel("values")
                if len(values[0]) < 10:
                    plt.plot(
                        ax_timeA,
                        values[0],
                        marker="o",
                        color="r",
                        label=shotA,
                        linewidth="0.5",
                        ms=2,
                    )
                else:
                    plt.plot(
                        ax_timeA,
                        values[0],
                        color="r",
                        label=shotA,
                        linewidth="0.5",
                        ms=2,
                    )
                if len(values[1]) < 10:
                    plt.plot(
                        ax_timeB,
                        values[1],
                        marker="D",
                        color="b",
                        label=shotB,
                        linewidth="0.5",
                        ms=2,
                    )
                else:
                    plt.plot(
                        ax_timeB,
                        values[1],
                        color="b",
                        label=shotB,
                        linewidth="0.5",
                        ms=2,
                    )
                plt.legend(loc="upper right")
                plt.grid()
                tmpfile = BytesIO()
                fig.savefig(tmpfile, format="png")
                encoded = base64.b64encode(tmpfile.getvalue()).decode("utf-8")
                plt.close()

                report_details = f"""<img src="data:image/png;base64, {encoded}" alt="Red dot"  class="img-fluid rounded"/>"""
                report_diff_line = f"""<tr>
                        <td>{key}</td>
                        <td>Array length : {len(values[0])}</td>
                        <td>Array length : {len(values[1])}</td>
                        <td><span class="badge {badge_color}">{values[3]}</span></td>
                        <td><button type="button" class="btn btn-outline-primary btn-sm" data-bs-toggle="collapse" data-bs-target="#plot{plot_counter}">View plot</button>
                        <div class="collapse" id="plot{plot_counter}">
                        <div class="card card-body">{report_details}
                        </div>
                        </div>
                        </td>
                    </tr>"""
                plot_counter = plot_counter + 1

            elif values[2] == list:
                report_diff_line = f"""<tr>
                        <td>{key}</td>
                        <td>List length : {len(values[0])}</td>
                        <td>List length : {len(values[1])}</td>
                        <td><span class="badge {badge_color}">{values[3]}</span></td>
                        <td></td>
                    </tr>"""
            else:
                report_diff_line = f"""<tr>
                        <td>{key}</td>
                        <td>{values[0]}</td>
                        <td>{values[1]}</td>
                        <td><span class="badge {badge_color}">{values[3]}</span></td>
                        <td></td>
                    </tr>"""
            report_field_difference += report_diff_line
        file_object.write(f"""   {report_field_difference}""")
    file_object.write(
        f"""</tbody></table>
                    </div>
                </body>
            </html>
            """
    )
    file_object.close()

    # import json

    # print(
    #     json.dumps(
    #         output,
    #         indent=4,
    #         default=lambda o: f"<<non-serializable: {type(o).__qualname__}>>",
    #     )
    # )

    # idsA = inputA.partial_get(idsname,"time_slice(0)/boundary")
    # idsB = inputB.partial_get(idsname,"time_slice(0)/boundary")

# #!/usr/bin/env python
import datetime
import logging
import imas
from idstools.cli import *
import numpy as np

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)
from src.compute.common.functions import compare_ids


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

    if args.ids == []:
        args.ids = [ids.value for ids in list(imas.IDSName)]
    file_object = open(file_name + ".html", "w")

    report_title = f"diff {args.shotA}/{args.runA} ~ {args.shotB}/{args.runB}"
    report_header_string = (
        """<head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                <title>"""
        + report_title
        + """</title>
                <style type="text/css">
                    p {
                        color: black;
                        font-size: 10pt;
                        font-weight: normal;
                    }

                    p.name {
                        color: red;
                        font-size: 16pt;
                        font-weight: bold;
                    }

                    p.welcome {
                        color: #3333aa;
                        font-size: 18pt;
                        font-weight: bold;
                        text-align: center;
                    }

                    span.head {
                        color: #3333aa;
                        font-size: 10pt;
                        font-weight: bold;
                    }
                </style>
                <link href="css/jquery.treetable.css" rel="stylesheet" type="text/css">
                <link href="css/maketree.css" rel="stylesheet">
            </head>"""
    )
    report_table_header = f"""
    <thead style="color:#ff0000">
                        <td>Field Name</td>
                        <td>{args.shotA}/{args.runA}</td>
                        <td>{args.shotB}/{args.runB}</td>
                        <td>Comments</td>
                        <td>Details</td>
                    </thead>"""
    file_object.write(
        f"""
            <html>
                {report_header_string}
                <p>{report_title}</p>
                <body>
                    <table>
                        {report_table_header}"""
    )
    for idsname in args.ids:
        idsA = inputA.get(idsname)
        idsB = inputB.get(idsname)

        compare_result, output = compare_ids(
            idsA,
            idsB,
            field=idsname,
            ignore_version=args.skip_provenance,
        )

        report_field_difference = ""
        report_details = ""
        report_diff_line = f"""<tr>
                        <td><span class="pathname">{idsname}</span></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>"""
        report_field_difference += report_diff_line
        for key, values in output.items():
            if values[2] is np.ndarray:
                import matplotlib.pyplot as plt
                import base64
                from io import BytesIO

                fig = plt.figure()
                xpoints = np.array([1, 8])
                ypoints = np.array([3, 10])
                plt.plot(xpoints, ypoints)

                tmpfile = BytesIO()
                fig.savefig(tmpfile, format="png")
                encoded = base64.b64encode(tmpfile.getvalue()).decode("utf-8")

                report_details = (
                    f"""<img src="data:image/png;base64, {encoded}" alt="Red dot" />"""
                )
                report_diff_line = f"""<tr>
                        <td><span class="pathname">{key}</span></td>
                        <td>{len(values[0])}</td>
                        <td>{len(values[1])}</td>
                        <td>{values[3]}</td>
                        <td>{report_details}</td>
                    </tr>"""

            elif values[2] == list:
                report_diff_line = f"""<tr>
                        <td><span class="pathname">{key}</span></td>
                        <td>{len(values[0])}</td>
                        <td>{len(values[1])}</td>
                        <td>{values[3]}</td>
                        <td></td>
                    </tr>"""
            else:
                report_diff_line = f"""<tr>
                        <td><span class="pathname">{key}</span></td>
                        <td>{values[0]}</td>
                        <td>{values[1]}</td>
                        <td>{values[3]}</td>
                        <td></td>
                    </tr>"""
            report_field_difference += report_diff_line
        file_object.write(f"""   {report_field_difference}""")
    file_object.write(
        f"""</table>
                    <script src="js/jquery-1.12.4.min.js"></script>
                    <script src="js/jquery.treetable.js"></script>
                    <script src="js/treeView2.js"></script>
                    <script>  makeTree('body>table');</script>
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

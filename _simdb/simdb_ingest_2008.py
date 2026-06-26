"""Ingest 2008 IMAS pulse data into local SimDB, one entry per pulse."""

import pathlib
import time
from datetime import timedelta
import imas
from simdb.config.config import Config
from simdb.database import get_local_db
from simdb.cli.manifest import Manifest
from simdb.database.models import Simulation

import logging

logging.getLogger("imas").setLevel(logging.WARNING)

REPO_ROOT = pathlib.Path(__file__).parent.parent
DB2008_ROOT = REPO_ROOT / "resources" / "results" / "2008"
SIMDB_DIR = pathlib.Path(__file__).parent

CODE_NAME = "idsmigration"
CODE_VERSION = ""
DB_REF = ""


def _report_progress(
    count: int, total: int, label: str, start: float, last_report: float, interval: float = 5.0
) -> float:
    now = time.monotonic()
    if now - last_report < interval:
        return last_report
    elapsed = now - start
    rate = count / elapsed if elapsed > 0 else 0
    eta = (total - count) / rate if rate > 0 else 0
    pct = 100 * count / total
    print(
        f"Progress: {count:{len(str(total))}d}/{total} ({pct:3.1f}%)  {label}  "
        f"elapsed {timedelta(seconds=int(elapsed))}  "
        f"ETA {timedelta(seconds=int(eta))}  "
        f"({rate:.1f} pulses/s)"
    )
    return now


def _report_summary(verb: str, count: int, total: int, start: float, suffix: str = "") -> None:
    print(f"{verb} {count}/{total} pulses{suffix} in {timedelta(seconds=int(time.monotonic() - start))}")


def _read_temporary_scalars(pulse_dir: pathlib.Path) -> dict:
    entry = imas.DBEntry(f"imas:hdf5?path={pulse_dir}", "r")
    try:
        tmp = entry.get("temporary", 0)
    except Exception:
        return {}
    finally:
        entry.close()

    result = {}
    for el in tmp.constant_float0d:
        name = str(el.identifier.name)
        if name and el.value.has_value:
            result[name] = float(el.value)
    for el in tmp.constant_integer0d:
        name = str(el.identifier.name)
        if name and el.value.has_value:
            result[name] = int(el.value)
    for el in tmp.constant_string0d:
        name = str(el.identifier.name)
        if name and el.value.has_value:
            result[name] = str(el.value)
    return result


def make_manifest(pulse_dir: pathlib.Path, machine: str, index: int, variables: dict) -> Manifest:
    alias = f"2008-{machine.lower()}-{index}"
    metadata = [
        {"dataset": "2008"},
        {"machine": machine},
        {"code": {"name": CODE_NAME, "version": CODE_VERSION}},
        {
            "description": (
                f"{machine} pulse from the 2008 ITPA L-H threshold database migrated to IMAS HDF5. "
                f"Reference: {DB_REF}."
            )
        },
    ]
    if variables:
        metadata.append({"variables": variables})
    data = {
        "manifest_version": 2,
        "alias": alias,
        "inputs": [],
        "outputs": [{"uri": f"imas:hdf5?path={pulse_dir.resolve().as_posix()}#summary"}],
        "metadata": metadata,
    }
    m = Manifest()
    m._data = data
    m._path = SIMDB_DIR / "dummy.yaml"
    m._metadata = {"metadata": data["metadata"]}
    return m


def main():
    pulse_dirs = sorted(p for p in DB2008_ROOT.iterdir() if p.name.startswith("pulse_"))
    total = len(pulse_dirs)
    print(f"Reading {total} pulses ...")

    labels = {}
    temp_vars = {}
    read_start = time.monotonic()
    last_report = read_start
    for i, p in enumerate(pulse_dirs, 1):
        entry = imas.DBEntry(f"imas:hdf5?path={p}", "r")
        labels[p] = str(entry.get("summary", 0).machine)
        entry.close()
        temp_vars[p] = _read_temporary_scalars(p)
        last_report = _report_progress(i, total, p.name, read_start, last_report)
    _report_summary("Read", total, total, read_start, " (machine labels + temporary IDS)")

    config = Config()
    db = get_local_db(config)

    counters: dict[str, int] = {}
    failed = []
    print("Ingesting ...")
    ingest_start = time.monotonic()
    last_report = ingest_start
    for i, p in enumerate(pulse_dirs, 1):
        machine = labels[p]
        idx = counters.get(machine, 0)
        counters[machine] = idx + 1
        alias = f"2008-{machine.lower()}-{idx}"
        try:
            sim = Simulation(make_manifest(p, machine, idx, temp_vars[p]), config)
            db.insert_simulation(sim)
        except Exception as e:
            print(f"[{i:3d}/{total}] {alias} FAILED: {e}")
            failed.append(p.name)
        last_report = _report_progress(i, total, alias, ingest_start, last_report)
    _report_summary("Ingested", total - len(failed), total, ingest_start)
    if failed:
        print("Failed:", failed)


if __name__ == "__main__":
    main()

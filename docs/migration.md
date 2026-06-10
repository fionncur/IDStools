# IDS Migration: Crosswalk Format and Script Reference

The `idsmigration` script converts tabular experimental data (CSV) into
IMAS IDS objects written to HDF5.  It is driven entirely by a spreadsheet
called the **crosswalk** (`resources/mappings/TC26_crosswalk.xlsx`).
Everything below describes how to read and extend that file.

---

## Crosswalk columns

| Column | Type | Purpose |
|--------|------|---------|
| `csv_column` | str | Column/variable name in the source CSV |
| `csv_unit` | str | Unit of the source value |
| `imas_unit` | str | Unit of the IDS target field (automatically populated by DD) |
| `csv_dtype` | str | Storage bucket for `status=temporary` rows (see [Temporary IDSs](#temporary-idss)) |
| `imas_dtype` | str | IDS data type (automatically populated by DD) |
| `imas_path` | str | Target path inside the IDS (see [Path notation](#path-notation-and-indexing)) |
| `csv_description` | str | Human-readable description of the source variable |
| `imas_description` | str | Description of the IDS target field (automatically populated by DD) |
| `kind` | str | `constant`, `dynamic`, or `static` (automatically populated by DD) |
| `status` | str | `mapped`, `mapped_caveat`, `temporary`, or `derived` (see [Status values](#status-values)) |
| `notes` | str | Free-text notes, caveats, warnings, etc. |
| `transform` | str | `identity`, `dictionary`, or `formula` (see [Transform types](#transform-types)) |
| `transform_args` | str | Arguments for the transform (dict literal or Python expression) |
| `needs_source` | bool | When `True`, write a value plus a companion sibling instead of a bare value (see [Value/source pairs](#valuesource-pairs)) |
| `source_fields` | str | Optional `("value_leaf", "source_leaf")` 2-tuple naming the sibling leaves written when `needs_source=True`; defaults to `("value", "source")` |
| `source` | str | Source string written to the companion sibling leaf when `needs_source=True` |

---

## Transform types

### `identity`

Copies the CSV value directly to the IDS path.  No `transform_args` needed.

```
csv_column: IP
imas_path:  summary/global_quantities/ip
transform:  identity
```

### `dictionary`

Maps discrete CSV values to IDS values via a Python dict in
`transform_args`.  The string is parsed with `ast.literal_eval()` and must be a valid Python
dict literal; any other result will raise a `ValueError` at parse time.

```
csv_column:     WALMAT
imas_path:      summary/wall/material/index
transform:      dictionary
transform_args: {"MO": 11, "W": 2, "Be": 10}
```

If a CSV value is not present as a key, the row is skipped with a warning
rather than raising an error.

#### Dictionary of lists

When a dict value is itself a Python list, the script performs a
**many-to-one expansion**: it iterates the list and writes each element to
a separate array-of-structures slot, using wildcard index replacement on
the `imas_path` (see [Wildcard indexing](#wildcard-indexing-)).

```
csv_column:     AUXHEAT
imas_path:      core_sources/source(:)/identifier/index
transform:      dictionary
transform_args: {"NB": 2, "IC": 5, "EC": 3,
                 "NBIC": [2, 5], "NBEC": [2, 3],
                 "ECIC": [3, 5], "NBICEC": [2, 5, 3]}
```

`AUXHEAT = "NBIC"` resolves to `[2, 5]` and writes:

- `core_sources/source(0)/identifier/index = 2`
- `core_sources/source(1)/identifier/index = 5`

Single-value entries (e.g. `"NB": 2`) are treated equivalently to a
one-element list and always land at index `0`.

### `formula`

Evaluates an arbitrary Python expression. The source value is bound to the
variable `x`.

```
transform:      formula
transform_args: x * 1e6
```

---

## Path notation and indexing

`imas_path` uses `/` for hierarchy and parenthetical suffixes for
array-of-structures (AoS) indexing:

### Fixed indexing `(n)`

```
nbi/unit(0)/energy/data
```

Always targets element `n` of the AoS.  The array is resized if needed.

### Wildcard indexing `(:)`

```
core_sources/source(:)/identifier/index
```

The `:` is a placeholder resolved at write time.  For `imas_path`
wildcards the index comes from the position in the list produced by the
dictionary-of-lists expansion (`enumerate(value)`), so the first element
lands at `(0)`, the second at `(1)`, and so on.  Two crosswalk rows that
both carry `(:)` in their paths are independent — each starts from `0`.

Wildcards are resolved segment-by-segment by `replace_wildcard_index()`:
it replaces only the `(:)` suffix of the matched segment (e.g.
`source(:)` → `source(0)`), leaving the rest of the path untouched.

### Multiple target paths `&`

A single crosswalk row can fan out to several IDS paths by separating them
with `&`.  The same (transformed) value is written to every path.

```
imas_path: summary/time(0)&equilibrium/time(0)&divertors/time(0)
```

Each path may belong to a different top-level IDS; the script creates IDS
objects on demand.

---

## Sibling-pair writes (`needs_source` and `source_fields`)

Many IDS nodes pair a measured value with a companion string (provenance,
label, etc.) as two sibling leaves under a shared parent.  When
`needs_source = True`, the script writes to **two** leaves at the same level
instead of one bare scalar:

1. The **value leaf** receives the transformed CSV value.
2. The **companion leaf** receives the string from the `source` column.

By default the two leaves are `value` and `source`:

```
# needs_source=True, source_fields blank, imas_path = "summary/global_quantities/ip"
summary/global_quantities/ip/value  ← transformed CSV value
summary/global_quantities/ip/source ← row["source"], e.g. "experiment"
```

### Customising the leaf names with `source_fields`

Set `source_fields` to a 2-tuple of strings to name the leaves explicitly.
The **first** element is the value leaf; the **second** is the companion leaf.
The cell is parsed with `ast.literal_eval()` and must be a 2-tuple of strings;
anything else raises a `ValueError` at startup naming the offending `csv_column`.

```
# needs_source=True, source_fields = ("name", "description")
# imas_path = "divertors/divertor(0)/identifier"
divertors/divertor(0)/identifier/name        ← transformed CSV value
divertors/divertor(0)/identifier/description ← row["source"]
```

This applies to every transform type (`identity`, `dictionary` including
dictionary-of-lists, and `formula`).  For dictionary-of-lists, the companion
string is written alongside each expanded AoS slot.

If `source` is blank the script falls back to `csv_description` and emits
a warning.

By default the companion string is written for every pulse.  Set the
script-level constant `REPEAT_SOURCE = False` to write it only on the first
pulse — useful when the provenance label is constant across pulses and
repeating it wastes space (see [Running the script](#running-the-script)).

**Constraint:** both named leaves must exist as sub-fields of the `imas_path`
node.  Check the Data Dictionary before setting `needs_source` on a new row.

---

## Temporary IDSs

Rows with `status = temporary` are **not** written to a named IDS in the
physics hierarchy.  Instead they are stored in IMAS's `temporary` IDS,
which provides generic typed buckets for values of arbitrary dimensionality
(0-D scalars through 5-D arrays).

The `csv_dtype` column names the bucket and its indexing mode:

| `csv_dtype` | Meaning |
|-------------|---------|
| `constant_float0d(:)` | Append a new float scalar slot each time (auto-incremented index) |
| `constant_string0d(:)` | Append a new string scalar slot each time (auto-incremented index) |
| `constant_float0d(2)` | Fix to slot 2; array is resized to at least 3 with `keep=True`, leaving intermediate slots empty if not yet filled |
| `constant_float0d` *(no index)* | Always write to slot 0; warns if the array is already non-empty |

The `(:)` suffix triggers a persistent per-pulse counter, keyed by the
segment name before `(:)` (e.g. `constant_float0d` from
`constant_float0d(:)`).  All temporary rows sharing the same base name
draw from the same counter, so they append sequentially within a pulse.
Counters reset between pulses.

Each temporary entry automatically receives three sub-fields:

```
constant_float0d(n)/value             ← transformed CSV value
constant_float0d(n)/identifier/name   ← csv_column name
constant_float0d(n)/identifier/description ← csv_description (if present)
```

The `imas_path` column is ignored for temporary rows; the entire path is
derived from `csv_dtype`.

---

## Status values

| Status | Behaviour |
|--------|-----------|
| `mapped` | Primary, authoritative mapping to the IDS hierarchy. |
| `mapped_caveat` | Written to the IDS but subject to known caveats (sign conventions, approximations). See `notes`. |
| `temporary` | Stored in the `temporary` IDS instead of a physics IDS.  Useful for quantities that have no stable IMAS path yet. |
| `derived` | Not currently implemented; row is skipped.  Reserved for quantities that must be computed from other fields. |

Rows without a recognised `transform` value (`identity`, `dictionary`,
`formula`) are also silently excluded from processing.

---

## Many-to-one transformations in the crosswalk

The crosswalk is **one-row-per-source-column**, not one-row-per-target-path.
A single source column can write to multiple targets in two complementary ways:

1. **`&`-separated paths** in `imas_path` — same value, multiple destinations.
2. **Dictionary of lists** — one source value expands into multiple elements
   of an AoS via wildcard indexing.

Both mechanisms are resolved within `apply_transform()` and require no
special columns beyond those already described.

---

## Running the script

```bash
python idstools/scripts/bin/idsmigration
```

Configuration constants at the top of the script control paths and behaviour:

| Constant | Default | Purpose |
|----------|---------|---------|
| `EXPERIMENT_FOLDER` | `"2008"` | Sub-folder under `resources/results/` for output |
| `DATASET_NAME` | `"2008_data.csv"` | Input CSV filename |
| `MAPPING_NAME` | `"2008_crosswalk.xlsx"` | Crosswalk spreadsheet filename |
| `REPEAT_SOURCE` | `True` | When `True`, the companion string (source/description/etc.) is written to every pulse. When `False`, it is written only on the **first pulse** for each target node and omitted for all subsequent pulses — useful when the provenance label is constant and repeating it wastes space. |

Output is one HDF5 directory per pulse:

```
resources/results/tc26/
  pulse_0000/
  pulse_0001/
  ...
```

Each directory is a valid IMAS DBEntry accessible via:

```python
uri = "imas:hdf5?path=resources/results/tc26/pulse_0000;pulse=0"
with imas.DBEntry(uri, "r") as entry:
    summary = entry.get("summary")
```

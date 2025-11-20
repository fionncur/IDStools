#########
 idsquery
#########

**idsquery** script for querying and extracting data from IDSes.
This script allows users to specify one or more IDS paths to extract data and optionally evaluate
query expressions on the extracted data. It supports rich console output for displaying results
and provides options for handling large arrays.
Features:
- Extract data from specified IDS paths.
- Evaluate query expressions on IDS fields.
- Display results in a formatted and readable manner using the `rich` library.
- Option to print all array elements for large datasets.
Usage:
- Provide one or more IDS paths to extract data.
- Optionally specify a query expression to evaluate on the extracted data.
- x1,x2,... refer to the first, second, etc. IDS path in the list when using query.
- Use the `--full` flag to display all elements of large arrays.


*****************
 Syntax idsquery
*****************

   .. command-output:: idsquery -h


******************
 Example idsquery
******************

   .. code-block:: bash

      idsquery -u "imas:hdf5?user=public;pulse=134174;run=117;database=ITER;version=3" "core_profiles/profiles_1d(:)/electrons/temperature" --query "np.mean(x1)"
      11:00:49 INFO     Parsing data dictionary version 4.0.0 @dd_zip.py:89
      11:00:50 INFO     Parsing data dictionary version 3.38.1 @dd_zip.py:89
      ────────────────────────────────────────── Evaluation Result ───────────────────────────────────────────
      ╭───────────────────────── core_profiles/profiles_1d(:)/electrons/temperature ─────────────────────────╮
      │ (106, 299) array (mean=4609.21)                                                                      │
      ╰──────────────────────────────────────────── numpy array ─────────────────────────────────────────────╯
      np.mean(x1):
      4609.209693491538


   .. code-block:: bash

      idsquery -u "imas:hdf5?user=public;pulse=134174;run=117;database=ITER;version=3" "core_profiles/profiles_1d(0)/ion(:)/label" "core_profiles/profiles_1d(0)/ion(:)/density" --query "x1[np.argmax(np.max(x2,axis=1))]"
      11:02:12 INFO     Parsing data dictionary version 4.0.0 @dd_zip.py:89
      11:02:12 INFO     Parsing data dictionary version 3.38.1 @dd_zip.py:89
      ────────────────────────────────────────── Evaluation Result ───────────────────────────────────────────
      ╭───────────────────────────── core_profiles/profiles_1d(0)/ion(:)/label ──────────────────────────────╮
      │ ['D' 'T' 'Be']                                                                                       │
      ╰──────────────────────────────────────────── numpy array ─────────────────────────────────────────────╯
      ╭──────────────────────────── core_profiles/profiles_1d(0)/ion(:)/density ─────────────────────────────╮
      │ (3, 299) array (mean=1782424597318344960.00)                                                         │
      ╰──────────────────────────────────────────── numpy array ─────────────────────────────────────────────╯
      x1:
      'T'
      (myenv) [sawantp1@sdcc-login02 idstools]$


   .. code-block:: bash

      idsquery -u "imas:hdf5?user=public;pulse=134174;run=117;database=ITER;version=3" "core_profiles/profiles_1d(0)/ion(:)/label" "core_profiles/profiles_1d(0)/ion(:)/density" --query "x2[np.where(x1 == 'D')[0][0]]"
      14:24:56 INFO     Parsing data dictionary version 4.0.0 @dd_zip.py:89
      14:24:57 INFO     Parsing data dictionary version 3.38.1 @dd_zip.py:89
      ───────────────────────────────────────────────────── Evaluation Result ─────────────────────────────────────────────────────
      ╭──────────────────────────────────────── core_profiles/profiles_1d(0)/ion(:)/label ────────────────────────────────────────╮
      │ ['D' 'T' 'Be']                                                                                                            │
      ╰─────────────────────────────────────────────────────── numpy array ───────────────────────────────────────────────────────╯
      ╭─────────────────────────────────────── core_profiles/profiles_1d(0)/ion(:)/density ───────────────────────────────────────╮
      │ (3, 299) array (mean=1782424597318344960.00)                                                         │
      ╰─────────────────────────────────────────────────────── numpy array ───────────────────────────────────────────────────────╯
      ╭────────────────────────────────────────────── x2[np.where(x1 == 'D')[0][0]] ──────────────────────────────────────────────╮
      │ (299,) array (mean=2619656079411998720.00)                                                                                │
      ╰─────────────────────────────────────────────────────── numpy array ───────────────────────────────────────────────────────╯
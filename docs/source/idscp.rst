#######
 idscp
#######

*idscp* tool helps you to copy ids from one pulse to another

**************
 Syntax idscp
**************

   .. code:: bash

      $ idscp -h
      usage: idscp [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -si SHOT_INPUT -ri
                      RUN_INPUT -so SHOT_OUTPUT -ro RUN_OUTPUT [-do DATABASE_OUTPUT] [-bo BACKEND_OUTPUT] [-f]
                      [--setDatasetVersion] [-a | -o OUTPUTOCCURRENCE]
                      [ids [ids ...]]

      Copy IDSs from a data-entry into another one

      positional arguments:
      ids                   IDSs to copy (leave empty to select all IDSs with default occurrence, or append "/n" to
                              copy a specific occurrence "n")

      optional arguments:
      -h, --help            show this help message and exit
      -u USER, --user_or_path USER
                              user (default=sawantp1)
      --database DATABASE, -d DATABASE
                              database name (default=ITER)
      --backend BACKEND, -b BACKEND
                              backend format (default=MDSPLUS)
      --version VERSION, -v VERSION
                              data version (default=3)
      -si SHOT_INPUT, --shot_input SHOT_INPUT
                              Input shot number
      -ri RUN_INPUT, --run_input RUN_INPUT
                              Input run number
      -so SHOT_OUTPUT, --shot_output SHOT_OUTPUT
                              Output shot number
      -ro RUN_OUTPUT, --run_output RUN_OUTPUT
                              Output run number
      -do DATABASE_OUTPUT, --database_output DATABASE_OUTPUT
                              Database name for the destination data-entry
      -bo BACKEND_OUTPUT, --backend_output BACKEND_OUTPUT
                              Backend name for the destination data-entry
      -f, --force           Force the creation of destination data-entry (existing data will be lost)
      --setDatasetVersion   Store current DD version into dataset_description IDS if it exists
      -a, --allOccurrences  Copy all occurrences available in the source into the destination
      -o OUTPUTOCCURRENCE, --outputOccurrence OUTPUTOCCURRENCE
                              Copy the selected source into the specified occurrence at the destination

***************
 Example idscp
***************

   .. code:: bash

      $ idscp -si 131024 -ri 10 -so 145000 -ro 2
      Copying equilibrium

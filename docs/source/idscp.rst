#######
 idscp
#######

*idscp* tool helps you to copy ids from one pulse to another

**************
 Syntax idscp
**************

   .. code-block:: bash

      $ idscp -h
      Usage: idscp [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [-sp SOURCE_PULSE] [-sr SOURCE_RUN] [-dp DESTINATION_PULSE]
             [-dr DESTINATION_RUN] [-dd DESTINATION_DATABASE] [-db DESTINATION_BACKEND] [-f] [--setDatasetVersion] [-i] [-a | -o OUTPUTOCCURRENCE]
             [ids [ids ...]]

      Copy IDSs from a data-entry into another one

      Positional Arguments:
      ids                   IDSs to copy (leave empty to select all IDSs with default occurrence, or append "/n" to copy a specific occurrence "n")

      Optional Arguments:
      -h, --help            show this help message and exit
      -u, --user_or_path USER
                              user (default=sawantp1)
      --database, -d DATABASE
                              database name (default=ITER)
      --backend, -b BACKEND
                              backend format (default=MDSPLUS)
      --version, -v VERSION
                              data version (default=3)
      -sp, --source_pulse SOURCE_PULSE
                              Source pulse number
      -sr, --source_run SOURCE_RUN
                              Source run number
      -dp, --destination_pulse DESTINATION_PULSE
                              Destination pulse number
      -dr, --destination_run DESTINATION_RUN
                              Destination run number
      -dd, --destination_database DESTINATION_DATABASE
                              Database name for the destination data-entry
      -db, --destination_backend DESTINATION_BACKEND
                              Backend name for the destination data-entry
      -f, --force           Force the creation of destination data-entry (existing data will be lost)
      --setDatasetVersion   Store current DD version into dataset_description IDS if it exists
      -i, --interactive     Prompt the user to overwrite the ids (Default is to overwrite the ids without asking)
      -a, --allOccurrences  Copy all occurrences available in the source into the destination
      -o, --outputOccurrence OUTPUTOCCURRENCE
                              Copy the selected source into the specified occurrence at the destination

***************
 Example idscp
***************

   .. code-block:: bash

      $ idscp -sp 131024 -sr 10 -dp 145000 -dr 2 
      Copying equilibrium

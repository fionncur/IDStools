#########
 idslist
#########

*idslist* is a utility that, as the name implies, shows list of all
idses along with count of time slices. It also shows timestamps of
slices. You can customize the output by choosing to display full array
values or generate output in YAML format.

****************
 Syntax idslist
****************

    .. code-block:: bash   
          
        $ idslist -h
        usage: idslist [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [-uri URI] [-s PULSE] [-r RUN] [-f] {yaml,occ} ...

      List available IDSes in the pulse. By deafult it prints all IDSes alone with their time length. fullarray option allows you to print complete time array.

      Possible commands are:
      yaml - List ids content for yaml files aimed at describing a scenario
      occ <--ids> <--comment> - List ids with their number of occurrences

      positional arguments:
      {yaml,occ}            sub-commands help
          yaml                List ids content for yaml files aimed at describing a scenario
          occ                 List ids with their number of occurrences

        optional arguments:
        -h, --help            show this help message and exit
        -u USER, --user_or_path USER
                                user (default=public)
        --database DATABASE, -d DATABASE
                                database name (default=ITER)
        --backend BACKEND, -b BACKEND
                                backend format (default=MDSPLUS)
        --version VERSION, -v VERSION
                                data version (default=3)
        -uri URI, --uri URI   uri (default=None)
        -s PULSE, --shot PULSE, --pulse PULSE
                                Pulse number
        -r RUN, --run RUN     Run number
        -f, --fullarray       Show full time array values



Example idslist
~~~~~~~~~~~~~~~~

   .. code-block:: bash

        $ idslist -s 134174 -r 117
        $ idslist --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3"
        core_profiles  : 106   slices: [10.6 10.6 10.6 ... 75.  75.  75. ]
        core_sources   : 106   slices: [10.6 10.6 10.6 ... 75.  75.  75. ]
        core_transport : 106   slices: [10.6 10.6 10.6 ... 75.  75.  75. ]
        edge_profiles  : 650   slices: [10.1 10.2 10.3 ... 74.8 74.9 75. ]
        edge_sources   : 650   slices: [10.1 10.2 10.3 ... 74.8 74.9 75. ]
        edge_transport : 650   slices: [10.1 10.2 10.3 ... 74.8 74.9 75. ]
        equilibrium    : 106   slices: [  1.2    1.5    1.8  ... 146.44 147.94 149.44]
        summary        : 106   slices: [10.3 10.3 10.3 ... 75.  75.  75. ]

   .. code-block:: bash

        $ idslist -s 134174 -r 117 yaml
        $ idslist --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3" yaml
        core_profiles:
            time_step_number: 106
            start_end_step:   [10.599230769230868 75.00005602665553 0.6133411929278538]
        core_sources:
            time_step_number: 106
            start_end_step:   [10.599230769230868 75.00005602665553 0.6133411929278538]
        core_transport:
            time_step_number: 106
            start_end_step:   [10.599230769230868 75.00005602665553 0.6133411929278538]
        edge_profiles:
            time_step_number: 650
            start_end_step:   [10.1 75.0 0.1]
        edge_sources:
            time_step_number: 650
            start_end_step:   [10.1 75.0 0.1]
        edge_transport:
            time_step_number: 650
            start_end_step:   [10.1 75.0 0.1]
        equilibrium:
            time_step_number: 106
            start_end_step:   [1.202 149.43759781205512 1.4117675982100488]
        summary:
            time_step_number: 106
            start_end_step:   [10.299692307692405 75.00005602665553 0.6161939401806011]

   .. code-block:: bash

        $ idslist -s 134174 -r 117 occ
        $ idslist --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3" occ
        core_profiles/0
        core_sources/0
        core_transport/0
        edge_profiles/0
        edge_sources/0
        edge_transport/0
        equilibrium/0
        summary/0

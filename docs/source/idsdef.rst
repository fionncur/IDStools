idsdef
======

*idsdef* tool helps you to get metadata and attributes from data dictionary xml


Syntax idsdef
~~~~~~~~~~~~~

    .. code-block:: bash

        $ idsdef -h
        Usage: idsdef [-h] [-a | -s SELECT] [-m] ids [path]

        Query the IDS XML Definition for documentation

        Positional Arguments:
        ids                   IDS name
        path                  Path for field of interest within the IDS

        Optional Arguments:
        -h, --help            show this help message and exit
        -a, --all             Print all attributes
        -s, --select SELECT   Select attribute to be printed (default=documentation)
        -m, --metaData        Print associated meta-data (version and cocos)


Example idscp
~~~~~~~~~~~~~

    .. code-block:: bash

        $ idsdef equilibrium -a
        Attributes of (args.path)
        ┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Attribute             ┃ Value                                                                                   ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ name                  │ equilibrium                                                                             │
        │ maxoccur              │ 3                                                                                       │
        │ documentation         │ Description of a 2D, axi-symmetric, tokamak equilibrium; result of an equilibrium code. │
        │ lifecycle_status      │ active                                                                                  │
        │ lifecycle_version     │ 3.1.0                                                                                   │
        │ lifecycle_last_change │ 3.40.0                                                                                  │
        └───────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────┘

    .. code-block:: bash

        $ idsdef edge_profiles -m
        This is Data Dictionary version = 3.40.1, following COCOS = 11
        ====================================================================================================
        Edge plasma profiles (includes the scrape-off layer and possibly part of the confined plasma)

    .. code-block:: bash


        $ idsdef core_transport vacuum_toroidal_field -a
        Attributes of (core_transport-vacuum_toroidal_field)
        ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Attribute           ┃ Value                                                                                                                   ┃
        ┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ name                │ vacuum_toroidal_field                                                                                                   │
        │ structure_reference │ b_tor_vacuum_1                                                                                                          │
        │ path                │ vacuum_toroidal_field                                                                                                   │
        │ documentation       │ Characteristics of the vacuum toroidal field (used in Rho_Tor definition and in the normalization of current densities) │
        │ data_type           │ structure                                                                                                               │
        │ path_doc            │ vacuum_toroidal_field                                                                                                   │
        │ cocos_alias         │ IDSPATH                                                                                                                 │
        │ cocos_replace       │ core_transport.vacuum_toroidal_field                                                                                    │
        └─────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

    .. code-block:: bash

        $ idsdef core_transport model -a
        Attributes of (core_transport-model)
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Attribute                    ┃ Value                                                               ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ name                         │ model                                                               │
        │ structure_reference          │ core_transport_model                                                │
        │ path                         │ model                                                               │
        │ documentation                │ Transport is described by a combination of various transport models │
        │ data_type                    │ struct_array                                                        │
        │ maxoccur                     │ 18                                                                  │
        │ path_doc                     │ model(i1)                                                           │
        │ coordinate1                  │ 1...N                                                               │
        │ appendable_by_appender_actor │ yes                                                                 │
        └──────────────────────────────┴─────────────────────────────────────────────────────────────────────┘

    .. code-block:: bash

        $ idsdef core_transport model/identifier -a
                Attributes of (core_transport-model/identifier)
        ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Attribute           ┃ Value                                        ┃
        ┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ name                │ identifier                                   │
        │ structure_reference │ identifier                                   │
        │ path                │ model/identifier                             │
        │ documentation       │ Transport model identifier                   │
        │ data_type           │ structure                                    │
        │ path_doc            │ model(i1)/identifier                         │
        │ doc_identifier      │ core_transport/core_transport_identifier.xml │
        └─────────────────────┴──────────────────────────────────────────────┘
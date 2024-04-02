viewhcdplots
============

*viewhcdplots* shows plots from distributions and waves for different data entries for analysis

Syntax viewhcdplots
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ viewhcdplots -h
    usage: viewhcdplots [-h] [-ech ECH] [-icrh ICRH] [-nbi NBI] [-fus FUS]

    --- Display H&CD results from multiple data sets
    - Each H&CD source is optional
    - Time is also optional
    - Example:
    hcdplot -ech 134713/200/schneim/MDSPLUS/TORBEAM/3 -nbi 130012/122/schneim/nf_fopla_synergy

    optional arguments:
    -h, --help  show this help message and exit
    -ech ECH    shot/run/user/backend/database/[time] for ECH results (waves)
    -icrh ICRH  shot/run/user/backend/database/version/[time] for ICRH results (distributions)
    -nbi NBI    shot/run/user/backend/database/version/[time] for NBI results (distributions)
    -fus FUS    shot/run/user/backend/database/version/[time] for fusion products (distributionss)

Example viewhcdplots
~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ hcd_plot -ech 104104/2/schneim/MDSPLUS/TORBEAM_XMODE/3 -nbi 130012/15/schneim/MDSPLUS/SPOT/3 -fus 130012/15/schneim/MDSPLUS/SPOT/3 -icrh 130012/15/schneim/MDSPLUS/SPOT/3




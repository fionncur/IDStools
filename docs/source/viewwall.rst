viewwall
========

*viewwall* script shows wall outline plot using limiter and vessel properties found in 2D description of Wall IDS. Here
Vessel is mechanical structure of the vacuum vessel. The script uses annular represenation. You can specify wall using wall 
command or you can specify database entry to retrive wall details. more information about wall ids is here
https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/wall.html

Syntax viewwall
~~~~~~~~~~~~~~~
.. code-block:: bash

    $ viewwall -h
    usage: viewwall [-h] {wall,database} ...

    Wall plot

    positional arguments:
    {wall,database}  Commands
        wall           Predefined wall information of different tokamaks : iter, tcs, west, aug, jet, jt60, d3d
        database       Get wall information from given database

    optional arguments:
    -h, --help       show this help message and exit

Example viewwall
~~~~~~~~~~~~~~~~
    .. code-block:: bash

        $ viewwall wall iter

    .. image:: _static/images/wallview_iter.png
        :alt: image not found
        :align: center

    .. code-block:: bash

        $ viewwall database -u schneim --database jet -s 92436 -r 271
        $ viewwall database --uri "imas:mdsplus?user=schneim;shot=92436;run=271;database=jet;version=3"

    .. image:: _static/images/wallview_jet.png
        :alt: image not found
        :align: center


viewmachinedescription
======================

*viewmachinedescription*  plots machine description data stored in databases


Syntax viewmachinedescription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash   

        $ viewmachinedescription -h
        usage: viewmachinedescription [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] {list,plot} ...

        ---- View machine description by getting information of data from md_summary file

        positional arguments:
        {list,plot}           sub-commands help
            list                list machine description databases
            plot                Plot Machine description databases

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


Example 
~~~~~~~

    .. code-block:: bash

        $ viewmachinedescription -d ITER_MD 
        23/11/20 23:20:26 WARNING: VS3U : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: VS3L : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: TF coil busbars (equivalent coil) : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: VC1 : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: VC2 : pf_active.coil.element.geometry.rectangle is empty

    .. image:: _static/images/machine_description.png
        :alt: image not found
        :align: center



    .. code-block:: bash

        $ viewmachinedescription list pf_active --obsolete
            Pulse |                       IDS Name |                    Status
        --------------------------------------------------------------------------
          111001/1 |                      pf_active |                  obsolete
          111001/2 |                      pf_active |                  obsolete
          111001/3 |                      pf_active |                  obsolete
          111001/4 |                      pf_active |                  obsolete
        111001/101 |                      pf_active |                  obsolete
        111001/201 |                      pf_active |                  obsolete
        111001/102 |                      pf_active |                  obsolete
        111001/202 |                      pf_active |                  obsolete
        111001/103 |                      pf_active |                    active
        111001/203 |                      pf_active |                    active

    .. code-block:: bash

        $ viewmachinedescription list wall pf_active
              Pulse |                       IDS Name |                    Status
        --------------------------------------------------------------------------
         111001/103 |                      pf_active |                    active
         111001/203 |                      pf_active |                    active
           116000/3 |                           wall |                    active
        116100/1001 |                           wall |                    active
        116100/2001 |                           wall |                    active
        116100/3001 |                           wall |                    active
           116612/1 |                           wall |                    active


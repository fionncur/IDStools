######################
 plotecstrayradiation
######################

*plotecstrayradiation* script shows electron cyclotron stray radiation
information by showing different plots. It shows cut off layer,
resonance layer, top view equilibrium.
`refer data dictionary <https://imas-data-dictionary.readthedocs.io/en/latest/>`_.

.. note::

   This program is experimental and currently is in development.

*****************************
 Syntax plotecstrayradiation
*****************************

   .. command-output:: plotecstrayradiation -h

*****************
 Example ecstray
*****************

   .. code-block:: bash

      $ plotecstrayradiation --uri "imas:mdsplus?user=public;pulse=134173;run=2326;database=TEST;version=3"

   .. image:: _static/images/plotecstrayradiation.png
      :alt: image not found
      :align: center

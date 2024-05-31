######################
 viewecstrayradiation
######################

*viewecstrayradiation* script shows electron cyclotron stray radiation
information by showing different plots. It shows cut off layer,
resonance layer, top view equilibrium.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

.. note::

   This program is experimental and currently is in development.

*****************************
 Syntax viewecstrayradiation
*****************************

   .. command-output:: viewecstrayradiation -h

*****************
 Example ecstray
*****************

   .. code-block:: bash

      $ viewecstrayradiation --uri "imas:mdsplus?user=public;pulse=134173;run=2326;database=TEST;version=3"

   .. thumbnail:: _static/images/viewecstrayradiation.png
      :alt: image not found
      :align: center

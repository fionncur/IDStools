plothcd
============

*plothcd* shows plots from distributions and waves for different data entries for analysis. It is alos possible to provide URI

Syntax plothcd
~~~~~~~~~~~~~~~~~~~

   .. command-output:: plothcd -h

Example plothcd
~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ plothcd -ech 134173/101/public/MDSPLUS/TEST/3 -nbi 130012/115/public/MDSPLUS/TEST/3 -fus 130012/115/public/MDSPLUS/TEST/3 -icrh 130012/15/public/MDSPLUS/TEST/3

        $ plothcd -ech "imas:mdsplus?user=public;pulse=134173;run=101;database=TEST;version=3" -nbi "imas:mdsplus?user=public;pulse=130012;run=115;database=TEST;version=3" 
###########
 dbscraper
###########

The *dbscraper* script scrapes data from a particular IDS path for a
specified series of pulses and displays the pulse along with the value.

******************
 dbscraper Syntax
******************

    .. command-output:: dbscraper -h

*******************
 dbscraper Example
*******************


   .. command-output:: dbscraper "equilibrium/time_slice(0)/global_quantities/volume" --list-count 10

   .. command-output:: dbscraper "equilibrium/time_slice(0)/global_quantities/volume" --list-count 10 --saveas "$PWD/output.csv"

   .. command-output:: cat "$PWD/output.csv"

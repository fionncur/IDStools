################
 watch_db_entry
################

Subscribe/unsubscribe as a watcher to a simulation file stored in IMAS DB

**********************
 Syntax watch_db_entry
**********************

.. code-block:: bash

   $ watch_db_entry -h
    usage: watch_db_entry [-h] -s SHOT -r RUN [-d DELETE] [-f FIRSTNAME] [-n NAME] [-e EMAIL]

    ---- Subscribe/unsubscribe as a watcher to a simulation file stored in IMAS DB

    optional arguments:
    -h, --help            show this help message and exit
    -s SHOT, --shot SHOT  shot number
    -r RUN, --run RUN     run number
    -d DELETE, --delete DELETE
                            email to remove from watcher list
    -f FIRSTNAME, --firstname FIRSTNAME
                            user firstname
    -n NAME, --name NAME  user name
    -e EMAIL, --email EMAIL
                            user e-mail`


create_db_entry -h
usage: create_db_entry [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN [--disable-validation]

---- Auto-generated yaml scenario and watcher files (!!! STILL TO BE COMPLETED BY HAND !!!)

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
  -s SHOT, --shot SHOT  shot number
  -r RUN, --run RUN     run number
  --disable-validation  disable IDS validation
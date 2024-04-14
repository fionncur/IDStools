#!/bin/bash
# Bamboo deploy script using Easybuild
# Execute script from root directory

# expand aliases
shopt -s expand_aliases

#print hostname
hostname -f

# Note Disable set -e option when using on local as it will exit the shell on error
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    set -e -o pipefail
fi

# Test on existing  databases
declare -a tests

tests+=("122525;1")
# tests+=("122525;1")
tests+=("123314;1")
# tests+=("123170;2")
# tests+=("123276;1")
# tests+=("120014;1")
# tests+=("131047;7")
# tests+=("135014;1")
# tests+=("134174;117")

set -x
#db tools test
dbscraper "core_profiles/profiles_1d(0)/electrons/temperature" --verbose --list-count 10 
dbselector core_profiles --list-count 10 
dbselector summary --list-count 10 
dblist -u public -d TEST list 
dblist -u public -d TEST list -c 
dblist -u public -d TEST list -M 
dblist databases 
dblist dataversions 
scenario_status -s 130012 -r 4 
scenario_summary 

# echo TESTING: dblist -u public slices
# dblist -u public slices  
# echo TESTING: dblist -u public  times
# dblist -u public times 

# pulse tests
for i in ${tests[@]}; do
    arr=(${i//;/ })
    shot=${arr[0]}
    run=${arr[1]}
    echo -------viewplasmacompo-------
    echo TESTING: shot=$shot : run=$run viewplasmacompo -s $shot -r $run
    viewplasmacompo -s $shot -r $run 
    echo --------------
    echo TESTING: shot=$shot : run=$run viewplasmacompo -s $shot -r $run --i
    viewplasmacompo -s $shot -r $run --i 
    echo --------------
    echo TESTING: shot=$shot : run=$run viewplasmacompo -s $shot -r $run --debug
    viewplasmacompo -s $shot -r $run --debug 

    echo -------viewequilibrium-------
    echo TESTING: shot=$shot : run=$run viewequilibrium -s $shot -r $run --rho --pfcoils --info --save
    viewequilibrium -s $shot -r $run --rho --pfcoils --info --save 

    echo TESTING: shot=$shot : run=$run viewequilibrium -s $shot -r $run --info --save
    viewequilibrium -s $shot -r $run --info --save 
    echo -------idsprint-------
    echo TESTING: idsprint -s $shot -r $run equilibrium
    idsprint -s $shot -r $run equilibrium 

    echo -------idslist-------
    echo TESTING: idslist -s $shot -r $run
    idslist -s $shot -r $run 

    echo -------idslist-------
    echo TESTING: idslist -s $shot -r $run yaml
    idslist -s $shot -r $run yaml 

    echo -------idslist-------
    echo TESTING: idslist -s $shot -r $run occ
    idslist -s $shot -r $run occ 

    echo -------idssize-------
    echo TESTING: idssize -s $shot -r $run equilibrium
    idssize -s $shot -r $run equilibrium 

    echo --------------
    echo TESTING: idssize -s $shot -r $run
    idssize -s $shot -r $run 

    echo -------idsperf-------
    echo TESTING: idsperf -s $shot -r $run equilibrium
    idsperf -s $shot -r $run equilibrium 

    echo -------viewfluxes-------
    echo TESTING: viewfluxes -s $shot -r $run -m CLOSEST
    viewfluxes -s $shot -r $run -m CLOSEST 

    echo -------viewneutron-------
    echo TESTING: viewneutron -s $shot -r $run -t 450 --save
    viewneutron -s $shot -r $run -t 450 --save 

    echo -------viewpressure-------
    echo TESTING: viewpressure -s $shot -r $run --save
    viewpressure -s $shot -r $run --save 

    echo -------viewsources-------
    echo TESTING: viewsources -s $shot -r $run
    viewsources -s $shot -r $run 

    echo -------viewedgeprofiles-------
    echo TESTING: viewedgeprofiles -s $shot -r $run --save
    viewedgeprofiles -s $shot -r $run --time 60 --save 

    echo -------viewscenario-------
    echo TESTING: viewscenario -s $shot -r $run --save
    viewscenario -s $shot -r $run --time 60 
    viewscenario -s $shot -r $run --noProfiles 

    echo -------viewrotation-------

    echo TESTING: viewrotation -s $shot -r $run --info --save
    viewrotation -s $shot -r $run --time 60 --info --save 

    echo -------viewcoresources-------
    echo TESTING: viewcoresources -s $shot -r $run --save
    viewcoresources -s $shot -r $run --save 
done

echo TESTING: viewwall --save wall iter
viewwall --save wall iter 
echo TESTING: viewwall --save wall iter
viewwall --save wall iter 

# echo -------idscp-------
# echo TESTING: idscp -si 131024 -ri 10 -so 145000 -ro 2 -f
# idscp -si 131024 -ri 10 -so 145000 -ro 2 

echo -------idsdiff-------
echo TESTING: idsdiff 122525 1 122525 2 summary
idsdiff 122525 1 122525 2 summary 
idsdiff 130011 6 130012 4 summary 

echo -------viewmachinedescription-------
viewmachinedescription list pf_active --checkValidity 
viewmachinedescription list pf_active --obsolete 
viewmachinedescription plot wall --save 

echo -------md_status-------
md_status -s 116000 -r 3 

echo -------md_summary-------
md_summary -s 150502/102 
md_summary -s nbi,on-on 

echo -------show_db_entry-------
show_db_entry -s 134174 -r 117 

echo -------vieweccomposition and viewecray-------
viewecray -d TEST -s 134173 -r 2326 --save 
vieweccomposition -d TEST -s 134173 -r 2326 --save 

echo -------viewspectrometry-------
viewspectrometry -d TEST -s 134000 -r 37 --save 

echo -------viewcoretransport-------
viewcoretransport -s 134000 -r 40 --save 
viewcoretransport -d TEST -s 92436 -r 850 --save 

# echo -------idsresample-------
# echo TESTING: idsresample -si 131024 -ri 10 -so 145000 -ro 2
# idsresample -si 131024 -ri 10 -so 145000 -ro 2 

echo -------viewhcdwaves-------
viewhcdwaves -s 134173 -r 101 -u public -d TEST --save 

echo -------viewhcddistributions-------
viewhcddistributions -s 130012 -r 115 -u public -d TEST --save 

echo -------viewcore_sources-------
viewcoresources -s 130012 -r 105 -d TEST
# viewequilibrium -s 134174 -r 117 --rho --pfcoils

# viewcoresources --uri "imas:mdsplus?user=public;shot=130012;run=105;database=TEST;version=3"
# viewcoretransport --uri "imas:mdsplus?user=public;shot=92436;run=850;database=TEST;version=3"
# vieweccomposition --uri "imas:mdsplus?user=public;shot=134173;run=2326;database=TEST;version=3"
# viewecray --uri "imas:mdsplus?user=public;shot=134173;run=2326;database=TEST;version=3"
# viewedgeprofiles --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3" --separatix --wall --time 60
# viewequilibrium --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3"
# viewfluxes --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3"
# viewhcddistributions --uri "imas:mdsplus?user=public;shot=130012;run=115;database=TEST;version=3".
# viewhcdplots -ech 134173/101/public/MDSPLUS/TEST/3 -nbi 130012/115/public/MDSPLUS/TEST/3 -fus 130012/115/public/MDSPLUS/TEST/3 -icrh 130012/15/public/MDSPLUS/TEST/3
# viewhcdwaves --uri "imas:mdsplus?user=public;shot=134173;run=101;database=TEST;version=3"
# viewkineticprofiles --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3"
# viewmachinedescription plot wall pf_active
# viewneutron --uri "imas:mdsplus?user=public;shot=121014;run=11;database=ITER;version=3"
# viewplasmacompo --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3"
# viewpressure --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3"
# viewrotation --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3"
# viewscenario --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3"
# viewsources --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3"
# viewspectrometry --uri "imas:mdsplus?user=public;shot=134000;run=37;database=TEST;version=3"
# viewall database --uri "imas:mdsplus?user=schneim;shot=92436;run=271;database=jet;version=3"

# eqdsk2ids -s 134174 -r 117 -g /home/ITER/sawantp1/git/idstools/tests/geqdsk/example.gfile -u sawantp1 -d ITER --log INFO
# eqdsk2ids --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3" -g /home/ITER/sawantp1/git/idstools/tests/geqdsk/example.gfile -u sawantp1 -d ITER --log INFO
# eqdsk2ids --uri "imas:mdsplus?user=sawantp1;shot=134174;run=117;database=ITER;version=3" -g /home/ITER/sawantp1/git/idstools/asset/geqdsk/example.gfile -u sawantp1 -d ITER --log INFO
# idschk --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3" -f /home/ITER/sawantp1/git/idstools/idstools/validation_schemas/generic/core_profiles.yml
# idscp --input_uri "imas:mdsplus?user=public;shot=131024;run=10;database=ITER;version=3" --output_uri "imas:mdsplus?user=sawantp1;shot=131024;run=2;database=ITER;version=3"
# idsdiff --uriA "imas:mdsplus?user=public;shot=122525;run=1;database=ITER;version=3" --uriB "imas:mdsplus?user=public;shot=122525;run=2;database=ITER;version=3" summary --generate-html
# idsdiff --pulseA 122525 --runA  1 --pulseB 122525 --runB 2 summary --generate-html
# idsprint --uri "imas:mdsplus?user=public;shot=131024;run=41;database=ITER;version=3" summary
# idsperf --uri "imas:mdsplus?user=public;shot=131024;run=41;database=ITER;version=3" summary
# idsperf --uri "imas:mdsplus?user=public;shot=131024;run=41;database=ITER;version=3" summary --verbose --outputRun 5 --showStats --repeat 2
# idsperf --uri "imas:mdsplus?user=public;shot=131024;run=41;database=ITER;version=3" summary --verbose --outputRun 5 --showStats --repeat 2 --uriOut "imas:mdsplus?user=sawantp1;shot=131024;run=20;database=ITER;version=3" --memoryBackend
# idsresample --input_uri "imas:mdsplus?user=public;shot=131024;run=10;database=ITER;version=3" --output_uri "imas:mdsplus?user=sawantp1;shot=131024;run=2;database=ITER;version=3"
# idssize --uri "imas:mdsplus?user=public;shot=131024;run=41;database=ITER;version=3"
# idslist --uri "imas:mdsplus?user=public;shot=131024;run=41;database=ITER;version=3"
echo -------idsrescale_equilibrium-------
idsrescale_equilibrium -si 134174 -ri 117 -so 122222 -ro 22 --rescale 2 

echo -------idsshift_equilibrium-------
idsshift_equilibrium -si 134174 -ri 117 -so 123001 -ro 1 --shift -0.01 
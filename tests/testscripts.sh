#!/bin/bash
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

#db tools test
echo -------dbscraper-------
echo TESTING: dbscraper "core_profiles/profiles_1d(0)/electrons/temperature"
dbscraper "core_profiles/profiles_1d(0)/electrons/temperature" --verbose --list-count 10 || exit 1

echo TESTING: dbscraper "equilibrium/time_slice(0)/global_quantities/volume"
dbscraper "equilibrium/time_slice(0)/global_quantities/volume" --verbose --list-count 10 || exit 1

echo -------dbselector-------
echo TESTING: dbselector core_profiles
dbselector core_profiles --list-count 10 || exit 1

echo TESTING: dbselector summary
dbselector summary --list-count 10 || exit 1

echo -------dblist-------
echo TESTING: dblist list
dblist -u public list || exit 1
dblist -u public list -c || exit 1
dblist -u public list -M || exit 1
echo TESTING: dblist --database ITER list
dblist -u public --database ITER list || exit 1
echo TESTING: dblist -u public databases
dblist databases || exit 1
echo TESTING: dblist -u public dataversions
dblist dataversions || exit 1

echo =====================================scenario_status=====================================================
echo TESTING: scenario_status -s 130012 -r 4
scenario_status -s 130012 -r 4 || exit 1

echo =====================================scenario_summary=====================================================
echo TESTING: scenario_summary
scenario_summary || exit 1

# echo TESTING: dblist -u public slices
# dblist -u public slices  || exit 1
# echo TESTING: dblist -u public  times
# dblist -u public times || exit 1

# pulse tests
for i in ${tests[@]}; do
    arr=(${i//;/ })
    shot=${arr[0]}
    run=${arr[1]}
    echo -------viewplasmacompo-------
    echo TESTING: shot=$shot : run=$run viewplasmacompo -s $shot -r $run
    viewplasmacompo -s $shot -r $run || exit 1
    echo --------------
    echo TESTING: shot=$shot : run=$run viewplasmacompo -s $shot -r $run --i
    viewplasmacompo -s $shot -r $run --i || exit 1
    echo --------------
    echo TESTING: shot=$shot : run=$run viewplasmacompo -s $shot -r $run --debug
    viewplasmacompo -s $shot -r $run --debug || exit 1

    echo -------viewequilibrium-------
    echo TESTING: shot=$shot : run=$run viewequilibrium -s $shot -r $run --rho --pfcoils --info --save
    viewequilibrium -s $shot -r $run --rho --pfcoils --info --save || exit 1

    echo TESTING: shot=$shot : run=$run viewequilibrium -s $shot -r $run --info --save
    viewequilibrium -s $shot -r $run --info --save || exit 1
    echo -------idsprint-------
    echo TESTING: idsprint -s $shot -r $run equilibrium
    idsprint -s $shot -r $run equilibrium || exit 1

    echo -------idslist-------
    echo TESTING: idslist -s $shot -r $run
    idslist -s $shot -r $run || exit 1

    echo -------idslist-------
    echo TESTING: idslist -s $shot -r $run yaml
    idslist -s $shot -r $run yaml || exit 1

    echo -------idslist-------
    echo TESTING: idslist -s $shot -r $run occ
    idslist -s $shot -r $run occ || exit 1

    echo -------idssize-------
    echo TESTING: idssize -s $shot -r $run equilibrium
    idssize -s $shot -r $run equilibrium || exit 1

    echo --------------
    echo TESTING: idssize -s $shot -r $run
    idssize -s $shot -r $run || exit 1

    echo -------idsperf-------
    echo TESTING: idsperf -s $shot -r $run equilibrium
    idsperf -s $shot -r $run equilibrium || exit 1

    echo -------viewfluxes-------
    echo TESTING: viewfluxes -s $shot -r $run -m CLOSEST
    viewfluxes -s $shot -r $run -m CLOSEST || exit 1

    echo -------viewneutron-------
    echo TESTING: viewneutron -s $shot -r $run -t 450 --save
    viewneutron -s $shot -r $run -t 450 --save || exit 1

    echo -------viewpressure-------
    echo TESTING: viewpressure -s $shot -r $run --save
    viewpressure -s $shot -r $run --save || exit 1

    echo -------viewsources-------
    echo TESTING: viewsources -s $shot -r $run
    viewsources -s $shot -r $run || exit 1

    echo -------viewedgeprofiles-------
    echo TESTING: viewedgeprofiles -s $shot -r $run --save
    viewedgeprofiles -s $shot -r $run --time 60 || exit 1

    echo -------viewscenario-------
    echo TESTING: viewscenario -s $shot -r $run --save
    viewscenario -s $shot -r $run --time 60 || exit 1
    viewscenario -s $shot -r $run --noProfiles || exit 1

    echo -------viewrotation-------

    echo TESTING: viewrotation -s $shot -r $run --info --save
    viewrotation -s $shot -r $run --time 60 || exit 1

    echo -------viewcoresources-------
    echo TESTING: viewcoresources -s $shot -r $run --save
    viewcoresources -s $shot -r $run --save || exit 1
done

echo TESTING: viewwall wall iter --save
viewwall wall iter || exit 1

# echo -------idscp-------
# echo TESTING: idscp -si 131024 -ri 10 -so 145000 -ro 2 -f
# idscp -si 131024 -ri 10 -so 145000 -ro 2 || exit 1

echo -------idsdiff-------
echo TESTING: idsdiff 122525 1 122525 2 summary
idsdiff 122525 1 122525 2 summary || exit 1
idsdiff 130011 6 130012 4 summary || exit 1

echo -------viewmachinedescription-------
viewmachinedescription list pf_active --checkValidity || exit 1
viewmachinedescription list pf_active --obsolete || exit 1
viewmachinedescription plot --save || exit 1

echo -------md_status-------
md_status -s 116000 -r 3 || exit 1

echo -------md_summary-------
md_summary -s 150502/102 || exit 1
md_summary -s nbi,on-on || exit 1

echo -------show_db_entry-------
show_db_entry -s 134174 -r 117 || exit 1

echo -------viewcoretransport-------
viewcoretransport -s 134000 -r 40 --save || exit 1

# echo -------idsresample-------
# echo TESTING: idsresample -si 131024 -ri 10 -so 145000 -ro 2
# idsresample -si 131024 -ri 10 -so 145000 -ro 2 || exit 1

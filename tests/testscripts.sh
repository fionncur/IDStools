# Test on existing  databases
declare -a tests

tests+=("122525;1")
# tests+=("123170;2")
# tests+=("123276;1")
# tests+=("120014;1")
# tests+=("131047;7")
# tests+=("134174;117")

#db tools test
echo =====================================dbscraper=====================================================
echo TESTING: dbscraper "core_profiles/profiles_1d(0)/electrons/temperature"
dbscraper "core_profiles/profiles_1d(0)/electrons/temperature" --verbose --list-count 10 || exit 1

echo TESTING: dbscraper "equilibrium/time_slice(0)/global_quantities/volume"
dbscraper "equilibrium/time_slice(0)/global_quantities/volume" --verbose --list-count 10 || exit 1

echo =====================================dbselector=====================================================
echo TESTING: dbselector core_profiles
dbselector core_profiles --list-count 10 || exit 1

echo TESTING: dbselector summary
dbselector summary --list-count 10 || exit 1

echo =====================================dblist=====================================================
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
# echo TESTING: dblist -u public slices
# dblist -u public slices  || exit 1
# echo TESTING: dblist -u public  times
# dblist -u public times || exit 1

# pulse tests
for i in ${tests[@]}; do
    arr=(${i//;/ })
    shot=${arr[0]}
    run=${arr[1]}
    echo =====================================viewidscompo=====================================================
    echo TESTING: shot=$shot : run=$run viewidscompo -s $shot -r $run
    viewidscompo -s $shot -r $run || exit 1
    echo ==========================================================================================
    echo TESTING: shot=$shot : run=$run viewidscompo -s $shot -r $run --i
    viewidscompo -s $shot -r $run --i || exit 1
    echo ==========================================================================================
    echo TESTING: shot=$shot : run=$run viewidscompo -s $shot -r $run --debug
    viewidscompo -s $shot -r $run --debug || exit 1

    echo =====================================viewequilibrium=====================================================
    echo TESTING: shot=$shot : run=$run viewequilibrium -s $shot -r $run --rho --pfcoils --info --save
    viewequilibrium -s $shot -r $run --rho --pfcoils --info --save || exit 1

    echo =====================================idsprint=====================================================
    echo TESTING: idsprint -s $shot -r $run equilibrium
    idsprint -s $shot -r $run equilibrium || exit 1

    echo =====================================idslist=====================================================
    echo TESTING: idslist -s $shot -r $run
    idslist -s $shot -r $run || exit 1

    echo TESTING: idslist -s $shot -r $run --yaml-format
    idslist -s $shot -r $run --yaml-format || exit 1

    echo TESTING: idssize -s $shot -r $run equilibrium
    idssize -s $shot -r $run equilibrium || exit 1

    echo TESTING: idssize -s $shot -r $run
    idssize -s $shot -r $run || exit 1

    echo TESTING: idsperf $shot $run equilibrium
    idsperf $shot $run equilibrium || exit 1

    echo TESTING: viewfluxes $shot $run -m CLOSEST
    viewfluxes $shot $run -m CLOSEST || exit 1

    echo TESTING: viewneutron -s $shot -r $run -t 450 --save
    viewneutron -s $shot -r $run -t 450 --save || exit 1

    echo TESTING: viewpressure $shot $run --save
    viewpressure $shot $run --save || exit 1

    echo TESTING: viewsources $shot $run --save
    viewsources $shot $run --save || exit 1

done

echo TESTING: viewwall.py wall iter
viewwall.py wall iter || exit 1

# echo =====================================idscp=====================================================
# echo TESTING: idscp -si 131024 -ri 10 -so 145000 -ro 2 -f
# idscp -si 131024 -ri 10 -so 145000 -ro 2 || exit 1

# echo =====================================idsdiff=====================================================
# echo TESTING: idsdiff 122525 1 122525 2 summary
# idsdiff 122525 1 122525 2 summary || exit 1

# echo =====================================idsresample=====================================================
# echo TESTING: idsresample -si 131024 -ri 10 -so 145000 -ro 2
# idsresample -si 131024 -ri 10 -so 145000 -ro 2 || exit 1

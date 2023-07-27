
# Test on existing  databases      
declare -a tests

tests+=("122525;1")
tests+=("123170;2")
tests+=("123276;1")
tests+=("120014;1")
tests+=("131047;7")
tests+=("134174;117")

#db tools test
echo =====================================dbscraper=====================================================
echo TESTING: dbscraper "core_profiles/profiles_1d(0)/electrons/temperature"
dbscraper "core_profiles/profiles_1d(0)/electrons/temperature" --verbose --list-count 10  || exit 1

echo TESTING: dbscraper "equilibrium/time_slice(0)/global_quantities/volume"
dbscraper "equilibrium/time_slice(0)/global_quantities/volume" --verbose --list-count 10 || exit 1 

echo =====================================dbselector=====================================================
echo TESTING: dbselector core_profiles
dbselector core_profiles --list-count 10 || exit 1 

echo TESTING: dbselector summary
dbselector summary --list-count 10 || exit 1 

echo =====================================dblist=====================================================
echo TESTING: dblist list
dblist -u public list  || exit 1 
dblist -u public list -c  || exit 1 
dblist -u public list -M  || exit 1 
echo TESTING: dblist  --database ITER list
dblist -u public  --database ITER list || exit 1 
echo TESTING: dblist -u public databases
dblist  databases || exit 1 
echo TESTING: dblist -u public  dataversions
dblist  dataversions  || exit 1 
# echo TESTING: dblist -u public slices
# dblist -u public slices  || exit 1 
# echo TESTING: dblist -u public  times
# dblist -u public times || exit 1 

# pulse tests
for i in ${tests[@]}
do
    arr=(${i//;/ })
    shot=${arr[0]}
    run=${arr[1]}
    echo =====================================pulsecomposition=====================================================
    echo TESTING: shot=$shot : run=$run  pulsecomposition -s $shot -r $run
    pulsecomposition -s $shot -r $run || exit 1 
    echo ==========================================================================================
    echo TESTING: shot=$shot : run=$run pulsecomposition -s $shot -r $run --i
    pulsecomposition -s $shot -r $run --i || exit 1  
    echo ==========================================================================================
    echo TESTING: shot=$shot : run=$run pulsecomposition -s $shot -r $run --debug
    pulsecomposition -s $shot -r $run --debug || exit 1 

    echo =====================================plotequilibrium=====================================================
    echo TESTING: shot=$shot : run=$run plotequilibrium -s $shot -r $run --rho --pfcoils --info --save
    plotequilibrium -s $shot -r $run --rho --pfcoils --info --save || exit 1 

    echo =====================================idscat=====================================================
    echo TESTING: idscat -s $shot -r $run  equilibrium
    idscat -s $shot -r $run  equilibrium || exit 1  

    # echo =====================================idscp=====================================================
    # echo TESTING: idscp -si 131024 -ri 10 -so 145000 -ro 2 -f
    # idscp -si 131024 -ri 10 -so 145000 -ro 2 || exit 1 

    # echo =====================================idsdiff=====================================================
    # echo TESTING: idsdiff 122525 1 122525 2 summary
    # idsdiff 122525 1 122525 2 summary || exit 1 

    echo =====================================idslist=====================================================
    echo TESTING: idslist -s $shot -r $run  
    idslist -s $shot -r $run   || exit 1 

    echo TESTING: idslist -s $shot -r $run  --yaml-format 
    idslist -s $shot -r $run  --yaml-format  || exit 1 

done


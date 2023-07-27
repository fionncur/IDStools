
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
test $(dbscraper "core_profiles/profiles_1d(0)/electrons/temperature" --verbose --list-count 10 2>&1 | tee dbscraper.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1

echo TESTING: dbscraper "equilibrium/time_slice(0)/global_quantities/volume"
test $(dbscraper "equilibrium/time_slice(0)/global_quantities/volume" --verbose --list-count 10 2>&1 | tee dbscraper.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1

echo =====================================dbselector=====================================================
echo TESTING: dbselector core_profiles
test $(dbselector core_profiles --list-count 10 2>&1 | tee dbselector.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1

echo TESTING: dbselector summary
test $(dbselector summary --list-count 10 2>&1 | tee dbselector.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1

echo =====================================dblist=====================================================
echo TESTING: dblist list
test $(dblist -u public list  2>&1 | tee scripts/dblist.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1
test $(dblist -u public list -c  2>&1 | tee scripts/dblist.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1
test $(dblist -u public list -M  2>&1 | tee scripts/dblist.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1
echo TESTING: dblist  --database ITER list
test $(dblist -u public  --database ITER list 2>&1 | tee scripts/dblist.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1
echo TESTING: dblist -u public databases
test $(dblist  databases 2>&1 | tee scripts/dblist.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1
echo TESTING: dblist -u public  dataversions
test $(dblist  dataversions  2>&1 | tee scripts/dblist.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1
# echo TESTING: dblist -u public slices
# test $(dblist -u public slices  2>&1 | tee scripts/dblist.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1
# echo TESTING: dblist -u public  times
# test $(dblist -u public times 2>&1 | tee scripts/dblist.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1

# pulse tests
for i in ${tests[@]}
do
    arr=(${i//;/ })
    shot=${arr[0]}
    run=${arr[1]}
    echo =====================================pulsecomposition=====================================================
    echo TESTING: shot=$shot : run=$run  pulsecomposition -s $shot -r $run
    test $(pulsecomposition -s $shot -r $run 2>&1 | tee pulsecomposition.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1
    echo ==========================================================================================
    echo TESTING: shot=$shot : run=$run pulsecomposition -s $shot -r $run --i
    test $(pulsecomposition -s $shot -r $run --i 2>&1 | tee pulsecomposition.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1 
    echo ==========================================================================================
    echo TESTING: shot=$shot : run=$run pulsecomposition -s $shot -r $run --debug
    test $(pulsecomposition -s $shot -r $run --debug 2>&1 | tee pulsecomposition.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1

    echo =====================================plotequilibrium=====================================================
    echo TESTING: shot=$shot : run=$run plotequilibrium -s $shot -r $run --rho --pfcoils --info --save
    test $(plotequilibrium -s $shot -r $run --rho --pfcoils --info --save 2>&1 | tee plotequilibrium.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1

    echo =====================================idscat=====================================================
    echo TESTING: idscat -s $shot -r $run  equilibrium
    idscat -s $shot -r $run  equilibrium || exit 1

    echo =====================================idscp=====================================================
    echo TESTING: idscp -si 131024 -ri 10 -so 145000 -ro 2 -f
    test $(idscp -si 131024 -ri 10 -so 145000 -ro 2 2>&1 | tee idscp.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1

    # echo =====================================idsdiff=====================================================
    # echo TESTING: idsdiff 122525 1 122525 2 summary
    # test $(idsdiff 122525 1 122525 2 summary 2>&1 | tee idsdiff.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1

    echo =====================================idslist=====================================================
    echo TESTING: idslist -s $shot -r $run  
    test $(idslist -s $shot -r $run   2>&1 | tee scripts/idslist.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1

    echo TESTING: idslist -s $shot -r $run  --yaml-format 
    test $(idslist -s $shot -r $run  --yaml-format  2>&1 | tee scripts/idslist.log  | grep -ciE "err|fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || exit 1

done


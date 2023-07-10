
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
test $(python dbscraper "core_profiles/profiles_1d(0)/electrons/temperature" --verbose --list-count 10 2>&1 | tee dbscraper.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

echo TESTING: dbscraper "equilibrium/time_slice(0)/global_quantities/volume"
test $(python dbscraper "equilibrium/time_slice(0)/global_quantities/volume" --verbose --list-count 10 2>&1 | tee dbscraper.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

echo =====================================dbselector=====================================================
echo TESTING: dbselector core_profiles
test $(python dbselector core_profiles --list-count 10 2>&1 | tee dbselector.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

echo TESTING: dbselector summary
test $(python dbselector summary --list-count 10 2>&1 | tee dbselector.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

echo =====================================dblist=====================================================
echo TESTING: dblist list
test $(python dblist list  2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
test $(python dblist list -c  2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
test $(python dblist list -m  2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
echo TESTING: dblist  --database ITER list
test $(python dblist  --database test list 2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
echo TESTING: dblist  databases
test $(python dblist  databases 2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
echo TESTING: dblist  dataversions
test $(python dblist  dataversions  2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
echo TESTING: dblist  slices
test $(python dblist  slices  2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
echo TESTING: dblist  times
test $(python dblist  times  2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

# pulse tests
for i in ${tests[@]}
do
    arr=(${i//;/ })
    shot=${arr[0]}
    run=${arr[1]}
    echo =====================================pulsecomposition=====================================================
    echo TESTING: shot=$shot : run=$run  pulsecomposition -s $shot -r $run
    test $(python pulsecomposition -s $shot -r $run 2>&1 | tee pulsecomposition.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
    echo ==========================================================================================
    echo TESTING: shot=$shot : run=$run pulsecomposition -s $shot -r $run --i
    test $(python pulsecomposition -s $shot -r $run --i 2>&1 | tee pulsecomposition.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed" 
    echo ==========================================================================================
    echo TESTING: shot=$shot : run=$run pulsecomposition -s $shot -r $run --debug
    test $(python pulsecomposition -s $shot -r $run --debug 2>&1 | tee pulsecomposition.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    echo =====================================plotequilibrium=====================================================
    echo TESTING: shot=$shot : run=$run plotequilibrium -s $shot -r $run --rho --pfcoils --info --save
    test $(python plotequilibrium -s $shot -r $run --rho --pfcoils --info --save 2>&1 | tee plotequilibrium.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    echo =====================================idscat=====================================================
    echo TESTING: idscat -s $shot -r $run  equilibrium
    test $(python idscat -s $shot -r $run  equilibrium 2>&1 | tee idscat.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    echo =====================================idscp=====================================================
    echo TESTING: idscp -si 131024 -ri 10 -so 145000 -ro 2
    test $(python idscp -si 131024 -ri 10 -so 145000 -ro 2 2>&1 | tee idscp.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    echo =====================================idsdiff=====================================================
    echo TESTING: idsdiff 122525 1 122525 2 summary
    test $(python idsdiff 122525 1 122525 2 summary 2>&1 | tee idsdiff.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    echo =====================================idslist=====================================================
    echo TESTING: idslist -s $shot -r $run  
    test $(python idslist -s $shot -r $run   2>&1 | tee scripts/idslist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    echo TESTING: idslist -s $shot -r $run  --yaml-format 
    test $(python idslist -s $shot -r $run  --yaml-format  2>&1 | tee scripts/idslist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

done


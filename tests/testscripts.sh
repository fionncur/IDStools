
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
echo TESTING: dbscraper.py "core_profiles/profiles_1d(0)/electrons/temperature"
test $(python ../scripts/dbscraper.py "core_profiles/profiles_1d(0)/electrons/temperature" --verbose --list-count 10 2>&1 | tee ../scripts/dbscraper.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

echo TESTING: dbscraper.py "equilibrium/time_slice(0)/global_quantities/volume"
test $(python ../scripts/dbscraper.py "equilibrium/time_slice(0)/global_quantities/volume" --verbose --list-count 10 2>&1 | tee ../scripts/dbscraper.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

echo =====================================dbselector=====================================================
echo TESTING: dbselector.py core_profiles
test $(python ../scripts/dbselector.py core_profiles --list-count 10 2>&1 | tee ../scripts/dbselector.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

echo TESTING: dbselector.py summary
test $(python ../scripts/dbselector.py summary --list-count 10 2>&1 | tee ../scripts/dbselector.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

echo =====================================dblist=====================================================
echo TESTING: dblist.py list
test $(python ../scripts/dblist.py list  2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
test $(python ../scripts/dblist.py list -c  2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
test $(python ../scripts/dblist.py list -m  2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
echo TESTING: dblist.py  --database ITER list
test $(python ../scripts/dblist.py  --database test list 2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
echo TESTING: dblist.py  databases
test $(python ../scripts/dblist.py  databases 2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
echo TESTING: dblist.py  dataversions
test $(python ../scripts/dblist.py  dataversions  2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
echo TESTING: dblist.py  slices
test $(python ../scripts/dblist.py  slices  2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
echo TESTING: dblist.py  times
test $(python ../scripts/dblist.py  times  2>&1 | tee scripts/dblist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

# pulse tests
for i in ${tests[@]}
do
    arr=(${i//;/ })
    shot=${arr[0]}
    run=${arr[1]}
    echo =====================================pulsecomposition=====================================================
    echo TESTING: shot=$shot : run=$run  ../scripts/pulsecomposition.py -s $shot -r $run
    test $(python ../scripts/pulsecomposition.py -s $shot -r $run 2>&1 | tee ../scripts/pulsecomposition.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
    echo ==========================================================================================
    echo TESTING: shot=$shot : run=$run ../scripts/pulsecomposition.py -s $shot -r $run --i
    test $(python ../scripts/pulsecomposition.py -s $shot -r $run --i 2>&1 | tee ../scripts/pulsecomposition.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed" 
    echo ==========================================================================================
    echo TESTING: shot=$shot : run=$run ../scripts/pulsecomposition.py -s $shot -r $run --debug
    test $(python ../scripts/pulsecomposition.py -s $shot -r $run --debug 2>&1 | tee ../scripts/pulsecomposition.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    echo =====================================plotequilibrium=====================================================
    echo TESTING: shot=$shot : run=$run ../scripts/plotequilibrium.py -s $shot -r $run --rho --pfcoils --info --save
    test $(python ../scripts/plotequilibrium.py -s $shot -r $run --rho --pfcoils --info --save 2>&1 | tee ../scripts/plotequilibrium.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    echo =====================================idscat=====================================================
    echo TESTING: idscat.py -s $shot -r $run  equilibrium
    test $(python ../scripts/idscat.py -s $shot -r $run  equilibrium 2>&1 | tee ../scripts/idscat.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    echo =====================================idscp=====================================================
    echo TESTING: idscp.py -si 131024 -ri 10 -so 145000 -ro 2
    test $(python ../scripts/idscp.py -si 131024 -ri 10 -so 145000 -ro 2 2>&1 | tee ../scripts/idscp.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    echo =====================================idsdiff=====================================================
    echo TESTING: idsdiff.py 122525 1 122525 2 summary
    test $(python ../scripts/idsdiff.py 122525 1 122525 2 summary 2>&1 | tee ../scripts/idsdiff.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    echo =====================================idslist=====================================================
    echo TESTING: idslist.py -s $shot -r $run  
    test $(python ../scripts/idslist.py -s $shot -r $run   2>&1 | tee scripts/idslist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    echo TESTING: idslist.py -s $shot -r $run  --yaml-format 
    test $(python ../scripts/idslist.py -s $shot -r $run  --yaml-format  2>&1 | tee scripts/idslist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

done



# Test on existing  databases      
declare -a tests

tests+=("122525;1")
tests+=("123170;2")
tests+=("123276;1")
tests+=("120014;1")
tests+=("131047;7")
tests+=("134174;117")

for i in ${tests[@]}
do
    arr=(${i//;/ })
    shot=${arr[0]}
    run=${arr[1]}
    # echo ==========================================================================================
    # echo TESTING: shot=$shot : run=$run  ../scripts/pulsecomposition.py -s $shot -r $run
    # test $(python ../scripts/pulsecomposition.py -s $shot -r $run 2>&1 | tee ../scripts/pulsecomposition.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"
    # echo ==========================================================================================
    # echo TESTING: shot=$shot : run=$run ../scripts/pulsecomposition.py -s $shot -r $run --i
    # test $(python ../scripts/pulsecomposition.py -s $shot -r $run --i 2>&1 | tee ../scripts/pulsecomposition.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed" 
    # echo ==========================================================================================
    # echo TESTING: shot=$shot : run=$run ../scripts/pulsecomposition.py -s $shot -r $run --debug
    # test $(python ../scripts/pulsecomposition.py -s $shot -r $run --debug 2>&1 | tee ../scripts/pulsecomposition.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    #--------
    # echo TESTING: shot=$shot : run=$run ../scripts/plotequilibrium.py -s $shot -r $run --rho --pfcoils --info --save
    # test $(python ../scripts/plotequilibrium.py -s $shot -r $run --rho --pfcoils --info --save 2>&1 | tee ../scripts/plotequilibrium.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    # echo ==========================================================================================
    # echo TESTING: dbscraper.py "core_profiles/profiles_1d(0)/electrons/temperature"
    # test $(python ../scripts/dbscraper.py "core_profiles/profiles_1d(0)/electrons/temperature" --verbose --list-count 10 2>&1 | tee ../scripts/dbscraper.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    # echo TESTING: dbscraper.py "equilibrium/time_slice(0)/global_quantities/volume"
    # test $(python ../scripts/dbscraper.py "equilibrium/time_slice(0)/global_quantities/volume" --verbose --list-count 10 2>&1 | tee ../scripts/dbscraper.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    # python scripts/dbselector.py core_profiles
    # python scripts/dbselector.py summary

    # echo TESTING: idscat.py -s $shot -r $run  equilibrium
    # test $(python ../scripts/idscat.py -s $shot -r $run  equilibrium 2>&1 | tee ../scripts/dbscraper.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    # echo TESTING: idscp.py -si 131024 -ri 10 -so 145000 -ro 2
    # test $(python ../scripts/idscp.py -si 131024 -ri 10 -so 145000 -ro 2 2>&1 | tee ../scripts/dbscraper.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    # echo TESTING: idsdiff.py 122525 1 122525 2 summary
    # test $(python ../scripts/idsdiff.py 122525 1 122525 2 summary 2>&1 | tee ../scripts/dbscraper.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    echo TESTING: idslist.py -s $shot -r $run  
    test $(python scripts/idslist.py -s $shot -r $run   2>&1 | tee scripts/idslist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

    echo TESTING: idslist.py -s $shot -r $run  --yaml-format 
    test $(python scripts/idslist.py -s $shot -r $run  --yaml-format  2>&1 | tee scripts/idslist.log  | grep -ciE "fault|error[ :]|exception|severe") -eq 0 && echo "ok passed" || echo "not ok failed"

done





# if test ${x} -eq "0"
# then
#   echo "ok passed"
# else
#   echo "not ok failed"
# fi
# test 0 -eq ()) echo . || echo 

# python scripts/idslist.py -s 134174 -r 117
# python scripts/idsdump.py -s 134174 -r 117 equilibrium 
# python scripts/idsdump.py -s 134174 -r 117 equilibrium 
# python scripts/idsdump.py -s 134174 -r 117 equilibrium 
# python scripts/pulsecomparer.py --generate-html 122525 1 122525 2 summary
# python scripts/pulsescraper.py equilibrium
# python scripts/pulseselector.py equilibrium
#!/bin/bash

declare -a tests

export ids_path="$IMAS_HOME/shared/imasdb/validation"

USR=$USER
TOKAMAK="test"
DATAVERSION="3"

#========================================================================#
# test = shot;run;ids;dataPath

#  >>> magnetics IDS  <<<

tests+=("$USR;$TOKAMAK;$DATAVERSION;53223;0;magnetics;flux_loop(1)/flux/data(1:5)")
tests+=("$USR;$TOKAMAK;$DATAVERSION;53223;0;magnetics;flux_loop(1)/flux")
tests+=("$USR;$TOKAMAK;$DATAVERSION;53223;0;magnetics;bpol_probe(2)/field/data")
tests+=("$USR;$TOKAMAK;$DATAVERSION;53223;0;magnetics;bpol_probe(2:3)/field/data")

#  >>> pf_passive IDS  <<<

tests+=("$USR;$TOKAMAK;$DATAVERSION;53223;0;pf_passive;loop(5:6)/current")
tests+=("$USR;$TOKAMAK;$DATAVERSION;53223;0;pf_passive;loop(:)/current")  
tests+=("$USR;$TOKAMAK;$DATAVERSION;53223;0;pf_passive;loop(34)/current") 
tests+=("$USR;$TOKAMAK;$DATAVERSION;53223;0;pf_passive;loop(33)/current")
tests+=("$USR;$TOKAMAK;$DATAVERSION;53223;0;pf_passive;loop(5:9)/current")
tests+=("$USR;$TOKAMAK;$DATAVERSION;53223;0;pf_passive;time")

#  >>> core_profiles IDS  <<<

tests+=("$USR;$TOKAMAK;$DATAVERSION;12;2;core_profiles;profiles_1d(2:)/grid/rho_tor_norm(2:4)")
tests+=("$USR;$TOKAMAK;$DATAVERSION;12;2;core_profiles;profiles_1d(2)")
tests+=("$USR;$TOKAMAK;$DATAVERSION;12;2;core_profiles;profiles_1d(8:)/time")
tests+=("$USR;$TOKAMAK;$DATAVERSION;12;2;core_profiles;profiles_1d(2)/ion(2)")
tests+=("$USR;$TOKAMAK;$DATAVERSION;12;2;core_profiles;profiles_1d(2)/ion(1)/element") #<= this test returns an error. It is OK as "element" is empty
tests+=("$USR;$TOKAMAK;$DATAVERSION;12;2;core_profiles;profiles_1d(1:2)/ion(1)/state")
tests+=("$USR;$TOKAMAK;$DATAVERSION;12;2;core_profiles;profiles_1d(3)/ion(2)/state(1:)/z_min")
tests+=("$USR;$TOKAMAK;$DATAVERSION;12;2;core_profiles;time(4::-1)")
tests+=("$USR;$TOKAMAK;$DATAVERSION;12;2;core_profiles;time(3:3)")
tests+=("$USR;$TOKAMAK;$DATAVERSION;12;2;core_profiles;time(3:4)")
tests+=("$USR;$TOKAMAK;$DATAVERSION;12;2;core_profiles;ids_properties")
tests+=("$USR;$TOKAMAK;$DATAVERSION;12;2;core_profiles;ids_properties/comment")

#  >>> equilibrium IDS  <<<

tests+=("$USR;$TOKAMAK;$DATAVERSION;400;20;equilibrium;ids_properties/comment")
tests+=("$USR;$TOKAMAK;$DATAVERSION;400;20;equilibrium;time_slice(2)/profiles_1d/q")  
tests+=("$USR;$TOKAMAK;$DATAVERSION;400;20;equilibrium;time_slice(2)/profiles_1d/q(3:)")
tests+=("$USR;$TOKAMAK;$DATAVERSION;400;20;equilibrium;time_slice(:3)/profiles_1d/q")  


#========================================================================#sssss


for i in ${tests[@]}
do
      arr=(${i//;/ })
      user=${arr[0]}
      tokamak=${arr[1]}
      dataversion=${arr[2]}
      shot=${arr[3]}
      run=${arr[4]}
      ids=${arr[5]}
      dataPath=${arr[6]}
      echo ==========================================================================================
      echo ==========================================================================================
      echo ===   TESTING: user=$user : tokamak=$tokamak : dataversion=$dataversion : shot=$shot : run=$run : ids=$ids : path=$dataPath
      echo ==========================================================================================
      echo ==========================================================================================
      echo ===
      echo === DumpPath [raw data]
      echo === CMD: ../bin/idsdumppath $user $tokamak $dataversion $shot $run $ids \"$dataPath\"
      echo ===================
      echo ------------
      ../bin/idsdumppath $user $tokamak $dataversion $shot $run $ids $dataPath
      echo ==========================================================================================
      echo ===
      echo === PartialGET
      echo === CMD: ../bin/idspartialget $user $tokamak $dataversion $shot $run $ids \"$dataPath\"
      echo ===================
      echo ------------
      ../bin/idspartialget $user $tokamak $dataversion $shot $run $ids $dataPath
done

exit 0


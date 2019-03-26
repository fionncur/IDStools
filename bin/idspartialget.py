#!/usr/bin/env python

import numpy
import imas
import sys

if __name__ == '__main__':

    if len(sys.argv) != 8:
        print('Usage: idspartialget <USER> <TOKAMAK> <VERSION> <SHOT> <RUN> <IDS> <DATA_PATH>')
        exit(1)

    user = sys.argv[1]
    tokamak = sys.argv[2]
    version = sys.argv[3]
    shot = int(sys.argv[4])
    run = int(sys.argv[5])
    idsFullName = sys.argv[6]
    dataPath = sys.argv[7]
    
    idsOccurrence = 0

    imas_obj = imas.ids(shot, run, 0, 0)
    imas_obj.open_env(user, tokamak, version)  
    

    idsNameElements = idsFullName.split('/')
    if len(idsNameElements) > 2:
      print('ERROR: "' + idsFullName + '" syntax error!')
      exit(1)
      
    idsName = idsNameElements[0]
    
    
    try:
        ids = getattr(imas_obj, idsName)
    except:
        print('ERROR: IDS "' + idsName + '" not found. Misspelled name?')
        exit(1)
    
    try:
        if len(idsNameElements) == 2:
            idsOccurrence = int(idsNameElements[1])
    except:
      print('ERROR: "' + idsFullName + '" syntax error!')
      exit(1)
    
    
    try:
        result = ids.partialGet(dataPath, idsOccurrence)
    except Exception, exc:
        print(str(exc))
        exit(1)
    
    #result = ids.partialGet(dataPath, idsOccurrence)
    
    
    resultType = type(result)
    print 'Type: ' + str(resultType)
    if result.__class__  == numpy.ndarray:
       print 'Shape: ' + str(result.shape)
       print 'Data type: ' + str(result.dtype.name)
       
    if result.__class__  == numpy.ndarray and len(result) < 1 :
        exit(0)
  
    print '----------------------------------------------'
    if result.__class__  == numpy.ndarray and result[0].__class__.__module__ != 'numpy' :
       for i in range(len(result)):
            print(result[i])
            print '-------------------------'
    else:       
        print(result)

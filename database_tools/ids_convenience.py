import imas

# ------------------------------------------------------------------------------------
def ids_read(idsname,shot,run,user_or_path,database,occ=0):
    input = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,database,shot,run,user_or_path)
    input.open()
    ids = input.get(idsname)
    input.close()
    return ids
# ------------------------------------------------------------------------------------
def ids_read_slice(idsname,time_slice,shot,run,user_or_path,database,occ=0,interp_method=1):
    input = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,database,shot,run,user_or_path)
    input.open()
    ids = input.get_slice(idsname,time_slice,interp_method,occ)
    input.close()
    return ids
# ------------------------------------------------------------------------------------
def ids_write(ids,shot,run,user_or_path,database,occ=0):
    output = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,database,shot,run,user_or_path)
    retstatus,idx = output.open()
    if retstatus == 0:
        print('IDS appended to existing '+str(shot)+'/'+str(run)+'/'+user_or_path+'/'+database+' datafile')
        output.put(ids)
        output.close()
    else:
        print('New '+str(shot)+'/'+str(run)+'/'+user_or_path+'/'+database+' datafile created')
        retstatus,idx = output.create()
        if retstatus == 0:
            output.put(ids)
            output.close()
        else:
            print('Could not create '+str(shot)+'/'+str(run)+'/'+user_or_path+'/'+database+' datafile')
# ------------------------------------------------------------------------------------
def ids_write_slice(ids,shot,run,user_or_path,database,occ=0):
    output = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,database,shot,run,user_or_path)
    retstatus,idx = output.open()
    if retstatus == 0:
        print('IDS appended to existing '+str(shot)+'/'+str(run)+'/'+user_or_path+'/'+database+' datafile')
        output.put_slice(ids)
        output.close()
    else:
        print('New '+str(shot)+'/'+str(run)+'/'+user_or_path+'/'+database+' datafile created')
        retstatus,idx = output.create()
        if retstatus == 0:
            output.put_slice(ids)
            output.close()
        else:
            print('Could not create '+str(shot)+'/'+str(run)+'/'+user_or_path+'/'+database+' datafile')
# ------------------------------------------------------------------------------------


import inspect
import imas


# ------------------------------------------------------------------------------------
def ids_read(idsname, shot, run, user_or_path, database, occ=0):
    input = imas.DBEntry(imas.imasdef.m_d_s_p_l_u_s__b_a_c_k_e_n_d, database, shot, run, user_or_path)
    input.open()
    ids = input.get(idsname)
    input.close()
    return ids


# ------------------------------------------------------------------------------------
def ids_read_slice(idsname, time_slice, shot, run, user_or_path, database, occ=0, interp_method=1):
    input = imas.DBEntry(imas.imasdef.m_d_s_p_l_u_s__b_a_c_k_e_n_d, database, shot, run, user_or_path)
    input.open()
    ids = input.get_slice(idsname, time_slice, interp_method, occ)
    input.close()
    return ids


# ------------------------------------------------------------------------------------
def ids_write(ids, shot, run, user_or_path, database, occ=0):
    output = imas.DBEntry(imas.imasdef.m_d_s_p_l_u_s__b_a_c_k_e_n_d, database, shot, run, user_or_path)
    retstatus, idx = output.open()
    if retstatus == 0:
        print(
            "IDS appended to existing " + str(shot) + "/" + str(run) + "/" + user_or_path + "/" + database + " datafile"
        )
        output.put(ids)
        output.close()
    else:
        print("New " + str(shot) + "/" + str(run) + "/" + user_or_path + "/" + database + " datafile created")
        retstatus, idx = output.create()
        if retstatus == 0:
            output.put(ids)
            output.close()
        else:
            print("Could not create " + str(shot) + "/" + str(run) + "/" + user_or_path + "/" + database + " datafile")


# ------------------------------------------------------------------------------------
def ids_write_slice(ids, shot, run, user_or_path, database, occ=0):
    output = imas.DBEntry(imas.imasdef.m_d_s_p_l_u_s__b_a_c_k_e_n_d, database, shot, run, user_or_path)
    retstatus, idx = output.open()
    if retstatus == 0:
        print(
            "IDS appended to existing " + str(shot) + "/" + str(run) + "/" + user_or_path + "/" + database + " datafile"
        )
        output.put_slice(ids)
        output.close()
    else:
        print("New " + str(shot) + "/" + str(run) + "/" + user_or_path + "/" + database + " datafile created")
        retstatus, idx = output.create()
        if retstatus == 0:
            output.put_slice(ids)
            output.close()
        else:
            print("Could not create " + str(shot) + "/" + str(run) + "/" + user_or_path + "/" + database + " datafile")


# ------------------------------------------------------------------------------------

# ----------------------------------------------------------------
# To display the sub-structure of an IDS
# ----------------------------------------------------------------
# Examples:
# ----------
# idsprint('nbi')
# idsprint('nbi.unit')
# idsprint('nbi.unit[0]')
# idsprint('nbi.unit[0].power_launched')
# idsprint('nbi.unit[0].power_launched.data')
# ----------
# idsrprint works the same, only that it is recursive over the
# sub-structure
# ----------------------------------------------------------------


# DISPLAY CONTENT OF AN IDS OR ONE OF ITS SUB-STRUCTURES
def idsprint(stringvar):
    obj_compounds = stringvar.split(".")
    # ids = inspect.stack()[1][0].f_globals[obj_compounds[0]]
    obj_compounds[0] = "ids"
    var = eval(".".join(obj_compounds))
    if hasattr(var, "__dict__"):
        # nkeys = eval("len(var.__dict__.keys())")
        for key in var.__dict__.keys():
            if key[0] != "_" and "_error_" not in key:
                if hasattr(var, "__len__"):
                    lenvar = len(var)
                    if lenvar > 0:
                        print("  " + stringvar + "[0:" + str(lenvar - 1) + "]")
                    else:
                        print("  " + stringvar + "[]")
                    break
                else:
                    if hasattr(eval("var." + key), "__len__"):
                        lenvar = len(eval("var." + key))
                        if hasattr(eval("var." + key), "__dict__"):
                            if lenvar > 0:
                                if lenvar == 1:
                                    print("  " + stringvar + "." + key + "[0]")
                                else:
                                    print("  " + stringvar + "." + key + "[0:" + str(lenvar - 1) + "]")
                            else:
                                print("  " + stringvar + "." + key + "[]")
                        else:
                            print("  " + stringvar + "." + key + "(" + str(lenvar) + ")")
                    else:
                        print("  " + stringvar + "." + key)
    else:
        print("  " + str(var))


# SAME STUFF BUT RECURSIVE OVER CHILD SUB-STRUCTURES
def idsrprint(stringvar):
    obj_compounds = stringvar.split(".")
    if obj_compounds[0] in globals():
        __idsrrprint(obj_compounds[0], stringvar)
    else:
        ids = inspect.stack()[1][0].f_globals[obj_compounds[0]]
        if hasattr(eval(stringvar.replace(stringvar.split(".")[0], "ids")), "__dict__"):
            __idsrrprint(ids, stringvar)
        else:
            print("  " + str(eval(stringvar.replace(stringvar.split(".")[0], "ids"))))


def __idsrrprint(ids, stringvar):
    obj_compounds = stringvar.split(".")
    stringvar = ".".join(obj_compounds)
    obj_compounds[0] = "ids"
    var = eval(".".join(obj_compounds))
    if hasattr(var, "__dict__"):
        # nkeys = eval("len(var.__dict__.keys())")
        for key in var.__dict__.keys():
            if key[0] != "_" and "_error_" not in key:
                if hasattr(var, "__len__"):
                    lenvar = len(var)
                    if lenvar > 0:
                        print("  " + stringvar + "[0:" + str(lenvar - 1) + "]")
                    else:
                        print("  " + stringvar + "[]")
                    for i in range(lenvar):
                        __idsrrprint(ids, stringvar + "[" + str(i) + "]")
                else:
                    if hasattr(eval("var." + key), "__len__"):
                        lenvar = len(eval("var." + key))
                        if hasattr(eval("var." + key), "__dict__"):
                            if lenvar > 0:
                                if lenvar == 1:
                                    print("  " + stringvar + "." + key + "[0]")
                                else:
                                    print("  " + stringvar + "." + key + "[0:" + str(lenvar - 1) + "]")
                            else:
                                print("  " + stringvar + "." + key + "[]")
                            for i in range(lenvar):
                                __idsrrprint(ids, stringvar + "." + key + "[" + str(i) + "]")
                        else:
                            print("  " + stringvar + "." + key + "(" + str(lenvar) + ")")
                    else:
                        print("  " + stringvar + "." + key)
                        __idsrrprint(ids, stringvar + "." + key)

import numpy as np
from packaging import version
ARRAY_EQUAL_KWARGS = "equal_nan=True" if version.parse(np.__version__)>version.parse("1.19") else ""



def compare(X, Y, field=None, ignore_version=True):
    """
    Iterate over every field and compare values depending on the type of field.
    
    Parameters
    ----------
    X, Y: IDS like objects
          IDSs (or sub-structures) objects being compared
    field: str, optional
          name of the IDS (or sub-structure) being compared
    ignore_version: bool, optional
          ignore content of ids_properties.version_put for the comparison
    """

    if hasattr(X,"__name__") and hasattr(Y,"__name__"):
        if X.__name__ == Y.__name__:
            if field is None:
                field=X.__name__
        else:
            print(f"Different IDSs: {X.__name__} and {Y.__name__}")
            return
    elif hasattr(X,"_base_path") and hasattr(Y,"_base_path"):
        if X._base_path == Y._base_path:
            if field is None:
                field=X._base_path
        else:
            print(f"Different structure: {X._base_path} and {Y._base_path}")
            return
    else:
        # un-expected different objects
        print(f"Unexpected objects: {type(X)} and {type(Y)}")
        return
    
            
    Xd = X.__dict__
    Yd = Y.__dict__
    for key in set(Xd.keys()).union(set(Yd.keys())):

        if key.startswith("_"):
            continue

        if "hli_utils" == key:
            continue

        if ignore_version and "version_put" == key:
            continue

        if key not in Xd:
            print(f"{key} not present in X")
            continue

        if key not in Yd:
            print(f"{key} not present in Y")
            continue

        Xo = X.__dict__[key]
        Yo = Y.__dict__[key]
        if type(Xo) != type(Yo):
            print(f"Different type for {field}.{key}")

        if hasattr(Xo, "__module__") and "imas" in Xo.__module__:
            #TO DO: To be removed, when private _base_path will be replaced by __name__
            if hasattr(Xo, "__name__"):
                attrname = Xo.__name__
            else:
                attrname = Xo._base_path
            compare(Xo, Yo, field=f"{field}.{attrname}", ignore_version=ignore_version)
            continue

        # treatment of struct_array and list of strings
        if type(Xo).__name__ == "list":
            if len(Xo) != len(Yo):
                # avoids printing "array" as this is internal attribute for AoS
                if key == "array":
                    f = field
                else:
                    f = f"{field}.{key}"
                print(f"{f} is of different length")
            else:
                for i in range(len(Xo)):
                    if "structArrayElement" in type(Xo[i]).__name__ :
                        compare(Xo[i], Yo[i], field = f"{field}[{i}]", ignore_version=ignore_version)
                    else:
                        #print("list of "+type(xo[i]).__name__)
                        continue
        else:
            if isinstance(Xo, np.ndarray) and isinstance(Yo, np.ndarray):
                result = np.array_equal(Xo, Yo, ARRAY_EQUAL_KWARGS) 
            else:
                result = Xo == Yo

            if not result:
                missing = [False]
                if isinstance( Xo, np.ndarray ):
                    if Xo.size == 0:
                        missing = [True, "first"]
                    elif Yo.size == 0:
                        missing = [True, "second"]
                else:
                    missmap = { int : -999999999, float : -9e+40}
                    for t in missmap:
                        if isinstance(Xo, t):
                            if Xo == missmap[t]:
                                missing = [True, "first"]
                            elif Yo == missmap[t]:
                                missing = [True, "second"]

                if missing[0]:
                    print(f"{field}.{key} is missing in the {missing[1]} IDS")
                else:
                    print(f"{field}.{key} has different values")
                        

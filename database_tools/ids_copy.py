import imas,copy

def ids_copy(ids1,idx=False):

    idsname = str(ids1.__class__).split('.')[-1].replace('\'','').replace('>','')

    new=imas.ids(0,0,0,0)
    ids2 = eval('new.'+idsname)
    if idx == False:
        idx_out = ids2.getPulseCtx()
    else:
        print(idx)
        idx_out = idx

    ids2 = copy.deepcopy(ids1)
    ids2.setPulseCtx(idx_out)

    return ids2

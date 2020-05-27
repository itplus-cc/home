def argsStrTolist(argsStr):
    todict = argsStr.strip().strip(',').split(",")
    if not todict:
        return []
    return list(map(lambda x: x.strip(), todict))


def kwargsStrTodict(kwargsStr):
    todict = {}
    strlist = kwargsStr.strip().strip(',').split(";")
    if not strlist:
        return {}
    for x in strlist:
        if ":" in x:
            tmp = x.split(':')
            if len(tmp) != 2:
                continue
            todict[tmp[0]] = tmp[1]
        else:
            continue
    return todict
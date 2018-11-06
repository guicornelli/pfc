import numpy as np
from datetime import timedelta


def removeerrors(value, timestamp, amostra):
    errorsTS = []
    errorsV = []
    val = []
    ts = []
    cDupVal = 0
    cDup = 0
    for i in range(amostra - 1):
        i = i + 1
        diffTS = timestamp[i] - timestamp[i - 1]
        diffV = value[i] - value[i - 1]
        if diffTS == timedelta(0):  # duplicados
            if (timestamp[i - 1].minute % 10 == 0) and (timestamp[i - 1].second < 7):
                ts.append(timestamp[i])
                val.append(value[i])
                cDupVal = cDupVal + 1
            else:
                errorsTS.append(timestamp[i])
                errorsV.append(value[i])
                cDup = cDup + 1
        elif (timestamp[i].minute % 10 == 0) and (timestamp[i].second < 7):  # congelados
            if (timestamp[i - 1].minute % 10 == 0) and (timestamp[i - 1].second < 7) and (diffTS.seconds < 500):
                ts.append(timestamp[i])
                val.append(value[i])
            else:
                errorsTS.append(timestamp[i])
                errorsV.append(value[i])
        else:  # amostra filtrada
            ts.append(timestamp[i])
            val.append(value[i])
    val = np.array(val)
    ts = np.array(ts)
    errorsTS = np.array(errorsTS)
    errorsV = np.array(errorsV)

    return val, ts, errorsTS, errorsV

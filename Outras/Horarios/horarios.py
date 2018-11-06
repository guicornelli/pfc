from datetime import date, datetime, timedelta
from bddataJun import data


def horastrabdia (dia, entM, saiM, entT, saiT):
    horarios = [dia, entM[0:2]+':'+entM[2:4], saiM[0:2]+':'+saiM[2:4], entT[0:2]+':'+entT[2:4], saiT[0:2]+':'+saiT[2:4]]
    return horarios


def verifica(hora):
    while len(hora) != 4 or int(hora[0:2]) > 23 or int(hora[2:4]) > 59:
        print("Hora invalida, favor inserir novamente")
        hora = input("insira o horario: ")
    return hora


def verificadia(dia):
    while len(dia) != 4 or int(dia[0:2]) > 31 or int(dia[2:4]) > 12 or dia+'2018' in data.keys():
        print("Data invalida ou ja inserida, favor inserir novamente")
        dia = input("insira a data: ")
    return dia


def inserirdados():
    dia = input("insira a data: ")
    dia = verificadia(dia)
    entM = input("insira o horario de entrada M: ")
    entM = verifica(entM)
    saiM = input("insira o horario de saida M: ")
    saiM = verifica(saiM)
    entT = input("insira o horario de entrada T: ")
    entT= verifica(entT)
    saiT = input("insira o horario de saida T: ")
    saiT = verifica(saiT)

    # ##MUDAR ANO QND NECESSARIO## #
    dia = datetime(year=int(2018), month=int(dia[2:4]), day=int(dia[0:2]))
    dia = dia.strftime('%d%m%Y')
    horas = horastrabdia(dia, entM, saiM, entT, saiT)

    # print [horas[i] for i in range(len(horas))]
    # print data.keys()
    # print "\'"+horas[0]+"\'"

    # ##MUDAR ARQUIVO QND TROCAR MES## #

    if horas[0] not in data.keys():
        with open('C:/Users/guilh/PycharmProjects/17274-COAtlantic/Udacity/Horarios/bddataJun.py', 'a') as arq:
            novosvalores = "data["+"\""+horas[0]+"\""+"]={'entM':"+" \'"+entM+"\'"+", 'saiM':"+" \'"+saiM+"\'"+", 'entT':"+" \'"+entT+"\'"+", 'saiT':"+" \'"+saiT+"\'"+"}\n"
            arq.write(novosvalores)
    else:
        print("esta data ja foi inserida")

    return horas


def calcmes():
    h = 0
    m = 0
    for j in data.keys():
        hsaiM = datetime(year=int(j[4:8]), month=int(j[2:4]), day=int(j[0:2]), hour=int((data.__getitem__(j).__getitem__('saiM'))[0:2]), minute=int((data.__getitem__(j).__getitem__('saiM'))[2:4]))
        diffM = hsaiM - timedelta(hours=int((data.__getitem__(j).__getitem__('entM'))[0:2]), minutes=int((data.__getitem__(j).__getitem__('entM'))[2:4]))
        hsaiT = datetime(year=int(j[4:8]), month=int(j[2:4]), day=int(j[0:2]), hour=int((data.__getitem__(j).__getitem__('saiT'))[0:2]), minute=int((data.__getitem__(j).__getitem__('saiT'))[2:4]))
        diffT = hsaiT - timedelta(hours=int((data.__getitem__(j).__getitem__('entT'))[0:2]), minutes=int((data.__getitem__(j).__getitem__('entT'))[2:4]))
        hdia = diffM + timedelta(hours=diffT.hour, minutes=diffT.minute)
        h = h + hdia.hour
        m = m + hdia.minute
        tmes = (h + (m / 60.0))

    hour2min = round((tmes % 1)*60, 0)
    salario = tmes*8.5
    vale = len(data.keys())*19

    return tmes, hour2min, salario, vale

# for i in range(19):
#    inserirdados()

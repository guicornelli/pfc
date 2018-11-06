from horarios import inserirdados, calcmes

resultado = calcmes()
### return tmes, hour2min, salario, vale

media = (resultado[0] / 17)
minred = round((media % 1)*60, 1)
### outlier dia 12/01/2018, equivalente a 3h23 min = 3.3833
#mediaout = (resultado[0] - 3.3833) / 21
#minredout = round((mediaout % 1)*60, 1)

frase1 = "Total de horas trabalhadas no mes foi %dh%dmin"%(resultado[0],resultado[1])
frase2 = "Total a receber sera: R$%.2f + R$%.2f de vale alimentacao"%(resultado[2],resultado[3])
frase3 = "Media de horas trabalhadas por dia: %dh%dmin"%(media, minred)
#frase4 = "Media de horas trabalhadas por dia (descontando outlier): %dh%dmin"%(mediaout, minredout)

with open('C:/Users/guilh/PycharmProjects/17274-COAtlantic/Udacity/Horarios/bddataJun.py', 'a') as arq:
    resultadomes = "\n" + frase1 + "\n" + frase2 + "\n" + frase3
    arq.write(resultadomes)

print("\n" + frase1 + "\n" + frase2 + "\n" + frase3)

#inserirdados()
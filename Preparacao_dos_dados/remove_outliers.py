import numpy as np


def remove_outlier(values, times):                    # define a função com uma variavel de entrada
    fator = 1.5                                       # 1.5 é o fator de multiplicacao
    q75, q25 = np.percentile(values, [75, 25])        # retorna o terceiro e primeiro quartil
    iqr = q75 - q25                                   # calcula o iqr(interquartile range)

    lowpass = q25 - (iqr * fator)                     # calcula o valor minimo para aplicar no filtro
    highpass = q75 + (iqr * fator)                    # calcula o valor maximo para aplicar no filtro

    outliers = np.argwhere(values < lowpass)          # descobre onde estao os valores menores que o valor minimo
    values = np.delete(values, outliers)              # deleta esses valores
    times = np.delete(times, outliers)

    outliers = np.argwhere(values > highpass)         # descobre onde estao os valores maiores que o valor maximo
    values = np.delete(values, outliers)              # deleta esses valores
    times = np.delete(times, outliers)

    return values, times, q75, q25                    # retorna a variavel sem outliers

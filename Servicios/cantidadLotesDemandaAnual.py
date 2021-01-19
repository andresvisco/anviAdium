import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def DivisionTemp(x):
    print(x['11'], x['2'])
    return x['11']/x['2']


def CalcularCantidadLotesDemandaAnual(Datos):
    if len(Datos.columns.values.tolist()) == 15:
        dfValores = Datos[Datos['CantidadLotesDemandaAnual'] >= 70]
    else:
        dfValores = Datos[Datos['16'] >= 70]
    pd.set_option('mode.chained_assignment', None)
    dfValores['DemandaAnual'] = dfValores.apply(DivisionTemp, axis=1).sum()
    sumaDemandaRetorno = dfValores['DemandaAnual'].head(1).iat[0]
    return sumaDemandaRetorno

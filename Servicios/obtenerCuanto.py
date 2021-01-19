# - *- coding: utf- 8 - *-
import pandas as pd
from listaColumnas import ObtenerColumnas
from listaColumnas import ObtenerColumnasCuanto
import sys
import numpy as np
import math
from datetime import datetime
from datetime import timedelta


mesFrom="QUIEBRA: 202001 - Estimar:  Mes antes"
cuando = "QUIEBRA: 201912 Producir: 201907 - Ya Cubierto: 4.0 - FaltaCubrir: 12"
def CuandoProducir(Quiebre):
    cuando = Quiebre[26:32]
    return cuando

def ObtenerCantidadLotes(Cuanto, TamanoLote):
    lotes = 0
    if(isinstance(Cuanto, (int, float)) and isinstance(TamanoLote,(int, float))):
        Cuanto = float(Cuanto)
        TamanoLote = float(TamanoLote)
    else:
        Cuanto = 1
        TamanoLote = 1
    if(Cuanto != 0):
        lotes = (Cuanto / TamanoLote)
    return lotes
"""
Cálculo de Máximo a producir

Obetener Quiebre por codigo
Definir el cuando producir para cada producto en función del quiebre y los demas valores
Obtener menor cuando producir de la molecula
Calcular el máximo para los productos del cuando producir consolidando hasta conseguir uun cierre de lote
Recalcular el cuando producir para el siguiente lote

"""
def ObtenerCuantoProducir(mesFrom, minima, porcentajeAjuste, multiplicador, codProd):
    if(porcentajeAjuste != '' and porcentajeAjuste != None):
        porcentajeAjusteDecimal, frac = math.modf(porcentajeAjuste)
    else:
        porcentajeAjusteDecimal = 1

    if(minima==''):
        minima=0
    else:
        minima = minima
    dataFrameMesesCuanto = pd.DataFrame(mesFrom)
    dataFrameMesesCuanto.reset_index(inplace=True)
    dataFrameMesesCuanto.columns=["CODIGOMES","TotalMes"]
    if not dataFrameMesesCuanto.empty:
        valorDFTem = dataFrameMesesCuanto[['TotalMes']].values[0][0] * porcentajeAjusteDecimal
    else:
        valorDFTem = "-"

    dataFrameMesesCuanto.at[0,'TotalMes']=valorDFTem
    dataFrameSuma = dataFrameMesesCuanto['TotalMes'].sum()
    if(type(dataFrameSuma)!=str):
        if(dataFrameSuma >= minima):
            if(isinstance(multiplicador,(int,float)) and isinstance(dataFrameSuma,(int, float))):
                multiplicador = float(multiplicador)
                dataFrameSuma = float(dataFrameSuma)
            else:
                multiplicador = 1
                dataFrameSuma = 1

            return(dataFrameSuma * multiplicador)

        else:
            return(0)
    else:
        return(0)

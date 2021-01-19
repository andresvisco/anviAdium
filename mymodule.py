# - *- coding: utf- 8 - *-
import xlwings
from xlwings import Range
from cargarExcel import cargarExcelDataframe
import math
import logginProcess
import urllib.request
from urllib.error import HTTPError, URLError
import json
import pandas as pd

URL_SERVICIO_WEB = 'http://viscoandres.pythonanywhere.com/' #?tipo='
# URL_SERVICIO = 'http://127.0.0.1:5000/?tipo='
# URL_SERVICIO = 'http://0.0.0.0:5003/?tipo='

# URL_SERVICIO = 'http://localhost:5003/?tipo='

def calcularPorcentajeLote(dfCuantoPLanificar, dfTamanoLote):
    valorPorcentaje = dfCuantoPLanificar / dfTamanoLote
    return valorPorcentaje


def flagRevisar(x):
    flag = 0
    frac, entero = math.modf(x)
    if (entero >= 1.01) and ((frac >= 0.4) and (frac <= 0.89)):
        flag = 1
    else:
        flag = 0
    return flag


def ValidarRevision(dfRevision):
    dfRevision.loc[:,'PorcentajeLoteAnterior'] = dfRevision.apply(
        lambda x: calcularPorcentajeLote(
            x['CuantoPlanificarNuevo'],
            x['TamanoLote']
            ),
        axis=1)
    dfRevision.loc[:, 'FlagRevisar'] = dfRevision.apply(
        lambda x: flagRevisar(
            x['PorcentajeLoteAnterior']
            ),
        axis=1)

    dfReturnFlag = dfRevision[dfRevision['FlagRevisar'] != 0]
    return dfReturnFlag


def EjecutarMotorDeSugerenciasRevision(gElaboracion):
    gElaboracion = str(gElaboracion).strip('][').split(', ')
    if len(gElaboracion) > 0:
        gElaboracion = gElaboracion
    else:
        gElaboracion = gElaboracion[0]

    costoTotal = 0
    # gElaboracionList = gElaboracion if isinstance(gElaboracion,int) else str(gElaboracion)
    # gElaboracionList = gElaboracion.split(",")
    logginProcess.logger.info("GElaboracion: {} Typo {} ".format(
        gElaboracion,
        type(gElaboracion))
        
    )

    dfCarga, fechaInicioPlan = cargarExcelDataframe(gElaboracion)

    columnas = dfCarga.columns.tolist()
    dfCargaJson = dfCarga.values.tolist()
    datosTotal = []
    datosTotal.append(columnas)
    datosTotal.append(dfCargaJson)
    tipo = 'REVISION'

    jsondata = json.dumps(datosTotal)
    # req = urllib.request.Request('http://127.0.0.1:5000')
    URL_SERVICIO = URL_SERVICIO_WEB + '?fechaInicio={}tipo={}'.format(fechaInicioPlan, tipo)
    req = urllib.request.Request(str(URL_SERVICIO))
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondataBytes = jsondata.encode('utf-8')
    req.add_header('Content-Length', len(jsondataBytes))
    response = urllib.request.urlopen(req, jsondataBytes)
    dfProcesoTemp = response.read()
    from io import StringIO
    s = str(dfProcesoTemp, 'utf-8')
    # data = StringIO(s)
    # # print(data.read())
    # # return(str(data))
    # dfProceso = pd.read_json(data)
    # logginProcess.logger.info("dfReturn: {} Typo {} ".format(
    #     dfProceso,
    #     type(dfProceso))
        
    # )
    # dfResult = EjecutarRevision(dfCarga)
    # dfResultMaximos = mainProcesoRevision(dfCarga)
    Range('A3').value = "Columna"
    Range('B3').value = "Suma Nulos"
    Range('A5').value = s
    Range('D3').value = "Grupo de Elaboracion"
    Range('D5').value = str(gElaboracion)
    Range('E1').value = s



def EjecutarMotorDeSugerencias(gElaboracion):
    # exit()
    gElaboracion = str(gElaboracion).strip('][').split(', ')
    if len(gElaboracion) > 0:
        gElaboracion = gElaboracion
    else:
        gElaboracion = gElaboracion[0]
    

    logginProcess.logger.info("GElaboracion: {} Typo {} ".format(
        gElaboracion,
        type(gElaboracion))
        
    )

    dfCarga, fechaInicioPlan = cargarExcelDataframe(gElaboracion)
    tipo = 'SUGERENCIAS'
    URL_SERVICIO = URL_SERVICIO_WEB + '?fechaInicio={}&tipo={}'.format(fechaInicioPlan, tipo)
    logginProcess.logger.info("dfCarga: {} Typo {} ".format(
        dfCarga,
        type(dfCarga))
        
    )
    logginProcess.logger.info(
        "URLServicio: {} ".format(URL_SERVICIO)
    )
    logginProcess.logger.info(
        "FechaInicioPlan: {} ".format(fechaInicioPlan)
    )

    # import sys
    # sys.exit()
    
    ######## VERISION COMENTADA SERVICIOS
    columnas = dfCarga.columns.tolist()
    dfCargaJson = dfCarga.values.tolist()
    datosTotal = []
    datosTotal.append(columnas)
    datosTotal.append(dfCargaJson)
    jsondata = json.dumps(datosTotal)
    # req = urllib.request.Request('http://127.0.0.1:5000')
    req = urllib.request.Request(str(URL_SERVICIO))
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondataBytes = jsondata.encode('utf-8')
    req.add_header('Content-Length', len(jsondataBytes))
    logginProcess.logger.info(
        "datos: {}".format(
            str(str(jsondataBytes) + " - " + str(req.data))
            )
        )
    response = urllib.request.urlopen(req, jsondataBytes)
    dfProcesoTemp = response.read()
    logginProcess.logger.info(
        "resp: {}".format(
            str(dfProcesoTemp)
            )
        )
    from io import StringIO
    s = str(dfProcesoTemp, 'utf-8')
    data = StringIO(s)
    # print(data.read())
    # return(str(data))
    dfProceso = pd.read_json(data)
    logginProcess.logger.info("dfReturn: {} Typo {} ".format(
            dfProceso,
            type(dfProceso))
            
        )
        
    # dfProceso.reset_index(inplace=True)
    # dfProceso.index.rename('CodigoProductoExp', inplace=True)
    dfProceso.set_index('CodigoProductoExp', inplace=True)
    columnasDf = dfProceso.columns.tolist()
    columnasDf[6] = 'TamanoLoteTotal'
    dfProceso.columns = columnasDf
    dfProceso['PorcentajeLote'] = dfProceso.Dist / dfProceso.TamanoLoteTotal
    
    dfGroupFinal = dfProceso.groupby(dfProceso['GrupoElaboracion'])
    listaDFReturn = []
    listaCompiladaDfReturn = []

    ####### FIN VERSION SERVICIOS

    # logginProcess.logger.info("DFCarga : {}".format(str(dfCarga)))
    # dfProceso = mainProceso(dfCarga, 0)
    columnasDf = dfProceso.columns.to_list()
    columnasDf[6] = 'TamanoLoteTotal'
    dfProceso.columns = columnasDf
    dfProceso['PorcentajeLote'] = dfProceso.Dist / dfProceso.TamanoLoteTotal
    wbSug = xlwings.Book.caller()
    sheetSug = wbSug.sheets('Sugerencias')

    if isinstance(dfProceso, str):
        dfProceso = ""
        dfProceso = "Recomendamos verificar los tamaños de lote y las cantidades en el forecast, ya que la suma de todos los maximos tratados no llegan a un entero del minimo lote"
        Range('A4').value =dfProceso
    else:
        Range('A5').value = dfProceso

    

if __name__ == '__main__':
#     # gElaboracion="[ANASTR]"
    gElaboracion="[PARACE2]"
#     # archivo = 'BP_190306_FAPASA_V01.xlsb'
    archivo = 'motor_ultimo (1).xlsb'
    # archivo = 'BP_190306_FAPASA_V01 - copia (2).xlsb'

#     # Expects the Excel file next to this source file, adjust accordingly.
    xlwings.Book(archivo).set_mock_caller()
    EjecutarMotorDeSugerencias(gElaboracion)
#     EjecutarMotorDeSugerenciasRevision(gElaboracion)

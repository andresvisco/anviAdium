# - *- coding: utf- 8 - *-
import pandas as pd
import xlwings as xw
from listaColumnas import ObtenerColumnas
from logginProcess import logger
# CARGO VARIABLES DE EJECU.
varCodigoElaboracion = 650165
gElaboracion = None


def lastRow(idx, workbook, col=1):
    """ Find the last row in the worksheet that contains data.
    idx: Specifies the worksheet to select. Starts counting from zero.
    workbook: Specifies the workbook
    col: The column in which to look for the last cell containing data.
    """
    ws = workbook.sheets[idx]
    # lower right cell
    lwr_r_cell = ws.cells.last_cell
    # row of the lower right cell
    lwr_row = lwr_r_cell.row
    # change to your specified column
    lwr_cell = ws.range((lwr_row, col))
    if lwr_cell.value is None:
        # go up untill you hit a non-empty cell
        lwr_cell = lwr_cell.end('up')
    return lwr_cell.row


# FUNCION DE CARGA DEL EXCEL Y SEGMENTADO DE RANGO DE CELDAS
# archivoExcel):
def cargarExcelDataframe(gElaboracion):
    book = xw.Book.caller()
    sheet = book.sheets('referencias (2)')
    DESTINO = sheet.used_range.current_region.shape[0]
    dfPrimeraParte = sheet.range(('A2:FP'+str(DESTINO)+'')).value
    dfSegundaParte = sheet.range(('FR2:GO'+str(DESTINO)+'')).value
    fechaInicioPlan = sheet.range(('ER1:ER2')).value[0].strftime("%Y%m")
    dfTerceraParte = sheet.range(('GP2:HM'+str(DESTINO)+'')).value
    dfCuartaParte = sheet.range(('HN2:RZ'+str(DESTINO)+'')).value
    # RESETO LOS INDICES QUE OBTENGO DEL RANGO DE COLUMNAS PARA TENER 2
    # DATAFRAMES IGUALES
    # PREVIAMENTE FUE PARTICIONADA LA SELECCION DE RANGOS PARA HACER
    # MAS EFICIENTE EL MODELO
    pdDataFramePrimera = pd.DataFrame(dfPrimeraParte)
    pdDataFramePrimera = pdDataFramePrimera.reset_index(drop=True)
    pdDataFrameSegunda = pd.DataFrame(dfSegundaParte)
    pdDataFrameSegunda = pdDataFrameSegunda.reset_index(drop=True)
    pdDataFrameTercera = pd.DataFrame(dfTerceraParte)
    pdDataFrameTercera = pdDataFrameTercera.reset_index(drop=True)
    pdDataFrameCuarta = pd.DataFrame(dfCuartaParte)
    pdDataFrameCuarta = pdDataFrameCuarta.reset_index(drop=True)

    dictColumnasPrimera = []
    dictColumnasTercera = []
    dictColumnasCuarta = []
    contadorPrimera = 0
    contadorTercera = 0
    contadorCuarta = 0
    for col in pdDataFrameCuarta.columns:
        nomreColumna = str(contadorCuarta)
        dictColumnasCuarta.append("AJUSTES" + str(nomreColumna))
        contadorCuarta += 1
    pdDataFrameCuarta.columns = dictColumnasCuarta
    pdDataFrameCuarta = pdDataFrameCuarta[
        [
            'AJUSTES0',
            'AJUSTES34',
            'AJUSTES68',
            'AJUSTES102',
            'AJUSTES136',
            'AJUSTES170',
            'AJUSTES204',
            'AJUSTES238',
            'AJUSTES272'
            ]
        ]
    columnasAjuste = [
        '02',
        '03',
        '04',
        '05',
        '06',
        '07',
        '08',
        '09',
        '10'
        ]
    pdDataFrameCuarta.columns = columnasAjuste

    for col in pdDataFrameTercera.columns:
        nombreColumna = str(contadorTercera)
        dictColumnasTercera.append(str(nombreColumna))
        contadorTercera = contadorTercera+1
    pdDataFrameTercera.columns = dictColumnasTercera
    # RENOMBRO LAS COLUMNAS
    for col in pdDataFramePrimera.columns:
        nombreColumna = "A"+str(contadorPrimera)
        dictColumnasPrimera.append(str(nombreColumna))
        contadorPrimera = contadorPrimera+1
    pdDataFramePrimera.columns = dictColumnasPrimera
    pdDataFrameSegunda.columns = ObtenerColumnas(fechaInicioPlan)
    # ESCRIBO LOS DATAFRAME PARCIALES
    # pdDataFramePrimera.to_excel("excelVersionDF1.xlsx",sheet_name="Prueba")
    # pdDataFrameSegunda.to_excel("excelVersionDF2.xlsx",sheet_name="Prueba")
    dfUnion = pd.concat(
        [
            pdDataFramePrimera,
            pdDataFrameSegunda,
            pdDataFrameTercera,
            pdDataFrameCuarta
            ],
        axis=1
        )
    # dfUnion[dfUnion.A3==varCodigoElaboracion]
    dfFiltrado = dfUnion
    # dfFiltradoReturn = dfFiltrado[dfFiltrado.A3 == int(gElaboracion)]
    if gElaboracion != "False":
        if type(gElaboracion) is list:
            dfFiltradoReturn = dfFiltrado[dfFiltrado.A3.isin(gElaboracion)]
        else:
            gElaboracion = int(gElaboracion) if isinstance(
                gElaboracion,
                int
                ) else str(gElaboracion)
            dfFiltradoReturn = dfFiltrado[dfFiltrado.A3 == gElaboracion]
    else:
        dfFiltradoReturn = dfFiltrado
    # dfFiltradoReturn = dfFiltrado
    logger.info(
        "dfFiltradoreturn: {} Valor: {} ShapeDF: {}".format(
            type(gElaboracion),
            gElaboracion,
            dfFiltrado.shape
            )
        )
    return(dfFiltradoReturn, fechaInicioPlan)

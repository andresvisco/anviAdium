import warnings
import logginProcess
from cantidadLotesDemandaAnual import CalcularCantidadLotesDemandaAnual
from funcionCosto import calcularCosto, calcularCostoLotes
# from iteracionGrupo import (CalcularMenorCosto, splitColumn,
#                             validarGrupoCantidad_nuevo)
from listaColumnas import (ObtenerColumnas, ObtenerColumnasCuanto,
                           listaColumnasCalculoCosto)
from obtenerColumnasAjuste import ObtenerAjuste, ObtenerColumnasAjuste
from obtenerCuanto import ObtenerCantidadLotes, ObtenerCuantoProducir
from obtenerMes import (ObtenerCuandoProducirMenor, ObtenerMesesFuturos,
                        ObtenerMesesQuiebre, ObtenerMesesQuiebreInt,
                        ObtenerMesesQuiebreMenor)
warnings.simplefilter(action='ignore', category=FutureWarning)
# sys.path.append('C:/Users/DELL/Anaconda3/envs/python35/lib/site-packages/pandas_explode')
# import pandas_explode as explode


# CARGO VARIABLES DE EJEC.
def EjecutarRevision(df):
    dictNulos = df.isnull().sum()
    dictNuevoNulos = {}
    for index, item in enumerate(dictNulos):
        if item > 0:
            columna = str(df.columns.tolist()[index])
            dictNuevoNulos['' + str(columna) + ''] = item
    return dictNuevoNulos


def listaMesesProducir(mesCuando, cuanto):
    if(isinstance(cuanto, str)):
        cuanto = 0
    else:
        cuanto = int(cuanto)
    return ObtenerColumnasCuanto(mesCuando, cuanto)


def listaColumnasCalculoCostoFn():
    return listaColumnasCalculoCosto()


dataframeRoot = ""


# EJECUTO LA FUNCION DE CARGA DE EXCEL Y LO ASIGNO A LA VARIABLE dataFrame -
# PANDAS DATAFRAME
# dataFrame = cargarExcelDataframe(archivoExcel)
def mainProcesoRevision(dataFrame,fechaInicioPlan):
    # dfUsarSortReturnLotes = ""
    # logginProcess.logger.info()
    logginProcess.logger.info("Inicio Proceso")
    # dataframeRoot = dataFrame.copy()

    # INICIO TRY

    try:
        # FUNCION QUE ADMINISTRA LOS NOMBRES DE LAS COLUMNAS A UTILIZAR
        listaMeses = ObtenerColumnas(fechaInicioPlan)
        listaAjustes = ObtenerColumnasAjuste()
        dataFrame.loc[:, 'CantidadLotesDemandaAnual'] = dataFrame.apply(
            lambda x: CalcularCantidadLotesDemandaAnual(
                dataFrame
                ),
            axis=1
            )
        dataFrameFiltradoLinea = dataFrame[dataFrame['A16'] != 40.0]
        dataFrameFiltradoLinea2 = dataFrameFiltradoLinea[
            dataFrameFiltradoLinea['A16'] != 60.0
            ]
        dataFrame = dataFrameFiltradoLinea2.copy()
        dataFrame.loc[:, 'Quiebre'] = dataFrame.apply(
            lambda x: ObtenerMesesQuiebre(
                (x[listaMeses]),
                x["A16"],
                x["12"],
                x["14"],
                x["15"],
                x["19"],
                x["13"],
                x["21"]
                ),
            axis=1
            )
        dataFrame.loc[:, 'QuiebreInt'] = dataFrame.apply(
            lambda x: ObtenerMesesQuiebreInt(
                x['Quiebre']
                ),
            axis=1
            )
        dataFrame.loc[:, 'QuiebreMenor'] = dataFrame.apply(
            lambda x: ObtenerMesesQuiebreMenor(
                dataFrame['QuiebreInt']
                ),
            axis=1
            )
        # PREGUNTA_ Por qué recorres todas las filas? Veo que x no participa
        dataFrame.loc[:, 'CuandoProducir'] = dataFrame.apply(
            lambda x: ObtenerCuandoProducirMenor(
                dataFrame['Quiebre']
                ),
            axis=1
            )
        dataFrame = dataFrame.dropna(subset=['QuiebreInt'])
        dataFrame.loc[:, 'AjustePlan'] = dataFrame.apply(
            lambda x: ObtenerAjuste(
                x['Quiebre'],
                (x[listaAjustes])
                ),
            axis=1
            )
        dataFrame.loc[:, 'MesesFuturos'] = dataFrame.apply(
            lambda x: ObtenerMesesFuturos(
                (x[listaMeses]),
                x["A16"],
                x["12"],
                x["14"],
                x["15"],
                x["19"],
                x["13"],
                x["21"],
                x["QuiebreMenor"]
                ),
            axis=1
            )
        dataFrameFilter = dataFrame[dataFrame['12'] == False]
        if(dataFrameFilter.empty is not True):
            return "Revisar Vida Util de todos los productos que tengan "\
                "un valor numérico"
        # EJECUTO LA FUNCION DE CALCULO DE "CUANTO" ENVIAR A PRODUCIR
        dataFrame.loc[:, 'CuantoPlanificar'] = dataFrame.apply(
            lambda x: ObtenerCuantoProducir(
                (
                    x[listaMesesProducir(
                        x['QuiebreMenor'],
                        x["MesesFuturos"]
                        )]
                    ),
                    x["MesesFuturos"],
                    x['AjustePlan'],
                    x['A4'],
                    x['A0']
                ),
                axis =1
                )
        
        dataFrame.loc[:, 'FormulaCosto'] = dataFrame.apply(lambda x: calcularCosto(x[listaColumnasCalculoCostoFn()]), axis=1)
        dataFrame.loc[:, 'FormulaCostoOptimoEnteroLote'] = dataFrame.apply(lambda x: calcularCostoLotes(x[listaColumnasCalculoCostoFn()],1), axis=1)
        
        # AGRUPAMIENTO POR LINEA DE PRODUCCION Y CUANDO PLANIFICAR
        # dataFrame.to_excel("excelversion1Previa.xlsx", sheet_name="Prueba")
        dataFrameFiltradoLinea = dataFrame[dataFrame['A16']!=40.0]
        dataFrameFiltradoLinea2 = dataFrameFiltradoLinea[dataFrameFiltradoLinea['A16']!=60.0 ]
        # copiaDFRoot = dataFrameFiltradoLinea2.copy()
        dataFrameGroupFilter = dataFrameFiltradoLinea2.loc[dataFrameFiltradoLinea2['CuantoPlanificar']!=0]
    
        dataFrameGroupCopy = dataFrameGroupFilter#dataFrameGroupDF

        dataFrameGroupCopy.loc[:, 'CantidadLotes'] = dataFrameGroupCopy.apply(lambda x: ObtenerCantidadLotes(x['CuantoPlanificar'],x['A5']), axis=1)
        # dataFrameGroupCopy.loc[:,'CuandoProducir'] = dataFrameGroupCopy.apply(lambda x: CuandoProducir(x['Quiebre']), axis=1)
        
        if dataFrameGroupCopy.CantidadLotes.sum() < 1:
            logginProcess.logger.error("SumaLotes : {}".format(dataFrameGroupCopy.CantidadLotes.sum()))
            return "La cantidad de maximos a distribuir no llega a completar un lote minimo"
        else:
            return "Los la suma de los máximos es adecuada para iniciar el proceso"
    except Exception as ex:
        return str(ex)

# - *- coding: utf- 8 - *-
import pandas as pd
import logginProcess
from listaColumnas import ObtenerColumnas
from obtenerMes import ObtenerMesesQuiebre, ObtenerMesesFuturos, ObtenerMesesQuiebreInt, ObtenerMesesQuiebreMenor
from listaColumnas import ObtenerColumnasCuanto
from listaColumnas import listaColumnasCalculoCosto
from obtenerCuanto import ObtenerCuantoProducir,ObtenerCantidadLotes, CuandoProducir
from funcionCosto import calcularCosto, calcularCostoLotes, ObtenerGrupo, ObtenerLotePertenencia
from obtenerColumnasAjuste import ObtenerAjuste
from obtenerColumnasAjuste import ObtenerColumnasAjuste
from cantidadLotesDemandaAnual import CalcularCantidadLotesDemandaAnual
from iteracionGrupo import splitColumn, validarGrupoCantidad_nuevo
from functools import reduce
import re
from iteracionDistribucion import iteracionCodigoProducto
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


#CARGO VARIABLES DE EJEC.
archivoExcel="XLSB/BP_190306_FAPASA_V01.xlsb"#"BPZP-190603_V01.xlsb"

def listaMesesProducir(mesCuando, cuanto):
    if(isinstance(cuanto, str)):
        cuanto = 0
    else:
        cuanto = int(cuanto)

    return ObtenerColumnasCuanto(mesCuando, cuanto)
    
def listaColumnasCalculoCostoFn():
    return listaColumnasCalculoCosto()

dataframeRoot = ""

#EJECUTO LA FUNCION DE CARGA DE EXCEL Y LO ASIGNO A LA VARIABLE dataFrame - PANDAS DATAFRAME
# dataFrame = cargarExcelDataframe(archivoExcel)
def mainProceso(dataFrame, origen, fechaInicioPlan):
    dfUsarSortReturnLotes = ""
    # logginProcess.logger.info()
    logginProcess.logger.info("Inicio Proceso")

    if origen == 1:
        dataFrame = "" # cargarExcelDataframeFile(dataFrame)
    else:
        dataFrame = dataFrame
    dataframeRoot = dataFrame.copy()

    # INICIO TRY

    try:
        listaMeses = ObtenerColumnas(fechaInicioPlan) # FUNCION QUE ADMINISTRA LOS NOMBRES DE LAS COLUMNAS A UTILIZAR
        listaAjustes = ObtenerColumnasAjuste()
        dataFrame.loc[:, 'CantidadLotesDemandaAnual']= dataFrame.apply(lambda x: CalcularCantidadLotesDemandaAnual(dataFrame), axis=1)
        dataFrameFiltradoLinea = dataFrame[dataFrame['A16']!=40.0]
        dataFrameFiltradoLinea2 = dataFrameFiltradoLinea[dataFrameFiltradoLinea['A16']!=60.0 ]
        dataFrame = dataFrameFiltradoLinea2.copy()
        dataFrame.loc[:,'Quiebre'] = dataFrame.apply(
            lambda x: ObtenerMesesQuiebre(
                (
                    x[listaMeses]
                ),
                x["A16"],
                x["12"],
                x["14"],
                x["15"],
                x["19"],
                x["13"],
                x["21"]
            ),
            axis =1
        )
        
        dataFrame.loc[:,'QuiebreInt'] = dataFrame.apply(lambda x: ObtenerMesesQuiebreInt(x['Quiebre']), axis =1)
        
        dataFrame.loc[:,'QuiebreMenor'] = dataFrame.apply(lambda x: ObtenerMesesQuiebreMenor(dataFrame['QuiebreInt']), axis =1) # _PREGUNTA_ Por qué recorres todas las filas? Veo que x no participa
        
        dataFrame.loc[:,'CuandoProducir'] = dataFrame['Quiebre'].str[26:32]
        dataFrame['CuandoProducir'] = dataFrame['CuandoProducir'].replace('Cubier', '')
        dataFrame= dataFrame.dropna(subset=['QuiebreInt'])

        dataFrame.loc[:,'AjustePlan'] = dataFrame.apply(lambda x: ObtenerAjuste(x['Quiebre'],(x[listaAjustes])),axis=1)
        dataFrame.loc[:,'MesesFuturos'] = dataFrame.apply(lambda x: ObtenerMesesFuturos((x[listaMeses]),x["A16"],x["12"],x["14"],x["15"],x["19"],x["13"],x["21"],x["QuiebreMenor"]), axis =1)
        
        # EJECUTO LA FUNCION DE CALCULO DE "CUANTO" ENVIAR A PRODUCIR
        dataFrame.loc[:,'CuantoPlanificar'] = dataFrame.apply(
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
        
        dataFrame.loc[:,'FormulaCosto'] = dataFrame.apply(lambda x: calcularCosto(x[listaColumnasCalculoCostoFn()]), axis=1)
        dataFrame.loc[:,'FormulaCostoOptimoEnteroLote'] = dataFrame.apply(lambda x: calcularCostoLotes(x[listaColumnasCalculoCostoFn()],1), axis=1)
        
        #AGRUPAMIENTO POR LINEA DE PRODUCCION Y CUANDO PLANIFICAR
        # dataFrame.to_excel("excelversion1Previa.xlsx", sheet_name="Prueba")
        dataFrameFiltradoLinea = dataFrame[dataFrame['A16']!=40.0]
        dataFrameFiltradoLinea2 = dataFrameFiltradoLinea[dataFrameFiltradoLinea['A16']!=60.0 ]
        copiaDFRoot = dataFrameFiltradoLinea2.copy()
        dataFrameGroupFilter = dataFrameFiltradoLinea2.loc[dataFrameFiltradoLinea2['CuantoPlanificar']!=0]
    
        dataFrameGroupCopy = dataFrameGroupFilter#dataFrameGroupDF

        dataFrameGroupCopy.loc[:,'CantidadLotes'] = dataFrameGroupCopy.apply(lambda x: ObtenerCantidadLotes(x['CuantoPlanificar'],x['A5']), axis=1)
        
        
        if dataFrameGroupCopy.CantidadLotes.sum() < 1:
            logginProcess.logger.error("SumaLotes : {}".format(dataFrameGroupCopy.CantidadLotes.sum()))

        dataFrameGroupCopyGrouped = dataFrameGroupCopy.groupby(['QuiebreInt','CuandoProducir','QuiebreMenor', 'AjustePlan','A4','A3','A0','A5','12','FormulaCosto','FormulaCostoOptimoEnteroLote','20','CantidadLotesDemandaAnual']).agg({'CantidadLotes':'sum','CuantoPlanificar':'sum'}).reset_index()
        dataFrameIterar = dataFrameGroupCopyGrouped.copy()
        # cantidadLotes = validarGrupoCantidad(dataFrameIterar)
        
        fecha_regex = re.compile('\d{6}')
        cols_mes = [c for c in dataFrame.columns.tolist() if fecha_regex.fullmatch(c)]
        cols_info_extra = ["MesesFuturos",'AjustePlan','A4','A0', "A16", "12", "14", "15", "19", "13", "21"]
        # df_infoExtra = dataFrame[cols_info_extra + cols_mes]
        df_infoExtra = dataFrame
        cantidadLotes1 = validarGrupoCantidad_nuevo(dataFrameIterar, df_infoExtra, fechaInicioPlan)

        # iteracionesLotes = len(cantidadLotes)
        grupoLoteList = []
        # grupoLoteList=[grupoLoteList.append(lote) for lote in cantidadLotes1]
        try:
            for item in cantidadLotes1:
                
                dataframeRootReturn=""
                dataframeRootReturn1=""
                grupoLote= validarGrupoCantidad_nuevo(dataFrameIterar, dataFrameFiltradoLinea2, fechaInicioPlan)
                grupoLoteList.append(grupoLote)

                
                continue
        except Exception as e:
            for item in e.args:
                errorVal = str(item)
                logginProcess.logger.error(errorVal)
        
        single_list = reduce(lambda x,y: x+y, grupoLoteList)
        logginProcess.logger.info(str("Creacion de cantidad Lotes: " + str(single_list)))
        
        grupoLote = cantidadLotes1
        # grupoLote = single_list
        
        # columnas = ['Tamanolote','IdLote','MesesIncluidos','CodigoProducto']
        #columnas = ['IdLote','CodigoProducto','Tamanolote','MesesIncluidos']
        reemplazo_columnas = {
            'SumaLotes': 'Tamanolote',
            'cuandoProducir': 'CuandoProducir',
            'idLote': 'IdLote',
            'listaMeses': 'MesesIncluidos',
            'prodCodigo': 'CodigoProducto'            
        }
        dataFrameLista = pd.DataFrame(grupoLote)
        nuevas_columnas = [reemplazo_columnas[col] for col in dataFrameLista.columns.to_list()]
        dataFrameLista.reset_index()
        
        dataFrameLista.columns = nuevas_columnas
        
        dfNuevoExplotado1 = dataFrameLista.assign(CodigoProductoExploded=dataFrameLista.CodigoProducto.str.split(',')).explode('CodigoProductoExploded').reset_index(drop=False)
        
        dfUsar = dfNuevoExplotado1[['IdLote','CodigoProducto','Tamanolote','MesesIncluidos','CodigoProductoExploded']]
        
        
        dfUsar.loc[:,'CuantoPlanificarNuevo'] = dfUsar.apply(lambda x: splitColumn(x['CodigoProductoExploded'],1) , axis=1)
        dfUsar.loc[:,'CodigoProductoExp'] = dfUsar.apply(lambda x: splitColumn(x['CodigoProductoExploded'],0) , axis=1)
        dfUsar.loc[:,'QuiebreIntExp'] = dfUsar.apply(lambda x: splitColumn(x['CodigoProductoExploded'],2) , axis=1)
        dfUsar.loc[:,'MinimoExp'] = dfUsar.apply(lambda x: splitColumn(x['CodigoProductoExploded'],3) , axis=1)
        dfUsar.loc[:,'CuandoProducir'] = dfUsar.apply(lambda x: splitColumn(x['CodigoProductoExploded'],4) , axis=1)
        dfUsar.loc[:,'TamanoLote'] = dfUsar.apply(lambda x: splitColumn(x['CodigoProductoExploded'],5) , axis=1)
        dfUsar.loc[:,'Presentacion'] = dfUsar.apply(lambda x: splitColumn(x['CodigoProductoExploded'],6) , axis=1)
        dfUsar.loc[:,'GrupoElaboracion'] = dfUsar.apply(lambda x: splitColumn(x['CodigoProductoExploded'],7) , axis=1)
        
        dfUsar = dfUsar[['Tamanolote','IdLote','CodigoProductoExp','CuantoPlanificarNuevo','QuiebreIntExp','MinimoExp','CuandoProducir','TamanoLote','Presentacion','GrupoElaboracion']]
        dfUsar.set_index(["CodigoProductoExp"],inplace = True, append = False, drop = True)
        
        #EJECUTO LA FUNCION DE CALCULO DE "COSTO"
        # dfUsar.to_excel("Fase1Lotes.xlsx",sheet_name="Prueba")
        #EXCEL DE VALIDACION DF
        dfReturn, datosSegmentados = iteracionCodigoProducto(copiaDFRoot, dfUsar)
        dfReturn = dfReturn.values.tolist()
        ListaReturnNueva = []
        for indice, itemReturn in enumerate(dfReturn):
            ListaReturnNueva.append(itemReturn[27:29])
            ListaReturnNueva[indice].insert(2,itemReturn[2:3][0])
        
        dfReturnDF = pd.DataFrame(ListaReturnNueva, columns=['Dist','Costo','Codigos'])
        dfReturn = dfReturnDF
        
        from iteracionDistribucion import NormalizarFila
        dfReturn['Codigos'] = dfReturn.apply(lambda row:NormalizarFila(row['Codigos']), axis=1)
        dfReturn.set_index(['Codigos'], inplace=True,append=False, drop = True)
        dfUsarSort = dfUsar.sort_values('CodigoProductoExp', ascending=True)
        dfReturnSort = dfReturn.sort_values('Codigos', ascending=True)
        dfUsarSort = dfUsarSort.loc[list(dfReturnSort.index)]
        dfUsarSort['Dist'] = dfReturnSort['Dist'].values
        dfUsarSort['Costo'] = dfReturnSort['Costo'].values
        dfUsarSortReturnLotes = dfUsarSort.sort_values('IdLote', ascending=True)
        logginProcess.logger.info("Proceso completado")
        return(dfUsarSortReturnLotes)

    except Exception as e:# UnAcceptedValueError as error:
        for item in e.args:
            errorVal = str(item)
            logginProcess.logger.error(errorVal)
        return("")
            
            

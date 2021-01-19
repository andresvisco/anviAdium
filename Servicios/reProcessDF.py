# - *- coding: utf- 8 - *-
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import xlwings as xw
import sys
import numpy as np
from listaColumnas import ObtenerColumnas
from obtenerMes import ObtenerMesesQuiebre, ObtenerMesesFuturos, ObtenerMesesQuiebreInt, ObtenerMesesQuiebreMenor, ObtenerCuandoProducirMenor
from listaColumnas import ObtenerColumnasCuanto
from listaColumnas import listaColumnasCalculoCosto
from obtenerCuanto import ObtenerCuantoProducir,ObtenerCantidadLotes, CuandoProducir
from funcionCosto import calcularCosto, calcularCostoLotes, ObtenerGrupo, ObtenerLotePertenencia
from obtenerColumnasAjuste import ObtenerAjuste
from obtenerColumnasAjuste import ObtenerColumnasAjuste
from cantidadLotesDemandaAnual import CalcularCantidadLotesDemandaAnual


#CARGO VARIABLES DE EJEC.

def explode(df, lst_cols, fill_value='', preserve_index=False):
    # make sure `lst_cols` is list-alike
    if (lst_cols is not None
        and len(lst_cols) > 0
        and not isinstance(lst_cols, (list, tuple, np.ndarray, pd.Series))):
        lst_cols = [lst_cols]
    # all columns except `lst_cols`
    idx_cols = df.columns.difference(lst_cols)
    # calculate lengths of lists
    lens = df[lst_cols[0]].str.len()
    # preserve original index values    
    idx = np.repeat(df.index.values, lens)
    # create "exploded" DF
    res = (pd.DataFrame({
                col:np.repeat(df[col].values, lens)
                for col in idx_cols},
                index=idx)
             .assign(**{col:np.concatenate(df.loc[lens>0, col].values)
                            for col in lst_cols}))
    # append those rows that have empty lists
    if (lens == 0).any():
        # at least one list in cells is empty
        res = (res.append(df.loc[lens==0, idx_cols], sort=False)
                  .fillna(fill_value))
    # revert the original index order
    res = res.sort_index()
    # reset index if requested
    if not preserve_index:        
        res = res.reset_index(drop=True)
    return res

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
def mainProcesoReProcess(dataFrame):
    

    
    dataframeRoot = dataFrame.copy()

    listaMeses =ObtenerColumnas()#FUNCION QUE ADMINISTRA LOS NOMBRES DE LAS COLUMNAS A UTILIZAR
    listaAjustes = ObtenerColumnasAjuste()
    dataFrame.loc[:, 'CantidadLotesDemandaAnual']= dataFrame.apply(lambda x: CalcularCantidadLotesDemandaAnual(dataFrame), axis=1)
    dataFrame.loc[:,'Quiebre'] = dataFrame.apply(lambda x: ObtenerMesesQuiebre((x[listaMeses]),x["A16"],x["12"],x["14"],x["15"],x["19"],x["13"],x["21"]), axis =1)

    dataFrame.loc[:,'QuiebreInt'] = dataFrame.apply(lambda x: ObtenerMesesQuiebreInt(x['Quiebre']), axis =1)
    
    dataFrame.loc[:,'QuiebreMenor'] = dataFrame.apply(lambda x: ObtenerMesesQuiebreMenor(dataFrame['QuiebreInt']), axis =1)
    dataFrame.loc[:,'CuandoProducir'] = dataFrame.apply(lambda x: ObtenerCuandoProducirMenor(dataFrame['Quiebre']), axis =1)
    dataFrame= dataFrame.dropna(subset=['QuiebreInt'])

    dataFrame.loc[:,'AjustePlan'] = dataFrame.apply(lambda x: ObtenerAjuste(x['Quiebre'],(x[listaAjustes])),axis=1)
    dataFrame.loc[:,'MesesFuturos'] = dataFrame.apply(lambda x: ObtenerMesesFuturos((x[listaMeses]),x["A16"],x["12"],x["14"],x["15"],x["19"],x["13"],x["21"],x["QuiebreMenor"]), axis =1)
    
    #EJECUTO LA FUNCION DE CALCULO DE "CUANTO" ENVIAR A PRODUCIR
    dataFrame.loc[:,'CuantoPlanificar'] = dataFrame.apply(lambda x: ObtenerCuantoProducir((x[listaMesesProducir(x['QuiebreMenor'],x["MesesFuturos"])]),x["MesesFuturos"], x['AjustePlan'], x['A4'], x['A0']), axis =1)
    
    dataFrame.loc[:,'FormulaCosto'] = dataFrame.apply(lambda x: calcularCosto(x[listaColumnasCalculoCostoFn()]), axis=1)
    dataFrame.loc[:,'FormulaCostoOptimoEnteroLote'] = dataFrame.apply(lambda x: calcularCostoLotes(x[listaColumnasCalculoCostoFn()],1), axis=1)
    
    #AGRUPAMIENTO POR LINEA DE PRODUCCION Y CUANDO PLANIFICAR
    # dataFrame.to_excel("excelversion1Previa.xlsx", sheet_name="Prueba")
    dataFrameFiltradoLinea = dataFrame[dataFrame['A16']!=40.0]
    dataFrameFiltradoLinea2 = dataFrameFiltradoLinea[dataFrameFiltradoLinea['A16']!=60.0 ]
    
    dataFrameGroupFilter = dataFrameFiltradoLinea2.loc[dataFrameFiltradoLinea2['CuantoPlanificar']!=0]

    # dataFrameGroup = dataFrameGroupFilter.groupby(['QuiebreInt','A3','A5'])['CuantoPlanificar'].agg('sum')

    # dataFrameGroupDF = dataFrameGroup.to_frame()


    dataFrameGroupCopy = dataFrameGroupFilter#dataFrameGroupDF

    dataFrameGroupCopy.loc[:,'CantidadLotes'] = dataFrameGroupCopy.apply(lambda x: ObtenerCantidadLotes(x['CuantoPlanificar'],x['A5']), axis=1)
    # dataFrameGroupCopy.loc[:,'CuandoProducir'] = dataFrameGroupCopy.apply(lambda x: CuandoProducir(x['Quiebre']), axis=1)
    
    dataFrameGroupCopyGrouped = dataFrameGroupCopy.groupby(['QuiebreInt','CuandoProducir','QuiebreMenor', 'AjustePlan','A4','A3','A0','A5','12','FormulaCosto','FormulaCostoOptimoEnteroLote','20','CantidadLotesDemandaAnual']).agg({'CantidadLotes':'sum','CuantoPlanificar':'sum'}).reset_index()
    dataFrameIterar = dataFrameGroupCopyGrouped.copy()
    return dataFrameGroupFilter
    # grupoLote = validarGrupo(dataFrameIterar, dataframeRoot)
    
    # dataFrameLista = pd.DataFrame(grupoLote)
    # dataFrameLista.reset_index()
    # columnas = ['Tamanolote','IdLote','MesesIncluidos','CodigoProducto']
    # dataFrameLista.columns=columnas
    # dfUsar = dataFrameLista[['Tamanolote','IdLote','MesesIncluidos','CodigoProducto']]
    
    # # dfUsar.explode('MesesIncluidos')
    # # dfUsar.loc[:,'Explotado'] = dfUsar.apply(lambda x: explotarMeses(x['MesesIncluidos']), axis=1)
    # # dfExplodedUsar = explode(dfUsar,'CodigoProducto','-',preserve_index=True)
    # dfNuevoExplotado = dfUsar.assign(CodigoProductoExploded=dfUsar.CodigoProducto.str.split(',')).explode('CodigoProductoExploded').reset_index(drop=False)
    
    # dfNuevoExplotado.loc[:,'CuantoPlanificarNuevo'] = dfNuevoExplotado.apply(lambda x: splitColumn(x['CodigoProductoExploded'],1) , axis=1)
    # dfNuevoExplotado.loc[:,'CodigoProductoExp'] = dfNuevoExplotado.apply(lambda x: splitColumn(x['CodigoProductoExploded'],0) , axis=1)
    # dfNuevoExplotado.loc[:,'QuiebreIntExp'] = dfNuevoExplotado.apply(lambda x: splitColumn(x['CodigoProductoExploded'],2) , axis=1)
    # dfNuevoExplotado.loc[:,'MinimoExp'] = dfNuevoExplotado.apply(lambda x: splitColumn(x['CodigoProductoExploded'],3) , axis=1)
    
    # dfNuevoExplotado = dfNuevoExplotado[['Tamanolote','IdLote','CodigoProductoExp','CuantoPlanificarNuevo','QuiebreIntExp','MinimoExp']]
    # dfNuevoExplotado.set_index(["CodigoProductoExp"],inplace = True, append = False, drop = True)
    # dfIterarCosto = CalcularMenorCosto(dataFrameGroupFilter, dfNuevoExplotado)
    # # dfNuevoExplotado.reset_index()
    # # print(dfNuevoExplotado)
    # # dfNuevo = pd.DataFrame(dataFrameLista['Tamanolote','IdLote',dataFrameLista.MesesIncluidos.str.split(',').tolist(),'CodigoProducto']).stack()
    # # dataFrameLista.reset_index()
    # # dataFrameLista.columns=columnas

    # # dfNuevoExplotado.to_excel("ListaLotes.xlsx",sheet_name="Prueba")
    # # dataFrameGroupCopyGrouped.to_excel("AgrupadosPrueba.xlsx",sheet_name="Prueba")
    # # # dataFrameIterar['GrupoLote'] = dataFrameIterar.apply(lambda x: validarGrupo(dataFrameIterar), axis=1)
    
    # # bins = pd.cut(dataFrameGroupCopyGrouped['QuiebreInt'], [0, 100, 250, 1500])
    # # dataFrameGroupCopyGrouped.rename(columns={'QuiebreInt':'Quiebre','A3':'LineaProducto','A5':'TLote','CuantoPlanificar':'CuantoPlanificar','CantidadLotes':'CantidadLotes'},inplace=True)
    # # dataFrameGroupCopyGrouped.loc[:,'LoteDePertenencia'] = dataFrameGroupCopyGrouped.apply(lambda x: ObtenerLotePertenencia(dataFrameGroupCopyGrouped) , axis=1)
    # # dataFrameGroupCopyGrouped.to_excel("excelFiltradoGroup.xlsx",sheet_name="PruebaFiltro")
    

    # #EJECUTO LA FUNCION DE CALCULO DE "COSTO"
    # dfIterarCosto.to_excel("Fase1Lotes.xlsx",sheet_name="Prueba")
    # #EXCEL DE VALIDACION DF
    # return dfIterarCosto#dataFrameIterar
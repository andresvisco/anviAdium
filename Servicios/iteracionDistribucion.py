import pandas as pd
from listaColumnas import listaCalculoCosto
from funcionCosto import calcularCosto, calcularCostoLotes, ObtenerGrupo, ObtenerLotePertenencia, calcularCostoFB
import math
import numpy as np
from pesos import InicioDistribucion
def NormalizarFila(valor):
    valorReturn = int(float(valor))

    return valorReturn

def ejecutarFB(df):
    
    varCostoMinimo = 0.0
    varTamano = 0.0

    minimo = df['20']
    
    if (math.isnan(df['CuantoPlanificarNuevo'])):
        maximo = df['CuantoPlanificar']
    else:
        maximo = df['CuantoPlanificarNuevo']
    
    for x in range(int(round(minimo,0)), int(round(maximo,0)), 100):
        CostoIter = calcularCostoFB(df, x)
        if (varCostoMinimo == 0):
            varCostoMinimo = CostoIter
            varTamano = x
        else:
            if CostoIter < varCostoMinimo:
                varCostoMinimo = CostoIter
                varTamano = x
            else:
                pass
    
    
    
    return varCostoMinimo, varTamano

def iteracionCodigoProducto(dfroot, dfGrupo):
    dfGrupo.reset_index()
    dfroot['A0'] = dfroot.apply(lambda row:NormalizarFila(row['A0']), axis=1)
    list_of_df = [g for _, g in dfGrupo.groupby(['IdLote'])]
    data=[]
    list_of_dfProcesados = []
    listaMerge = []
    dfProcesadosLst = []
    costoAlmacenado = []
    distribucionAlmacenada = []
    listaCodigos=[]
    quiebresList = []
    lotesListTamano=[]
    listCuando = []
    listMinimo = []
    listPresentacion=[]
    dfDictEmpty = pd.DataFrame()
    returnDatos=False
    dfEscalarEmpty=pd.DataFrame()
    dfDatosSegmentados = pd.DataFrame()
    for df in list_of_df:
        dfCompleto = dfroot[listaCalculoCosto]
        dfCompleto.reset_index(inplace=True)
        df.reset_index(inplace=True)
        

        listaColumnasFiltro = df['CodigoProductoExp'].tolist()
        listaColumnasFiltro = list(map(int, listaColumnasFiltro))
        dfCompletoNuevoIterador = dfCompleto[dfCompleto.A0.isin(listaColumnasFiltro)]
        # dfCompletoNuevoIterador['CuantoPlanificarNuevo'] = df['CuantoPlanificarNuevo']
        
        dfCompletoReset = dfCompletoNuevoIterador.sort_values('A0', ascending=True)
        dfCompletoReset.reset_index(inplace=True)
        dfReset = df.sort_values('CodigoProductoExp', ascending=True)
        dfReset.reset_index(inplace=True)
        columnasDfReset = ['CodigoProductoExp','Tamanolote','IdLote','CuantoPlanificarNuevo','QuiebreIntExp','MinimoExp','CuandoProducir','Presentacion']

        dfResetSelect=dfReset[columnasDfReset]
        dfCompilado = dfCompletoReset.join(dfResetSelect)
        dfCompiladoSort = dfCompilado.sort_values('A0', ascending=True)
        dfProcesadosLst.append(dfCompiladoSort)
        ############FUERZA BRUTA
        listaNodos=[]
        Nodo1PorDistribuir = 0
        resto = 0
        # for index, row in dfCompilado.iterrows():
        #     TLPT = row['A5']
        #     reiniciar = False
        #     minimo = int(round(row['20'],0))
        #     maximo = int(round(row['CuantoPlanificarNuevo'],0))
        # Distribucion, costoAlmacenadoReturn, codigosList, dfDictNuevo = InicioDistribucion(dfCompiladoSort)
        
        dfDictNuevoDf, DistriIter = InicioDistribucion(dfCompiladoSort)
        from datetime import datetime
        if(len(DistriIter)!=0):
            returnDatos=True
            now=datetime.now()
            nowStr = str(now.strftime("%H:%M:%S")).replace(":","")
            dfDatosSegmentados = pd.DataFrame(DistriIter)
            # list_of_dfProcesados.append(dfDatosSegmentados)

            # dfDatosSegmentados.to_excel("debugLotesEscalar"+nowStr+".xlsx", sheet_name="Prueba")
        dfDictNuevo = pd.DataFrame(dfDictNuevoDf)
        
        
        
        
        # tamanoHead = int(len(dfCompiladoSort))
        # dfDictNuevoSorted = dfDictNuevo.sort_values('CostoSum', ascending=True).head(tamanoHead)
        dfDictEmpty = dfDictEmpty.append(dfDictNuevo)
    

    # dfProcesar = pd.DataFrame(list_of_dfProcesados)
    
    if(dfDatosSegmentados.empty):
        dfDatosSegmentados = pd.DataFrame()
    return(dfDictEmpty,dfDatosSegmentados)
    
    
    
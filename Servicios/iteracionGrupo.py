import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from fechas import fechaFormatear, incrementarMesFecha
import math
from numpy import arange
import numpy as np
from itertools import combinations
from obtenerMes import ObtenerMesesFuturos
from obtenerCuanto import ObtenerCuantoProducir, ObtenerCantidadLotes
from listaColumnas import ObtenerColumnas, ObtenerColumnasCuanto
from lotesScipy import distribucionSciPyNueva
from datetime import datetime
# from fromExcel import listaMesesProducir

def close_to_any(a, floats, **kwargs):
    return np.any(np.isclose(a, floats, **kwargs))


def CheckForLess(list1, val):  
    resultado = False
    for x in list1:
        if(val <= x):
            resultado = True    
        else:
            resultado = False
    return resultado
    

def CalculoIterar(dataframe):
    menorCosto = []
    for index, item in dataframe.iterrows():
        maximo = int(item['CuantoPlanificarNuevo'])
        minimo = float(item['MinimoExp'])
        calculo = (maximo / 30) * (minimo * 3)
        menorCosto.append(calculo)
    menorValor = sorted(menorCosto)[0]

    return menorValor
    

def CalcularMenorCosto(dataFrame, dataFrameLotes):
    varDFOriginal = dataFrame
    varDFLotes = dataFrameLotes
    grupos = varDFLotes.groupby(['IdLote'])['IdLote'].mean().to_frame().values.tolist()
    varDFLotes['MenorCosto']=0.0
    for item in grupos:
        menorCosto = ""
        dfFiltradoReturn = varDFLotes[varDFLotes.IdLote == int(item[0])]
        menorCosto = CalculoIterar(dfFiltradoReturn)
        varDFLotes.loc[varDFLotes['IdLote']==int(item[0]), ['MenorCosto']]=float(menorCosto)
        
        

        # dataFrameLotes.ix[dataFrameLotes.IdLote==int(item[0]), ['MenorCosto']] = float(menorCosto)
        print(varDFLotes)
        
    return varDFLotes


def splitColumn(valor, posicion):
    if posicion == 0:
        valorRetorno = str(str(valor).replace("{","").replace("}","").replace("'","").split("-")[0])[0:-2]
        valorRetorno = int(float(valorRetorno))
    elif posicion == 1:
        valorRetornoInt = str(valor).replace("{","").replace("}","").replace("'","").split("-")[1]
        valorRetorno = float(str(valorRetornoInt))
    elif posicion == 2:
        valorRetorno = str(valor).replace("{","").replace("}","").replace("'","").split("-")[2]
    elif posicion == 3:
        valorRetorno = str(valor).replace("{","").replace("}","").replace("'","").split("-")[3]
    elif posicion == 4:
        valorRetorno = str(valor).replace("{","").replace("}","").replace("'","").split("-")[4]
    elif posicion == 5:
        valorRetorno = str(valor).replace("{","").replace("}","").replace("'","").split("-")[5]
        valorRetorno = int(float(valorRetorno))
    elif posicion == 6:
        valorRetorno = str(valor).replace("{","").replace("}","").replace("'","").split("-")[6]
        valorRetorno = int(float(valorRetorno))
    elif posicion == 7:
        valorRetorno = str(valor).replace("{","").replace("}","").replace("'","").split("-")[7]
        valorRetorno = int(float(valorRetorno)) if str(valorRetorno).isdecimal() else str(valorRetorno)
    
    return valorRetorno

def explotarMeses(meses):
    mesesParsed = meses.replace("[","").replace("'","").replace(" ","").replace("]","")
    
    return mesesParsed
def IniciarReglaNegocio(VU, DemandaAnual):
    # _PREGUNTA_ Qué hacemos con esta regla de negocio?
    if(VU >= 24):
        if(DemandaAnual >= 12):
            CantidadMeses = 2
            
        else:
            CantidadMeses = 2
    else:
        CantidadMeses = 2
            
    return CantidadMeses

def CalcularMesesLotes(listaMeses, dataFrame):
    filtrado = dataFrame.QuiebreInt.isin(listaMeses)
    dataFrameNuevo = dataFrame[filtrado]
    lotes = round(dataFrameNuevo.CantidadLotes.sum(),2)
    

    return lotes

def CalcularProdCodigo(listaMeses, dataFrame):
    filtrado = dataFrame.QuiebreInt.isin(listaMeses)
    dataFrameNuevo = dataFrame[filtrado]
    itemBack=[]
    prod = dataFrameNuevo[['A0','CuantoPlanificar','QuiebreInt','20','CuandoProducir','A5', 'A4','A3']].values.tolist()
    for item in prod:
        itemBack.append(str(item[0]) + "-"+ str(item[1]) + "-" + str(item[2]) + "-" + str(item[3]) + "-" + str(item[4])+ "-" + str(item[5])+ "-" + str(item[6]) + "-" + str(item[7]))
        
    # prodReturn = str(prod).replace("[[","[").replace("]]","]").replace(",","-")
    # prodReturn = prodReturn.replace(" ","").replace("[","").replace("]","")

    return itemBack #prodReturn

def validarGrupo(dataFrame, dataframeRoot, posicionIDLote):
    dataFrameVidaUtil = dataFrame.sort_values(by='12', ascending=True)
    dataFrameVidaUtilVU = dataFrameVidaUtil['12'].head(1).iat[0]
    dataFrameVidaUtilDemandaAnual = dataFrameVidaUtil['CantidadLotesDemandaAnual'].head(1).iat[0]
    posicion=0
     
    MesesInicial = IniciarReglaNegocio(dataFrameVidaUtilVU, dataFrameVidaUtilDemandaAnual) - 1
    listaLotes=[]
    ultimoMesLoopMain = ""
    listaValores = []
    listaCodigoTerminado = str(dataFrame['A0'].tolist()).replace(".0","")
    ProdTerminadoLista = listaCodigoTerminado.replace("[","").replace("]","").replace(",","").split()
    ProdTerminadoLista = [int(i) for i in ProdTerminadoLista]
    # dataframeRootFilter = dataframeRoot.A0.isin(ProdTerminadoLista)
    # dataframeRootFilterValues = dataframeRoot[dataframeRootFilter]
    dfRootFiltro = dataframeRoot.copy()
    for index, row in dataFrame.iterrows():
        
        indexPosition=int(index)
        listaMesesInicial=[]
        PrimerQuiebre = str(row['QuiebreInt'])
        
        
        if(ultimoMesLoopMain != ""):
            if(int(PrimerQuiebre) < int(ultimoMesLoopMain) ):
                PrimerQuiebre = incrementarMesFecha(fechaFormatear(ultimoMesLoopMain,'%Y%m'), 1)
        
        PrimerQuiebre = fechaFormatear(PrimerQuiebre,'%Y%m')    
        listaMesesInicial.append(str(PrimerQuiebre))
        listaMesesInicial.append(str(incrementarMesFecha(PrimerQuiebre,MesesInicial)))
        sumaLotes = CalcularMesesLotes(listaMesesInicial, dataFrame)
        prodCodigo = str(CalcularProdCodigo(listaMesesInicial, dataFrame))
        
        posicion = posicion + 1
        dictLista={}
        if( (sumaLotes >= 0.97) and (int(index)<=int(row.name))):
            lotesTotal = 0    
            
            rango0 = arange(0.97,1.94,0.01).tolist()
            rango1 = arange(1.94,2.91,0.01).tolist()
            rango2 = arange(2.91,3.88,0.01).tolist()
            rango3 = arange(3.88,4.85,0.01).tolist()
            rango4 = arange(4.85,5.81,0.01).tolist()
            rango5 = arange(5.81,6.78,0.01).tolist()
            rango6 = arange(6.78,7.75,0.01).tolist()
            rango7 = arange(7.75,8.72,0.01).tolist()
            rango8 = arange(8.72,9.69,0.01).tolist()
            
            valor0 = close_to_any(round(sumaLotes,2), rango0)
            valor1 = close_to_any(round(sumaLotes,2), rango1)
            valor2 = close_to_any(round(sumaLotes,2), rango2)
            valor3 = close_to_any(round(sumaLotes,2), rango3)
            valor4 = close_to_any(round(sumaLotes,2), rango4)
            valor5 = close_to_any(round(sumaLotes,2), rango5)
            valor6 = close_to_any(round(sumaLotes,2), rango6)
            valor7 = close_to_any(round(sumaLotes,2), rango7)
            valor8 = close_to_any(round(sumaLotes,2), rango8)

            if(valor0):
                sumaLotes = 1
            elif (valor1):
                sumaLotes = 2
            elif (valor2):
                sumaLotes = 3
            elif (valor3):
                sumaLotes = 4
            elif (valor4):
                sumaLotes = 5
            elif (valor5):
                sumaLotes = 6
            elif (valor6):
                sumaLotes = 7
            elif (valor7):
                sumaLotes = 8
            elif (valor8):
                sumaLotes = 9
                
            dictLista={
                "SumaLotes":sumaLotes,
                "idLote":posicionIDLote,
                "listaMeses":str(listaMesesInicial).replace("[","").replace("]","").replace(" ",""),
                "prodCodigo":str(prodCodigo).replace("[","{").replace("]","}").replace("{{","[{").replace("}}","}]").replace("[","").replace("]","")
                }


            lista = [sumaLotes, row.name,listaMesesInicial ,prodCodigo]
            # listaValores.append(lista)
            valores = dictLista
            listaValores.append(valores)
            # listaLotes.append("{"+str(str(sumaLotes)+ ";" + str(int(row.name)) + ";" + str(listaMesesInicial).replace("[","").replace("]","").replace(" ",""))+"}")
            
            print(sumaLotes)
            sumaLotes=0
            posicion = posicion +1
            ultimoMesLoop = listaMesesInicial[len(listaMesesInicial)-1]
            ultimoMesLoopMain = listaMesesInicial[len(listaMesesInicial)-1]
            # listaMesesInicial.clear()
            del listaMesesInicial [:]
            codigoStr = prodCodigo.replace("'","").replace("[","").replace("]","").split()
            # Se corrigió la cantidad de caracteres del código de producto
            prodCodigoList = [w[0:w.find(".")] for w in prodCodigo.replace("'","").replace("[","").replace("]","").split()]
            # fin de correccion
            prodCodigoList = [int(i) for i in prodCodigoList]
            dfRootnot_in = dfRootFiltro[-dfRootFiltro['A0'].isin(prodCodigoList)]
            return listaValores, dfRootnot_in

            
            
        
        else:

            while ((sumaLotes < 0.97) and (int(indexPosition)<=int(len(dataFrame.index)))):
                
                ultimoMesLoop = listaMesesInicial[len(listaMesesInicial)-1]
                # ultimoMesLoop = fechaFormatear(listaMesesInicial.sort()[0], '%Y%m')
                listaMesesInicial.append(str(incrementarMesFecha(ultimoMesLoop,MesesInicial)))
                ultimoMesLoopMain = listaMesesInicial[len(listaMesesInicial)-1]
                prodCodigo = str(CalcularProdCodigo(listaMesesInicial, dataFrame))

                sumaLotes = CalcularMesesLotes(listaMesesInicial, dataFrame)
                if sumaLotes >= 0.97:
                    rango0 = arange(0.97,1.94,0.01).tolist()
                    rango1 = arange(1.94,2.91,0.01).tolist()
                    rango2 = arange(2.91,3.88,0.01).tolist()
                    rango3 = arange(3.88,4.85,0.01).tolist()
                    rango4 = arange(4.85,5.81,0.01).tolist()
                    rango5 = arange(5.81,6.78,0.01).tolist()
                    rango6 = arange(6.78,7.75,0.01).tolist()
                    rango7 = arange(7.75,8.72,0.01).tolist()
                    rango8 = arange(8.72,9.69,0.01).tolist()
                    
                    valor0 = close_to_any(round(sumaLotes,2), rango0)
                    valor1 = close_to_any(round(sumaLotes,2), rango1)
                    valor2 = close_to_any(round(sumaLotes,2), rango2)
                    valor3 = close_to_any(round(sumaLotes,2), rango3)
                    valor4 = close_to_any(round(sumaLotes,2), rango4)
                    valor5 = close_to_any(round(sumaLotes,2), rango5)
                    valor6 = close_to_any(round(sumaLotes,2), rango6)
                    valor7 = close_to_any(round(sumaLotes,2), rango7)
                    valor8 = close_to_any(round(sumaLotes,2), rango8)
                    


                    if(valor0):
                        sumaLotes = 1
                    elif (valor1):
                        sumaLotes = 2
                    elif (valor2):
                        sumaLotes = 3
                    elif (valor3):
                        sumaLotes = 4
                    elif (valor4):
                        sumaLotes = 5
                    elif (valor5):
                        sumaLotes = 6
                    elif (valor6):
                        sumaLotes = 7
                    elif (valor7):
                        sumaLotes = 8
                    elif (valor8):
                        sumaLotes = 9
                    dictLista={
                        "SumaLotes":sumaLotes,
                        "idLote":posicionIDLote,
                        "listaMeses":str(listaMesesInicial).replace("[","").replace("]","").replace(" ",""),
                        "prodCodigo":str(prodCodigo).replace("[","{").replace("]","}").replace("{{","[{").replace("}}","}]").replace("[","").replace("]","")
                        }
                    lista = [sumaLotes, row.name,listaMesesInicial ,prodCodigo]
                    # lista = [str(sumaLotes), str(int(row.name)),listaMesesInicial,prodCodigo]
                    #lista = str(sumaLotes)+ ";" + str(int(row.name)) + ";" + listaMesesInicial + ";"+ prodCodigo
                    # lista = str(str(sumaLotes)+ ";" + str(int(row.name)) + ";" + str(listaMesesInicial) + ";"+str(prodCodigo))
                    #lista = str(str(sumaLotes)+ ";" + str(int(row.name)) + ";" + str(listaMesesInicial).replace("[","").replace("]","").replace(" ","") + ";"+str(prodCodigo).replace("[","").replace("]","").replace(" ",""))
                    valores = dictLista
                    listaValores.append(valores)

                    # listaMesesInicial.clear()
                    del listaMesesInicial [:]
                    print(sumaLotes)
                    sumaLotes=0
                    posicion = posicion + 1
                    codigoStr = prodCodigo.replace("'","").replace("[","").replace("]","").split()
                    prodCodigoList = [w[0:w.find(".")] for w in prodCodigo.replace("'","").replace("[","").replace("]","").split()]
                    prodCodigoList = [int(i) for i in prodCodigoList]
                    dfRootnot_in = dfRootFiltro[-dfRootFiltro['A0'].isin(prodCodigoList)]
                    return listaValores, dfRootnot_in
                    
                else:
                    indexPosition = indexPosition + 1
                    print(sumaLotes)
                    continue
            return listaValores, dfRootFiltro

def validarGrupoCantidad_nuevo(df, df_info_extra, fechaInicioPlan):
    """
    df: Dataframe con información de los productos a organizar en lotes
    info_extra: array de diccionarios con información adicional de los productos utilizada para 
    recalcular la sugerencia de produccion según el mes actual
    """
    def to_lote_dict(serie):
        familia_prod = serie['A3']
        familia_prod_value = str(int(familia_prod)) if (str(serie['A3']).isdecimal()) else str(serie['A3'])

        return dict(
            cod_producto=str(int(serie['A0'])),
            cuanto_planificar=serie['CuantoPlanificar'],
            mes_quiebre=str(int(serie['QuiebreInt'])),
            campo_20=serie['20'],
            cuando_producir=serie['CuandoProducir'],
            tamano_lote=serie['A5'],
            tamano_presentacion=serie['A4'],
            familia_producto=familia_prod_value, #str(int(serie['A3'])),
            sugerencia_produccion=serie['CantidadLotes']
        )


    def validar_valor_cierra_lote(valor, tamano_lote_sin_merma):
        entero, residuo = divmod(valor, tamano_lote_sin_merma)
        print(entero, residuo)
        return entero >= 1 and round(residuo, 2) <= 0.03 * entero


    def actualizar_sugerencia_produccion(quiebre_actual, lote_dict):        
        fila_producto = df_info_extra[df_info_extra['A0'].astype('int') == int(lote_dict['cod_producto'])].iloc[0]
        lista_meses_base = ObtenerColumnas(fechaInicioPlan)
        meses_futuros = ObtenerMesesFuturos(
            fila_producto[lista_meses_base],
            fila_producto["A16"],
            fila_producto["12"],
            fila_producto["14"],
            fila_producto["15"],
            fila_producto["19"],
            fila_producto["13"],
            fila_producto["21"],
            quiebre_actual
        )
        lista_meses_producir = ObtenerColumnasCuanto(quiebre_actual, meses_futuros)
        sugerencia_produccion = ObtenerCuantoProducir(
            fila_producto[lista_meses_producir],
            fila_producto["MesesFuturos"],
            fila_producto['AjustePlan'], 
            fila_producto['A4'],
            fila_producto['A0']
        )
        sugerencia_porcentaje_lote = ObtenerCantidadLotes(sugerencia_produccion, lote_dict['tamano_lote'])
        lote_dict['sugerencia_produccion'] = sugerencia_porcentaje_lote


    def prod_dict_to_text(producto):
        campos = [
            str(float(producto["cod_producto"])),
            str(producto["cuanto_planificar"]),
            producto["mes_quiebre"],
            str(producto["campo_20"]),
            str(producto["cuando_producir"]),
            str(producto["tamano_lote"]),
            str(producto["tamano_presentacion"]),
            producto["familia_producto"]
        ]
        return "'" + "-".join(campos) + "'"
    
    def calcular_costo(productos, df_data_adicional):
        columnas_orden_final = ["level_0", "index", "A0", "A5", "1", "22", "9", "3", "4", "5", "8", "2", "6", "10", "11", "CuantoPlanificar", "A4", "20", "CodigoProductoExp", "Tamanolote", "IdLote", "CuantoPlanificarNuevo", "QuiebreIntExp", "MinimoExp", "CuandoProducir", "Presentacion"]
        lista_codigos = [int(p['cod_producto']) for p in productos]
        # Filtrar solo los productos que pertenecientes al lote
        filtro_productos = df_data_adicional['A0'].isin(lista_codigos)
        df_data_adicional = df_data_adicional[filtro_productos]
        # Tomar las columnas necesarias del dataframe total y ordenar el dataframe por codigo
        df_data_adicional = df_data_adicional[["A0", "A5", "1", "22", "9", "3", "4", "5", "8", "2", "6", "10", "11", "CuantoPlanificar", "A4", "20", "CuandoProducir"]]
        df_data_adicional.sort_values(by=['A0'], inplace=True)
        # Insertar las columnas iniciales necesesarias para coincidir con lo que requiere el metodo existente
        df_data_adicional.insert(0, 'index', range(len(productos)))
        df_data_adicional.insert(0, 'level_0', range(len(productos)))
        df_data_adicional.reset_index(inplace=True, drop=True)

        # Convertir la lista de productos a un dataframe ordenado por producto con los nombres de columnas necesarios
        lista_columnas_original = ["cod_producto", "tamano_lote", "IdLote", "cuanto_planificar", "mes_quiebre", "campo_20", "tamano_presentacion"]
        lista_columnas_reemplazo = ['CodigoProductoExp','Tamanolote','IdLote','CuantoPlanificarNuevo','QuiebreIntExp','MinimoExp','Presentacion']
        df_productos = pd.DataFrame(productos, columns=lista_columnas_original)
        df_productos.sort_values(by=["cod_producto"], inplace=True)
        df_productos.columns = lista_columnas_reemplazo
        df_productos.reset_index(inplace=True, drop=True)
        df_para_calculo_costo = df_data_adicional.join(df_productos)
        df_para_calculo_costo = df_para_calculo_costo[columnas_orden_final]
        result = distribucionSciPyNueva(df_para_calculo_costo)

        return result if result is not None else []

    merma = 0.03
    tamano_lote_sin_merma = 1 - merma    
    lista_quiebres = list(set(df['QuiebreInt']))
    lista_quiebres.sort()
    lista_quiebres = [str(e) for e in lista_quiebres]
    lote_en_proceso = None
    grupo_lotes = []
    
    for quiebre in lista_quiebres:
    # Por cada Quiebre
        mes_quiebre_lote_actual = quiebre if lote_en_proceso is None else lote_en_proceso['mesQuiebre']
        filtro_productos_quiebre_actual = df["QuiebreInt"].astype("str") == quiebre
        productos_quiebre_actual = [to_lote_dict(row) for i, row in df[filtro_productos_quiebre_actual].iterrows()]
        # Actualizar Sugerencia de Produccion
        [actualizar_sugerencia_produccion(mes_quiebre_lote_actual, p) for p in productos_quiebre_actual]
        if lote_en_proceso is None:
        # lote abierto ?        
            # loteEnProceso = IniciarNuevoLote con todos los productos del quiebre
            lote_en_proceso = dict(
                idLote=len(grupo_lotes),
                mesQuiebre=quiebre,
                prodCodigo=productos_quiebre_actual,
                cuandoProducir=productos_quiebre_actual[0]['cuando_producir']
            )
            # sugerencia_produccion_actual = sum([ p["sugerencia_produccion"] for p in productos_quiebre_actual ])
            #### ---- MINIMIZAR COSTO ----- #####      
            if sum([x['cuanto_planificar']/x['tamano_lote'] for x in productos_quiebre_actual]) > 1:
                costos = calcular_costo(productos_quiebre_actual, df_info_extra)            
                # el tamaño del lote se encuentra en el indice 3 de costos 
                # la distribucion para el producto se encuentra en el índice 27            
                sugerencia_produccion_actual = sum([c[27]/(c[4] * .97) for c in costos])
            else:
                sugerencia_produccion_actual = 0

            if validar_valor_cierra_lote(sugerencia_produccion_actual, tamano_lote_sin_merma):
            # Lote cierra ?
                grupo_lotes.append(lote_en_proceso)
                lote_en_proceso = None
                # Agregar a grupo de lotes
        else:
        # Continuacion de Lote ?        
            combinaciones = []
            suma_sugerencia_produccion_actual = sum([p['sugerencia_produccion'] for p in lote_en_proceso['prodCodigo']])
                        
            # Preparar todas las combinaciones de productos de lote actual
            for i in range(1, len(productos_quiebre_actual) + 1):
                for combinacion in combinations(productos_quiebre_actual ,i):
                    productos = lote_en_proceso['prodCodigo'] + list(combinacion)
                    costos = calcular_costo(productos, df_info_extra)            
                    # el tamaño del lote se encuentra en el indice 3 de costos 
                    # la distribucion para el producto se encuentra en el índice 27            
                    # el costo total del lote se repite para todos los elementos en el último indice
                    if len(costos) > 0:
                        suma_producir = sum([c[27]/(c[4]*.97) for c in costos])
                        costo_produccion = costos[0][-1] / sum([c[27] for c in costos])
                        # suma_producir = sum([x['sugerencia_produccion'] for x in combinacion]) + suma_sugerencia_produccion_actual
                        codigos = [x['cod_producto'] for x in productos]
                        combinaciones.append( (suma_producir, costo_produccion, codigos) )
                                    
            # Ordenar de candidatos de menor a mayor costo
            combinaciones.sort(key=lambda tup: tup[1])
            # pd.DataFrame(combinaciones).to_excel('temp/{}.xlsx'.format(datetime.now().strftime('%d-%b-%Y-(%H-%M-%S.%f)')))
            # Encontrar el primer candidato que caiga dentro de el rango entre y x * lote
            candidato_encontrado = False
            for suma_producir, costo_produccion, codigos_productos in combinaciones:                
                if validar_valor_cierra_lote(suma_producir, tamano_lote_sin_merma):                
                # Se encontró candidato ?
                    candidato_encontrado = True
                    productos_para_cerrar_lote = [p for p in productos_quiebre_actual if p['cod_producto'] in codigos_productos]
                    # Cerrar el lote con los productos de la combinacion
                    lote_en_proceso['prodCodigo'].extend(productos_para_cerrar_lote)
                    grupo_lotes.append(lote_en_proceso)
                    lote_en_proceso = None
                    
                    productos_restantes = [p for p in productos_quiebre_actual if p['cod_producto'] not in codigos_productos]
                    if len(productos_restantes) > 0:
                    # quedan productos no utilizados?
                        [actualizar_sugerencia_produccion(quiebre, p) for p in productos_restantes]
                        lote_en_proceso = dict(
                            idLote=len(grupo_lotes),
                            mesQuiebre=quiebre,
                            prodCodigo=productos_restantes,
                            cuandoProducir=productos_restantes[0]['cuando_producir']
                        )
                        # suma_sugerencia_produccion = sum([p['sugerencia_produccion'] for p in productos_restantes])
                        costos = calcular_costo(lote_en_proceso['prodCodigo'], df_info_extra)            
                        # el tamaño del lote se encuentra en el indice 3 de costos 
                        # la distribucion para el producto se encuentra en el índice 27            
                        suma_sugerencia_produccion = sum([c[27]/(c[4]*.97) for c in costos])
                        if validar_valor_cierra_lote(suma_sugerencia_produccion, tamano_lote_sin_merma):
                        # Lote cierra?
                            grupo_lotes.append(lote_en_proceso)
                            lote_en_proceso = None
                            # Agregar a grupo de lotes
                    # Si se encontró un candidato, no continuar el loop
                    break

            if not candidato_encontrado:
            # No se encontró candidato ?            
                # Sumar todo el quiebre al loteEnProceso
                lote_en_proceso['prodCodigo'].extend(productos_quiebre_actual)
            
    # Agregar el loteEnProceso a grupo de Lotes
    if lote_en_proceso:
        grupo_lotes.append(lote_en_proceso)

    # "SumaLotes":sumaLotes,
    # "idLote":posicionIDLote,
    # "listaMeses":str(listaMesesInicial).replace("[","").replace("]","").replace(" ",""),
    # "prodCodigo":str(prodCodigo).replace("[","{").replace("]","}").replace("{{","[{").replace("}}","}]").replace("[","").replace("]","")
    for grupo in grupo_lotes:        
        grupo['SumaLotes'] = sum([p['sugerencia_produccion'] for p in grupo['prodCodigo']])
        grupo['listaMeses'] = list(set([p['mes_quiebre'] for p in grupo['prodCodigo']]))
        grupo['listaMeses'] = ",".join(["'{}'".format(m) for m in grupo['listaMeses']])
        # Todos los productos del lote se producen en el mes asignado al lote.
        for p in grupo['prodCodigo']:
            p['cuando_producir'] = grupo['cuandoProducir']

        grupo['prodCodigo'] ="{" + ", ".join([prod_dict_to_text(p) for p in grupo['prodCodigo']]) + "}"
        del(grupo['mesQuiebre'])

    return grupo_lotes

# def validarGrupoCantidad(dataFrame):
#     dataFrameVidaUtil = dataFrame.sort_values(by='12', ascending=True)
#     dataFrameVidaUtilVU = dataFrameVidaUtil['12'].head(1).iat[0]
#     dataFrameVidaUtilDemandaAnual = dataFrameVidaUtil['CantidadLotesDemandaAnual'].head(1).iat[0]
#     posicion=0
     
#     MesesInicial = IniciarReglaNegocio(dataFrameVidaUtilVU, dataFrameVidaUtilDemandaAnual) - 1
#     listaLotes=[]
#     ultimoMesLoopMain = ""
#     listaValores = []
#     listaCodigoTerminado = str(dataFrame['A0'].tolist()).replace(".0","")
#     ProdTerminadoLista = listaCodigoTerminado.replace("[","").replace("]","").replace(",","").split()
#     ProdTerminadoLista = [int(i) for i in ProdTerminadoLista]
#     # dataframeRootFilter = dataframeRoot.A0.isin(ProdTerminadoLista)
#     # dataframeRootFilterValues = dataframeRoot[dataframeRootFilter]
    
#     for index, row in dataFrame.iterrows():
        
#         indexPosition=int(index)
#         listaMesesInicial=[]
#         PrimerQuiebre = str(row['QuiebreInt'])
        
        
#         if(ultimoMesLoopMain != ""):
#             if(int(PrimerQuiebre) < int(ultimoMesLoopMain) ):
#                 PrimerQuiebre = incrementarMesFecha(fechaFormatear(ultimoMesLoopMain,'%Y%m'), 1)
        
#         PrimerQuiebre = fechaFormatear(PrimerQuiebre,'%Y%m')    
#         listaMesesInicial.append(str(PrimerQuiebre))
#         listaMesesInicial.append(str(incrementarMesFecha(PrimerQuiebre,MesesInicial)))
#         sumaLotes = CalcularMesesLotes(listaMesesInicial, dataFrame)
#         prodCodigo = str(CalcularProdCodigo(listaMesesInicial, dataFrame))
        
#         posicion = posicion + 1
#         dictLista={}
#         if( (sumaLotes >= 0.97) and (int(index)<=int(row.name))):
#             lotesTotal = 0
            
#             rango0 = arange(0.97,1.94,0.01).tolist()
#             rango1 = arange(1.94,2.91,0.01).tolist()
#             rango2 = arange(2.91,3.88,0.01).tolist()
#             rango3 = arange(3.88,4.85,0.01).tolist()
#             rango4 = arange(4.85,5.81,0.01).tolist()
#             rango5 = arange(5.81,6.78,0.01).tolist()
#             rango6 = arange(6.78,7.75,0.01).tolist()
#             rango7 = arange(7.75,8.72,0.01).tolist()
#             rango8 = arange(8.72,9.69,0.01).tolist()
            
#             valor0 = close_to_any(round(sumaLotes,2), rango0)
#             valor1 = close_to_any(round(sumaLotes,2), rango1)
#             valor2 = close_to_any(round(sumaLotes,2), rango2)
#             valor3 = close_to_any(round(sumaLotes,2), rango3)
#             valor4 = close_to_any(round(sumaLotes,2), rango4)
#             valor5 = close_to_any(round(sumaLotes,2), rango5)
#             valor6 = close_to_any(round(sumaLotes,2), rango6)
#             valor7 = close_to_any(round(sumaLotes,2), rango7)
#             valor8 = close_to_any(round(sumaLotes,2), rango8)

#             if(valor0):
#                 sumaLotes = 1
#             elif (valor1):
#                 sumaLotes = 2
#             elif (valor2):
#                 sumaLotes = 3
#             elif (valor3):
#                 sumaLotes = 4
#             elif (valor4):
#                 sumaLotes = 5
#             elif (valor5):
#                 sumaLotes = 6
#             elif (valor6):
#                 sumaLotes = 7
#             elif (valor7):
#                 sumaLotes = 8
#             elif (valor8):
#                 sumaLotes = 9

#             dictLista={
#                 "SumaLotes":sumaLotes,
#                 "idLote":row.name,
#                 "listaMeses":str(listaMesesInicial).replace("[","").replace("]","").replace(" ",""),
#                 "prodCodigo":str(prodCodigo).replace("[","{").replace("]","}").replace("{{","[{").replace("}}","}]").replace("[","").replace("]","")
#                 }


#             lista = [sumaLotes, row.name,listaMesesInicial ,prodCodigo]
#             # listaValores.append(lista)
#             valores = dictLista
#             listaValores.append(valores)
#             # listaLotes.append("{"+str(str(sumaLotes)+ ";" + str(int(row.name)) + ";" + str(listaMesesInicial).replace("[","").replace("]","").replace(" ",""))+"}")
            
#             print(sumaLotes)
#             sumaLotes=0
#             posicion = posicion +1
#             ultimoMesLoop = listaMesesInicial[len(listaMesesInicial)-1]
#             ultimoMesLoopMain = listaMesesInicial[len(listaMesesInicial)-1]
#             del listaMesesInicial [:]
#             # listaMesesInicial.clear()
#             continue

            
            
        
#         else:

#             while ((sumaLotes < 0.97) and (int(indexPosition)<=int(len(dataFrame.index)))):
                
#                 ultimoMesLoop = listaMesesInicial[len(listaMesesInicial)-1]
#                 # ultimoMesLoop = fechaFormatear(listaMesesInicial.sort()[0], '%Y%m')
#                 listaMesesInicial.append(str(incrementarMesFecha(ultimoMesLoop,MesesInicial)))
#                 ultimoMesLoopMain = listaMesesInicial[len(listaMesesInicial)-1]
#                 prodCodigo = str(CalcularProdCodigo(listaMesesInicial, dataFrame))

#                 sumaLotes = CalcularMesesLotes(listaMesesInicial, dataFrame)
#                 if sumaLotes >= 0.97:
#                     rango0 = arange(0.97,1.94,0.01).tolist()
#                     rango1 = arange(1.94,2.91,0.01).tolist()
#                     rango2 = arange(2.91,3.88,0.01).tolist()
#                     rango3 = arange(3.88,4.85,0.01).tolist()
#                     rango4 = arange(4.85,5.81,0.01).tolist()
#                     rango5 = arange(5.81,6.78,0.01).tolist()
#                     rango6 = arange(6.78,7.75,0.01).tolist()
#                     rango7 = arange(7.75,8.72,0.01).tolist()
#                     rango8 = arange(8.72,9.69,0.01).tolist()
                    
#                     valor0 = close_to_any(round(sumaLotes,2), rango0)
#                     valor1 = close_to_any(round(sumaLotes,2), rango1)
#                     valor2 = close_to_any(round(sumaLotes,2), rango2)
#                     valor3 = close_to_any(round(sumaLotes,2), rango3)
#                     valor4 = close_to_any(round(sumaLotes,2), rango4)
#                     valor5 = close_to_any(round(sumaLotes,2), rango5)
#                     valor6 = close_to_any(round(sumaLotes,2), rango6)
#                     valor7 = close_to_any(round(sumaLotes,2), rango7)
#                     valor8 = close_to_any(round(sumaLotes,2), rango8)
                    


#                     if(valor0):
#                         sumaLotes = 1
#                     elif (valor1):
#                         sumaLotes = 2
#                     elif (valor2):
#                         sumaLotes = 3
#                     elif (valor3):
#                         sumaLotes = 4
#                     elif (valor4):
#                         sumaLotes = 5
#                     elif (valor5):
#                         sumaLotes = 6
#                     elif (valor6):
#                         sumaLotes = 7
#                     elif (valor7):
#                         sumaLotes = 8
#                     elif (valor8):
#                         sumaLotes = 9
#                     dictLista={
#                         "SumaLotes":sumaLotes,
#                         "idLote":row.name,
#                         "listaMeses":str(listaMesesInicial).replace("[","").replace("]","").replace(" ",""),
#                         "prodCodigo":str(prodCodigo).replace("[","{").replace("]","}").replace("{{","[{").replace("}}","}]").replace("[","").replace("]","")
#                         }
#                     lista = [sumaLotes, row.name,listaMesesInicial ,prodCodigo]
#                     # lista = [str(sumaLotes), str(int(row.name)),listaMesesInicial,prodCodigo]
#                     #lista = str(sumaLotes)+ ";" + str(int(row.name)) + ";" + listaMesesInicial + ";"+ prodCodigo
#                     # lista = str(str(sumaLotes)+ ";" + str(int(row.name)) + ";" + str(listaMesesInicial) + ";"+str(prodCodigo))
#                     #lista = str(str(sumaLotes)+ ";" + str(int(row.name)) + ";" + str(listaMesesInicial).replace("[","").replace("]","").replace(" ","") + ";"+str(prodCodigo).replace("[","").replace("]","").replace(" ",""))
#                     valores = dictLista
#                     listaValores.append(valores)
#                     del listaMesesInicial [:]
                    
#                     print(sumaLotes)
#                     sumaLotes=0
#                     posicion = posicion + 1
#                     codigoStr = prodCodigo.replace("'","").replace("[","").replace("]","").split()
                    
#                     break
                    
                    
#                 else:
#                     indexPosition = indexPosition + 1
#                     print(sumaLotes)
#                     continue
#     return listaValores

# rango0 = arange(0.97,1.94,0.01)
# rango1 = arange(1.94,2.91,0.01)
# rango2 = arange(2.91,3.88,0.01)

# for i in arange(0.96, 3.81, 0.01).tolist():
#     if ((round(i,2) < rango0[0])==True):
#         i = 0
#         # print(str(sumaLotes) + " - " + str("0 lote"))
#     if ((round(i,2) in rango0)==True):
#         i = 1
#         # print(str(sumaLotes) + " - " + str("1 lote"))
#     if ((round(i,2) in rango1)==True):
#         i = 2
#         # print(str(sumaLotes) + " - " + str("2 lotes"))
#     if ((round(i,2) in rango2)==True):
#         i = 3
#     print(i)
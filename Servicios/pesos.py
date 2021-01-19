import itertools
from itertools import count
import numpy
from funcionCosto import calcularCostoFB
import math
# listaCantidades = []
import pandas as pd
from lotesScipy import distribucionSciPyNueva#, distribucionSciPyNuevaIter
import logginProcess
def update_value(index, new_value, listaElementos,  TLPT):
    limite = TLPT
    listaCantidades=[]
    listaCodigos=[]
    listaMinimos=[]
    retorno = False
    limiteUnitario = round((limite / 275000),0)
    limiteTLPT = 0
    if limiteUnitario == 1:
        limiteTLPT = limiteTLPT
    else:
        limiteTLPT = limite / limiteUnitario

    for item in listaElementos:
        listaCantidades.append(item[0])
        listaCodigos.append(int(item[1]))
        listaMinimos.append(item[2])
    if 908143 in listaCodigos:
        print(new_value)
        pass

    
    
    
    continuar = False
    for indexCant, item in enumerate(listaCantidades):
        if (indexCant == index):
            listaCantidades[indexCant]=int(new_value)
            continuar = True
            
        
    if len(listaCantidades) == 2:
        for indexCantidad, itemCant in enumerate(listaCantidades):
            listaCantidades[indexCantidad] = limite / 2
            retorno = True
        return (listaCantidades, listaCodigos, listaMinimos, retorno)
        
    
    #dif = (1.0-new_value) / (1.0-listaCantidades[index])
    if len(listaCantidades)>1:
        
        
        # dif = (limite)/(sum(listaCantidades))
        dif = (limite-new_value)/(sum(listaCantidades)-new_value)
        # dif = (limite)/(sum(listaCantidades))
        # dif = (sumaTotalLista-new_value) / (sumaTotalLista-listaCantidades[index])
        for i in range(len(listaCantidades)):
            # dif = (limite-new_value)/(sum(listaCantidades)-new_value)
            
            if i == index:
                listaCantidades[i] = new_value
            else:
                if ((listaCantidades[i] * dif) - int(round(listaMinimos[i],0))) < 0 :
                    listaCantidades[i] = int(round(listaMinimos[i],0)) + (int(round(listaMinimos[i],0)) - (listaCantidades[i] * dif))
                else:
                    valorTemp = round(listaCantidades[i] * dif,0)
                    if(round(valorTemp,0) <= round(listaCantidades[i],0)):
                        listaCantidades[i] = valorTemp
                    else:
                        listaCantidades[i] = round(listaCantidades[i],0) * dif
                        #
                    
    else:
        pass
            
    
    return(listaCantidades, listaCodigos, listaMinimos, retorno)

def InicioDistribucion(grupoLotes):
    listaElementos = grupoLotes[['CuantoPlanificarNuevo','A0','20']].values.tolist()
    listaElementosMinimo = grupoLotes['20'].values.tolist()
    listaCodigos = grupoLotes['A0'].values.tolist()
    grupoLotesCopy = grupoLotes.copy()
    costoAlmacenado = []
    distribucionAlm = []
    codigosOrden=[]
    retorno=False

    distriNueva = distribucionSciPyNueva(grupoLotes)
    if distriNueva is None or len(distriNueva)==0:
        logginProcess.logger.error("Lista de distribucion vacia")
    else:
        logginProcess.logger.info("Se distribuyeron: " + str(distriNueva) + " lotes.")

    tamanoLote = grupoLotes[['Tamanolote']].values.tolist()[0][0]
    if tamanoLote>1:
        for i in range(1, int(round(tamanoLote,0))+1):
            returnDistriNuevaIter = 0#distribucionSciPyNuevaIter(grupoLotes,i) 
            distribucionAlm.append(returnDistriNuevaIter)
            # distribucionAlm.append([i-1])
        pass
    else:
        returnDistriNuevaIter = distriNueva
        distribucionAlm.append(returnDistriNuevaIter)
    

    # distribucionAlm.append(distriNueva)
    # tamanoLote = grupoLotes[['Tamanolote']].values.tolist()[0][0]
    # if tamanoLote > 1:
    #     for i in range(1, tamanoLote+1):
    #         grupoLotes[['TamanoLote']]=i
    #         distriNueva=distribucionSciPyNueva(grupoLotes)
    #         distribucionAlm.append(distriNueva)
    #         pass
        
    #     pass
    return(distriNueva,distribucionAlm)
    
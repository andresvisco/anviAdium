from scipy.optimize import minimize
import numpy as np
from numpy import array
from funcionCosto import calcularCostoSciPy
import math
import pandas as pd
from operator import itemgetter
from scipy.optimize import NonlinearConstraint, LinearConstraint, Bounds
import sys

def distribucionSciPyNueva(grupoLotes):    
    listaPresentaciones=[]
    listaDatos = []
    listaDatosSegmentados = []
    n = len(grupoLotes)
    x0 = np.zeros(n)
    xMaximosNP = np.zeros(n)
    xMaximos = np.zeros(n)
    bTuples = []
    bnds = tuple()
    xMinimosNP=np.zeros(n)
    
    TLPTReal=0

    entero_lote_actual = None
    tamano_lote = grupoLotes['A5'].values[0] * .97
    cantidad_minima_lote_actual = sum((grupoLotes['MinimoExp'].astype('float') * grupoLotes['Presentacion'].astype('float')).values)
    cantidad_maxima_lote_actual = sum(grupoLotes['CuantoPlanificarNuevo'].values)
    cantidad_minima_lotes = cantidad_minima_lote_actual / tamano_lote
    cantidad_maxima_lotes = cantidad_maxima_lote_actual / tamano_lote

    if cantidad_maxima_lotes < 1:
        return None

    def ineq_constraint(x):
        maximo = TLPTReal
        respuesta = maximo - sum([item for item in x])
        return respuesta
    

    def eq_LoteEntero(x):        
        result = ( sum([i for i in x]) / tamano_lote ) - entero_lote_actual
        return result


    xDatos = listaDatos
    def objective(x):
        listaCostos=[]
        entro= 0
        
        if np.isnan(x).any():
            return np.nan

        valorSuma = int(float(sum(x)))
        # if valorSuma in range(2031495,2031498):
        #     entro=1

        
        for index, item in enumerate(x):
            enteroLote = int(xDatos[index][3]) * .97
            valor = round(item,0)
            porcentajeLote = valor/enteroLote
            valorMod = 0
            frac, entero = math.modf(porcentajeLote)
            if entero > 0:
                if frac < 0.8:
                    valorMod = enteroLote * entero
                    x[index] = valorMod
                    valor=x[index]
            # if (valor >= 137400) and (valor <= 141000):
            #     # x[index]=137500
            #     costo = calcularCostoSciPy(xDatos[index],valor)
            #     pass        
            
            # elif (valor >= 274995) and (valor <= 275000):
            #     costo = calcularCostoSciPy(xDatos[index],valor)
            #     pass
            #     # listaCostos.append(costo)
                
            #     # sys.stdin.readline()
            # elif (valor >= 399995) and (valor <= 400000):
            #     costo = calcularCostoSciPy(xDatos[index],valor)
            #     pass    
            # elif (valor >= 554995) and (valor <= 550000):
                
            #     costo = calcularCostoSciPy(xDatos[index],valor)
            #     pass
            #     # listaCostos.append(costo)
            # elif (valor >= 824985) and (valor <= 825000):
                
            #     costo = calcularCostoSciPy(xDatos[index],valor)
            #     pass
            #     # listaCostos.append(costo)
            # elif (valor >= 999980) and (valor <= 1100000):
                
            #     costo = calcularCostoSciPy(xDatos[index],valor)
            #     pass
            # else:
            #     costo = calcularCostoSciPy(xDatos[index],valor)
            #     pass
            costo = calcularCostoSciPy(xDatos[index],valor)
                # listaCostos.append(costo)
            listaCostos.append(costo)    
            # costo = calcularCostoSciPy(xDatos[index],valor)
            # listaCostos.append(costo)
            # listaCostosTotal.append([costo,valor,xDatos[index][17]])
        
            
        costoReturn = sum(listaCostos)
        
        # # listaX0.append(x)
        
        return costoReturn
    
    

    for itemLote in grupoLotes.iterrows():
        listaDatos.append(itemLote[1].values.tolist())
        listaPresentaciones.append(itemLote[1]['A4'])
        pass
    
    for index, item in enumerate(listaDatos):
        x0[index] = int(float(item[24]) * float(item[17]))
        xMaximosNP[index] = int(float(item[22]))
        xMinimosNP[index] = int(float(item[24]))
    xMaximos = xMaximosNP      
    for indexb, itemB in enumerate(x0):
        error = str()
        if (x0[indexb] > xMaximos[indexb] ):
            xMaximos[indexb] = listaDatos[indexb][16]
            pass
        bTuples.append((x0[indexb],xMaximos[indexb]))
        pass

    listaTLPT = [item[3] for index, item in enumerate(grupoLotes.values.tolist())]
    
    xMaximosTLP = []
    
    TLPTReal = int(sum(xMaximos)) #275000*int((sum(xMaximos)/275000))
    bnds = tuple(bTuples)
    arrayX0 = x0 #np.array(listaDatos)
    # bounds = Bounds(xMinimosNP,xMaximosNP,keep_feasible=False)
    con = [
        {'type': 'ineq', 'fun': ineq_constraint},
        {'type': 'eq', 'fun': eq_LoteEntero}
    ]    
    
    # consTraints = [con, con2]
    
    xtol = 1e-08
    gtol = 1e-08
    barrier = 1e-01
    tol1 = 0.5
    initialParameterBarrier=0.3
    options={'verbose':3, 
    'disp':True,'maxiter':10000,
    'xtol': xtol, 'gtol': gtol, 
    'sparse_jacobian':False,
    'initial_constr_penalty': 1.0, 'initial_tr_radius': 1.0,
    'barrier_tol': barrier,   'initial_barrier_parameter': initialParameterBarrier, 'initial_barrier_tolerance': tol1}
    solution = None
    list_solutions = []
    for entero_lote in range(math.ceil(cantidad_minima_lotes), int(cantidad_maxima_lotes) + 1):
        entero_lote_actual = entero_lote
        try:
            solution = minimize(objective, arrayX0,constraints=con,bounds=bnds) #constraints=con),
            if solution.success:
                list_solutions.append(solution)
                print(solution)
                print(sum(solution.x))
                menorCosto = round(solution.fun,2)
        except Exception:
            print(Exception)
            pass
        
    if len(list_solutions) == 0:
        return None
    
    list_solutions.sort(key=lambda s: s.fun / sum(s.x))
    solution = list_solutions[0]

    for itemSol in solution.x:
        listaDatosSegmentados.append(itemSol)
        
    
    for indexDato, itemDato in enumerate(listaDatos):
        listaDatos[indexDato].insert((len(listaDatos[indexDato])),listaDatosSegmentados[indexDato])
        listaDatos[indexDato].insert((len(listaDatos[indexDato])+1),round(solution.fun,2))
    
    return listaDatos

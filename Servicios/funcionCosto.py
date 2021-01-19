# - *- coding: utf- 8 - *-
import math
import pandas as pd

def ObtenerLotePertenencia(valores):
    dfValores = valores['CuantoPlanificar'].reset_index()
    
    
    for index, item in dfValores.iterrows():
        minVal = int(item['20'])
        maxVal = int(item['CuantoPlanificar'])
        for a in range(minVal, maxVal, 1000 ):

            print(str(a) + " - " + str(item['A0']))
    


    return True

def ObtenerGrupo(valores):
    
    return valores

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def calcularCostoLotes(calculo, lotes):
    x=calculo['A5'] / calculo['A4']
    lotes = calculo['CuantoPlanificar'] / calculo['A5']
    if lotes < 1.0:
        lotes = 1
    if lotes > 1.0:
        decimal = lotes % 1
        if decimal > 85:
            lotes = round_up(lotes, decimals=0)
        else:
            lotes = math.floor(lotes)



   
    if x != 0:
        if(lotes!=0):
            x=x*lotes    

        M = calculo['9']
        Cmat = calculo['3']
        CMod = calculo['4']
        CostoNeto = calculo['3'] + calculo['4'] + calculo['5']
        CinvMasCfij = calculo['8']
        CfinCinv = calculo['6']
        D = calculo['11']
        TLPT = calculo['2']
        CfijoOrden = calculo['8']
        Canalisis = calculo['10']
        Canalisis = Canalisis.iloc[0]
        Cm = 0
        Cg = 0
        try:
            if (D != 0.0) and (D is not None) and (D is not "NaN"):
                Cm = ((x-(math.ceil(x/TLPT)*M))/2)*(Cmat + CMod)*(CfinCinv)*((x-(math.ceil(x/TLPT)*M))/D)
                # Cm = ((x-M)/2)*(Cmat + CMod)*(CfinCinv)
            else:
                Cm = 0
        except Exception:
            print(Exception)
            pass

        
        
        # Cm = ((x-M)/2)*(Cmat+CMod)*(0.06)
        Cg = (CfijoOrden + Canalisis) * math.ceil(x/TLPT) +M  * CostoNeto *math.ceil(x/TLPT)
        # Cg = ((CfijoOrden + Canalisis) * math.ceil(x/TLPT) * (D+((D/x)*math.ceil(x/TLPT)*M))/x) + M * (Cmat + CMod)
        Ct = Cm + Cg
        print(Ct)
    else:
        Ct=0
    return Ct

def calcularCosto(calculo):#x,M,Cmat,CMod,CinvMasCfij, CfijoOrden, Canalisis, TLPT, D):
    # x = calculo['22']
    x = calculo["CuantoPlanificar"] / calculo["A4"]
    

    if x != 0:
        
        M = calculo['9']
        Cmat = calculo['3']
        CMod = calculo['4']
        CostoNeto = calculo['3'] + calculo['4'] + calculo['5']
        CinvMasCfij = calculo['8']
        CfinCinv = calculo['6']
        D = calculo['11']
        TLPT = calculo['2']
        CfijoOrden = calculo['8']
        Canalisis = calculo['10']
        Canalisis = Canalisis.iloc[0]
        Cm = 0
        Cg = 0
        try:
            if (D != 0.0) or (D is not None) or (D is not "NaN"):
                Cm = ((x-(math.ceil(x/TLPT)*M))/2)*(Cmat + CMod)*(CfinCinv)*((x-(math.ceil(x/TLPT)*M))/D)
                # Cm = ((x-M)/2)*(Cmat + CMod)*(CfinCinv)
            else:
                Cm = 0
        except Exception:
            print(Exception)
            pass

        
        
        # Cm = ((x-M)/2)*(Cmat+CMod)*(0.06)
        Cg = (CfijoOrden + Canalisis) * math.ceil(x/TLPT) +M  * CostoNeto *math.ceil(x/TLPT)
        # Cg = ((CfijoOrden + Canalisis) * math.ceil(x/TLPT) * (D+((D/x)*math.ceil(x/TLPT)*M))/x) + M * (Cmat + CMod)
        Ct = Cm + Cg
        print(Ct)
    else:
        Ct=0
    return Ct

def calcularCostoFB(calculo, x):#x,M,Cmat,CMod,CinvMasCfij, CfijoOrden, Canalisis, TLPT, D):
    # x = calculo['22']
    calculo = calculo[1]
    x = x / calculo["A4"]

    

    if x != 0:
        
        M = calculo['9']
        Cmat = calculo['3']
        CMod = calculo['4']
        CostoNeto = calculo['3'] + calculo['4'] + calculo['5']
        CinvMasCfij = calculo['8']
        CfinCinv = calculo['6']
        D = calculo['11']
        TLPT = calculo['2']
        CfijoOrden = calculo['8']
        Canalisis = calculo['10']
        Canalisis = Canalisis.iloc[0]
        Cm = 0
        Cg = 0
        try:
            if (D != 0.0) or (D is not None) or (D is not "NaN"):
                Cm = ((x-(math.ceil(x/TLPT)*M))/2)*(Cmat + CMod)*(CfinCinv)*((x-(math.ceil(x/TLPT)*M))/D)
                # Cm = ((x-M)/2)*(Cmat + CMod)*(CfinCinv)
            else:
                Cm = 0
        except Exception:
            print(Exception)
            pass

        
        
        # Cm = ((x-M)/2)*(Cmat+CMod)*(0.06)
        Cg = (CfijoOrden + Canalisis) * math.ceil(x/TLPT) +M  * CostoNeto *math.ceil(x/TLPT)
        # Cg = ((CfijoOrden + Canalisis) * math.ceil(x/TLPT) * (D+((D/x)*math.ceil(x/TLPT)*M))/x) + M * (Cmat + CMod)
        Ct = Cm + Cg
        
    else:
        Ct=0
    return Ct

def calcularCostoSciPy(calculo, x):#x,M,Cmat,CMod,CinvMasCfij, CfijoOrden, Canalisis, TLPT, D):
    """
    [17]: Presentacion: Cantidad de pastillas por unidad de presentación   
    """
    cantidad=int(calculo[17])
    x = x / cantidad
    
    TLPTGal = calculo[3] * .97
    if (x != 0):        
        TLPT = TLPTGal / cantidad
        
        M = calculo[6] # calculo['9']
        Cmat = calculo[7]
        CMod = calculo[8]
        CostoNeto = calculo[7] + calculo[8] + calculo[9]
        # CinvMasCfij = calculo[10]
        CfinCinv = calculo[12]
        D = calculo[15]
        # TLPT = x*cantidad #calculo[11]
        CfijoOrden = calculo[10]
        Canalisis = calculo[13]
        # Canalisis = Canalisis.iloc[0]
        Cm = 0
        Cg = 0
        try:
            if (D != 0.0) or (D is not None) or (D is not "NaN"):
                Cm = ((x-(math.ceil(x/TLPT)*M))/2)*(Cmat + CMod)*(CfinCinv)*((x-(math.ceil(x/TLPT)*M))/D)
                # Cm = ((x-M)/2)*(Cmat + CMod)*(CfinCinv)
            else:
                Cm = 0
        except Exception:
            print(Exception)
            pass

        
        
        # Cm = ((x-M)/2)*(Cmat+CMod)*(0.06)
        Cg = (CfijoOrden + Canalisis) * math.ceil(x/TLPT) +M  * CostoNeto *math.ceil(x/TLPT)
        # Cg = ((CfijoOrden + Canalisis) * math.ceil(x/TLPT) * (D+((D/x)*math.ceil(x/TLPT)*M))/x) + M * (Cmat + CMod)
        Ct = Cm + Cg
        
    else:
        Ct=0
    return Ct



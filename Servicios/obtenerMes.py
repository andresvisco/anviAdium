# - *- coding: utf- 8 - *-
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from listaColumnas import ObtenerColumnas
from listaColumnas import ObtenerColumnasCuanto
import sys
import numpy as np
from datetime import datetime
from datetime import timedelta
import math

quiebre = "QUIEBRA: 202007 Producir: 202005 - Ya Cubierto: 1.0 - FaltaCubrir: 21"
globalProducir = ""

def ObtenerCuandoProducirMenor(quiebre):
        dfQuiebreCuando = quiebre.to_frame()
        dfQuiebreCuando['Cuando'] = dfQuiebreCuando.Quiebre.str[26:32]
        dfQuiebreCuandoFiltrado = dfQuiebreCuando[dfQuiebreCuando.Cuando != 'Cubier']
        dfOrdenado = dfQuiebreCuandoFiltrado['Cuando'].sort_values(ascending=True)
        dfOrdenadoQuiebre = dfOrdenado.head(1).iat[0]
        if int(dfOrdenadoQuiebre) < 201901 : # _PREGUNTA_ Por que esta fecha?
                dfOrdenadoQuiebre = 201902
                pass

        

        return dfOrdenadoQuiebre



def ObtenerMesesFuturos(dfMeses, linea, VU, CME,BUFFER, CM, LTP, Maximo, QuiebreMenor):
        if(CME=="-"):
                CME=0
        else:
                CME = CME
        if(CME is None):
                CME = 0
        

        CuandoProducir =(CM + LTP) * 30
        if(math.isnan(CuandoProducir)):
                CuandoProducir=0
        else:
                CuandoProducir = CuandoProducir
        if(Maximo is None or str(Maximo).isdecimal() != True):
                Maximo = 0
        else:
                Maximo = Maximo
        if(math.isnan(VU)):
                VU=0
        else:
                VU=VU
        if(math.isnan(BUFFER)):
                BUFFER=0
        else:
                BUFFER=BUFFER

        dfQuiebre = pd.DataFrame(dfMeses)
        dfQuiebre.reset_index(inplace=True)        
        col = ["Mes","Filtro"]
        dfQuiebre.columns=col
        dfQuiebreFilter = dfQuiebre[dfQuiebre.Filtro=='-']# dfQuiebre.loc[dfQuiebre['Filtro']=="-"]
        result = dfQuiebreFilter.empty
        valorRetorno = ""
        valorRetornoResta = ""
        delta = ""
        strQuiebre= ""
        strProducir=""
        MesesCubiertos = ""
        faltan=""
        if(result!=True):
                dfQuiebreSort = dfQuiebreFilter.sort_values(by='Mes', ascending=True)
                dfQuiebreSortHead = dfQuiebreSort.head(1)
                valorRetorno =QuiebreMenor #dfQuiebreSortHead['Mes'].iat[0]
                valorRetorno1 = valorRetorno[:4]
                valorRetorno2 = valorRetorno[4:].rstrip()
                valorString = str(valorRetorno1) + "-" + str(valorRetorno2)
                quiebre = datetime.strptime(valorString, '%Y-%m')
                producir = quiebre - timedelta(days=CuandoProducir)
                delta = quiebre - producir
                strQuiebre = str(quiebre).replace("-","")[:6]
                strProducir= str(producir).replace("-","")[:6]
                
                MesesCubiertos = ((delta.days)/30) - 1
                faltan = int(VU) - int(CME) - int(BUFFER) - int(MesesCubiertos)

                
        else:
                quiebre = "N/A"
                producir = "N/A"
            
        
        
        return faltan

def ObtenerMesesQuiebreMenor(QuiebreInt):
        dfQuiebreCuando = QuiebreInt.to_frame()
        dfQuiebreCuando['QuiebreMenor'] = dfQuiebreCuando.QuiebreInt
        
        dfOrdenado = dfQuiebreCuando['QuiebreMenor'].dropna().sort_values(ascending=True).head(1).iat[0]
        

        return dfOrdenado


def ObtenerMesesQuiebreInt(quiebre):
        largoCadena = len(quiebre)
        valorRetorno = ""
        if(largoCadena>65):
                valorRetorno = str(quiebre[9:16]).rstrip()
        else:
                valorRetorno = np.nan
        return(valorRetorno)

def ObtenerMesesQuiebre(dfMeses, linea, VU, CME,BUFFER, CM, LTP, Maximo ):
       
        if(CME=="-"):
                CME=0
        else:
                CME = CME
        if(CME is None):
                CME = 0
        

        CuandoProducir = (CM + LTP) * 30
        if(math.isnan(CuandoProducir)):
                CuandoProducir=0
        else:
                CuandoProducir = CuandoProducir
        if(Maximo is None or str(Maximo).isdecimal() != True):
                Maximo = 0
        else:
                Maximo = Maximo
        if(math.isnan(VU)):
                VU=0
        else:
                VU=VU
        if(math.isnan(BUFFER)):
                BUFFER=0
        else:
                BUFFER=BUFFER

        dfQuiebre = pd.DataFrame(dfMeses)
        dfQuiebre.reset_index(inplace=True)        
        col = ["Mes","Filtro"]
        dfQuiebre.columns=col
        listaFiltro = [0,'-']
        dfQuiebreFilter = dfQuiebre[dfQuiebre.Filtro=='-']# dfQuiebre.loc[dfQuiebre['Filtro']=="-"]
        # dfQuiebreFilter = dfQuiebre[dfQuiebre.Filtro.isin(listaFiltro)]# dfQuiebre.loc[dfQuiebre['Filtro']=="-"]
        result = dfQuiebreFilter.empty
        valorRetorno = ""
        valorRetornoResta = ""
        delta = ""
        strQuiebre= ""
        strProducir=""
        MesesCubiertos = ""
        faltan=""
        if(result!=True):
                dfQuiebreSort = dfQuiebreFilter.sort_values(by='Mes', ascending=True)
                dfQuiebreSortHead = dfQuiebreSort.head(1)
                valorRetorno = dfQuiebreSortHead['Mes'].iat[0]
                valorRetorno1 = valorRetorno[:4]
                valorRetorno2 = valorRetorno[4:]
                valorString = str(valorRetorno1) + "-" + str(valorRetorno2)
                quiebre = datetime.strptime(valorString, '%Y-%m')
                producir = quiebre - timedelta(days=CuandoProducir)
                delta = quiebre - producir
                strQuiebre = str(quiebre).replace("-","")[:6]
                strProducir= str(producir).replace("-","")[:6]
                
                MesesCubiertos = ((delta.days)/30) - 1
                faltan = int(VU) - int(CME) - int(BUFFER) - int(MesesCubiertos)

                
        else:
                quiebre = "N/A"
                producir = "N/A"
            
        # if(valorRetorno!= "N/A"):
        #     cadenaRetorno = "Estimar: " + str(CuandoProducir) + " Mes antes"
        # else:
        #     cadenaRetorno = ""
        quiebreComparar = strProducir[4:6]

        if (quiebreComparar == "01"):
            quiebreComparar = "02"
            strProducir = str(strProducir[:4] + str(quiebreComparar))


        
        
            
        varStrRetorno = str("QUIEBRA: " + str(strQuiebre) + " Producir: " + str(strProducir) + " - Ya Cubierto: " + str(MesesCubiertos) + " - FaltaCubrir: " + str(faltan))
        
        return varStrRetorno
# quiebreTxt = "Producir: 202011"
# quiebreComparar = quiebreTxt[14:16]

# if (quiebreComparar == "01"):
#     quiebreComparar = "02"
#     quiebreTxt = str(quiebreTxt[:14] + str(quiebreComparar))
#     pass
# print(quiebreTxt)
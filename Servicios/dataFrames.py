import pandas as pd
import os
from flask import Flask
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


app=Flask(__name__)



alldfPercepPadron = []
alldfRetPadron=[]
statusP=None
stautsR=None

columnas = [
        'Tipo',
        'FechaPublicacion',
        'FechaVigenciaDesde',
        'FechaVigenciaHasta',
        'NumerodeCuit',
        'Tipo-Contr_Insc',
        'Marca-alta sujeto',
        'Marca-alicuota',
        'Alicuota-Percepción',
        'Alicuota-Retención',
        'Nro-GrupoPercepción',
        'Nro-GrupoRetención',
        'RazonSocial']


def cargaRealP(path):
    return(pd.read_csv(path, sep=";", header=None ,names=columnas, index_col='NumerodeCuit'))


def cargaRealR(path):
    return(pd.read_csv(path, sep=";", header=None ,names=columnas, index_col='NumerodeCuit'))




global pdPadronPercepConcat
global pdPadronRetConcat
archivo = "/home/viscoandres/mysite/PADRONES DE RETENCIONES IIBB/"
pathRel = os.path.abspath(os.path.dirname(archivo))
path1= pathRel + '/PadronRGSPer022020.txt'
path1_1= pathRel + '/PadronRGSPer0220201.txt'
path1_2= pathRel + '/PadronRGSPer0220202.txt'
path2=pathRel + '/PadronRGSRet022020.txt'
path2_1=pathRel + '/PadronRGSRet0220201.txt'
# path1='PADRONES DE RETENCIONES IIBB/PadronRGSPer022020.txt'
# path1_1='PADRONES DE RETENCIONES IIBB/PadronRGSPer0220201.txt'
# path1_2='PADRONES DE RETENCIONES IIBB/PadronRGSPer0220202.txt'
# path2='PADRONES DE RETENCIONES IIBB/PadronRGSRet022020.txt'
# path2_1='PADRONES DE RETENCIONES IIBB/PadronRGSRet0220201.txt'
# path3='PADRONES DE RETENCIONES IIBB/ARDJU008022020.txt'
# path3_1='PADRONES DE RETENCIONES IIBB/ARDJU0080220201.txt'

listaPathsPercep=[path1, path1_1, path1_2]
listaPathsRet=[path2, path2_1]

for item in listaPathsPercep:
    # thread = threading.Thread(target=cargaRealP, args=(item,))
    # thread.start()
    # while statusP is None:
    #     pass
    alldfPercepPadron.append(cargaRealP(item))



for item in listaPathsRet:
    # thread = threading.Thread(target=cargaRealR, args=(item,))
    # thread.start()
    # while stautsR is None:
    #     pass
    # largo = "hola"
    alldfRetPadron.append(cargaRealR(item))



# dfPadronPercep = cargaReal(path1)
# dfPadronPercep_1 = cargaReal(path1_1)
# dfPadronPercep_2 = cargaReal(path1_2)
# dfPadronRet = cargaReal(path2)
# dfPadronRet_1 = cargaReal(path2_1)

# alldfPercepPadron = [dfPadronPercep, dfPadronPercep_1, dfPadronPercep_2]
# alldfRetPadron = [dfPadronRet, dfPadronRet_1]

pdPadronPercepConcat = pd.concat(alldfPercepPadron)
pdPadronRetConcat = pd.concat(alldfRetPadron)

def darInfo():
    return pdPadronPercepConcat, pdPadronRetConcat

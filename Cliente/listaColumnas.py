import pandas as pd
import sys
from datetime import datetime
from datetime import timedelta
import logging
import logginProcess
from collections import OrderedDict
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
# dataFrameMesesCompuestos=""


def obtenerListaES(fechaInicioPlan):
    if not fechaInicioPlan:
        fechaInicioPlan = "202001"
    
    fechaInicioPlan = str(fechaInicioPlan + "01")
    mesInicioAnoActual='09'
    anoActual=str(date.today().year)
    # fechaNormalizadaInicio = datetime(int(anoActual),int(mesInicioAnoActual),1)
    fechaNormalizadaInicio = datetime(int(fechaInicioPlan[:4]), int(fechaInicioPlan[4:-2]), 1)
    fechaNormalizadaFinTem = fechaNormalizadaInicio
    fechaNormalizadaFinTem += relativedelta(months=23)
    anoFin = fechaNormalizadaFinTem.year
    mesFin = fechaNormalizadaFinTem.month

    fechaNormalizadaFinCompiled = datetime(anoFin, mesFin, 1)
    listaes = pd.date_range(str(fechaNormalizadaInicio),str(fechaNormalizadaFinTem), freq='MS').strftime("%Y%m").to_list()
    

    #__PREGUNTA__ Por qué está en duro una lista de meses de feb-2019 a feb-2020 ?
    # listaes = ["201902","201903","201904","201905","201906","201907","201908","201909","201910","201911","201912","202001","202002","202003","202004","202005","202006","202007","202008","202009","202010","202011","202012","202101","202102"]
    # listaes=[]
    
    return(listaes)


listaCalculoCosto = ["A0","A5","1","22","9","3","4","5","8","2","6","10","11","CuantoPlanificar","A4","20"] #valores temporarios
listaMesesProducirValores = ["A97","A98","A99","A100","A101","A102","A103","A104","A105","A106","A107","A108","A109","A110","A111","A112","A113","A114","A115","A116","A117","A118","A119","A120"]
listaes = obtenerListaES(fechaInicioPlan = None) 
d = {'ANOMESNorm':listaes,'COLUMNAS':listaMesesProducirValores}
data_tuples = list(zip(listaes,listaMesesProducirValores))
dataFrameMesesCompuestos = pd.DataFrame(data_tuples, columns=['ANOMESNorm','COLUMNAS'])

def listaColumnasCalculoCosto():
    return listaCalculoCosto
def ObtenerColumnas(fechaInicioPlan):
    if len(obtenerListaES(fechaInicioPlan))==0:
        logginProcess.logger.error("La lista de meses se encuentra vacía")
    else:
        return obtenerListaES(fechaInicioPlan)#listaes
        
def ObtenerColumnasCuanto(fromColumna, toColumna):
    try:
        mesesList = []
        fechas = ""
        sumaMeses = 0
        # if( len(fromColumna) >= 53):
        anoQuiebre = int(fromColumna[:4])
        mesQuiebre = fromColumna[4:6]
        fechaQuiebre = str(anoQuiebre) + "-" + str(mesQuiebre)
        quiebre = datetime.strptime(fechaQuiebre, '%Y-%m')
        delta = quiebre + timedelta(days=(toColumna*30))
        deltaTocolumn = str(delta).replace("-","")[:6]
        fechaCompuestaFromTo = str(anoQuiebre) + str(mesQuiebre)
        tofecha = int(deltaTocolumn)
        fechas = str(tofecha) + " - " + str(fechaCompuestaFromTo)
        meses = dataFrameMesesCompuestos[(dataFrameMesesCompuestos['ANOMESNorm']<=str(int(tofecha))) & (dataFrameMesesCompuestos['ANOMESNorm']>=str(fechaCompuestaFromTo))]
        mesesList = meses['COLUMNAS'].values.tolist()
        if len(mesesList)==0:
            logginProcess.logger.error("La lista de meses se encuentra vacía en la composicion de fechas")
        else:
            return mesesList
    except Exception as e:
        for item in e.args:
            errorVal = str(item)
            logginProcess.logger.error(errorVal)
    # textoQuiebre ="QUIEBRA: 202004 - Estimar: 1 Mes antes"
# ObtenerCuanto = ObtenerColumnasCuanto(textoQuiebre,4)
# print(ObtenerCuanto)

import json
from ejecutarRevision import mainProcesoRevision, EjecutarRevision
from fromExcel import mainProceso
import pandas as pd
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():

    tipoEjecucion = request.args.get('tipo')
    fechaInicioPlan = str(request.args.get('fechaInicio'))[:6]

    req_data = request.get_data()
    jsonData = json.loads(req_data)[1]
    jsonDataColumns = json.loads(req_data)[0]
    dfUsar = pd.DataFrame.from_records(jsonData)
    dfUsar.columns=jsonDataColumns
    listafinal = list(dict.fromkeys(dfUsar.A3.values.tolist()))
    dfProcesar = list()

    if tipoEjecucion == 'REVISION':
        dfRevisionResult = EjecutarRevision(dfUsar)
        dfResultMaximos = mainProcesoRevision(dfUsar, fechaInicioPlan)
        resultado = str(dfRevisionResult) + " - " + str(dfResultMaximos)
        return(resultado)

    else:
        for item in listafinal:
            dfUsarFiltrado = dfUsar[dfUsar.A3 == str(item)]
            dfUsarFiltradoJson = mainProceso(dfUsarFiltrado,0, fechaInicioPlan)
            dfProcesar.append(dfUsarFiltradoJson)

        dfReturn = pd.concat(dfProcesar)
        dfReturn.reset_index(inplace=True)
        dfReturnJson = dfReturn.to_json()

        return(dfReturnJson)

    # dfProcesar = mainProceso(dfUsar, 0)
    # dfProcesar.reset_index()
    # dfProcesarJson = dfProcesar.to_json()
    # return(dfProcesarJson)

    # return str(req_data)

if __name__=='__main__':
    app.run()
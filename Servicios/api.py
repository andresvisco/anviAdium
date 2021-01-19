from flask import Flask
from flask import request
import dataFrames
from flask import jsonify

app=Flask(__name__)
global pdPadronPercepConcat, pdPadronRetConcat

@app.route('/<consulta>', methods=["GET"])
def ejecutarBusqueda(consulta):
    global pdPadronPercepConcat, pdPadronRetConcat
    opEracion=request.args.get('operacion', default="P", type=str)
    if opEracion == "":
        opEracion = "P"
    cuit=request.args.get('cuit', default=30699038896, type=int)
    pdPadronPercepConcat, pdPadronRetConcat = dataFrames.darInfo()
    respuesta = main(cuit, opEracion)

    return(jsonify(
    operacion=opEracion,
    FechaDesde=respuesta[0][1],
    AlicuotaPercepcionRetencion=respuesta[0][3],
    cuit=cuit)
    )
    # return(render_template('index.html',
    #     FechaDesde=respuesta[0][1],
    #     FechaHasta=respuesta[0][2],
    #     AlicuotaPercepcion=respuesta[0][3],
    #     AlicuotaRetencion=respuesta[0][4],
    #     operacionTipo=respuesta[0][0],
    #     cuit=cuit))


def main(valorCuit, op):
    global pdPadronPercepConcat, pdPadronRetConcat
    argumentoFiltro= int(valorCuit) #args.cuit
    tipodeOperacion = op

    filter_dfPercep = pdPadronPercepConcat[pdPadronPercepConcat.index == argumentoFiltro]
    filter_dfRet = pdPadronRetConcat[pdPadronRetConcat.index == argumentoFiltro]
    # print("########## NUMERO CUIT: "+ str(argumentoFiltro) + "##########")
    if(tipodeOperacion=='P'):
        return(filter_dfPercep[['Tipo','FechaVigenciaDesde','FechaVigenciaHasta','Alicuota-Percepción']].values.tolist())
        # print("########## PERCEPCION ##########")
        # print(filter_dfPercep[['Tipo','FechaVigenciaDesde','FechaVigenciaHasta','Alicuota-Percepción','Alicuota-Retención']])
        # print("                                         ")
    if(tipodeOperacion=='R'):
        return(filter_dfRet[['Tipo','FechaVigenciaDesde','FechaVigenciaHasta','Alicuota-Percepción']].values.tolist())
        # print("                                         ")
        # print("########## RETENCION ##########")
        # print(filter_dfRet[['Tipo','FechaVigenciaDesde','FechaVigenciaHasta','Alicuota-Percepción','Alicuota-Retención']])


    # dfPadron2 = pd.read_csv(path2, sep=";")
    # dfPadron3 = pd.read_csv(path2, sep=";")

    # listaPadrones = [dfPadron1, dfPadron2, dfPadron3]

    # dfPadron1.columns = columnas
    # print(dfPadron1)
    # for padron in listaPadrones:
    #     print(padron.head(10))
if __name__=='__main__':
    # print("inicio")
    # thread = threading.Thread(target=cargarDF)
    # thread.start()
    # print("Entró")

    # while result is None:
    #     pass
    # print("paso")
    app.run()



# path1='PADRONES DE RETENCIONES IIBB/PadronRGSPer022020.txt'
#     path1_1='PADRONES DE RETENCIONES IIBB/PadronRGSPer0220201.txt'
#     path1_2='PADRONES DE RETENCIONES IIBB/PadronRGSPer0220202.txt'
#     path2='PADRONES DE RETENCIONES IIBB/PadronRGSRet022020.txt'
#     path2_1='PADRONES DE RETENCIONES IIBB/PadronRGSRet0220201.txt'
#     # path3='PADRONES DE RETENCIONES IIBB/ARDJU008022020.txt'
#     # path3_1='PADRONES DE RETENCIONES IIBB/ARDJU0080220201.txt'

#     columnas = [
#         'Tipo',
#         'FechaPublicacion',
#         'FechaVigenciaDesde',
#         'FechaVigenciaHasta',
#         'NumerodeCuit',
#         'Tipo-Contr_Insc',
#         'Marca-alta sujeto',
#         'Marca-alicuota',
#         'Alicuota-Percepción',
#         'Alicuota-Retención',
#         'Nro-GrupoPercepción',
#         'Nro-GrupoRetención',
#         'RazonSocial']


#     dfPadronPercep = pd.read_csv(path1, sep=";", header=None ,names=columnas, index_col='NumerodeCuit')
#     dfPadronPercep_1 = pd.read_csv(path1_1, sep=";", header=None ,names=columnas, index_col='NumerodeCuit')
#     dfPadronPercep_2 = pd.read_csv(path1_2, sep=";", header=None ,names=columnas, index_col='NumerodeCuit')
#     dfPadronRet = pd.read_csv(path2, sep=";", header=None ,names=columnas, index_col='NumerodeCuit')
#     dfPadronRet_1 = pd.read_csv(path2_1, sep=";", header=None ,names=columnas, index_col='NumerodeCuit')

#     alldfPercepPadron = [dfPadronPercep, dfPadronPercep_1, dfPadronPercep_2]
#     alldfRetPadron = [dfPadronRet, dfPadronRet_1]

#     pdPadronPercepConcat = pd.concat(alldfPercepPadron)
#     pdPadronRetConcat = pd.concat(alldfRetPadron)
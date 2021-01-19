import pandas as pd
listaMesesAjuste=["02","03","04","05","06","07","08","09","10"]
def ObtenerColumnasAjuste():
    return listaMesesAjuste

def ObtenerAjuste(quiebre, mesesAjuste):
    valor=""
# _PREGUNTA_ qué son los mesesAjuste
    mesQuiebre = quiebre[13:15]
    mesQuiebreInt = int(mesQuiebre) - 1
    mesQuiebre = str(mesQuiebreInt)
    if(len(mesQuiebre)<2):
        mesQuiebre = "0" + str(mesQuiebreInt)
    else:
        mesQuiebre = str(mesQuiebreInt)
    if(int(mesQuiebre)<11 and int(mesQuiebre) > 1):

        print(type(mesesAjuste))
        dfMesAjusteFrame = mesesAjuste.to_frame()
        dfMesAjusteTransposed = dfMesAjusteFrame.T
        dfMesAjusteTransposed = dfMesAjusteTransposed[[mesQuiebre]]
        dfMesAjusteTransposed.reset_index()
        valor=dfMesAjusteTransposed[[mesQuiebre]].values[0][0]
    else:
        valor =""
    return valor
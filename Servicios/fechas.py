import datetime
from dateutil.relativedelta import relativedelta

def corregirFecha(fecha):
    anioCorregida = fecha[0:4]
    mesCorregida = fecha[4:6]
    diaCorregida = '01'
    # fecha = anioCorregida + "-" + mesCorregida + "-01 08:15:27.243860"
    fecha = datetime.datetime(int(anioCorregida),int(mesCorregida),int(diaCorregida) )
    return fecha
    

def fechaFormatear(fecha, formato):
    
    fechaCorrect = corregirFecha(fecha)
    retorno = datetime.datetime.strftime(fechaCorrect, formato)
    
    return str(retorno)

def incrementarMesFecha(fecha,mesesIncremento):
    fechaCorrect = corregirFecha(fecha)
    formato = '%Y%m'
    fechaReturn = fechaCorrect + relativedelta(months=mesesIncremento)
    retorno = datetime.datetime.strftime(fechaReturn, formato)
    return retorno

# fecha = '201906'
# fechaForm = fechaFormatear(fecha, '%Y%m')
# print(fechaForm)
# print(incrementarMesFecha(fechaForm,2))
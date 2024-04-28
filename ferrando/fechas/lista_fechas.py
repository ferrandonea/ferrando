import pandas as pd
from datetime import datetime
from holidays import country_holidays


def lista_fechas(start_date: str, end_date:str) -> list[datetime]:
    """
    Obtiene lista de fechas entre dos fechas
    TODO: casi todo, copiar función local
    """
    return [fecha.to_pydatetime() for fecha in pd.date_range(start=start_date, end=end_date)]

def chequea_feriado_chile(input_date: datetime, sabado_feriado = True) :
    """ Chequea si es feriado usando libreria holidays
    https://python-holidays.readthedocs.io/en/latest/index.html
    Además ve los sabados y domingos
    """
    feriados_chile = country_holidays("CL")
    dia_semana = input_date.weekday()
    
    if dia_semana == 6 or (dia_semana == 5 and sabado_feriado):
        return True
    return input_date in feriados_chile




if __name__ == "__main__":
    inicio = "2024-01-01"
    fin = "2025-01-01"

    print (lista_fechas(inicio, fin))
    print ("###")
    for fecha in lista_fechas(inicio, fin):
        print (fecha, chequea_feriado_chile(fecha, sabado_feriado=True), fecha.strftime("%a"))


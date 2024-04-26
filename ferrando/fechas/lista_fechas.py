import pandas as pd
from datetime import datetime


def lista_fechas(start_date: str, end_date:str) -> list[datetime]:
    """
    Obtiene lista de fechas entre dos fechas
    TODO: casi todo, copiar función local
    """
    for fecha in pd.date_range(start=start_date, end=end_date):
        print (fecha, type(fecha), fecha.to_pydatetime(), type(fecha.to_pydatetime()))
    

if __name__ == "__main__":
    inicio = "2024-01-01"
    fin = "2024-10-01"

    print (lista_fechas(inicio, fin))


"""
Este módulo proporciona funcionalidades para calcular días laborales en Chile y en la Bolsa de Nueva York (NYSE),
excluyendo feriados específicos y fines de semana. Utiliza la biblioteca pandas para la manipulación de fechas y
la biblioteca holidays (https://python-holidays.readthedocs.io/en/latest/api.html) para acceder a los feriados de Chile y de la NYSE.

El módulo define una clase, FinancialHolidays, que extiende la clase de feriados de Chile para incluir feriados
financieros adicionales. También configura objetos CustomBusinessDay para calcular rangos de días laborales
que excluyen tanto feriados como fines de semana en ambos contextos financieros.

Ejemplos de uso:
- Generar un rango de fechas de días laborales en Chile que excluyan feriados y fines de semana.
- Generar un rango de fechas de días laborales para la NYSE que excluyan sus feriados.

El módulo es útil para sincronizar actividades y proyecciones
con días laborales reales en estos dos ámbitos geográficos y financieros.
"""
from datetime import datetime, date
from typing import Iterator, Optional

from holidays.countries import CL
from holidays import NYSE
import numpy as np
import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay

from generales import named_weekday


# Configuración inicial de fechas
first_date: datetime = datetime(1990, 1, 1)  # Fecha inicial
last_date: datetime = datetime(2050, 1, 1)  # Fecha final
included_years: Iterator[int] = range(
    first_date.year, last_date.year + 1
)  # iterador de años
current_date: datetime = datetime.now()  # Fecha actual

# Verificación para asegurar cobertura de datos hasta al menos 3 años en el futuro
if current_date.year + 3 > max(included_years):
    print(f"OJO: SOLO HAY DATOS HASTA {max(included_years)}")
    print("--> Modificar variable *last_date*")


class FinancialHolidays(CL):
    """
    Clase para manejar feriados financieros en Chile, incluyendo un feriado bancario el 31 de diciembre.
    Extiende la clase CL de la librería holidays para incluir feriados específicos financieros.
    """

    def _populate(self, year: int) -> None:
        """Popula la lista de feriados para el año dado, incluyendo feriados estándares y personalizados."""
        super()._populate(
            year
        )  # Llama a la función de la clase base para obtener feriados estándar de Chile
        self[date(year, 12, 31)] = "Feriado bancario"  # Añade el feriado bancario


# Creación de objetos CustomBusinessDay para Chile y NYSE, esto es para pandas
chile_financial_days: CustomBusinessDay = CustomBusinessDay(
    holidays=FinancialHolidays(years=list(included_years))
)
nyse_financial_days: CustomBusinessDay = CustomBusinessDay(
    holidays=NYSE(years=list(included_years))
)


def is_trading_day(
    input_date: datetime, calendar: Optional[CustomBusinessDay] = chile_financial_days
) -> bool:
    """
    Verifica si una fecha dada es un día de trading, es decir, no es ni fin de semana ni feriado.

    Args:
    input_date (datetime): La fecha a verificar.
    calendar (CustomBusinessDay, optional): El calendario que contiene los feriados y los días no laborables. Por defecto asume Chile

    Returns:
    bool: False si la fecha es un fin de semana o un feriado, True en caso contrario.
    """
    # Verificar si es fin de semana
    if input_date.weekday() > 4:  # 5 y 6 son sábado y domingo
        return False
    # Verificar si es un feriado
    return not (np.datetime64(input_date) in calendar.holidays)

def add_trading_days(
    input_date: datetime,
    days: int,
    calendar: Optional[CustomBusinessDay] = chile_financial_days,
) -> datetime:
    """
    Agrega o sustrae un número específico de días de trading a una fecha dada. Los días de trading se calculan
    excluyendo los fines de semana y cualquier feriado especificado en el calendario proporcionado. Esta función
    permite moverse hacia adelante o hacia atrás en el calendario.

    Args:
        input_date (datetime): La fecha a partir de la cual se agregarán o sustraerán los días de trading.
        days (int): El número de días de trading que se deben agregar (positivo) o sustraer (negativo).
        calendar (Optional[CustomBusinessDay]): Un calendario de días hábiles que define los feriados y los días de trading.
            Si no se proporciona, se utiliza un calendario predeterminado que debe estar definido previamente.

    Returns:
        datetime: La nueva fecha después de agregar o sustraer los días de trading especificados.

    Example:
        >>> add_trading_days(datetime(2023, 5, 1), 5)
        datetime.datetime(2023, 5, 8, 0, 0)
        >>> add_trading_days(datetime(2023, 5, 8), -3)
        datetime.datetime(2023, 5, 3, 0, 0)
    """
    if days == 0:
        print(
            f"WARNING: {add_trading_days.__name__}: OJO QUE {input_date:%Y-%m-%d} PUEDE SER FERIADO"
        )
        return input_date
    return (input_date + days * calendar).to_pydatetime()

def range_trading_days(
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    periods: Optional[int] = None,
    freq: str | CustomBusinessDay = chile_financial_days,
    normalize: bool = True,
) -> list[datetime]:
    """
    Genera un rango de días hábiles de trading entre dos fechas, o a partir de una fecha dada durante un número de períodos.

    Parámetros:
    start (datetime, opcional): Fecha de inicio del rango. Si es None, se deben proporcionar 'end' y 'periods'.
    end (datetime, opcional): Fecha de fin del rango. Si es None, se deben proporcionar 'start' y 'periods'.
    periods (int, opcional): Número de períodos a generar. Puede ser negativo para generar fechas hacia atrás.
    freq (str | CustomBusinessDay, opcional): Cadena de frecuencia o instancia de CustomBusinessDay que define los días hábiles.
    normalize (bool, opcional): Si se normaliza o no las fechas de inicio/fin a medianoche.

    Devoluciones:
    list[datetime]: Índice de fechas que representa los días de trading dentro del rango especificado.

    Errores:
    ValueError: Si el número de parámetros especificados es incorrecto o si falta algún parámetro requerido.

    Ejemplos:
    >>> range_trading_days(start=datetime(2023, 1, 1), periods=5)
    DatetimeIndex(['2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06'], dtype='datetime64[ns]', freq='B')
    """
    # Validación de los parámetros de entrada
    params = [start, end, periods]
    #Chequea que haya al menos 2 de 3 de los params
    if sum(p is not None for p in params) != 2:
        raise ValueError(
            "Se deben especificar exactamente dos de los parámetros 'start', 'end' y 'periods'."
        )

    if periods is not None and periods < 0:
        start, end = end, start  # Invertir start y end para manejar períodos negativos
        periods = abs(periods)  # Tomar el valor absoluto de los períodos

    # Generación del rango de fechas
    result = pd.date_range(
        start=start, end=end, periods=periods, freq=freq, normalize=normalize
    )

    # Como 'freq' puede ser un CustomBusinessDay que maneja feriados, el resultado ya debería considerar los días no comerciales.
    # Convierte el resultado a datetime y una lista
    return result.to_pydatetime().tolist()

def count_trading_days(start: datetime, end: datetime, calendar: Optional[CustomBusinessDay] = chile_financial_days) -> int:
    """
    Calcula el número de días de trading entre dos fechas, excluyendo fines de semana y feriados.

    Args:
    start (datetime): La fecha de inicio del período.
    end   (datetime): La fecha de fin del período.
    calendar (Optional[CustomBusinessDay]): Un calendario de días hábiles que define los feriados y los días de trading.
                                            Si no se proporciona, se utiliza un calendario predeterminado que debe estar definido previamente.


    Returns:
    int: El número de días de trading entre las dos fechas, sin incluir el inicial.
    """

    # Generar el rango de fechas de trading entre las dos fechas
    trading_days = range_trading_days(start = start, end=end, freq=calendar)
    # Contar el número de días en el rango generado
    return len(trading_days)-1



if __name__ == "__main__":
    # Genera y muestra 10 próximos días laborales en Chile excluyendo feriados y fines de semana
    for d in pd.date_range(
        start=current_date, periods=10, freq=chile_financial_days, normalize=True
    ):
        print(d.to_pydatetime().date(), d.to_pydatetime().weekday())

    print("PRUEBO NYSE")  # Espacio entre las salidas de dos series de fechas

    # Genera y muestra 10 próximos días laborales según el calendario de la NYSE
    for d in pd.date_range(
        start=current_date, periods=10, freq=nyse_financial_days, normalize=True
    ):
        print(d.to_pydatetime().date(), d.to_pydatetime().weekday())

    print("PRUEBO is_trading")  # Espacio entre las salidas de dos series de fechas

    for i in range(1, 10):
        fecha = datetime(2024, 5, i)
        print(
            f"{i=} | {fecha.date() =} | {fecha.weekday() = } | {named_weekday(fecha, long=False) = } | {is_trading_day(fecha) = }"
        )

    print("PRUEBO add_trading")  # Espacio entre las salidas de dos series de fechas

    fecha = datetime(2024, 5, 2)
    for i in range(-7, 7):
        print(f"{fecha = } | {i=} | {add_trading_days(fecha, days=i) = }")

    print("PRUEBA RANGOS")

    start = datetime(2024, 4, 26)
    end = None
    periods = 10
    print(f"{start = } {end = } {periods = }")
    print(range_trading_days(start, end, periods))

    start = datetime(2024, 4, 26)
    end = None
    periods = 10
    freq = nyse_financial_days
    print(f"{start = } {end = } {periods = } {freq = } NYSE")
    print(range_trading_days(start, end, periods, freq))

    start = datetime(2024, 4, 26)
    end = None
    periods = -10
    print(f"{start = } {end = } {periods = } {freq = } CHILE")
    print(range_trading_days(start, end, periods, freq))

    print ("PRUEBA TRADING DAYS LEN")
    start = datetime(2024, 4, 26)
    end = datetime(2024, 5, 6)
    print (count_trading_days(start=start, end= end))
    print (range_trading_days(start=start, end=end))
    

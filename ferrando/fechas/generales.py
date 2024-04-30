from datetime import datetime


def named_weekday(input_date: datetime, long: bool = True) -> str:
    """
    Obtiene el nombre del día de la semana (en inglés) para una fecha dada. Esto sirve más que nada para debug.

    Args:
    input_date (datetime): La fecha de la que se quiere obtener el nombre del día.
    long (bool, optional): Si es True, devuelve el nombre completo del día (e.g., 'Monday').
                           Si es False, devuelve la abreviatura (e.g., 'Mon').

    Returns:
    str: El nombre del día de la semana de la fecha dada.
    """
    date_format = "%A" if long else "%a"
    return input_date.strftime(date_format)

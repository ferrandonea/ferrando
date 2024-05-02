from datetime import datetime, date
from dateutil import parser
import pytz

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

def normalize_to_datetime(input_date: datetime | date | str) -> datetime:
    """
    Normaliza un input que puede ser datetime, date o string a un objeto datetime.

    Args:
        input_date (Union[datetime, date, str]): La fecha en formato datetime, date o string.

    Returns:
        datetime: El objeto datetime normalizado.

    Raises:
        ValueError: Si el input es un string y no puede ser parseado a datetime.

    Example:
        >>> normalize_to_datetime(datetime(2023, 1, 1, 12, 0))
        datetime.datetime(2023, 1, 1, 12, 0)
        >>> normalize_to_datetime(date(2023, 1, 1))
        datetime.datetime(2023, 1, 1, 0, 0)
        >>> normalize_to_datetime("2023-01-01 12:00")
        datetime.datetime(2023, 1, 1, 12, 0)
    """
    if isinstance(input_date, datetime):
        return input_date
    elif isinstance(input_date, date):
        return datetime(input_date.year, input_date.month, input_date.day)
    elif isinstance(input_date, str):
        try:
            return parser.parse(input_date)
        except ValueError:
            raise ValueError(f"El string '{input_date}' no se pudo parsear a datetime.")
    else:
        raise TypeError("El tipo de input proporcionado no es válido; debe ser datetime, date o string.")

def local_current_time(time_zone: str = "America/Santiago") -> datetime:
    """
    Devuelve la hora actual en la zona horaria especificada.

    Args:
    - time_zone (str): La zona horaria en la que se desea obtener la hora actual.
                       Por defecto es "America/Santiago".

    Returns:
    - datetime: Un objeto datetime que representa la hora actual en la zona horaria dada.

    Esta función utiliza la biblioteca pytz para manejar correctamente las zonas horarias.
    Se puede especificar cualquier zona horaria soportada por pytz para obtener la hora local correspondiente.
    """
    santiago_tz = pytz.timezone(time_zone)  # Obtener el objeto de zona horaria de pytz
    return datetime.now(santiago_tz)  # Devolver la hora actual en la zona horaria especificada

if __name__ == "__main__":
    # Ejemplos de uso:
    print(normalize_to_datetime(datetime.now()))  # datetime
    print(normalize_to_datetime(date.today()))  # date
    print(normalize_to_datetime("2023-01-01 15:30"))  # string
    print (local_current_time())

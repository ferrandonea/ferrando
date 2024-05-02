import random
from generales import remove_dots

def calculate_verification_digit(rut_sin_dv: int) -> str:
    """
    Calcula el dígito verificador de un RUT chileno utilizando el algoritmo del módulo 11.

    Args:
    - rut_sin_dv (int): El número del RUT sin el dígito verificador.

    Returns:
    - str: El dígito verificador del RUT.
    """
    # Convertir el RUT a una lista de enteros para facilitar el cálculo
    numeros = list(map(int, str(rut_sin_dv)))
    # Secuencia de multiplicadores según el algoritmo
    multiplicadores = [2, 3, 4, 5, 6, 7]
    # Iniciar sumatoria y el índice para los multiplicadores
    suma = 0
    multiplicador = 0

    # Recorrer los números del RUT de derecha a izquierda
    for numero in reversed(numeros):
        suma += numero * multiplicadores[multiplicador]
        multiplicador = (multiplicador + 1) % 6  # Ciclar el índice de multiplicadores

    # Calcular el módulo 11
    resto = suma % 11
    # Determinar el dígito verificador
    if resto == 1:
        return 'K'
    elif resto == 0:
        return '0'
    else:
        return str(11 - resto)


def is_dv_valid(full_rut: str) -> bool:
    """
    Valida un RUT chileno.

    Argumentos:
    - full_rut (str): El RUT completo en el formato '12345678-9' o '12345678-K'.

    Devuelve:
    - bool: Verdadero si el RUT es válido, Falso en caso contrario.
    """
    original_rut = full_rut
    full_rut = remove_dots(full_rut)  # Elimina los puntos del RUT para consistencia de formato

    try:
        rut_without_dv, dv = full_rut.split('-')
        calculated_dv = calculate_verification_digit(int(rut_without_dv))
        # Convierte ambos dígitos verificadores a mayúsculas para asegurar insensibilidad a mayúsculas/minúsculas
        return calculated_dv == dv.upper()
    except (ValueError, IndexError):
        # Si el RUT es incorrecto devuelve Falso
        print(f"Error: El RUT {original_rut} no es correcto")
        return False

def complete_rut(rut_without_dv: int | str) -> str:
    """
    Completa un número de RUT con su dígito verificador correspondiente.

    Args:
    - rut_without_dv (int | str): El número de RUT sin el dígito verificador, como entero o cadena.

    Returns:
    - str: El RUT completo en formato '12345678-K'.

    Raises:
    - ValueError: Si el input no puede ser convertido a un entero.

    Esta función convierte el input a entero, calcula el dígito verificador usando
    la función calculate_verification_digit y retorna el RUT completo con el formato adecuado.
    """
    rut_without_dv = int(rut_without_dv)  # Convertir a entero, fallará si el input no es un número válido
    dv = calculate_verification_digit(rut_without_dv)  # Calcular el dígito verificador
    return f"{rut_without_dv}-{dv}"  # Formatear y retornar el RUT completo

def format_rut(rut: str) -> str:
    """
    Formatea un RUT a un formato estandarizado con puntos y guión.

    Args:
    - rut (str): El RUT en cualquier formato, por ejemplo '12345678K' o '12.345.678-K'.

    Returns:
    - str: El RUT formateado en el estilo '12.345.678-K'.

    Esta función elimina puntos y guiones del RUT original, extrae el cuerpo y el dígito verificador,
    y luego formatea el cuerpo del RUT con puntos como separadores de miles.
    """
    rut = rut.replace('.', '').replace('-', '')  # Limpiar el RUT de puntos y guiones
    rut_body = rut[:-1]  # Extraer el cuerpo del RUT
    dv = rut[-1]  # Extraer el dígito verificador
    return f"{int(rut_body):,d}-{dv}".replace(',', '.')  # Formatear el cuerpo y retornar el RUT completo

def generate_random_valid_rut(min_seed: int = int(1e6), max_seed: int = int(27e6)) -> str:
    """
    Genera un número de RUT aleatorio válido dentro de un rango especificado.

    Args:
    - min_seed (int): El valor mínimo para el cuerpo del RUT. Default: 1,000,000.
    - max_seed (int): El valor máximo para el cuerpo del RUT. Default: 27,000,000.

    Returns:
    - str: Un RUT completo y válido en formato '12345678-K'.

    Esta función genera un cuerpo de RUT aleatorio dentro del rango especificado,
    calcula su dígito verificador y retorna el RUT completo.
    """
    import random  # Importar random para generar números aleatorios
    rut_body = random.randint(min_seed, max_seed)  # Generar un cuerpo de RUT aleatorio
    dv = calculate_verification_digit(rut_body)  # Calcular el dígito verificador para el cuerpo generado
    return f"{rut_body}-{dv}"  # Formatear y retornar el RUT completo


if __name__ == "__main__":
    # Ejemplo de uso
    rut = 12345670
    digito_verificador = calculate_verification_digit(rut)
    print(f"El dígito verificador del RUT {rut} es: {digito_verificador}")
    rut = 10689138
    digito_verificador = calculate_verification_digit(rut)
    print(f"El dígito verificador del RUT {rut} es: {digito_verificador}")
    rut = 9007586
    digito_verificador = calculate_verification_digit(rut)
    print(f"El dígito verificador del RUT {rut} es: {digito_verificador}")

    rut = "9007586-1"
    print (f"{rut= } {is_dv_valid(rut)= }")
    rut = "9007586-K"
    print (f"{rut= } {is_dv_valid(rut)= }")
    rut = "12345670-K"
    print (f"{rut= } {is_dv_valid(rut)= }")
    rut = "12.345.670-K"
    print (f"{rut= } {is_dv_valid(rut)= }")
    rut = "12345670"
    print (f"{rut= } {is_dv_valid(rut)= }")

    rut = "9007586-1"
    print (format_rut(rut))
    rut = "9.007.586-1"
    print (format_rut(rut))    
    rut = "9.007586-1"
    print (format_rut(rut))    

    for i in range(5):
        print (generate_random_valid_rut())

    rut = "9007586"
    print (complete_rut(rut))
    rut = 9007586
    print (complete_rut(rut))
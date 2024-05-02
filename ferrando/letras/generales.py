def remove_extra_spaces(cadena_entrada: str) -> str:
    """
    Elimina los espacios sobrantes de una cadena de texto.

    Toma una cadena de texto y elimina cualquier espacio extra, dejando solo un
    espacio entre palabras y eliminando espacios al inicio y al final de la cadena.

    Parámetros:
    - cadena_entrada (str): La cadena de la cual se quieren eliminar los espacios sobrantes.

    Retorna:
    - str: La cadena con los espacios sobrantes eliminados.
    """
    # Divide la cadena en una lista de palabras y luego une estas palabras con un solo espacio.
    return " ".join(cadena_entrada.split())

def remove_dots(input_string: str) -> str:
    """
    Elimina todos los puntos de la cadena proporcionada.

    Argumentos:
    - input_string (str): La cadena de la cual se eliminarán los puntos.

    Devuelve:
    - str: La cadena sin ningún punto.
    """
    return input_string.replace(".", "")

if __name__ == "__main__":
    texto = "Esto      es una     prueba"
    print (remove_extra_spaces(texto))
    texto = "Esto es una prueba"
    print (remove_extra_spaces(texto))
""" 
Utilidades relacionadas con la toma del tiempo
"""
from time import perf_counter
from typing import Callable, Any
from functools import wraps

def get_time(func: Callable) -> Callable:
    """
    Un decorador que mide el tiempo de ejecución de una función.
    
    Envuelve una función específica y mide el tiempo que tarda en ejecutarse desde el inicio hasta el final. 
    Imprime el tiempo de ejecución de la función decorada en segundos con una precisión de tres decimales.
    
    Parameters:
        func (Callable): La función a la que se le medirá el tiempo de ejecución.
        
    Returns:
        Callable: La función envuelta que, al ser llamada, imprime el tiempo de ejecución y devuelve el resultado de la función original.
    
    TODO: Poder personalizar el mensaje de salida
    """
    @wraps(func)  # Preserva el nombre, docstring y otros atributos de 'func'
    def wrapper(*args, **kwargs) -> Any:
        """ 
        Función envoltura que ejecuta la función decorada, mide y imprime su tiempo de ejecución.
        
        Captura cualquier argumento posicional o de palabra clave enviado a la función decorada.
        
        Returns:
            Any: El resultado de la función decorada.
        """
        # Inicio temporizador
        start_time: float = perf_counter()
        # Salida de la función
        result: Any = func(*args, **kwargs)
        # Fin del temporizador
        end_time: float = perf_counter()

        print(f'"{func.__name__}()" tomó {end_time - start_time:.3f} segundos en ejecutar')
        return result
    return wrapper
    
      
        
if __name__ == "__main__":
    @get_time
    def hola():
        for i in range(100000000):
            hola = i

    hola()
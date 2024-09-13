# Lista de convenciones a utilizar

- Utilizamos snake_case
- Las clases son en PascalCase
- Prefieran nombres largos en vez de cortos que no explican bien el codigo (ejemplo evitar abreviaturas o variables poco descriptivas). 
- Docstrings
    - Ejemplo:
    ``` 
    def sumar(a: int, b: int) -> int:
    """
    Suma dos números y devuelve el resultado.
    
    Parámetros:
    a (int, float): Primer número.
    b (int, float): Segundo número.
    
    Devuelve:
    int, float: La suma de a y b.
    """
    return a + b
- Utilizamos la convencion de los commits (feat, fix,...)
    - Para más detalles ver: https://dev.to/achamorro_dev/conventional-commits-que-es-y-por-que-deberias-empezar-a-utilizarlo-23an 

- La mayoria de igualdades se separan por espacios.  ``` a = 1  ``` en vez de ```a=1```.

- En general dejar una clase por archivo pero puede tener excepciones.

import sympy as sp
from cmath import *
import warnings

# devuelve un diccionario donde cada llave es un elemento de la tupla y cada elemento una lista vacía
def create_dictionary(tuple):
    result = {}
    for key in tuple:
        result.setdefault(key, [])
    return result

# agrega los datos especificados a una tabla
def add_info(dictionary, columns, data):
    i = 0
    for c in columns:
        dictionary[c].append(data[i])
        i += 1

def first_divided_difference(f,x1,x0):
    return (f(x1)-f(x0))/(x1-x0)

def second_divided_difference(f,x2,x1,x0):
    return (first_divided_difference(f,x1,x0) - first_divided_difference(f,x2,x1))/(x0-x2)

# Validación de la función
def valid_function(a, b, c):
    # se asume que si la diferencia relativa entre los valores es menor o igual a 1% la función es constante y por lo tanto
    # no es válida para seguir investigando raíces
    if ( isclose(a,b,rel_tol=1e-2) and isclose(a,c,rel_tol=1e-2) and isclose(b,c,rel_tol=1e-2)):
         return False
    else:
         return True

# Función para encontrar una raíz, devuelve una fila para formar una tabla posteriormente
def muller(x_0, x_1, x_2, f, tol, max_iterations = 100):
    # datos iniciales para el algoritmo
    a = 0 + 0j
    b = 0 + 0j
    c = 0 + 0j
    x_n = x_2
    x0, x1, x2 = x_0, x_1, x_2
    d = 0 + 0j
    e = 0 + 0j
    i = 0
    while( abs(f(x_n)) > tol and i < max_iterations ):
        with warnings.catch_warnings(record = True):
            warnings.filterwarnings("error")
            try:
                a = second_divided_difference(f, x2, x1, x0)
                b = first_divided_difference(f,x2,x1) + first_divided_difference(f,x2,x0) - first_divided_difference(f,x1,x0)
                c = f(x2)
                d = sqrt(b**2 - 4*a*c)
                # Eligiendo signo para maximizar la magnitud del denominador:
                e = ( b + d ) if ( abs( b - d ) < abs( b + d ) ) else ( b - d ) 
                h = -2*c/e
                x_n = x2 + h
                x0 = x1
                x1 = x2
                x2 = x_n
                i += 1
            except Warning as e:
                print("Hubo un error de división por cero.\nIntente otros valores iniciales u otra precisión")
                return i, x_n, f(x_n)
        
    if(i == max_iterations):
        print("No se pudo encontrar una raíz con la precisión especificada")
    return i, x_n, f(x_n)

# Función para encontrar hasta n raíces de la función
def find_roots(f_s, tol,x_0 = 3, x_1 = 4, x_2 = 5, max_roots = 5, max_iterations = 1000):
    # datos de la tabla
    columns = ("it","root","f(r)")
    table = create_dictionary(columns)
    rows = 0 # cada fila representa una raíz
    # definiciones simbólicas
    x = sp.Symbol("x")
    f_sym = f_s
    f = sp.lambdify(x,f_sym)
    # valores iniciales
    x0, x1, x2 = x_0, x_1, x_2
    # iterando mientras sea posible encontrar una raíz utilizando el procedimiento de supresión
    while valid_function(f(x0), f(x1), f(x2)) and rows < max_roots:
        with warnings.catch_warnings(record = True):
            warnings.filterwarnings("error")
            try:
                add_info(table, columns, muller(x0,x1,x2,f,tol,max_iterations))
                f_sym = f_sym/(sp.sympify(x-(table["root"][rows])))
                f = sp.lambdify(x,f_sym)
                rows += 1  
            except Warning as e:
                print("Problemas")
                return table
    return table
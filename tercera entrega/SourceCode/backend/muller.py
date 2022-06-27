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
    with warnings.catch_warnings(record = True):
        try:
            return (f(x1)-f(x0))/(x1-x0)
        except (Exception, Warning) as e:
            print(e)
            return 1

def second_divided_difference(f,x2,x1,x0):
    with warnings.catch_warnings(record = True):
        try:
            return (first_divided_difference(f,x1,x0) - first_divided_difference(f,x2,x1))/(x0-x2)
        except (Exception, Warning) as e:
            print(e)
            return 1

# Validación de la función
def valid_function(a, b, c):
    # se asume que si la diferencia relativa entre los valores es menor o igual a 1% la función es constante y por lo tanto
    # no es válida para seguir investigando raíces
    try:
        if ( isclose(a,b,rel_tol=1e-2) and isclose(a,c,rel_tol=1e-2) and isclose(b,c,rel_tol=1e-2)):
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False

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
    stop = False
    while( abs(f(x_n)) > tol and i < max_iterations ):
        with warnings.catch_warnings(record = True):
            warnings.filterwarnings("error")
            try:
                try:
                    a = second_divided_difference(f, x2, x1, x0)
                except Exception as es:
                    print("on second divided")
                    return i, x_n, f(x_n)
                try:
                    b = first_divided_difference(f,x2,x1) + first_divided_difference(f,x2,x0) - first_divided_difference(f,x1,x0)
                except Exception as e:
                    print("on first divided")
                    return i, x_n, f(x_n)
                c = f(x2)
                d = sqrt(b**2 - 4*a*c)
                # Eligiendo signo para maximizar la magnitud del denominador:
                e = ( b + d ) if ( abs( b - d ) < abs( b + d ) ) else ( b - d )
                try: 
                    h = -2*c/e
                except Exception as e:
                    stop = True
                    print("on h")
                    return i, x_n, f(x_n), stop
                x_n = x2 + h
                x0 = x1
                x1 = x2
                x2 = x_n
                i += 1
            except (Exception, Warning) as e:
                print("Hubo un error de división por cero.\nIntente otros valores iniciales u otra precisión")
                stop = True
                return i, x_n, f(x_n), stop
        
    if(i == max_iterations or abs(f(x_n)) > tol):
        print("No se pudo encontrar una raíz con la precisión especificada")
    return i, x_n, f(x_n), stop

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
    valid = False
    try:
        valid = valid_function(f(x0), f(x1), f(x2))
    except ZeroDivisionError:
        return []
    while rows < max_roots:
        with warnings.catch_warnings(record = True):
            warnings.filterwarnings("error")
            try:
                #Once the method fails it will stop searching for more roots
                i, x_n, f_xn, stop = muller(x0,x1,x2,f,tol,max_iterations)
                print((i,x_n,f_xn, stop))
                if stop:
                    return table
                add_info(table, columns, (i, x_n, f_xn))
                f_sym = f_sym/(sp.sympify(x-(table["root"][rows])))
                f = sp.lambdify(x,f_sym)
                rows += 1  
                #valid = valid_function(f(x0), f(x1), f(x2)) and not stop
            except Warning as e:
                print("Problemas")
                return table
    return table
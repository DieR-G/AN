
import pandas as pd
import sympy as sp
import numpy as np 

import matplotlib.pyplot as plt
from cmath import *

pd.set_option("display.precision", 10)

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

# Graphs
def draw_graph(f_s, a, b):
    xarr = np.linspace(a,b,10000)
    x = sp.Symbol("x")
    g = sp.lambdify(x,f_s)
    out = g(xarr)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # plot the function
    plt.plot(xarr,out, 'g')




def secant(f_s, tol, x_0, x_1, max_it = 100):
    #Define variable for PDF
    process_answer = ""
    generate_file = False

    #configuaratin to save daata
    columns = ("it", "xn-1", "xn-2","f(xn-1)","f(xn-2)","xn","error")
    table = create_dictionary(columns)

    #Variables for the method
    x = sp.Symbol("x")
    f_ = sp.sympify(f_s)
    f = sp.lambdify(x,f_)
    i = 0
    x0 = x_0
    x1 = x_1
    xn = 0
    xn1 = 1e9
    error = abs(xn-xn1) # se asume un error muy grande al iniciar las iteraciones
    q0 = f(x0)
    q1 = f(x1)
    data = []
    while  i < max_it:
        try:
            xn = x1 - q1*(x1-x0)/(q1-q0)
        except:
            process_answer = f"Error, la función genera una división entre cero para calcular Xn+1."
            return generate_file, process_answer, table
        
        error = abs(xn-xn1)
        data = [i, x1, x0, q0, q1, xn, error]
        add_info(table, columns, data)
        x0, x1 = x1, xn
        q0 = q1
        q1 = f(xn)
        xn1 = xn
        i += 1

        if (error < tol):
            generate_file = True
            process_answer = f"La raíz encontrada es: {round(xn, 10)}"
            break

    if (i >= max_it):
        process_answer = f"Error, N_max alcanzado, no se pudo encontrar una raíz con la precisión especificada."
        return generate_file, process_answer, table
    else:
        return generate_file, process_answer, table
    
    
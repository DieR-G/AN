import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy.calculus.util import continuous_domain
from sympy.parsing.latex import parse_latex #pip3 install antlr4-python3-runtime==4.7.2

################################################################

#Calculating Absolute error: |xn - xn-1|
def AbsoluteError(x,y):
    return (abs(x - y))

################################################################

#Base dictionary structure to store data
def CreateDictionary(columns):
    dictionary = {}

    for c in columns:
        dictionary[c] = []

    return dictionary

#Adding info to our dictionary
def AddInfo(dictionary, columns, values):
    i = 0

    for c in columns:
        dictionary[c].append(values[i])
        i += 1

################################################################

# Graphs
def DrawGraph(f_s, a, b):
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
    plt.plot(xarr,out, 'r')

################################################################

def RegulaFalsi(f_s, f_v, p0, p1, TOL, n_max):
    #Define variable for PDF
    process_answer = ""
    generate_file = False

    
    #Define table in order to store data:
    cols = ("Xn-1", "f(Xn-1)", "Xn", "f(Xn)", "Xn+1", "f(Xn+1)", "error")
    table = CreateDictionary(cols)

    #Function f(x) from string to lambda(int)
    x = sp.Symbol(f_v)
    f = sp.lambdify(x,f_s)

    if (p0 > p1):
        process_answer = f"Error, el punto a = {p0} es mayor que el punto b = {p1}"
        return generate_file, process_answer, table

    #Get f(x) domain
    try:
        domain = continuous_domain(f_s, x, sp.Interval(p0, p1))
    except:
        process_answer = f"Error, el programa no es capaz de determinar el dominio de la función"
        return generate_file, process_answer, table

    try:
        domain_start = domain.start
        try:
            domain_end = domain.end
        except:
            process_answer = f"Error, la función contenida entre [{p0}, {p1}] no es continua"
            return generate_file, process_answer, table
    except:
        process_answer = f"Error, la función contenida entre [{p0}, {p1}] no es continua"
        return generate_file, process_answer, table

    #Define initial values, p = last approximation and pn = current approximation
    i = 2

    try:
        q0 = f(p0)
    except:
        process_answer = f"Error, la función genera una división entre cero para calcular f(Xn-1)."
        return generate_file, process_answer, table

    try:
        q1 = f(p1)
    except:
        process_answer = f"Error, la función genera una división entre cero para calcular f(Xn)."
        return generate_file, process_answer, table

    data = []

    if ((q0 * q1) > 0):
        process_answer = f"Error, no existe ninguna raíz contenida entre [{p0}, {p1}]"
        return generate_file, process_answer, table
    elif ((domain_start > p0) or (domain_end < p1)):
        process_answer = f"Error, la función contenida entre [{p0}, {p1}] no es continua"
        return generate_file, process_answer, table

    while (i <= n_max):
        
        #Regula falsi algorithm
        try:
            p = (p0 - ((q0 * (p1 - p0)) / (q1 - q0)))
        except:
            process_answer = f"Error, la función genera una división entre cero para calcular Xn+1."
            return generate_file, process_answer, table

        approximation_error = AbsoluteError(p, p0)

        try:
            q = f(p)
        except:
            process_answer = f"Error, la función genera una división entre cero para calcular f(Xn+1)."
            return generate_file, process_answer, table

        #Interpolate table
        data = [p0, q0, p1, q1, p, q, approximation_error]
        AddInfo(table, cols, data)

        
        if (approximation_error < TOL):
            generate_file = True
            process_answer = f"La raíz encontrada es: {round(p, 10)}"
            break

        i = (i + 1)

        if (q*q1 < 0):
            p0 = p1
            q0 = q1

        p0 = p
        q0 = q

    if (i >= n_max):
        process_answer = f"Error, N_max alcanzado, no se pudo encontrar una raíz con la precisión especificada."
        return generate_file, process_answer, table
    else:
        return generate_file, process_answer, table

################################################################
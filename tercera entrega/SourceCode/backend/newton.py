import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Definicion de simbolos 
z = sp.symbols('z')

#Color domain
def color_domain(func,px,py,step=1000):
    """
    Método que genera una gráfica de la función compleja func, a través de su visualización mediante
    el dominio de color de la función
    
    Argumentos:
        -func -> función base
        -px -> máximo valor para x, será usado para calcular los limites positivos y negativos en el eje real
        -py ->  máximo valor para y, será usado para calcular los limites positivos y negativos en el eje imaginario
        -step -> distancia entre cada una de las coordenadas a evaluar en el arreglo, su valor por defecto es 1000 
        -cmap -> Mapa de colores a usar
    
    """
    f = sp.lambdify(z,func,"numpy")
    
    xs,ys = np.ogrid[-px:px:step*1j, -py:py:step*1j]

    return np.angle(f((xs - 1j*ys).T))

#función que retorna las raíces encontradas
def return_roots(zs, not_rooted):
    """
    Retorna las raices encontradas en un arreglo de coordenadas complejas
    Argumentos:
        - zs -> arreglo de coordenadas complejas 
        - not_rooted -> arreglo booleano que indica que posiciones no llegaron a una raiz  
    Retorna:
        - roots_arr -> arreglo con las raices encontradas
    """
    
    found_root = np.invert(not_rooted) #Se invierten los valores booleanos para determinar cuales valores 
    #de zs son raices
    zs = np.around(zs, 6) #Redondeo de los valores a una precision de 6 decimales

    # Creacion de un set, y posterior insercion de los valores que sean raices, si un valor ya se encuentra en el set
    # este no ingresara, dado que los set de python no permiten valores repetidos
    roots = set()
    for i in zs[found_root]:
        roots.add(i)

    roots_arr = list(roots)
    roots_arr.sort() #ordenamiento de raices
    return roots_arr

def fractals(func,px,py,TOL,n_max,step=500):
    df = sp.diff(func)
    print(df)
    return True

def nr_fractals(func,px,py,TOL,n_max,step=500):
    
    """
    Método de Newton Rhapson que obtiene las raices y el color domain de una función en los complejos, basado 
    en la rapidez con la que convergeran a una raiz, mayor claridad en el color significa mayor número de iteraciones
    
    Argumentos:
        -func -> función base
        -px -> máximo valor para x, será usado para calcular los limites positivos y negativos en el eje real
        -py ->  máximo valor para y, será usado para calcular los limites positivos y negativos en el eje imaginario
        -TOL -> tolerancia del error, usado para determinar que se ha encontrado una raiz satisfactoria
        -n_max -> cantidad máxima de iteraciones en las que se ejecutará el método
        - step -> distancia entre cada una de las coordenadas a evaluar en el arreglo, su valor por defecto es 500 
        
    Retorna:
        - arreglo con la cantidad de iteraciones que le toma a cada punto evaluado llegar a una raíz 
        - arreglo de n raíces encontradas
        - False en caso de que ocurra algun error
    
    
    """
    
    #Creacion de funciones lambda para la evaluacion de los puntos
    f = sp.lambdify(z,func,"numpy")
    df = sp.lambdify(z,sp.diff(func),"numpy") #Derivada de la función a emplear
    
    
    #Verificando que la funcion, al derivarla no se vuelva 0 e indefina el método
    if df == 0:
        raise  ValueError("derivada igual a 2")

    
    #Creación de arreglos de 1xstep de tamaño, con las coordenadas desde [-valor limite] 
    # hasta [valor limite] con una cantidad de divisiones igual a step, siendo inclusivo en el último valor
    try:
        ys, xs = np.ogrid[-py:py:step*1j, -px:px:step*1j]
    except Exception as e:
        print(e)
    print("Here")
    #Unión de ambos arreglos para crear una matriz de coordenadas complejas
    zs = xs + ys*1j
    
    #Creación de matriz de iteraciones, la cual esta populada del valor máximo de iteraciones
    iterations = n_max + np.zeros(zs.shape)
    not_rooted = iterations < 100000 #Creación de matriz de booleanos, que indica si aún no se encuentra una  raíz
    
    
    for i in range(n_max):
        
        
        previous_z = zs
        dev = (df(zs))
        np.place(dev,dev==0,1)
        
        
        #Método de Newton - Raphson, extendido a los complejos, aplicado a matrices de valores
        zs = zs - (f(zs))/ dev
       
        
        #Evaluando si se encontraron raices, basandose en la tolerancia y si el valor no habia sido encontrado
        roots = (abs(previous_z-zs)<TOL) & not_rooted
        #Sustiuyendo en el arreglo de iteraciones la cantidad de estas que tomo encontrar la raiz
        iterations[roots] = i
        
        #Creación de un nuevo arreglo booleano para determinar que valores siguen sin llegar a una raíz
        not_rooted = np.invert(roots) & not_rooted
    rts =  return_roots(zs, not_rooted)
    
    
    return [iterations,rts] 



def complex_newton(f, df, z0,TOL, n_max=1000):
    """
    Método de Newton-Raphson extendido a los complejos, aplicada a un solo valor en lugar de una matriz completa
    
    Argumentos:
        - f -> función de interés, ya lambdificada en términos de z
        - df -> derivada de la función de interés, ya lambdificada en términos de z
        
    Retorna:
        - False si no se encuentra una raíz luego de la cantidad máxima de iteraciones
        - La raíz a la que se aproximó el valor si la encuentra

    """

    pz = z0
    for i in range (n_max):
        dz = f(pz)/df(pz)
        if abs(dz) < TOL:
            return pz
        pz -= dz
    return False

def newton_colors(func, px ,py ,step, TOL=10**(-8)):
    """
    Función que genera una matriz que indica hacia que raiz se acerca cada uno de los valores dentro de las coordenadas
        
    Argumentos:
        -func -> función de interés, en términos de z
        -px -> máximo valor para x, será usado para calcular los limites positivos y negativos en el eje real
        -py ->  máximo valor para y, será usado para calcular los limites positivos y negativos en el eje imaginario
        -step -> distancia entre cada una de las coordenadas a evaluar en el arreglo, su valor por defecto es 500 
        -TOL -> tolerancia del error, usado para determinar que se ha encontrado una raiz satisfactoria, valor por defecto
                10^  (-8)
        
    Retorna:
        un arreglo con la raiz al que los valores complejos iniciales se aproximaran

    """

    roots = []
    aproximations = np.zeros((step, step))
    f = sp.lambdify(z,func,"numpy")
    df = sp.lambdify(z,sp.diff(func),"numpy")

    def get_root_index(roots, r):
        """
        Método que obtiene el indice de la raíz obtenida, si esta no existe dentro del arreglo de raices, la añade
        
        Argumentos: 
            - roots -> arreglo de raices
            - r -> raiz obtenida
            
        Retorna:
            - el indice de la raiz en el arreglo
            -tamaño del arreglo -1 si la raiz no existe dentro del arreglo

        """

        try:
            return np.where(np.isclose(roots, r, atol=TOL))[0][0]
        except IndexError:
            roots.append(r)
            return len(roots) - 1

    
    for ix, x in enumerate(np.linspace(-px, px, step)):
        for iy, y in enumerate(np.linspace(-py, py, step)):
            z0 = x + y*1j
            r = complex_newton(f, df, z0,TOL)
            if r is not False:
                ir = get_root_index(roots, r)
                aproximations[iy, ix] = ir
                
                
    return aproximations



def grid(columns,rows,table, images,cmap,colors):
    """
    Función que generá un grid con las imagenes solicitadas de la función en cuestion
    
    """
    
    
    

    fig = plt.figure(figsize=(12, 9))
    
    fig.add_subplot(rows, columns, 1)
    plt.scatter(np.real(table),np.imag(table),c=colors)
    plt.axis('on')
    
    fig.add_subplot(rows, columns, 2)
    plt.imshow(images[0], cmap=cmap)
    plt.axis("off")
   

    fig.add_subplot(rows, columns, 3)
    plt.imshow(images[1], cmap=cmap)
    plt.axis('off')
    
    
    fig.add_subplot(rows, columns, 4)
    plt.imshow(images[2], cmap=cmap)



def newthon_fractals_method(func,px,py,TOL,n_max,step=500):
    iterations, roots= nr_fractals(func,px,py,TOL,n_max,step)
    color_map = newton_colors(func,px,py,step,TOL)
    graph = color_domain(func,px,py,step)

    #Generador de colores aleatorios para los puntos obtenidos como raíces 
    np.random.seed()
    N = len(roots)
    colors = np.random.rand(N)

    images = [iterations, color_map,graph]

    #Renderización de las gráficas y tablas

    grid(2,2,roots, images,"viridis",colors)
    
    return roots

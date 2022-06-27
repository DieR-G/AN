import os
from datetime import datetime
from pylatex import Document, Section, Subsection, Command, Package, NewLine, Math, Figure
from pylatex.utils import NoEscape
import pandas as pd

def WritePDF(method, method_name, input_data, process_answer, iteration_table, generate_file = False):
    def fill_document(doc):
        with doc.create(Section(method_name)): #Section
            
            with doc.create(Subsection('Datos')): #Subsection
                for input_value in input_data:
                    doc.append(Math(data=NoEscape(input_value)))
                    doc.append(NewLine())
            
            with doc.create(Subsection('Resultado')): #Subsection
                if ((method == 1) or (method == 2)):
                    doc.append(process_answer)
                elif (method == 3):
                    for answer in iteration_table["root"]:
                        doc.append(NoEscape(f'\\indent La raíz encontrada es: {answer}'))
                        doc.append(NewLine())
                elif (method == 4):
                    for answer in iteration_table:
                        doc.append(NoEscape(f'\\indent La raíz encontrada es: {answer}'))
                        doc.append(NewLine())
            
            if (generate_file and (method == 1)): #Check if everything is okay | for Secante only
                with doc.create(Subsection('Iteraciones')): #Subsection
                    doc.append(NoEscape(pd.DataFrame(iteration_table).style.to_latex(environment='longtable', hrules=True)))
            elif (generate_file and (method == 2)): #Check if everything is okay | for Regula only
                with doc.create(Subsection('Iteraciones')): #Subsection
                    doc.append(NoEscape(pd.DataFrame(iteration_table).style.to_latex(environment='longtable', hrules=True)))
                
                with doc.create(Subsection('Gráfica')): #Subsection
                    with doc.create(Figure(position='htbp')) as plot:
                        plot.add_plot()
                        plot.add_caption(f'Gráfica - {method_name}')
            elif (method == 3): #Check if everything is okay | for Muller only
                with doc.create(Subsection('Iteraciones')): #Subsection
                    doc.append(NoEscape(pd.DataFrame(iteration_table).style.to_latex(environment='longtable', hrules=True)))
            elif (method == 4): #Check if everything is okay | for Newton only
                #Change to new Graphics
                with doc.create(Subsection('Gráfica')): #Subsection
                    with doc.create(Figure(position='htbp')) as plot:
                        plot.add_plot()

    # Basic document
    doc = Document()
    fill_document(doc)

    # Document with `\maketitle` command activated
    doc = Document()

    doc.packages.append(Package('babel', options=['spanish']))
    doc.packages.append(Package('booktabs'))
    doc.packages.append(Package('longtable'))

    doc.preamble.append(Command('title', 'Resultados'))
    doc.preamble.append(Command('author', 'Raíces de funciones irracionales'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    fill_document(doc)

    #Generate PDF
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    date = datetime.now().strftime("%Y%m%d_%I%M%S%p")
    name_file = f"Resultados_{method_name}_{str(date)}"

    location_path = f'{desktop}\\{name_file.replace(" ", "")}'

    try:
        doc.generate_pdf(location_path, clean_tex=True)
        return True, location_path
    except Exception as e:
        print(e)
        return False, location_path
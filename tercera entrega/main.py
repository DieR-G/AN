from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from backend.backend_kivyagg import FigureCanvasKivyAgg
from sympy.parsing.latex import parse_latex #requires antlr4 4.7.2 installed with pip3 install antlr4-python3-runtime==4.7.2
from sympy.printing.latex import latex
from backend.muller import find_roots as muller_roots
from cmath import *
import matplotlib.pyplot as plt
import kivy.metrics as kivy_metrics
import sympy as sp


Window.minimum_height = 500
Window.minimum_width = 500
Window.clearcolor = (1,1,1,1)

class ErrorPopup(Popup):
    def __init__(self, error_title, error_msg, **kwargs):
        super().__init__(**kwargs)
        app = App.get_running_app()
        self.title = error_title
        self.size_hint = (0.6,0.8)
        self.pos_hint = {"x-center":0.5, "y-center":0.5}
        self.error_msg = error_msg
        box_content = BoxLayout(orientation = "vertical", size = (app.root.width, app.root.height), padding = "16dp")
        box_content.add_widget(Label(markup = True, font_name = "fonts/JetBrainsMono-Bold.ttf", font_size = "20sp", text_size = (kivy_metrics.dp(300), None), size_hint = (1, 0.8),text = "[color=#92B4EC][b]%s[/b][/color]"%self.error_msg))
        box_content.add_widget(Button(text = "Cerrar", font_name = "fonts/JetBrainsMono-ExtraBold.ttf", font_size = "20sp", background_normal="",background_color = (255/255,230/255,154/255,1), size_hint = (1,0.2), on_release=self.dismiss, pos_hint = {"center_x":0.5}))
        self.content = box_content

# Some basic components
class CustomDropDown(DropDown):
    pass

class MethodContainer(BoxLayout):
    pass

class DropDownContainer(AnchorLayout):
    pass

class Home(BoxLayout):
    pass

# The <Method>Form classes are used to define the UI form
# for each method
class SecantForm(BoxLayout):
    #clearing text inputs
    def clear_inputs(self, inputs_to_clear):
        for input in inputs_to_clear:
            input.text = ""
    #clearing image
    def clear_picture(self):
        box = self.ids['function_canvas']
        box.clear_widgets()
    #rendering the text when the function input loses focus
    def lost_focus(self, data, focused):
        box = self.ids['function_canvas']
        self.clear_picture()
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        if not focused:
            try:
                x = sp.Symbol('x')
                expr = parse_latex(data)
                #Checks that the input is a function in x. Constant functions have to be declared as "0x+C"
                if x not in expr.free_symbols or len(expr.free_symbols) != 1:
                    raise Exception("Bad symbol")
                plt.plot()
                plt.axis('off')
                plt.text(-0.05, 0, "$%s$"%latex(expr), fontsize=20)
                box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            #The parsing of the function input was incorrect
            except Exception as e:
                self.clear_inputs([self.ids["function_text"]])
                popup = ErrorPopup("Error al leer la función", "Verifica que la función esté definida sobre la variable 'x' y tenga el formato LaTeX correcto")
                popup.open()
                print(e)
            
    def return_home(self):
        self.clear_picture()
        self.clear_inputs([ self.ids["function_text"], self.ids["tol"], self.ids["iterations"], self.ids["x_0"], self.ids["x_1"] ])
        app = App.get_running_app()
        app.root.transition.direction = "right"
        app.root.current = "home"

class RegulaForm(BoxLayout):
    #clearing text inputs
    def clear_inputs(self, inputs_to_clear):
        for input in inputs_to_clear:
            input.text = ""
    #clearing image
    def clear_picture(self):
        box = self.ids['function_canvas']
        box.clear_widgets()
    #rendering the text when the function input loses focus
    def lost_focus(self, data, focused):
        box = self.ids['function_canvas']
        self.clear_picture()
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        if not focused:
            try:
                x = sp.Symbol('x')
                expr = parse_latex(data)
                #Checks that the input is a function in x. Constant functions have to be declared as "0x+C"
                if x not in expr.free_symbols or len(expr.free_symbols) != 1:
                    raise Exception("Bad symbol")
                plt.plot()
                plt.axis('off')
                plt.text(-0.05, 0, "$%s$"%latex(expr), fontsize=20)
                box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            #The parsing of the function input was incorrect
            except Exception as e:
                self.clear_inputs([self.ids["function_text"]])
                popup = ErrorPopup("Error al leer la función", "Verifica que la función esté definida sobre la variable 'x' y tenga el formato LaTeX correcto")
                popup.open()
                print(e)
    def return_home(self):
        self.clear_picture()
        self.clear_inputs([ self.ids["function_text"], self.ids["tol"], self.ids["iterations"], self.ids["a"], self.ids["b"] ])
        app = App.get_running_app()
        app.root.transition.direction = "right"
        app.root.current = "home"

#########################################################################
class MullerForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table = []
        self.expr = None
    #clearing text inputs
    def clear_inputs(self, inputs_to_clear):
        for input in inputs_to_clear:
            input.text = ""
    #clearing image
    def clear_picture(self):
        box = self.ids['function_canvas']
        box.clear_widgets()
    #pop up when the function is incorrectly typed
    def bad_function(self):
        self.clear_inputs([self.ids["function_text"]])
        popup = ErrorPopup("Error al leer la función", "Verifica que la función esté definida sobre la variable 'x' y tenga el formato LaTeX correcto")
        popup.open()

    #finding the roots
    def submit(self):
        if self.expr is None:
            self.bad_function()
            return
        f_s = self.expr
        tol = float(self.ids["tol"].text) if self.ids["tol"].text != "" else 0.1
        iterations = int(self.ids["iterations"].text) if self.ids["iterations"].text != "" else 100
        x_0 = complex(
            float(self.ids["x_0_r"].text) if self.ids["x_0_r"].text != "" else 0.0,
            float(self.ids["x_0_i"].text) if self.ids["x_0_i"].text != "" else 0.0
        )
        x_1 = complex(
            float(self.ids["x_1_r"].text) if self.ids["x_1_r"].text != "" else 0.0,
            float(self.ids["x_1_i"].text) if self.ids["x_1_i"].text != "" else 0.0
        )
        x_2 = complex(
            float(self.ids["x_2_r"].text) if self.ids["x_2_r"].text != "" else 0.0,
            float(self.ids["x_2_i"].text) if self.ids["x_2_i"].text != "" else 0.0
        )
        if x_0 == x_1 or x_0 == x_2 or x_1 == x_2:
            popup = ErrorPopup("Error de valores de entrada", "Verifica que los valores iniciales sean distintos entre sí")
            popup.open()
            return 
        self.table = muller_roots(f_s, tol, x_0, x_1, x_2, 10, iterations)
        print(self.table)
        pass

    #rendering the text when the function input loses focus
    def lost_focus(self, data, focused):
        box = self.ids['function_canvas']
        self.clear_picture()
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        if not focused:
            try:
                x = sp.Symbol('x')
                self.expr = parse_latex(data)
                #Checks that the input is a function in x. Constant functions have to be declared as "0x+C"
                if x not in self.expr.free_symbols or len(self.expr.free_symbols) != 1:
                    raise Exception("Bad symbol")
                plt.plot()
                plt.axis('off')
                plt.text(-0.05, 0, "$%s$"%latex(self.expr), fontsize=20)
                box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            #The parsing of the function input was incorrect
            except Exception as e:
                self.bad_function()
                print(e)

    def return_home(self):
        self.clear_picture()
        self.clear_inputs([ self.ids["function_text"], self.ids["tol"], self.ids["iterations"], self.ids["x_0_r"], self.ids["x_0_i"],self.ids["x_1_r"], self.ids["x_1_i"], self.ids["x_2_r"], self.ids["x_2_i"] ])
        app = App.get_running_app()
        app.root.transition.direction = "right"
        app.root.current = "home"

##################################################################
class NewtonForm(BoxLayout):
    #clearing text inputs
    def clear_inputs(self, inputs_to_clear):
        for input in inputs_to_clear:
            input.text = ""
    #clearing image
    def clear_picture(self):
        box = self.ids['function_canvas']
        box.clear_widgets()
    #rendering the text when the function input loses focus
    def lost_focus(self, data, focused):
        box = self.ids['function_canvas']
        self.clear_picture()
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        if not focused:
            try:
                z = sp.Symbol('z')
                expr = parse_latex(data)
                #Checks that the input is a function in x. Constant functions have to be declared as "0x+C"
                if z not in expr.free_symbols or len(expr.free_symbols) != 1:
                    raise Exception("Bad symbol")
                plt.plot()
                plt.axis('off')
                plt.text(-0.05, 0, "$%s$"%latex(expr), fontsize=20)
                box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            #The parsing of the function input was incorrect
            except Exception as e:
                self.clear_inputs([self.ids["function_text"]])
                popup = ErrorPopup("Error al leer la función", "Verifica que la función esté definida sobre la variable 'z' y tenga el formato LaTeX correcto")
                popup.open()
                print(e)
    def return_home(self):
        self.clear_picture()
        self.clear_inputs([ self.ids["function_text"], self.ids["tol"], self.ids["iterations"], self.ids["z_0_r"], self.ids["z_0_i"] ])
        app = App.get_running_app()
        app.root.transition.direction = "right"
        app.root.current = "home"

#First screen
class HomeScreen(Screen):
    def method_selected(self, instance, data):
        app = App.get_running_app()
        app.root.transition.direction = "left"
        if(data == "Secante"):
            app.root.current = 'secant'
        elif(data == "Regula falsi"):
            app.root.current = "regula"
        elif(data == "Muller"):
            app.root.current = "muller"
        else:
            app.root.current = "newton"
    def __init__(self, **kw):
        super().__init__(**kw)
        #Constructing the home interface
        self.main_container = FloatLayout()
        self.view = Home()
        self.container = MethodContainer()
        self.dropdown_container = DropDownContainer()
        self.drop_button = Button(text = "Elige un método", font_name = "fonts/JetBrainsMono-Bold.ttf", font_size = "20sp", background_normal = "", background_color = (255/255, 210/255, 76/255,1), size_hint_y = None, height = "35.dp")
        self.dropdown = CustomDropDown()
        self.image = Image(source="images/function-mathematical-symbol.png", pos_hint = {"center_x":0.5, "y":0.1}, size_hint = [0.5,0.5])
        self.drop_button.bind(on_release = self.dropdown.open)
        self.dropdown.bind(on_select=self.method_selected)

        self.dropdown_container.add_widget(self.drop_button)
        self.container.add_widget(self.dropdown_container)
        self.view.add_widget(self.container)
        setattr(self.view, 'pos_hint', {"x":0, "top":1})

        self.main_container.add_widget(self.view)
        self.main_container.add_widget(self.image)

        self.add_widget(self.main_container)

        
class WindowManager(ScreenManager):
    pass

class IrrationalRoots(App):
    def build(self):
        sm = ScreenManager()
        #Creating each method screen
        secant_screen = Screen(name = "secant")
        secant_screen.add_widget(SecantForm())
        
        regula_screen = Screen(name = "regula")
        regula_screen.add_widget(RegulaForm())

        muller_screen = Screen(name = "muller")
        muller_screen.add_widget(MullerForm())
        
        newton_screen = Screen(name = "newton")
        newton_screen.add_widget(NewtonForm())
        #Adding them to the manager so that we can navigate through them
        sm.add_widget(HomeScreen(name = "home"))
        sm.add_widget(muller_screen)
        sm.add_widget(regula_screen)
        sm.add_widget(secant_screen)
        sm.add_widget(newton_screen)
        return sm
        
try:
    IrrationalRoots().run()
except Exception as e:
    print(e)
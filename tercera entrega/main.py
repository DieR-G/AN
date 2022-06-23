from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout

Window.minimum_height = 500
Window.minimum_width = 500
Window.clearcolor = (1,1,1,1)

class CustomDropDown(DropDown):
    pass

class Home(BoxLayout):
    pass

class MethodContainer(BoxLayout):
    pass

class DropDownContainer(AnchorLayout):
    pass

class IrrationalRoots(App):
    def method_selected(self, instance, data):
        setattr(self.drop_button, 'text', data)

    def build(self):
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

        return self.main_container
        

IrrationalRoots().run()
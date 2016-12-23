from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.

# Declare both screens
class SelectScreen(Screen):
    pass

class ProgressScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

class ContinueButton(Button):
    pass

class ModelSpinner(Spinner):
    values = [
        'PV400-G0-E51-M0',
        'PV400-G0-E53-M0',
        'PV400-G0-E54-M0',
        'PV400-G1-E51-M0',
        'PV400-G1-E53-M0',
        'PV400-G1-E54-M0',
        'PV400-G0-E51-M1',
        'PV400-G0-E53-M1',
        'PV400-G0-E54-M1',
        'PV400-G1-E51-M1',
        'PV400-G1-E53-M1',
        'PV400-G1-E54-M1',
        'PV2001-G0-E51',
        'PV2001-G0-E53',
        'PV2001-G0-E54',
        'PV2001-G1-E51',
        'PV2001-G1-E53',
        'PV2001-G1-E54'
    ]
class TestApp(App):

    def build(self):
        presentation = Builder.load_file("main.kv")
        return presentation

if __name__ == '__main__':
    TestApp().run()

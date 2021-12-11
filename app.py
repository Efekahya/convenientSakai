import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.core.window import Window
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import main
from main import *
Window.size = (375, 412)


class LoginWidget(Widget):
    def __init__(self, **kwargs):
        super(LoginWidget, self).__init__(**kwargs)

    def login(self):
        email = App.get_running_app().root.get_screen("screen1").ids.login.ids.email.text
        password = App.get_running_app().root.get_screen("screen1").ids.login.ids.password.text
        auth = {'eid': email, 'pw': password, 'submit': 'Giriş'}

        dersler = main.calistir(auth)
        print(auth)
        showOdevler(dersler)
        showDuyurular(dersler)
        showMeeting(dersler)


def showOdevler(dersler):
    layout = GridLayout(cols=1, spacing=10)
    view = ScrollView()
    for i in range(len(dersler)):
        for j in range(len(dersler[i].odev)):
            h = dersler[i].odev[j]
            if h != "Yok":
                layout.add_widget(Label(text=h["content"]))

    view.add_widget(layout)
    App.get_running_app().root.get_screen(
        "screen2").ids.main.ids.tab1.add_widget(view)


def showDuyurular(dersler):
    layout = GridLayout(cols=1, spacing=10)
    view = ScrollView()
    for i in range(len(dersler)):
        for j in range(len(dersler[i].duyuru)):
            h = dersler[i].duyuru[j]
            layout.add_widget(Label(text=h))

    view.add_widget(layout)
    App.get_running_app().root.get_screen(
        "screen2").ids.main.ids.tab2.add_widget(view)


def showMeeting(dersler):
    layout = GridLayout(cols=1, spacing=10)
    view = ScrollView()
    for i in range(len(dersler)):
        for j in range(len(dersler[i].meeting)):
            if dersler[i].meeting[j] != "Yok":
                h = dersler[i].meeting[j]
                text = h["meetingStartDate"] + " - " + h["meetingUrl"]
                layout.add_widget(Label(text=text))

    view.add_widget(layout)
    App.get_running_app().root.get_screen(
        "screen2").ids.main.ids.tab3.add_widget(view)


class MainWidget(TabbedPanel):
    pass


class ScreenOne(Screen):
    pass


class ScreenTwo(Screen):
    pass


class ScreenManager(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        return ScreenManager()


MyApp().run()

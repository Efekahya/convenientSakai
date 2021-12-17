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
from kivy.metrics import sp
import main
from main import *


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
    App.get_running_app().root.get_screen("screen2").ids.main.ids.rv2grid.add_widget(Label(text=""))
    for i in range(len(dersler)):
        App.get_running_app().root.get_screen(
            "screen2").ids.main.ids.rv2grid.add_widget(Label(text=dersler[i].name, size_hint_x=None, width=Window.size[0]))
        y = 0
        for j in range(len(dersler[i].odev)):
            h = dersler[i].odev[j]
            if h != "Yok":
                text = h["dueTime"] + " - " + h["content"]
                a = len(text.strip().replace('\n'*2, '\n'))
                x = Window.size[0]
                x = x/12
                a = a/x
                y = 30
                for l in range(text.strip().replace('\n'*2, '\n').count('\n')):
                    y += 15
                for k in range(int(a)):
                    y += 12

                App.get_running_app().root.get_screen(
                    "screen2").ids.main.ids.rv2grid.add_widget(TextInput(text=text.strip().replace('\n'*2, '\n'), size_hint_y=None,  height=sp(y), multiline=True, disabled=True))


def showDuyurular(dersler):
    App.get_running_app().root.get_screen("screen2").ids.main.ids.rv1grid.add_widget(Label(text=""))
    for i in range(len(dersler)):
        App.get_running_app().root.get_screen(
            "screen2").ids.main.ids.rv1grid.add_widget(Label(text=dersler[i].name, size_hint_x=None, width=Window.size[0]))
        y = 0
        for j in range(len(dersler[i].duyuru)):
            h = dersler[i].duyuru[j]
            a = len(h.strip().replace('\n'*2, '\n'))
            x = Window.size[0]
            x = x/12
            a = a/x
            y = 30

            for l in range(h.strip().replace('\n'*2, '\n').count('\n')):
                y += 12
            for k in range(int(a)):
                y += 12
            App.get_running_app().root.get_screen(
                "screen2").ids.main.ids.rv1grid.add_widget(TextInput(text=h.strip().replace('\n'*2, '\n'), size_hint_y=None, height=sp(y), multiline=True, disabled=True))


def showMeeting(dersler):
    App.get_running_app().root.get_screen("screen2").ids.main.ids.rv3grid.add_widget(Label(text=""))

    for i in range(len(dersler)):
        App.get_running_app().root.get_screen(
            "screen2").ids.main.ids.rv3grid.add_widget(Label(text=dersler[i].name, size_hint_x=None, width=Window.size[0]))
        y = 0
        for j in range(len(dersler[i].meeting)):
            if dersler[i].meeting[j] != "Yok":
                h = dersler[i].meeting[j]
                text = h["meetingStartDate"] + " - " + h["meetingUrl"]
                a = len(text.strip().replace('\n'*2, '\n'))

                x = Window.size[0]
                x = x/12
                a = a/x
                y = 30
                for k in range(int(a)):
                    y += 20
                App.get_running_app().root.get_screen(
                    "screen2").ids.main.ids.rv3grid.add_widget(TextInput(text=text.strip().replace('\n'*2, '\n'), size_hint_y=None, height=sp(y), multiline=True, disabled=True))


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

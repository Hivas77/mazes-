from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import json
import os


USER_DATA_FILE = "user_data.json"


DEFAULT_XP = 100


def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.username = TextInput(hint_text='Enter Username')
        self.password = TextInput(hint_text='Enter Password', password=True)
        self.status = Label(text='')
        login_btn = Button(text='Login', on_press=self.login)
        register_btn = Button(text='Register', on_press=self.register)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_btn)
        layout.add_widget(register_btn)
        layout.add_widget(self.status)
        self.add_widget(layout)

    def login(self, instance):
        users = load_users()
        name = self.username.text
        pwd = self.password.text
        if name in users and users[name]['password'] == pwd:
            self.status.text = "Login successful!"
            self.manager.current = 'game'
            self.manager.get_screen('game').load_user(name)
        else:
            self.status.text = "Incorrect credentials!"

    def register(self, instance):
        users = load_users()
        name = self.username.text
        pwd = self.password.text
        if name in users:
            self.status.text = "Username already exists."
        else:
            users[name] = {'password': pwd, 'xp': DEFAULT_XP, 'enemies_defeated': 0}
            save_users(users)
            self.status.text = "User registered."

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Game will load here...")
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)

    def load_user(self, username):
        self.user = username
        users = load_users()
        xp = users[username]['xp']
        self.label.text = f"Welcome {username}! XP: {xp}"

class MazeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    MazeApp().run()

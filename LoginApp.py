from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.metrics import dp

Window.size = (600, 700)  # Reduced window height


class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)  # Reduced padding
        self.spacing = dp(10)  # Reduced spacing

        # School logo/header - smaller size
        self.add_widget(Image(source='Business Salesman.gif',
                              size_hint=(1, 0.2),
                              allow_stretch=True))

        # Title - smaller font
        self.add_widget(Label(text="Login System",
                              font_size=dp(20),
                              bold=True,
                              size_hint=(1, 0.08)))

        # Username input
        self.username = TextInput(
            hint_text='Username',
            size_hint=(1, None),
            height=dp(40),
            multiline=False
        )
        self.add_widget(self.username)

        # Password input
        self.password = TextInput(
            hint_text='Password',
            size_hint=(1, None),
            height=dp(40),
            multiline=False,
            password=True  # Hide password characters
        )
        self.add_widget(self.password)

        # Role selection spinner - smaller height
        self.role_spinner = Spinner(
            text='Select Role',
            values=('Admin', 'Teacher', 'DoS', 'Registrar', 'Bursar', 'Guest'),
            size_hint=(1, None),
            height=dp(40),
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.add_widget(self.role_spinner)

        # Login button (blue) - smaller height
        self.login_btn = Button(
            text="Login",
            size_hint=(1, None),
            height=dp(40),
            background_color=(0.2, 0.6, 1, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.login_btn)

        # Forgot password button (green) - smaller height
        self.forgot_btn = Button(
            text="Forgot Password?",
            size_hint=(1, None),
            height=dp(35),
            background_color=(0.2, 0.8, 0.4, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size=dp(12)
        )
        self.add_widget(self.forgot_btn)

        # Footer - smaller font
        self.add_widget(Label(text="© 2023 School Management System",
                              font_size=dp(10),
                              size_hint=(1, 0.05)))


class LoginApp(App):
    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    LoginApp().run()

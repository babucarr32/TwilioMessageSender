from twilio.rest import Client
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

String_Builder = """
Screen:
    ScreenManager: 
        id: screen_manager
        MainScreen:

<MainScreen>
    name: "main"
    MDNavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: "vertical"
                    size: self.size
                    pos: self.pos
                    FitImage:
                        source: "TheBadjie.png"
                MDTextFieldRound:
                    id: message
                    hint_text: "Enter Message"
                    size_hint: 0.75, 0.06
                    pos_hint: {"center_x": 0.5,"center_y": 0.3}
                    normal_color: 1,1,1,0.1
                    line_color: 1,1,1,0.1
                    color_active: 1,1,1,1
                    line_color_focus: 1,1,1,1
                    theme_text_color: "Custom"
                    text_color: 1,1,1,1
                MDRoundFlatIconButton:
                    text: "Send"
                    size_hint: 0.85, None
                    pos_hint: {"center_x": 0.5,"center_y": 0.2}
                    line_color: 1,1,1,1
                    text_color: 1,1,1,1
                    icon_color: 1,1,1,1
                    icon: "send"
                    on_release: app.sendMessage()
                MDFloatingActionButton:
                    icon: "menu"
                    pos_hint: {"center_x": 0.1,"center_y": 0.95}
                    md_bg_color: 229/255.0,150/255.0,38/255.0,1
                    on_press: nav_drawer.set_state("open")

"""


class MainScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(MainScreen(name="main"))


class TheBadjie(MDApp):
    def build(self):
        AppBuilder = Builder.load_string(String_Builder)
        return AppBuilder

    def sendMessage(self):
        pass
        account_sid = "ACd0b3026ad89c12f156833dbd4665a3d6"
        auth_token = "83a73cdc1ead169a16e915eea33cd908"
        text_message = self.root.ids.screen_manager.get_screen("main").ids.message.text
        client = Client(account_sid, auth_token)
        self.messsageSid = ""
        client.messages.create(
            from_="+yourTwillioNumber",
            body=f'Message=> {text_message}',
            to="TheNumberOfThePersonYouWantToSendTo"
        )


TheBadjie().run()

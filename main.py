import json
from twilio.rest import Client
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDFlatButton
from twilio.base.exceptions import TwilioRestException

String_Builder = """
Screen:
    ScreenManager: 
        id: screen_manager
        MainScreen:
        AddNumber:

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
                    
    MDNavigationDrawer:
        id: nav_drawer
        BoxLayout:
            orientation: "vertical"
            FitImage:
                source: "MyImage.jpg"    
            MDCard:
                orientation: "vertical"
                MDToolbar:
                    title: "PHONEBOOK"  
                    md_bg_color: 0,0,0,0.75
                    font_style: "Caption"
                ScrollView:
                    MDList:
                        id: phoneNums
                MDFloatingActionButton:
                    icon: "plus"
                    pos_hint: {"center_x": 0.8,"center_y": 0.3}
                    md_bg_color: 229/255.0,150/255.0,38/255.0,1
                    on_release: root.manager.current="number"
                MDLabel:
                    text: "   Baboucarr Bajie"
                    size_hint_y:None 
                    height: self.texture_size[1]
                MDLabel:
                    text: "    bbabucarr32@gmail.com\\n"
                    size_hint_y:None 
                    height: self.texture_size[1] 
                    font_style: "Caption"
<AddNumber>
    name: "number"
    MDCard:
        orientation: "vertical"
        size_hint: 1, 0.7
        pos_hint: {"center_x": 0.5, "center_y": 0.7}
        FitImage:
            source: "addContact.png"
    MDFloatingActionButton:
        icon: "home"
        md_bg_color: 229/255.0,150/255.0,38/255.0,1
        pos_hint: {"center_x": 0.1, "center_y": 0.95}
        on_release: root.manager.current="main"       
    MDCard:
        orientation: "vertical"
        size_hint: 1, 0.5
        padding: "20dp"
        ScrollView:
            MDList:
                MDTextField:
                    id: FirstName
                    hint_text: "First name"
                    pos_hint: {"center_x": 0.5}
                MDTextField:
                    id: LastName
                    hint_text: "Last name"
                    pos_hint: {"center_x": 0.5}
                MDTextField:
                    id: Phone
                    hint_text: "Phone"
                    pos_hint: {"center_x": 0.5}
                MDTextField:
                    id: Email
                    hint_text: "Email"
                    pos_hint: {"center_x": 0.5}
        MDFloatingActionButton:
            icon: "content-save"
            pos_hint: {"center_x": 0.5,"center_y": 0.2}
            md_bg_color: 0,0,0,0.75
            on_release: app.saveContact()                                  
"""


class MainScreen(Screen):
    pass


class AddNumber(Screen):
    pass


sm = ScreenManager()
sm.add_widget(MainScreen(name="main"))
sm.add_widget(AddNumber(name="number"))


class TheBadjie(MDApp):
    def build(self):
        AppBuilder = Builder.load_string(String_Builder)
        return AppBuilder

    def saveContact(self):
        with open("contact.json", "r") as fr:
            reader = json.load(fr)

        FirstName = self.root.ids.screen_manager.get_screen("number").ids.FirstName.text
        LastName = self.root.ids.screen_manager.get_screen("number").ids.LastName.text
        Phone = self.root.ids.screen_manager.get_screen("number").ids.Phone.text
        Email = self.root.ids.screen_manager.get_screen("number").ids.Email.text
        with open("contact.json", "w") as f:
            reader[FirstName] = Phone
            json.dump(reader, f, indent=2)
        fr.close()
        self.root.ids.screen_manager.get_screen("number").ids.FirstName.text = ""
        self.root.ids.screen_manager.get_screen("number").ids.LastName.text = ""
        self.root.ids.screen_manager.get_screen("number").ids.Phone.text = ""
        self.root.ids.screen_manager.get_screen("number").ids.Email.text = ""
        self.on_start()

    def on_start(self):
        with open("Message_Sender\contact.json", "r") as fr:
            self.phone_numbers = json.load(fr)
        for key, value in self.phone_numbers.items():
            self.root.ids.screen_manager.get_screen("main").ids.phoneNums.add_widget(TwoLineListItem(text=key,
                                                                                                     secondary_text=value))

    def sendMessage(self):
        pass
        try:
            account_sid = 'AC6e55cf0ae5a8caa8ab3774998f1de4ab' 
            auth_token = "e5fd5a778413a4b33643304bd405522c"
            text_message = self.root.ids.screen_manager.get_screen("main").ids.message.text
            client = Client(account_sid, auth_token)
            self.messsageSid = ""
            message_splitter = str(text_message).split()
            if len(message_splitter) > 1:
                single_Num = self.phone_numbers[str(message_splitter[0])]  # single phone number to send to
                space_index = str(text_message).index(" ")

                if message_splitter[0] in self.phone_numbers:  # single phone number to send to condition

                    message = client.messages.create(
                        from_="+1 831 304 3302",
                        body=f'Message=>\n{text_message[int(space_index + 1):]}',
                        to=f'{single_Num}'
                    )
                    self.messsageSid += str(message) + '\n'

            else:
                dismisser = MDFlatButton(text="Dismiss",
                                         on_release=self.dismiss)
                for key, value in self.phone_numbers.items():
                    print(value)
                    message = client.messages.create(
                        from_="+1 831 304 3302",
                        body=f'Password=>\n{text_message}',
                        to=f'{value}'
                    )
                    self.messsageSid += str(message) + '\n'
                self.dialog = MDDialog(title="Message Sent!",
                                       text=self.messsageSid,
                                       buttons=[dismisser],
                                       size_hint=(0.75, 0.5)
                                       )
                self.dialog.open()
        except TwilioRestException as e:
            dismisser = MDFlatButton(text="Dismiss",
                                     on_release=self.dismiss)
            self.dialog = MDDialog(title="Error Message!",
                                   text=str(e),
                                   buttons=[dismisser],
                                   size_hint=(0.75, 0.5)
                                   )
            self.dialog.open()

    def dismiss(self, obj):
        pass
        self.dialog.dismiss()


TheBadjie().run()
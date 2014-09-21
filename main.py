# -*- coding: UTF-8 -*-

from random import randint
from os import name as os_name
import kivy

kivy.require('1.1.2')
if os_name == "nt":
    #running windows, let's emulate the correct screen size
    from kivy.config import Config
    Config.set('graphics', 'width', '540')
    Config.set('graphics', 'height', '560')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty # New property
from kivy.clock import Clock

# New Variable
# inside list -> [Question part, Good answer, Bad answer]
LANGUAGES = {"FRENCH": ["Combien font", "Bonne réponse", "Désolé"],
             "ENGLISH": ["What is", "Good answer", "Sorry"]}

class multipy(BoxLayout):
    """
        class comment
    """
    value1 = NumericProperty()
    value2 = NumericProperty()
    bon = NumericProperty()  #nombre de réponses justes
    score = NumericProperty()  #nombre de réponses justes consécutives
    total = NumericProperty()  #nombre de réponses données en tout
    record = NumericProperty()  #meilleur "score" de la session
    language_type = StringProperty() #  New Property

    def __init__(self, **args):
        BoxLayout.__init__(self)
        self.score = 0
        self.bon = 0
        self.total = 0
        self.record = 0
        
        # New Variables
        config = multipyApp.get_running_app().config
        language = config.getdefault("General", "language_type", "French")
        self.language_type = language.upper()
        # End new Variables
        
        self.newQuestion()

    def resetScore(self):
        self.score = 0

    def newQuestion(self):
        """Gennerates a new question"""
        language = LANGUAGES[self.language_type][0] # New Var
        print "\n\nMY NEW LANGUAGE IS", self.language_type
        
        self.value1 = randint(1, 10)
        self.value2 = randint(1, 10)
        self.ids.afficheur.text = ""
        self.ids.question.text = "{} {} x {} ?".format(language, # Add var here
                                            self.value1, self.value2)

    def control(self):
        """Verifies the result against the question"""
        good = LANGUAGES[self.language_type][1] # New Vars
        bad  = LANGUAGES[self.language_type][2] # New Vars
        
        cont = self.ids.afficheur.text
        correct = str(self.value1 * self.value2)
        if self.ids.afficheur.text == "":
            self.ids.afficheur.color = [1, 1, 1, 1]
        elif int(cont) == int(correct):
            popup = Popup(title='Bravo !',
                          title_color=[0.5, 1, 0.5, 1],
                          separator_color=[0.5, 1, 0.5, 1],
                          content=Label(text=
                                        "{} !\n{} x {} = {}".format(good, # Add here
                                            self.value1, self.value2, correct),
                                        font_size="32sp"),
                          size_hint=(1, 0.2))
            popup.open()
            Clock.schedule_once(popup.dismiss, 1)
            self.ids.afficheur.text = ""
            self.score += 1
            self.bon += 1
            if self.score > self.record:
                self.record = self.score

        elif int(cont) != int(correct):
            popup = Popup(title=bad, # And Here
                          title_color=[1, 0.5, 0.5, 1],
                          separator_color=[1, 0.5, 0.5, 1],
                          content=Label(text='{} x {} = {}'.format(self.value1,
                                                                   self.value2,
                                                                   correct),
                                        font_size="32sp"),
                          size_hint=(0.5, 0.2))
            popup.open()
            Clock.schedule_once(popup.dismiss, 5)
            self.resetScore()
        self.total += 1
        self.newQuestion()


class multipyApp(App):
    # New Var
    use_kivy_settings = False
    def build(self):
        self.title = 'Révision des Tables'
        return multipy()
    
    # New Method
    def build_config(self, config):
        config.setdefaults("General",{"language_type": "French"})
    
    # New Method
    def build_settings(self, settings):
        settings.add_json_panel("App Settings", self.config, data="""
            [
                {"type": "options",
                    "title": "Language Settings",
                    "section": "General",
                    "key": "language_type",
                    "options": ["English", "French"]
                }
            ]"""
        )
    
    # New Method
    def on_config_change(self, config, section, key, value):
        if config is self.config and key == "language_type":
            try:
                self.root.language_type = value.upper()
                self.root.newQuestion()
            except:
                pass
                

def main():
    multipyApp().run()


if __name__ == '__main__':
    main()

# -*- coding: UTF-8 -*-

from random import randint

import kivy
kivy.require('1.1.2')
#from kivy.config import Config
#Config.set('graphics', 'width', '540')
#Config.set('graphics', 'height', '960')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.clock import Clock


class multipy(BoxLayout):
    """
        class comment
    """
    value1 = NumericProperty()
    value2 = NumericProperty()
    bon = NumericProperty()     #nombre de réponses justes
    score = NumericProperty()   #nombre de réponses justes consécutives
    total = NumericProperty()   #nombre de réponses données en tout
    record = NumericProperty()  #meilleur "score" de la session

    def __init__(self, **args):
        BoxLayout.__init__(self)
        self.score = 0
        self.bon = 0
        self.total = 0
        self.newQuestion()
        self.record = 0

    def resetScore(self):
        self.score = 0

    def newQuestion(self):
        """Gennerates a new question"""
        self.value1 = randint(1, 10)
        self.value2 = randint(1, 10)
        self.ids.afficheur.text = ""
        self.ids.question.text = "Combien font {} x {} ?".format(self.value1, self.value2)

    def control(self):
        """Verifies the result against the question"""
        cont = self.ids.afficheur.text
        correct = str(self.value1*self.value2)
        if self.ids.afficheur.text == "":
            self.ids.afficheur.color = [1, 1, 1, 1]
        elif int(cont) == int(correct):
            popup = Popup(title='Bravo !',
                          title_color=[0.5, 1, 0.5, 1],
                          separator_color=[0.5, 1, 0.5, 1],
                          content=Label(text='Bonne réponse !\n{} x {} = {}'.format(self.value1,self.value2,correct),
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
            popup = Popup(title='Désolé',
                          title_color=[1, 0.5, 0.5, 1],
                          separator_color=[1, 0.5, 0.5, 1],
                          content=Label(text='{} x {} = {}'.format(self.value1,self.value2,correct),
                            font_size="32sp"),
                          size_hint=(0.5, 0.2))
            popup.open()
            Clock.schedule_once(popup.dismiss, 5)
            self.resetScore()
        self.total += 1
        self.newQuestion()


class multipyApp(App):
    def build(self):
        self.title = 'Révision des Tables'
        return multipy()


def main():
    multipyApp().run()

if __name__ == '__main__':
    main()

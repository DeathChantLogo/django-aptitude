import random

from django.db.models import get_model
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe as ms
from django.template.defaultfilters import escape, linebreaksbr

from question_parsers import *

class RenderMixin(object):
    
    def render(self, session=None, difficulty=None, test=False):
        """
        Parses the choices data, makes the RenderedQuestion object, saves it
        to the database, and then returns it. The 'test' option does not save
        the RenderedQuestion instance into the database
        """
        
        # done this way to avoid recursive imports
        RenderedQuestion = get_model('aptitude', 'RenderedQuestion')
    
        try:
            parsed = self.parse(difficulty)
        except:
            parsed = {"text": self.text,
                      "right": 'correct (unable to parse question choices)',
                      "wrong": ['wrong', 'wrong', 'wrong']}
        
        # shuffle all the choices, right and wrong
        choices = parsed['wrong'] + [parsed['right']]
        random.shuffle(choices)
        
        text = parsed['text']
        right = parsed['right']
        
        # figure out which one of the choices will be the correct answer
        choice_letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m']
        for index,choice in enumerate(choices):
            letter = choice_letters[index]

            if choice == right:
                correct_choice_letter = letter
        
        html = render_to_string('question_render.html',
                               {'choices': choices,
                                'question_text': text})
        
        if not session:
            from models import AptSession
            session = AptSession(id=0)
                              
        rq = RenderedQuestion(aptsession=session, html=html,
                              correct_choice=correct_choice_letter,
                              data=self)
                                  
        if not test:                          
            rq.save()
        
        return rq
  
    def parse(self, difficulty=None):
        """
        Call the correct parser depending on the type of question, returns
        a dict with the correct choices and wrong choices in a list
        """
        
        Renderer = globals()[self.get_type_display() + "Renderer"]
        
        r = Renderer(difficulty=difficulty,
                     text=self.text,
                     choices=self.choices)
                            
        return r.split_choices()



























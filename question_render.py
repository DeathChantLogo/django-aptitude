import random

from django.db.models import get_model
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe as ms
from django.template.defaultfilters import escape, linebreaksbr

class RenderMixin(object):
    
    def render(self, session, difficulty=None):
        """
        Parses the choices data, makes the RenderedQuestion object, saves it
        to the database, and then returns it.
        """
        
        # done this way to avoid recursive imports
        RenderedQuestion = get_model('aptitude', 'RenderedQuestion')
        
        parsed = self.parse(difficulty)
        
        if parsed is None:
            parsed = {"right": ['unable to parse'],
                      "wrong": ['derp', 'doop', 'poop'],
                      "type": "regular"}
        
        # convert all newlines into <br> tags only if the question is not a
        # snippet type question
        space2br = 'snippet' not in parsed['type']
        
        # shuffle all the choices, right and wrong
        choices = parsed['wrong'] + parsed['right']
        random.shuffle(choices)
        
        html = render_to_string('question_render.html',
                               {'choices': choices,
                                'question_text': self.text})
        
        # figure out which one of the choices will be the correct answer
        choice_letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m']
        for index,choice in enumerate(choices):
            letter = choice_letters[index]
            choice = escape(linebreaksbr(choice)) if space2br else choice

            if choice == parsed['right'][0]:
                correct_choice_letter = letter
        
        rq = RenderedQuestion(aptsession=session, html=html,
                              correct_choice=correct_choice_letter,
                              data=self)
        rq.save()
        
        return rq
        
    def parse(self, difficulty=None):
        """
        Call the correct parser depending on the type of question
        """
    
        if self.type == 1:
            return self._parse_regular_choices()
        
        elif self.type == 5:
            return self._parse_snippet_choices()
    
        return None
    
    def _parse_regular_choices(self):
        """
        Gets the choices for regular ol' questions
        returns them as a dict of lists
        """
        
        wrong_choices = []
        correct_choice = None
        
        for opt in self.choices.splitlines():
            if opt.startswith('<c>'):
                correct_choice = [opt[3:]]
            else:
                wrong_choices.append(opt)
                
        if not correct_choice:
            # if no correct choice is found with the <c> tag, then
            # just use the first choice as the correct one
            correct_choice = [wrong_choices[0]]
            wrong_choices = wrong_choices[1:]
        
        return {"right": correct_choice,
                "wrong": wrong_choices,
                "type": "regular"}
                
    def _parse_snippet_choices(self):
        """
        Gets the choices for snippet questions
        returns them as a dict of lists
        The first choice is always the correct choice, also it adds <tt> tags
        """
        
        split = self.choices.splitlines()
        
        # iterate through the lines until you get to the first line of dashes
        # all these lines make up the correct snippet, everything below makes
        # up the wrong snippets
        
        correct_choice = []
        done_with_first = False
        wrong_lines = []
        
        for line in split:
            if not line.startswith('---') and not done_with_first:
                correct_choice.append(line)
            elif done_with_first:
                wrong_lines.append(line)
            elif line.startswith('---'):
                done_with_first = True
        
        # turn the lines into a string with newlines between them, and then
        # make into a single list
        correct_choice = ["\n".join(correct_choice)]
        
        # iterate again, this time putting each line between the dashes into
        # a seperate question item
        
        wrong_choices = []
        this_choice = []
        
        for line in wrong_lines:
            if not line.startswith('---'):
                this_choice.append(line)
            else:
                wrong_choices.append("\n".join(this_choice))
                this_choice = []
        
        # join the last line because there shouldn't be a trailing "---" at the
        # end of the snippets
        wrong_choices.append("\n".join(this_choice))
        
        ###################### add the <tt> tag to each choice
        
        pre = lambda x: "<pre>" + str(x) + "</pre>"
        
        pre_correct_choice = [pre(correct_choice[0])]
            
        pre_wrong_choices = []
        for line in wrong_choices:
            pre_wrong_choices.append(pre(line))
        
        return {"right": pre_correct_choice,
                "wrong": pre_wrong_choices,
                "type": "snippet"}



























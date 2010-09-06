import random

import markdown
import utils

def convert_no_p(*a, **k):
    "Monkey patch to not have markdown.convert wrap everything in <p> tags"
    return markdown.Markdown.convert(*a, **k)[3:][:-4]
setattr(markdown.Markdown, 'convert_no_p', convert_no_p)

class GenericParser(object):
    def __init__(self, text, choices, difficulty=50, mode='html4'):
        self.choices_raw = choices.strip()
        self.mode = mode
        self.md = markdown.Markdown(output_format=mode).convert
        self.text = text
        self.difficulty = difficulty

class RegularParser(GenericParser):
    
    def split_choices(self):
        
        text = self.md(self.text)
        
        self.md = markdown.Markdown(output_format=self.mode).convert_no_p
        
        wrong_choices = []
        correct_choice = None
        
        for opt in self.choices_raw.splitlines():
            if opt.startswith('<c>'):
                correct_choice = self.md(opt[3:])
            else:
                #print opt
                wrong_choices.append(self.md(opt))
        
        if not correct_choice:
            # if no correct choice is found with the <c> tag, then
            # just use the first choice as the correct one
            correct_choice = wrong_choices[0]
            wrong_choices = wrong_choices[1:]
        
        #print wrong_choices
        
        return {"text": text,
                "right": correct_choice,
                "wrong": wrong_choices}
                
class SnippetRegularParser(GenericParser):
    
    def split_choices(self):
        """
        Gets the choices for snippet questions returns them as a dict of lists
        The first choice is always the correct choice, also it adds tags
        """

        # iterate through the lines until you get to the first line of dashes
        # all these lines make up the correct snippet, everything below makes
        # up the wrong snippets
        
        correct_choice = []
        done_with_first = False
        wrong_lines = []
        
        for line in self.choices_raw.splitlines():
            if not line.startswith('---') and not done_with_first:
                correct_choice.append('    ' + line) # add 4 spaces for markdown
            elif done_with_first:
                wrong_lines.append('    ' + line)
            elif line.startswith('---'):
                done_with_first = True
        
        # needs to be a list for consistency
        correct_choice = self.md("\n".join(correct_choice))
        
        # iterate again, this time putting each line between the dashes into
        # a seperate question item
        
        wrong_choices = []
        this_choice = []
        
        for line in wrong_lines:
            if not line.startswith('    ---'):
                this_choice.append(line)
            else:
                wrong_choices.append(self.md("\n".join(this_choice)))
                this_choice = []
        
        # join the last line because there shouldn't be a trailing "---" at the
        # end of the snippets
        wrong_choices.append(self.md("\n".join(this_choice)))
        
        return {"text": self.md(self.text),
                "right": correct_choice,
                "wrong": wrong_choices}

class PythonVersionParser(GenericParser):
    VERSIONS = ['0.5', '0.7', '0.9.0', '1.0', '1.1', '1.2', '1.3', '1.4', '1.5',
                '1.8', '2.0', '2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.6.5',
                '2.7', '3.0', '3.1', '3.2']
    
    def split_choices(self):
        ret = utils.parse_python_version(self.choices_raw, self.VERSIONS)
        rand = random.random()
        wrong_choice_count = 2  # the number of wrong choices to render
        
        text = self.md(self.text)
        right = ret['right']
        wrong = ret['wrong']
        
        number_of_right = len(right)
        number_of_wrong = len(wrong)

        # one random right answer
        single_right = right[int(number_of_right*random.random())] 
        
        # a list random wrong answers (makes sure none are duplicated)
        choices_wrong = []
        while len(choices_wrong) < wrong_choice_count:
            index = int(number_of_wrong*random.random())
            rand_wrong = wrong[index]
            if not rand_wrong in choices_wrong:
                choices_wrong.append(rand_wrong)
        
        return {'text': text, 
                'right': single_right,
                'wrong': choices_wrong}
            
        
        
        
        
        
        
        
        
        

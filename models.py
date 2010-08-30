import random

from django.db import models
from django.conf import settings

from question_render import RenderMixin

QUESTION_TYPES = (
                    (1, "Regular"),
                    (5, "SnippetRegular"),
                    (2, "DownScale"),
                    (3, "TimeScale"),
                    (4, "PythonVersion"),
                 )

__all__ = ['QuestionData', 'AptSession', 'RenderedQuestion']

class AptSession(models.Model):
    """
    This model handles the testing session. It keeps track of how many questions
    have been asked, and how many of them are correct. If the `time_ended`
    attribute is null, the test is still in session, otherwise, the grade is
    final.
    """
    
    user = models.ForeignKey('auth.User')
    user_index = models.IntegerField(default=1) #1st/2nd/3rd test they've taken

    d_right = models.IntegerField(default=0)
    d_wrong = models.IntegerField(default=0)
    
    c_right = models.IntegerField(default=0)
    c_wrong = models.IntegerField(default=0)
    
    b_right = models.IntegerField(default=0)
    b_wrong = models.IntegerField(default=0)
    
    a_right = models.IntegerField(default=0)
    a_wrong = models.IntegerField(default=0)
    a_score = models.IntegerField(default=100)
    
    final_grade = models.CharField(max_length=5, blank=True)
    
    time_started = models.DateTimeField(auto_now_add=True)
    time_ended = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        
        if not self.time_ended:
            return "%s - still in session" % self.user.username
    
        return "%s (%s) - %s" % (self.user.username, self.user_index,
                                 self.final_grade)
                                 
    def increment_right_wrong(self, right_wrong, difficulty):
        """
        Save the status of the answer of a question as either being right or
        wrong.
        right_wrong = a string either "right" or "wrong"
        difficulty = 'a1' or 'b' or 'c' or 'd' or 'a5', etc.
        """
        
        letter = difficulty[0]
        
        if len(difficulty) == 1:
            old = getattr(self, "%s_%s" % (letter.lower(), right_wrong))
            setattr(self, "%s_%s" % (letter.lower(), right_wrong), old + 1)
            
        elif right_wrong == 'wrong':
            score = int(difficulty[1:])
            self.a_score -= score
        
        self.save()
    
    
    def get_question_data(self):
        """
        Get the next QuestionData object to ask the user. Returns None if the
        test is completed.
        """
        
        if self.total_asked() >= settings.TOTAL_QUESTION_COUNT:
            return None
        
        index = random.randint(0, QuestionData.objects.count() - 1)
        return QuestionData.objects.all()[index]

    def total_asked(self):
        """
        Returns the total number of questions already asked for this session
        """
        
        return (self.a_right + self.b_right + self.c_right + self.d_right +
                self.a_wrong + self.b_wrong + self.c_wrong + self.d_wrong)

    def calc_final_grade(self):
        return "not implemented yet"

    def get_final_grade(self):
        """
        Returns the grade for this session, if it isn't already set, it will
        calculate it and then save the results.
        """
        
        if self.final_grade:
            return self.final_grade
        
        if not self.time_ended:
            self.final_grade = self.calc_final_grade()
            self.save()
            return self.final_grade
        
        return "N/A"
        
class QuestionData(models.Model, RenderMixin):
    """
    Raw question data. Used to define each question that will be asked.
    """
    
    text = models.TextField()
    choices = models.TextField()
    type = models.IntegerField(choices=QUESTION_TYPES, default=1)
    difficulty = models.CharField(max_length=3)
    
    def __unicode__(self):
        return "%s - %s" % (self.text, self.get_type_display())


class RenderedQuestion(models.Model):
    """
    A QuestionData instance that has been rendered into HTML. Each rendering
    has it's choices shuffled and sometimes even varying question test and
    number of choices. Each instance has attached to it the correct answer
    for later grading.
    """
    
    html = models.TextField()
    correct_choice = models.CharField(max_length=1)
    answered_choice = models.CharField(max_length=1)
    aptsession = models.ForeignKey('AptSession')
    data = models.ForeignKey('QuestionData')
    
    def __unicode__(self):
        correct = self.correct_choice == self.answered_choice
        return "%s - %s" % (self.pk, correct)
    
    def grade(self, answer):
        """
        determine if the answer given is correct or not.
        """
        
        return answer.upper() == self.correct_choice.upper()

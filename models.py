import random

from django.db import models
from question_render import RenderMixin

QUESTION_TYPES = (
                    (1, "Regular"),
                    (5, "SnippetRegular"),
                    (2, "DownScale"),
                    (3, "TimeScale"),
                    (4, "VersionScale"),
                 )

__all__ = ['QuestionData', 'Session', 'RenderedQuestion']

class Session(models.Model):
    user = models.ForeignKey('auth.User')
    user_index = models.IntegerField(default=1) #1st/2nd/3rd test they've taken

    d_asked = models.IntegerField(default=0)
    d_score = models.FloatField(default=0)
    
    c_asked = models.IntegerField(default=0)
    c_score = models.FloatField(default=0)
    
    b_asked = models.IntegerField(default=0)
    b_score = models.FloatField(default=0)
    
    a_asked = models.IntegerField(default=0)    
    a_score = models.FloatField(default=100)
    
    final_grade = models.CharField(max_length=3, blank=True)
    
    time_started = models.DateTimeField(auto_now_add=True)
    time_ended = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        if not self.time_ended:
            return "%s - still in session" % self.user.username
        
        grade = self.final_grade
        if grade == 'A':
            grade = "%s-%s" % (self.final_grade, self.a_score)
            
        return "%s (%s) - %s" % (self.user.username, self.user_index, grade)
    
    def get_question_data(self):
        """
        Get the next QuestionData object to ask the user
        """
        index = random.randint(0, QuestionData.objects.count() - 1)
        return QuestionData.objects.all()[index]

    def total_asked(self):
        """
        Returns the total number of questions already asked
        """
        
        return self.a_asked + self.b_asked + self.c_asked + self.d_asked


class QuestionData(models.Model, RenderMixin):
    text = models.TextField()
    choices = models.TextField()
    type = models.IntegerField(choices=QUESTION_TYPES)
    difficulty = models.CharField(max_length=3)
    
    def __unicode__(self):
        return self.text


class RenderedQuestion(models.Model):
    html = models.TextField()
    correct_choice = models.CharField(max_length=1)
    answered_choice = models.CharField(max_length=1)
    session = models.ForeignKey('session')
    data = models.ForeignKey('questiondata')
    
    def __unicode__(self):
        correct = self.correct_choice == self.answered_choice
        return "%s - %s" % (self.pk, correct)
    
    def grade(self, answer):
        """
        determine if the answer given is correct or not.
        """
        
        return answer.upper() == self.correct_choice.upper()

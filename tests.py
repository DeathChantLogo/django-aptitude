"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from models import QuestionData

from utils import parse_python_version

class ParseTest(TestCase):
    def test_tagged_regular_parsing(self):
        """
        Tests that rendering of regular test questions work when a <c>
        tag is used to denote the correct answer
        """
        
        q = QuestionData(text="guess the answer", choices="a\n<c>b\nc", type=1)
        q.save()
        
        parsed = q.parse()
        
        self.assertEquals(parsed['right'], u'b')
        self.assertEquals(parsed['wrong'], [u'a', u'c'])

    
    def test_untagged_regular_parsing(self):
        """
        Tests that rendering of regular test questions work when there is
        no <c> tag
        """
        
        q = QuestionData(text="guess the answer", choices="a\nb\nc", type=1)
        q.save()
        
        parsed = q.parse()
        
        self.assertEquals(parsed['right'], u'a')
        self.assertEquals(parsed['wrong'], [u'b', u'c'])
        
    def test_snippet_choices(self):
        """
        Test that the snippet rendered is working correctly
        """
        
        ch = "snippet\nright\nwoop\n---\nwrong\nd\nw\n---\na\nb\nc\n---\ng"
        
        q = QuestionData(text="guess the answer", choices=ch, type=5)
        q.save()
        
        parsed = q.parse()
        
        self.assertEquals(parsed['right'], '<pre><code>snippet\nright\nwoop\n</code></pre>')
        self.assertEquals(parsed['wrong'][0], '<pre><code>wrong\nd\nw\n</code></pre>')
        self.assertEquals(parsed['wrong'][1], '<pre><code>a\nb\nc\n</code></pre>')
        self.assertEquals(parsed['wrong'][2], '<pre><code>g\n</code></pre>')

    def test_pythonversion_choices(self):
        
        ch = "2.6"
        
        q = QuestionData(text="guess the answer", choices=ch, type=4)
        q.save()
        
        parsed = q.parse()
        
        self.assertEquals(parsed['right'], ['2.6'])















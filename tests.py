"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from models import QuestionData

from utils import parse_python_version

class ParseTest(TestCase):
    """
    General question parsing tests
    """
    
    def test_tagged_regular_parsing(self):
        """
        Rendering of regular test questions work when a <c>
        tag is used to denote the correct answer
        """
        
        q = QuestionData(text="guess the answer", choices="a\n<c>b\nc", type=1)
        q.save()
        
        parsed = q.parse()
        
        self.assertEquals(parsed['right'], u'b')
        self.assertEquals(parsed['wrong'], [u'a', u'c'])

    
    def test_untagged_regular_parsing(self):
        """
        Rendering of regular test questions work when there is no <c> tag
        """
        
        q = QuestionData.objects.create(text="ff", choices="a\nb\nc", type=1)
        parsed = q.parse()
        
        self.assertEquals(parsed['right'], u'a')
        self.assertEquals(parsed['wrong'], [u'b', u'c'])
        
    def test_snippet_choices(self):
        """
        Snippet render is working correctly
        """
        
        ch = "snippet\nright\nwoop\n---\nwrong\nd\nw\n---\na\nb\nc\n---\ng"
        
        q = QuestionData.objects.create(text="ff", choices=ch, type=5)
        parsed = q.parse()
        
        self.assertEquals(parsed['right'], '<pre><code>snippet\nright\nwoop\n</code></pre>')
        self.assertEquals(parsed['wrong'][0], '<pre><code>wrong\nd\nw\n</code></pre>')
        self.assertEquals(parsed['wrong'][1], '<pre><code>a\nb\nc\n</code></pre>')
        self.assertEquals(parsed['wrong'][2], '<pre><code>g\n</code></pre>')

    def test_strip_choices(self):
        """
        Strip all leading whitespace from each question before rendering
        """
        
        ch = "\n\n \na\nb\nc\n\n    \n\n   \n"
        
        q = QuestionData.objects.create(text="ff", choices=ch, type=1)
        parsed = q.parse()

        self.assertEquals(parsed['right'], u'a')
        self.assertEquals(parsed['wrong'], [u'b', u'c'])

class PythonParseTest(TestCase):
    VERSIONS = ['0.9', '1.0', '1.8', '2.0', '2.6', '2.7', '3.0', '3.1']

    def test_greater(self):
        correct = {'right': ['2.7', '3.0', '3.1'],
                   'wrong': ['0.9', '1.0', '1.8', '2.0', '2.6']}
                   
        r = parse_python_version('>2.7', self.VERSIONS)
        self.assertEquals(r, correct)
                              
        r = parse_python_version('2.7+', self.VERSIONS)
        self.assertEquals(r, correct)
        
    def test_x(self):
        r = parse_python_version('2.x', self.VERSIONS)
        self.assertEquals(r, {'right': ['2.0', '2.6', '2.7'],
                              'wrong': ['0.9', '1.0', '1.8', '3.0', '3.1']})

        r = parse_python_version('3.x', self.VERSIONS)
        self.assertEquals(r, {'right': ['3.0', '3.1'],
                              'wrong': ['0.9', '1.0', '1.8', '2.0', '2.6', '2.7']})
        
        r = parse_python_version('1.x', self.VERSIONS)
        self.assertEquals(r, {'right': ['1.0', '1.8'],
                              'wrong': ['0.9', '2.0', '2.6', '2.7', '3.0', '3.1']})
                              
    def test_lesser(self):
        r = parse_python_version('<2.6', self.VERSIONS)
        self.assertEquals(r, {'right': ['0.9', '1.0', '1.8', '2.0'],
                              'wrong': ['2.6', '2.7', '3.0', '3.1']})
                              
    def test_single(self):
        r = parse_python_version('2.6', self.VERSIONS)
        self.assertEquals(r, {'right': ['2.6'],
                              'wrong': ['0.9', '1.0', '1.8', '2.0',
                                        '2.7', '3.0', '3.1']})

        r = parse_python_version('0.9', self.VERSIONS)
        self.assertEquals(r, {'right': ['0.9'],
                              'wrong': ['1.0', '1.8', '2.0', '2.6',
                                        '2.7', '3.0', '3.1']})






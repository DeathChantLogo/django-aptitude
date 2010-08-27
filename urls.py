from django.conf.urls.defaults import *

urlpatterns = patterns('aptitude.views',
    url('session-(?P<session_pk>\d+)', 'question', name="question"),
    url('answer-(?P<rendered_pk>\d+)', 'answer', name="answer"),
    url('start_session', 'start_session', name="start_session"),
)

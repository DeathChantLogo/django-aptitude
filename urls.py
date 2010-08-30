from django.conf.urls.defaults import *

urlpatterns = patterns('aptitude.views',
    url('session-(?P<session_pk>\d+)/(?P<q_index>\d+)', 'question', name="question"),
    url('answer-(?P<rendered_pk>\d+)', 'answer', name="answer"),
    url('start_session', 'start_session', name="start_session"),
    url('session_complete-(?P<session_pk>\d+)', 'session_complete', name="session_complete"),
    url('test_question-(?P<pk>\d+)', 'test_question')
)

from main.decorators import render_to
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from models import *


@render_to('question_display.html')
def question(request, session_pk):
    session = Session.objects.get(pk=session_pk)
    
    rq = session.get_question_data().render(session)

    return locals()
    
    
def answer(request, rendered_pk):
    """
    When the user answeres a question, the data gets POSTed to this view. It
    then gets graded, and a new question is rendered.
    """
    
    rq = RenderedQuestion.objects.get(pk=rendered_pk)
    session = rq.session
    
    answer = request.POST['choice']
    right = rq.grade(answer)
    difficulty = rq.data.difficulty
    letter = difficulty[0] # the difficulty can either be F/D/C. etc or A##
    
    #incriment the total number of questions asked for this difficulty.
    asked = getattr(session, letter.lower() + "_asked")
    setattr(session, letter.lower() + "_asked", asked + 1)
    session.save()
    
    url = reverse('question', args=[session.pk])
    return HttpResponseRedirect(url)


@render_to('test_done.html')
def session_complete(request, session):
    return locals()


def start_session(request):
    """
    Create a session, and then get started!
    """

    if Session.objects.filter(user=request.user, time_ended__isnull=True).exists():
        return None
    
    session = Session(user=request.user)
    session.save()
    
    url = reverse('question', args=[session.pk])
    return HttpResponseRedirect(url)

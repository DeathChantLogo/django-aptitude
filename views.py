from main.decorators import render_to
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from models import AptSession, RenderedQuestion


@render_to('question_display.html')
def question(request, session_pk):
    session = AptSession.objects.get(pk=session_pk)
    
    rq = session.get_question_data().render(session)

    return locals()
    
    
def answer(request, rendered_pk):
    """
    When the user answeres a question, the data gets POSTed to this view. It
    then gets graded, and a new question is rendered.
    """
    
    rq = RenderedQuestion.objects.get(pk=rendered_pk)
    session = rq.aptsession
    
    answer = request.POST['choice']
    right_wrong = "right" if rq.grade(answer) else "wrong"
    difficulty = rq.data.difficulty
    
    #incriment the total number of questions asked for this difficulty.
    session.increment_right_wrong(right_wrong, difficulty)
    
    url = reverse('question', args=[session.pk])
    return HttpResponseRedirect(url)


@render_to('test_done.html')
def session_complete(request, session):
    return locals()


def start_session(request):
    """
    Create a session, and then get started!
    """

    if AptSession.objects.filter(user=request.user, time_ended__isnull=True).exists():
        return None
    
    session = AptSession(user=request.user)
    session.save()
    
    # go to the first question
    url = reverse('question', args=[session.pk])
    return HttpResponseRedirect(url)

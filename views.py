from main.decorators import render_to
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from models import AptSession, RenderedQuestion, QuestionData


@render_to('question_display.html')
def question(request, session_pk, q_index):
    """
    This view chooses the question, and then renders it.
    """
    
    session = AptSession.objects.get(pk=session_pk)
    q_number = session.total_answered() + 1
    data = session.get_question_data()
    question_id = data.pk
    
    if data:
        rq = data.render(session)
    else:
        # the session will return None instead of a question when the session
        # is complete
        url = reverse('session_complete', args=[session.pk])
        return HttpResponseRedirect(url)

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
    
    url = reverse('question', kwargs={'session_pk': session.pk,
                                      'q_index': session.total_answered()})
    return HttpResponseRedirect(url)


@render_to('test_done.html')
def session_complete(request, session_pk):
    return locals()


def start_session(request):
    """
    Create a session, and then get started! Or, if an open session exists,
    resume it instead
    """
    
    try:
        session = AptSession.objects.filter(user=request.user,
                                            time_ended__isnull=True)[0]
    except (AptSession.DoesNotExist, IndexError):
        session = AptSession(user=request.user)
        session.save()
        q = 1  # created a new session, go to first question
        
    else:
        # resuming session, return to next question
        q = session.total_answered() + 1
        
    url = reverse('question', kwargs={'session_pk': session.pk,
                                      'q_index': q})    
    return HttpResponseRedirect(url)


@render_to('question_display.html')
def test_question(request, pk, difficulty=50):
    """
    Render this question in the browser to make sure it looks OK.
    """
    
    data = QuestionData.objects.get(pk=pk)
    rq = data.render(session=None, difficulty=difficulty, test=True)
    return locals()
    




























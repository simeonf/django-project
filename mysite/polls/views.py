from django.shortcuts import render_to_response, get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect

from polls.forms import RegistrationForm

from polls.models import Poll, Choice

def register(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        if form.save():
            u = authenticate(username=form.cleaned_data['username'],
                             password=form.cleaned_data['password1'])
            login(request, u)
            return HttpResponseRedirect("/polls/")
    return render(request, "registration/register.html", {'form': form})

    
def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render(request, 'polls/index.html',
                              {'latest_poll_list' : latest_poll_list})

def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/detail.html',
                              {'poll': poll})
                 
def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll':poll})

@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('polls/detail.html', {
            'poll': poll,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('poll_results', args=(poll.id,)))

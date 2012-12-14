from django.shortcuts import render_to_response, get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect

from polls.forms import RegistrationForm, VoteForm, ProfileForm

from polls.models import Poll, Choice

def register(request):
    form = RegistrationForm(request.POST or None, prefix="rf")
    form2 = ProfileForm(request.POST or None, prefix="up")
    if form.is_valid() and form2.is_valid():
        if form.save():
            u = authenticate(username=form.cleaned_data['username'],
                             password=form.cleaned_data['password1'])
            user_profile = form2.save(commit=False)
            user_profile.user = u
            user_profile.save()
            login(request, u)
            return HttpResponseRedirect(reverse("poll_index"))
    return render(request, "registration/register.html",
                  {'form': form, 'up_form': form2})


def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render(request, 'polls/index.html',
                              {'latest_poll_list' : latest_poll_list})

def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    form = VoteForm(request.POST or None)
    form.fields['choice'].queryset = Choice.objects.filter(poll=poll)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(poll.get_absolute_url() + "results/")
    return render(request, 'polls/detail.html',
                              {'poll': poll, 'form': form})

def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll':poll})

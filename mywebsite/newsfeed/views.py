from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Question, Choice
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NameForm


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'newsfeed/formtest.html', {'form': form})


class IndexView(generic.ListView):
    template_name = 'newsfeed/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'newsfeed/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'newsfeed/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'newsfeed/detail.html', {
            'error_message': "You did not make a choice",
            'question': question,
        })
    else:
        choice.votes += 1
        choice.save()
    return HttpResponseRedirect(reverse('newsfeed:results', args=(question.id,)))


def latest(request):
    response = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': response
    }
    return render(request, 'newsfeed/index.html', context)

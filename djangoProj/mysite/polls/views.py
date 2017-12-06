from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views import generic


from .models import Question, Choice, Airbnb_listing, business, attribute, category
import csv

def index(request):
    template_name = 'polls/index.html'
    latest_airbnb_list = Airbnb_listing.objects.order_by('price')[:5]
    #context_object_name = 'latest_airbnb_list'
    cities = Airbnb_listing.objects.order_by().values('city').distinct()
    context = {'latest_airbnb_list': latest_airbnb_list,'cities': cities}
    return render(request, template_name, context)


    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Airbnb_listing.objects.order_by('price')[:5]

def yours(request):
    city = request.POST.get("Cities", "")
    Price_Range = request.POST.get("Price_Range", "")
    num_adults = request.POST.get("Adults", "")
    num_kids = request.POST.get("Kids", "")
    rating = request.POST.get("star", "")
    context = {'city': city,
                'Price_Range': Price_Range,
                'num_adults': num_adults,
                'num_kids': num_kids,
                'rating': rating
            }
    return render(request, 'polls/yours.html', context)





class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

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
    More_Cuisines = ["Afghan", "American (Traditional)", "Arabian" ,"Argentine",
        "Asian Fusion","Barbeque","Beer Garden","Bistros","Brazilian","Buffets","Bulgarian", "Cafes","Cajun/Creole" ,
        "Caribbean","Colombian","Creperies","Cuban","Delis" ,"Diners","Dinner Theater","Ethiopian","French" ,
        "German", "Greek","Haitian","Halal","Indian" ,"Indonesian","Japanese" ,"Korean","Latin American",
        "Mediterranean" ,"Middle Eastern","Mongolian" ,"Moroccan","Noodles","Pakistani","Pan Asian","Peruvian",
        "Portuguese","Puerto Rican","Seafood","Senegalese","Singaporean","Soul Food","Southern","Spanish","Steakhouses",
        "Taiwanese","Tapas/Small Plates","Tex-Mex","Thai","Turkish","Venezuelan" ,"Vietnamese","Wok"]

    Activities = ["ATV Rentals/Tours","Amusement Parks","Aquariums","Archery","Badminton" ,
        "Baseball Fields" ,"Basketball Courts" ,"Beaches" ,"Bicycle Paths","Boating" ,
        "Bobsledding","Bowling" ,"Bungee Jumping" ,"Carousels" ,"Climbing" ,"Free Diving" ,"Scuba Diving",
        "Fishing" , "Go Karts" ,"Golf" ,"Hiking" ,"Horseback Riding" ,"Hot Air Balloons" ,"Jet Skis" ,
        "Laser Tag" ,"Mini Golf" , "Paddleboarding" ,"Paintball" ,"Parasailing","Parks" ,
        "Playgrounds" ,"Rafting/Kayaking" ,"Rock Climbing" ,"Sailing" ,"Skating Rinks" ,
        "Skiing" ,"Skydiving" ,"Sledding" ,"Snorkeling","Surfing" ,"Swimming Pools",
        "Water Parks" , "Ziplining" ,"Beauty & Spas","Zoos" ]

    arts = ["Arcades","Art Galleries","Betting Centers","Botanical Gardens","Cabaret" ,
        "Casinos","Cinema","Cultural Center","Festivals","Haunted Houses","Jazz & Blues",
        "LAN Centers","Museums","Children's Museums","Music Venues" ,"Observatories" ,"Opera & Ballet" ,
        "Performing Arts" ,"Planetarium" ,"Professional Sports Teams", "Race Tracks",
        "Rodeo","Social Clubs" ,"Veterans Organizations","Stadiums & Arenas","Street Art" ,
        "Supernatural Readings","Psychics","Wineries" ,"Wine Tasting Room" ,"Nightlife","Tours"]

    city = request.POST.get("Cities", "")
    Price_Range = request.POST.get("Price_Range", "")
    num_adults = request.POST.get("Adults", "")
    num_kids = request.POST.get("Kids", "")
    rating = request.POST.get("star", "")
    context = {'city': city,
                'Price_Range': Price_Range,
                'num_adults': num_adults,
                'num_kids': num_kids,
                'rating': rating,
                'More_Cuisines': More_Cuisines,
                'Activities': Activities,
                'arts': arts
            }
    return render(request, 'polls/yours.html', context)

def done(request):
    city = request.POST.get("Cities", "")
    Price_Range = request.POST.get("Price_Range", "")
    num_adults = request.POST.get("Adults", "")
    num_kids = request.POST.get("Kids", "")
    rating = request.POST.get("star", "")
    firstname = request.POST.get("firstname", "")
    Cuisines = request.POST.getlist('Cuisines', [])
    Activities = request.POST.getlist('Activities', [])
    Entertainment = request.POST.getlist('Entertainment', [])
    Diet = request.POST.getlist('Diet', [])

    context = {'city': city,
                'Price_Range': Price_Range,
                'num_adults': num_adults,
                'num_kids': num_kids,
                'rating': rating,
                'firstname':firstname,
                'Cuisines':Cuisines,
                'Activities':Activities,
                'Entertainment':Entertainment,
                'Diet':Diet

                }
    return render(request, 'polls/done.html', context)




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

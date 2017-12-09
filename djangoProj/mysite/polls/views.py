from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.db.models import Min, Max, Avg


from .models import Question, Choice, Airbnb_listing, business, attribute, category
import csv
import operator
from math import sin, cos, sqrt, atan2, radians, floor
from geopy.distance import great_circle

def index(request):
    template_name = 'polls/index.html'
    latest_airbnb_list = Airbnb_listing.objects.order_by('price')[:5]

    lowest_price = Airbnb_listing.objects.filter().values('price').annotate(Min('price')).order_by('price')[1]['price']
    cheapest_airbnb = Airbnb_listing.objects.get(price=lowest_price)

    max_price = Airbnb_listing.objects.filter().values('price').annotate(Max('price')).order_by('-price')[0]['price']
    expensive_airbnb = Airbnb_listing.objects.get(price=max_price)

    avg_abnb = Airbnb_listing.objects.all().aggregate(Avg('price'))
    average_price = avg_abnb["price__avg"]

    #context_object_name = 'latest_airbnb_list'
    cities = Airbnb_listing.objects.order_by().values('city').distinct()
    context = {'latest_airbnb_list': latest_airbnb_list,'cities': cities, 'cheapest_airbnb': cheapest_airbnb,
        'expensive_airbnb':expensive_airbnb,
        'average_price': average_price}
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

    # render(request, 'polls/loading.html')

    yelp_cats = Cuisines + Activities + Entertainment
    # busi_cats = category.objects.filter(category__in=Cuisines).select_related()
    business_id_for_cat = category.objects.filter(category__in=yelp_cats).values_list('business_id')
    print 'start'
    # i = 0
    # for cat in busi_cats:
    #     print cat.business_id, cat.category
    # print 'cat_done'

    # for id in business_id_for_cat:
    #     print id

    busi = business.objects.filter(id__in=business_id_for_cat)

    # for b in busi:
    #     print b.name

    people = float(num_adults) + float(num_kids)
    # rating = float(rating)

    airbnbs = Airbnb_listing.objects.filter(city__exact=city, accommodates__exact=people)#, overall_satisfaction__gte=rating)

    print('lens', len(busi), len(airbnbs))

    lat_low = 360
    lat_high = -360
    lon_low = 360
    lon_high = -360

    for a in airbnbs:
        if a.latitude > lat_high:
            lat_high = a.latitude
        if a.latitude < lat_low:
            lat_low = a.latitude
        if a.longitude > lon_high:
            lon_high = a.longitude
        if a.longitude < lon_low:
            lon_low = a.longitude
    lat_low -= 0.1
    lon_low -= 0.1
    lat_high += 0.1
    lon_high += 0.1
    print 'extremes set'

    # busi_loc = busi.filter(latitude__gt=lat_low-0.1, latitude__lt=lat_high+0.1, longitude__gt=lon_low-0.1, longitude__lt=lon_high+0.1).order_by('latitude')
    busi_loc = busi.filter(latitude__gt=lat_low, latitude__lt=lat_high, longitude__gt=lon_low, longitude__lt=lon_high).order_by('latitude')

    scores = {}
    # for a in airbnbs:
    for a_ind, a in enumerate(airbnbs):
        # alat = a.latitude
        # alon = a.longitude
        min_i = 0
        max_i = len(busi_loc) - 1
        i = int(floor(max_i / 2))
        while i >= 0 and i <= len(busi_loc) - 1:
            # print (a_ind, len(airbnbs), i, busi_loc[i])
            print (a_ind, len(airbnbs), i)
            # if a.latitude > busi_loc[i].latitude + 0.1:
            if busi_loc[i].latitude < a.latitude - 0.1:
                min_i = i + 1
                i = int(floor((min_i + max_i) / 2))
                if i > len(busi_loc):
                    break
            # elif a.latitude < busi_loc[i].latitude - 0.1:
            elif busi_loc[i].latitude > a.latitude + 0.1:
                max_i = i - 1
                i = int(floor((min_i + max_i) / 1))
                if i < 0:
                    break
            else:
                # print 'found', a.latitude, busi_loc[i].latitude
                pointer = i
                # print (i, pointer, busi_loc[pointer], busi_loc[pointer].latitude, busi_loc[pointer].longitude)
                # while pointer > 0 and a.latitude - 0.1 >= busi_loc[pointer].latitude - 0.1:
                while pointer > 0 and busi_loc[pointer].latitude > a.latitude - 0.1:
                    b = busi_loc[pointer]
                    distance = great_circle((a.latitude, a.longitude), (b.latitude, b.longitude)).miles
                    # print (a_ind, pointer, len(airbnbs), len(busi_loc), 'distance', distance)  
                    if distance < 5:
                        if a.room_id in scores:
                            scores[a.room_id] += b.stars
                        else:
                            scores[a.room_id] = b.stars
                    pointer -= 1

                pointer = i + 1
                # while pointer < len(busi_loc) and a.latitude > busi_loc[pointer].latitude + 0.1:
                while pointer < len(busi_loc) and busi_loc[pointer].latitude < a.latitude + 0.1:
                    b = busi_loc[pointer]
                    distance = great_circle((a.latitude, a.longitude), (b.latitude, b.longitude)).miles
                    # print (a_ind, pointer, len(airbnbs), len(busi_loc), 'distance', distance)  
                    if distance < 5:
                        if a.room_id in scores:
                            scores[a.room_id] += b.stars
                        else:
                            scores[a.room_id] = b.stars
                    pointer += 1
                break

        # # for b in busi:
        # # lat_low = a.latitude - 0.1
        # # lat_high = a.latitude + 0.1
        # # lon_low = a.longitude - 0.1
        # # lon_high = a.longitude + 0.1
        # # for b_ind, b in enumerate(busi.filter(latitude__gt=lat_low, latitude__lt=lat_high, longitude__gt=lon_low, longitude__lt=lon_high)):
        # for b_ind, b in enumerate(busi_loc):
        #     # print(a_ind, a, b_ind, b, a.latitude, a.longitude, b.latitude, b.longitude)
        #     # lat_dif = radians(b.latitude) - radians(a.latitude)
        #     # lon_dif = radians(b.longitude) - radians(a.longitude)
        #     # alpha = sin(lat_dif / 2)**2 + cos(a.latitude) * cos(b.latitude) * sin(lon_dif / 2)**2
        #     # print sin(lat_dif / 2)**2, cos(a.latitude), cos(b.latitude), sin(lon_dif / 2)**2, alpha
        #     # c = 2 * atan2(sqrt(alpha), sqrt(1 - alpha))
        #     # distance = 6373.0 * c
        #     distance = great_circle((a.latitude, a.longitude), (b.latitude, b.longitude)).miles
        #     # print (a_ind, b_ind, len(airbnbs), len(busi_loc), 'distance', distance)
            
        #     if distance < 5:
        #         if a.room_id in scores:
        #             scores[a.room_id] += b.stars
        #         else:
        #             scores[a.room_id] = b.stars

    a_sorted = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

    for a in a_sorted:
        print a

    # top_airbnbs = [a_sorted[0], a_sorted[1], a_sorted[2], a_sorted[3], a_sorted[4]]
    top_airbnbs = [airbnbs.get(room_id=a_sorted[0][0]), airbnbs.get(room_id=a_sorted[1][0]), airbnbs.get(room_id=a_sorted[2][0]), airbnbs.get(room_id=a_sorted[3][0]), airbnbs.get(room_id=a_sorted[4][0])]

    busi_loc_ids = busi_loc.values_list('id')
    cat_loc = category.objects.filter(business_id__in=busi_loc_ids)

    best_yelps = [{}, {}, {}, {}, {}]
    cats = Cuisines + Activities + Entertainment
    for c_ind, cat in enumerate(cats):
        for a in best_yelps:
            a[c_ind] = { 'name': "", 'rating': -1 }

    busi_cats = {}
    for b_ind, b in enumerate(busi_loc):
        busi_cats[b.id] = {}
        # b.myCats = [ False ] * len(cats)
        # b.myCats = []
        for c_ind, c in enumerate(cats):
            print (b_ind, c_ind)
            # if cat_loc.get(category=c, business_id=b.id):
            #     b.myCats = b.myCats + [ True ]
            # else:
            #     b.myCats = b.myCats + [ False ]
            busi_cats[b.id][c] = False

    for ind, bc in enumerate(cat_loc):
        print ind
        busi_cats[bc.business_id][bc.category] = True

    for a_ind, a in enumerate(top_airbnbs):
        # top_id = a[0]
        # print ('top_id', top_id)
        # top = airbnbs.get(room_id=top_id)
        # print (top, top.name)
        # a =
        for b_ind, b in enumerate(busi_loc):
            print (a_ind, b_ind)
            distance = great_circle((a.latitude, a.longitude), (b.latitude, b.longitude)).miles
            if distance < 5:
                for c_ind, c in enumerate(cats):
                    # if cat_loc.filter(category__exact=c, business_id=b.id) and b.stars > best_yelps[a_ind][c]['rating']:
                    # if b.myCats[c_ind] and b.stars > best_yelps[a_ind][c]['rating']:
                    if busi_cats[b.id][c] and b.stars > best_yelps[a_ind][c_ind]['rating']:
                        best_yelps[a_ind][c_ind]['name'] = b.name
                        best_yelps[a_ind][c_ind]['rating'] = b.stars

    print best_yelps[0][0]['name']

    context = {'city': city,
                'Price_Range': Price_Range,
                'num_adults': num_adults,
                'num_kids': num_kids,
                'rating': rating,
                'firstname':firstname,
                'Cuisines':Cuisines,
                'Activities':Activities,
                'Entertainment':Entertainment,
                'Diet':Diet,
                'TopAirbnbs':top_airbnbs,
                'BestYelps':best_yelps,
                'Categories':cats
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

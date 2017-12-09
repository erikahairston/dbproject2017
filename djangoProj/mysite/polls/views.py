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

    city = request.POST.get("Cities", "")
    most_here = ""
    least_here = ""
    avg_here = ""
    if city != "":
        most_here = Airbnb_listing.objects.filter(city__exact=city).values('price').annotate(Max('price')).order_by('-price')[0]['price']
        #print ('most_here', most_here)

        least_here = Airbnb_listing.objects.filter(city__exact=city).values('price').annotate(Min('price')).order_by('price')[1]['price']
        #print ('least_here', least_here)

        avg_here = Airbnb_listing.objects.filter(city__exact=city).aggregate(Avg('price'))
        avg_here = avg_here["price__avg"]
        #print ('avg_here', avg_here)


    lowest_price = Airbnb_listing.objects.filter().values('price').annotate(Min('price')).order_by('price')[1]['price']
    cheapest_airbnb = Airbnb_listing.objects.get(price=lowest_price)

    max_price = Airbnb_listing.objects.filter().values('price').annotate(Max('price')).order_by('-price')[0]['price']
    expensive_airbnb = Airbnb_listing.objects.get(price=max_price)

    avg_abnb = Airbnb_listing.objects.all().aggregate(Avg('price'))
    average_price = avg_abnb["price__avg"]

    dictionary = {}
    count = 1;
    name_query_set = Airbnb_listing.objects.values('name')
    most_common_word = " "
    for index, item in enumerate(name_query_set):
        for j in name_query_set[index]['name'].split(" "):
            if((j.isalpha()) & (len(j)>2)):
                if((j in dictionary) & (j.isalpha()) & (len(j)>2)):
                    dictionary[j] = dictionary[j] + 1
                    if(count < dictionary[j]):
                        count = dictionary[j]
                        most_common_word = j
                else:
                    dictionary[j] = 1

    print ("below is most common")
    print (most_common_word)

    cities = Airbnb_listing.objects.order_by().values('city').distinct()
    context = {'latest_airbnb_list': latest_airbnb_list,'cities': cities, 'cheapest_airbnb': cheapest_airbnb,
        'expensive_airbnb':expensive_airbnb,
        'average_price': average_price,
        'most_common_word': most_common_word,
        'most_here': most_here,
        'city': city,
        'least_here': least_here,
        'avg_here': avg_here}
    return render(request, template_name, context)

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

    yelp_cats = Cuisines + Activities + Entertainment
    business_id_for_cat = category.objects.filter(category__in=yelp_cats).values_list('business_id')

    busi = business.objects.filter(id__in=business_id_for_cat)

    if num_adults == "":
        num_adults = 0
    if num_kids == "":
        num_kids = 0
    if rating == "":
        rating = 0
    if Price_Range == "":
        Price_Range = Price_Range

    people = float(num_adults) + float(num_kids)
    rating = float(rating)

    airbnbs = Airbnb_listing.objects.filter(city__exact=city, accommodates__exact=people, overall_satisfaction__gte=rating, price__lte=Price_Range)

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

    busi_loc = busi.filter(latitude__gt=lat_low, latitude__lt=lat_high, longitude__gt=lon_low, longitude__lt=lon_high).order_by('latitude')

    scores = {}
    for a_ind, a in enumerate(airbnbs):
        min_i = 0
        max_i = len(busi_loc) - 1
        i = int(floor(max_i / 2))
        while i >= 0 and i <= len(busi_loc) - 1:
            if busi_loc[i].latitude < a.latitude - 0.1:
                min_i = i + 1
                i = int(floor((min_i + max_i) / 2))
                if i > len(busi_loc):
                    break
            elif busi_loc[i].latitude > a.latitude + 0.1:
                max_i = i - 1
                i = int(floor((min_i + max_i) / 1))
                if i < 0:
                    break
            else:
                pointer = i
                while pointer > 0 and busi_loc[pointer].latitude > a.latitude - 0.1:
                    b = busi_loc[pointer]
                    distance = great_circle((a.latitude, a.longitude), (b.latitude, b.longitude)).miles
                    if distance < 2:
                        if a.room_id in scores:
                            scores[a.room_id] += b.stars
                        else:
                            scores[a.room_id] = b.stars
                    pointer -= 1

                pointer = i + 1
                while pointer < len(busi_loc) and busi_loc[pointer].latitude < a.latitude + 0.1:
                    b = busi_loc[pointer]
                    distance = great_circle((a.latitude, a.longitude), (b.latitude, b.longitude)).miles
                    if distance < 2:
                        if a.room_id in scores:
                            scores[a.room_id] += b.stars
                        else:
                            scores[a.room_id] = b.stars
                    pointer += 1
                break

    a_sorted = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

    if len(a_sorted) > 5:
        top_n = 5
    else:
        top_n = len(a_sorted)
    top_airbnbs = []
    for i in range(top_n):
        top_airbnbs = top_airbnbs + [airbnbs.get(room_id=a_sorted[i][0])]

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
        for c_ind, c in enumerate(cats):
            busi_cats[b.id][c] = False

    for ind, bc in enumerate(cat_loc):
        busi_cats[bc.business_id][bc.category] = True

    for a_ind, a in enumerate(top_airbnbs):
        for b_ind, b in enumerate(busi_loc):
            distance = great_circle((a.latitude, a.longitude), (b.latitude, b.longitude)).miles
            if distance < 2:
                for c_ind, c in enumerate(cats):
                    if busi_cats[b.id][c] and b.stars > best_yelps[a_ind][c_ind]['rating']:
                        best_yelps[a_ind][c_ind]['name'] = b.name
                        best_yelps[a_ind][c_ind]['rating'] = b.stars


    for a_ind, a in enumerate(top_airbnbs):
        for c_ind, c in enumerate(cats):
            if best_yelps[a_ind][c_ind]['rating'] == -1:
                best_yelps[a_ind][c_ind]['rating'] = 0
                best_yelps[a_ind][c_ind]['name'] = 'None nearby'

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

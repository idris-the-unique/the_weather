from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    cities = City.objects.all()

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate

    form = CityForm()
    weather_data = []

    for city in cities:
        url = 'https://api.weatherapi.com/v1/current.json?key=7ef389f4e59b4d6295a15939221806&q='
        city_weather = requests.get(url+str(city)).json() #request the API data and convert the JSON to Python data types

        weather = {
            'city' : city,
            'temperature' : city_weather['current']['temp_c'],
            'description' : city_weather['current']['condition']['text'],
            'icon' : city_weather['current']['condition']['icon']
        }

        weather_data.append(weather)

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weather/index.html', context) 
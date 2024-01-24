
from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import requests
from datetime import datetime, timezone, date 
from datetime import date as dt_date 


def home(request):
    if request.method == 'POST':
        city = request.POST.get('city', 'London')
    else:
        city = 'London'

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=2576387e1412869240d79ec96fc7e218"
    PARAMS = {'units': 'metric'}

    try:
        data = requests.get(url, params=PARAMS).json()

        if data.get('cod') == '404':  # Check if the city was not found
            exception_occured = True
            messages.error(request, f"City '{city}' not found in the API.")
            day = datetime.date.today()
            return render(request, 'weatherapp/index.html', {'exception_occured': True, 'day': day, 'na_image': True})

        description = data['weather'][0]['description']
        
        icon = data['weather'][0]['icon']
        
        temp = data.get('main', {}).get('temp')
       
        day = dt_date.today()

        return render(request, 'weatherapp/index.html',{'description':description, 'icon':icon, 'temp':temp , 'day':day, 'city':city,'exception_occured': False})

    except Exception as e:
        exception_occured = True
        messages.error(request, f"An error occurred while fetching data from the API: {e}")
        day = datetime.date.today()
        return render(request, 'weatherapp/index.html', {'exception_occured': True, 'day': day})

# Function to convert UTC timestamp to readable datetime string
def convert_utc_to_readable(timestamp):
    if timestamp:
        dt_utc = datetime.utcfromtimestamp(timestamp)
        return dt_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
    else:
        return None


def city_detail(request):
    selected_city = request.GET.get('city', '')

    # Fetch detailed forecast information for the selected city using OpenWeatherMap API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={selected_city}&appid=2576387e1412869240d79ec96fc7e218"
    params = {'units': 'metric'}

    try:
        data = requests.get(url, params=params).json()

        # Add this line for debugging
        print(data)

        detailed_info = {

            'description': data['weather'][0]['description'],
            'main': data['weather'][0]['main'],
            'icon': data['weather'][0]['icon'],
            'temp': data['main']['temp'],
            'temp_feels_like': data['main'].get('feels_like'),
            'temp_min': data['main'].get('temp_min'),
            'temp_max': data['main'].get('temp_max'),
            'pressure': data['main'].get('pressure'),
            'humidity': data['main'].get('humidity'),
            'visibility': data.get('visibility'),
            'wind_speed': data['wind'].get('speed'),
            'wind_degree': data['wind'].get('deg'),
            'clouds': data['clouds'].get('all'),
            'sunrise': convert_utc_to_readable(data['sys'].get('sunrise')),
            'sunset': convert_utc_to_readable(data['sys'].get('sunset')),
        }

        print(detailed_info)

        return render(request, 'weatherapp/city_detail.html', { 'selected_city': selected_city, 'detailed_info': detailed_info})


    except Exception as e:
        #this line for debugging
        print(e)
        return render(request, 'weatherapp/city_detail.html', {'selected_city': selected_city, 'error_message': str(e)})

@require_GET
def city_autocomplete(request):
    partial_city = request.GET.get('q', '')
    if partial_city:
        # Make a request to Geonames for city suggestions
        geonames_username = 'gatsby_18'
        geonames_url = f'http://api.geonames.org/searchJSON?q={partial_city}&maxRows=5&username={geonames_username}'
        response = requests.get(geonames_url)
        data = response.json()
        suggestions = [city['name'] for city in data.get('geonames', [])]
        return JsonResponse({'suggestions': suggestions})

    return JsonResponse({'suggestions': []})

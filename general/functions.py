import googlemaps 
import urllib # Python URL functions
import urllib.request as urllib2 # Python URL functions
from django.contrib.auth.decorators import login_required
from general.models import Location, ShopDetails
from main.functions import get_auto_id


@login_required
def get_or_create_location(request,location_name,latitude,longitude):
    if Location.objects.filter(location_name = location_name, latitude=latitude, longitude=longitude).exists():
        location = Location.objects.get(location_name = location_name, latitude=latitude, longitude=longitude)
    else:
        short = location_name.split(',')
        short_name = short[0]
        location = Location.objects.create(
            location_name = location_name,
            latitude = latitude,
            longitude = longitude,
            short_name = short_name,
            creator = request.user,
            updater = request.user,
            auto_id = get_auto_id(Location)
        )

    return location


def get_location_distance(request, destination):
    gmaps = googlemaps.Client(key='AIzaSyB_tosasT8mLBttRlEJugdVDWnfJp-pr_A')

    try:
        shop = ShopDetails.objects.first()

        location = shop.location
        latitude = location.latitude
        longitude = location.longitude
        origins = (latitude, longitude)

        result = gmaps.distance_matrix(origins, destination, mode='driving')["rows"][0]["elements"][0]

        distance = result['distance']
        distance = distance['text']
        distance = distance.split(" ")
        distance_1 = distance[0]
        distance_type = distance[1]
        distance_1 = float(distance_1)
        if distance_type == "km":
            distance_1 = 1000 * distance_1

        duration = result['duration']
        duration = duration['text']
        duration = duration.split(" ")
        duration_1 = duration[0]
        duration_type = duration[1]
        duration_1 = float(duration_1)
        try:
            if duration_type == "hour" or duration_type == "hours":
                duration_1 = duration_1 * 60
                dur_min = duration[2]
                dur_min = float(dur_min)
                duration_1 += dur_min
        except:
            pass
    except:
        distance_1 = ''
        duration_1 = ''

    print("distance",distance_1, "duration", duration_1)

    return {"distance":distance_1, "duration": duration_1}


def send_sms(phone,otp):

    mobiles = "91"+str(phone) # Multiple mobiles numbers separated by comma.

    # importing the module
    import http.client as ht
    
    # establishing connection
    conn = ht.HTTPSConnection("api.msg91.com")

    message = "is your OTP for registering in Modicare Cart application"
    
    # determining the payload

    payload = "{\"flow_id\": \"613cf77784d60641e700a192\",\"sender\": \"MoCare\",\"mobiles\":" + mobiles + ",\"otp\":" + str(otp) +"}"
    
    # creating the header
    headers = {
        'authkey': "366479ADWl8nQzzhb612c9cbfP1", 
        'content-type': "application/JSON"
    }
    
    # sending the connection request
    conn.request("POST", "/api/v5/flow/", payload, headers)
    
    res = conn.getresponse()
    data = res.read()
    
    # printing the acknowledgement
    print(data.decode("utf-8"))
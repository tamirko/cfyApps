import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyAwBmRsa_dmWJzSCuYaIUSqZcFc9HX7uY4')

# Geocoding an address
#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
#print geocode_result

# Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
# print reverse_geocode_result
# Hadera
#reverse_geocode_result = gmaps.reverse_geocode((32.714224, 34.961452))

## Tel Aviv, Shlomo Lahat Promenade
#reverse_geocode_result = gmaps.reverse_geocode((32.0853, 34.761452))

## 17, Rue du Louvre, Paris, Paris,
#reverse_geocode_result = gmaps.reverse_geocode((48.864179, 2.342501))

## 2, Rue de l'Amiral de Coligny, Paris, Paris,
reverse_geocode_result = gmaps.reverse_geocode((48.85899, 2.339858))

## 20 Argyll Street, Soho, London,
#reverse_geocode_result = gmaps.reverse_geocode((51.515309, -0.141289))

## 10a, Rose Street, London, London,
# reverse_geocode_result = gmaps.reverse_geocode((51.511627, -0.125999))

## 50, Baldry Gardens, London, London,
# reverse_geocode_result = gmaps.reverse_geocode((51.42, -0.12500))

## 43 Charing Cross Road,London, London,
# reverse_geocode_result = gmaps.reverse_geocode((51.511612, -0.128549))

# pip install -U googlemaps
# https://github.com/googlemaps/google-maps-services-python
# https://developers.google.com/maps/documentation/geocoding/intro#Geocoding
# https://gist.github.com/ebinnion/2317191
# http://py-googlemaps.sourceforge.net/
# return gmaps._get("/maps/api/directions/json", params)["routes"]
# response = gmaps._get("/maps/api/place/photo", params, extract_body=lambda response: response, requests_kwargs={"stream": True})
# url = "/maps/api/place/%sautocomplete/json" % url_part
# return gmaps._get(url, params)["predictions"]
# params = {"minprice": min_price, "maxprice": max_price}
# if query:
#    params["query"] = query
# url = "/maps/api/place/%ssearch/json" % url_part
# return gmaps._get(url, params)
# [method for method in dir(gmaps) if callable(getattr(gmaps, method))]
# curl -i -X POST -k -d '{"accessKey": "API_KEY_REMOVED", "streamName": "REMOVED", "point": {"latitude": -21.98, "longitude": 13.70, "color": "blue"}}'
# curl -X POST 'https://...xxxx' -H 'Content-Type: application/json' -d @config.json
# curl --silent --header "Authorization: GoogleLogin auth=AIzaSyAwBmRsa_dmWJzSCuYaIUSqZcFc9HX7uY4" "http://picasaweb.google.com/data/feed/api/user/default" | tidy -xml -indent -quiet


#print reverse_geocode_result
#print "------------"
arr_size = len(reverse_geocode_result)
x = 0
if arr_size > 2:
    arr0 = reverse_geocode_result[0]
    address_components = arr0['address_components']
    arr_size = len(address_components)
    if arr_size > 2:
        str = ""
        for x in range(0, 4):
            str += "{0}, ".format(address_components[x]['long_name'])
        print str
        print "------------------------"
else:
    print "xxxx N/A"
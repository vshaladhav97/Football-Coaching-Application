import requests
import re

api_key = "AIzaSyCkmGTKI9Ak0_t47TDu-_0i5A22jfHgWxA"

post_code_validation_regex = r'^(^[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}?$)'

def call_distance_matrix(origins, destinations):

    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&sensor=false&origins={}&destinations={}&key={}".format(
        origins, destinations, api_key)

    response = requests.get(url)

    return response


def sort_list_of_location(locations):
    result = sorted(locations, key=lambda i: (
        float(i['distance'].split(' ')[0])))
    return result

def validate_postcode(postcode):
    pat = re.compile(post_code_validation_regex)
    if re.fullmatch(pat, postcode):
        return True
    else:
        return False